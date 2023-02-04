import time
from copy import copy

import MySQLdb

from ..static import cfg as ewcfg

db_pool = {}
db_pool_id = 0

caches = []
enabled_caches = []

cache_type_to_load_fn = {}


class ObjCache():
    """
        Template for caches. Initialized with the type.__name__ of the objects it stores.
        Handles setting and retrieval of cached data, ensuring that all data entering or exiting the cache is
        identified and copied as its type should be, and that the data within the cache is never directly pointed to
        by an external function.
        This ensures that the cache is only updated when these methods are called, and in the case where an object is
        initialized and changed without being persisted, that the cached data is not affected
    """

    entry_type = None

    identifiers = []
    nested_props = []
    entries = {}
    indexes = {}

    def __init__(self, ew_obj_type=None):
        """
            Takes the string representing the class type. Found with `type(instance).__name__`
            Sets up type specific variables used in the cache.
        """

        # Track the object type stored in the cache
        self.entry_type = ew_obj_type

        # If this isn't done all instances use the same dict
        self.entries = {}

        # Check if it has been given an identifying column
        if ew_obj_type in ewcfg.obj_type_to_identifiers.keys():
            # declare the unique columns
            self.identifiers = ewcfg.obj_type_to_identifiers.get(ew_obj_type)

        # Find any nested properties so copying will work right
        if ew_obj_type in ewcfg.obj_type_to_nested_props.keys():
            self.nested_props = ewcfg.obj_type_to_nested_props.get(ew_obj_type)

        # Setup any common search parameters as indexes
        if ew_obj_type in ewcfg.obj_type_indexes.keys():
            self.indexes = {}
            for prop_name in ewcfg.obj_type_indexes.get(ew_obj_type):
                self.indexes.update({prop_name: {}})

        # Leave a pointer to this object, so it can actually be found
        caches.append(self)

        # Load the cache if there are instructions for doing so
        if (ew_obj_type in cache_type_to_load_fn.keys()) and (ew_obj_type in ewcfg.autoload_types):
            cache_type_to_load_fn.get(ew_obj_type)()

    def get_data_id(self, data):
        """
            Takes a dictionary of property names and values. Must at least contain the unique properties of the type.
            Returns a string combining all unique properties, or False if a unique property is not present in the data.

            Unnecessary for EwItems or EwPlayers, which have only one unique property. But necessary for expansion into
            EwUsers or stocks which combine multiple fields to achieve unique identification
        """

        # Set Up
        return_id = None

        # Iterate through all identifying properties
        for prop_type in self.identifiers:
            # Allow for entry_id to be recognized as user_id or item_id etc.
            shared_names = [name for name in data.keys() if name in prop_type]

            # Handle the value if it exists
            if shared_names:
                prop_val = data.get(shared_names[0])
                # Format the value based on whether it's the first, and add to the final id
                return_id = str(prop_val) if (return_id is None) else "{}~{}".format(return_id, prop_val)
            else:
                # Data is missing a necessary identifier
                return False

        # Return the made identifier
        if return_id is not None:
            return return_id
        elif len(self.identifiers) == 0:
            # If the type has no identifiers, then simple number the entries as they come in.
            # Everything from the DB should have a unique column or pair of, this shouldn't ever be used
            return str(len(self.entries) + 1)

    def copy_entry(self, data):
        """
            Takes the data of an entry for the cache's given type.
            Returns a surface copy of the data, with any fields defined as nested being surface copied individually.

            Deepcopy works for the most part, but threw errors when used on EwPlayer data, so while those are not being
            cached yet, the potential issue was pre-emptively fixed when found.
        """

        # Run a surface level copy
        ret_dat = copy(data)

        # Since the caches are being typed, we know what values will be too deep to copy. So Get those replaced
        for prop in self.nested_props:
            # Ensure the data has the prop, then copy and replace
            if prop in ret_dat.keys():
                # Ensure the pointing entry is removed
                ret_dat.pop(prop)

                # And replaced with the copy
                prop_cop = copy(data.get(prop))
                ret_dat.update({prop: prop_cop})

            else:
                # Data was incompatible, make it known
                return False

        return ret_dat

    def set_entry(self, data):
        """
            Takes data of the cache's entry type and updates the cache with a new copy of the data.
            Returns true if successful, and False if it was unable to find the identifier or make a copy.
        """

        # Attempt to get unique ID for the data
        entry_id = self.get_data_id(data)
        # Ensure saved data is separated from active use data
        unique_data = self.copy_entry(data)

        # Save it if it's real, if it's missing a property it should have, one of these should return false
        if (entry_id is not False) and (unique_data is not False):
            # Grab old data if it exists (for index purposes)
            old_data = self.entries.get(entry_id, None)
            # Update any necessary indexes
            for index_prop_name, index_dict in self.indexes.items():
                # Remove old index entries
                if old_data is not None:
                    # Remove the entry from the list of items within that index, assume it's properly indexed.
                    index_dict.get(str(old_data.get(index_prop_name))).remove(entry_id)

                # Index the new data
                new_index_value = str(unique_data.get(index_prop_name))
                # Create the index if it doesn't exist yet, or add the entry id to its existing contents
                if new_index_value not in index_dict.keys():
                    index_dict.update({new_index_value: [entry_id]})
                else:
                    index_dict.get(new_index_value).append(entry_id)

            # Now save the data
            self.entries.update({entry_id: unique_data})
            return True
        else:
            print("Cache for {}s was passed incompatible or incomplete data. \nData Passed: {}".format(self.entry_type, data))
            return False

    def get_entry(self, unique_vals = None):
        """
            Takes dictionary of the values unique to all entries. Should just be the Primary Keys.
            Returns a copy of the cached data, or False if there is no data with the given identifiers.
        """

        # Convert identifiers to a string of consistent order and format
        id_str = self.get_data_id(unique_vals)

        # Find the target data and copy it so nothing receives a pointer to the cache
        return self.copy_entry(self.entries.get(id_str)) if (id_str in self.entries.keys()) else False

    def delete_entry(self, unique_vals = None):
        """
            Takes the unique properties of a given entry as a dictionary of property names and values.
            Returns True if the entry existed and was removed, returns false if nothing was found
            Deletes entry if one matching the passed identifiers is found
        """

        # Convert identifiers to a string of consistent order and format
        id_str = self.get_data_id(unique_vals)

        if id_str in self.entries.keys():
            # Remove entry from any indexes
            old_data = self.entries.get(id_str)
            for index_prop_name, index_dict in self.indexes.items():
                index_dict.get(str(old_data.get(index_prop_name))).remove(id_str)

            # Delete the entry if it exists
            self.entries.pop(id_str)

            # Allow for things that use this to know whether something was successfully deleted
            return True
        return False

    def find_entries(self, criteria = None, id_list = None):
        """
            Takes a dictionary of object property names and values. Checks against all data entered in the cache.
            Returns a list of copies of all data that met the given criteria.
        """
        copied_matches = []

        if id_list != None:
            for id in id_list:
                copied_matches.append(self.copy_entry(self.entries.get(id)))

        else:
            # Create list to search
            ids_to_search = None
            criteria_indexed = []
            # Use indexes to narrow searches
            for key, value in criteria.items():
                skey = str(key)
                value = str(value)
                if skey in self.indexes.keys() and value in self.indexes.get(skey).keys():
                    # Index found, Note that the term doesnt need to be checked later
                    criteria_indexed.append(key)
                    if ids_to_search is None:
                        # Limit search to found index
                        ids_to_search = self.indexes.get(skey).get(value)
                    else:
                        # Limit search to items that share all indexes
                        ids_to_search = list(set(ids_to_search).intersection(set(self.indexes.get(skey).get(value))))

            # Remove indexed criteria
            for k in criteria_indexed:
                criteria.pop(k)

            # grab the actual entry data to be vetted
            if ids_to_search is not None:
                valid_data = list(map(lambda ident: self.entries.get(ident), ids_to_search))
            else:
                valid_data = self.entries.values()

            # iterate through all entered data
            for data in valid_data:
                # Check against all given criteria
                meets = True
                for key, value in criteria.items():
                    # For search through props type things
                    if key in self.nested_props:
                        for k2, v2 in value.items():
                            if not (k2 in data.get(key).keys() and str(v2) == str(data.get(key).get(k2))):
                                meets = False
                                break
                    # Stop and mark if it isn't a match
                    elif not ((key in data.keys()) and (str(value) == str(data.get(key)))):
                        meets = False
                        break

                # track data if it matches
                if meets:
                    copied_matches.append(self.copy_entry(data))

        return copied_matches

    def bulk_set_entry(self, entries = None):
        """
            Takes a list of entry data dictionaries
            Returns true on success, false on failure
            Prepares all index and entry changes to be run as simultaneously as possible with .update and adding lists
        """
        # Compile all changes into things to be run simultaneously
        entries_update = {}
        index_additions = {}
        index_removals = {}

        # Setup Index edit dictionaries
        for key in self.indexes.keys():
            index_removals.update({key: {}})
            index_additions.update({key: {}})

        # Figure out what to change
        for data in entries:
            entry_id = self.get_data_id(data)
            old_data = self.entries.get(entry_id)

            # Figure out index changes
            for prop_name in self.indexes.keys():
                # Compile index entries to be removed
                old_val = old_data.get(prop_name)
                removal_index = index_removals.get(prop_name)
                if removal_index.get(old_val, None) is not None:
                    removal_index.get(old_val).append(entry_id)
                else:
                    removal_index.update({old_val: [entry_id]})

                # Compile index entries to be added
                new_val = data.get(prop_name)
                addition_index = index_additions.get(prop_name)
                if addition_index.get(new_val, None) is not None:
                    addition_index.get(new_val).append(entry_id)
                else:
                    addition_index.update({new_val: [entry_id]})

            # Compile Entry updates
            entries_update.update({entry_id: data})

        # Remove old index values
        for prop_name, index_data in index_removals.items():
            for index_val, ids_to_remove in index_data.items():
                # We assume that the items are already properly indexed, that way if they aren't, this can warn us :)
                list_to_edit = self.indexes.get(prop_name).get(index_val)
                for removed_id in ids_to_remove:
                    list_to_edit.remove(removed_id)

        # add new index values
        for prop_name, index_data in index_additions.items():
            # iterating through all property indexes, and all of the subsequent indexed values and their id lists
            for index_val, ids_to_add in index_data.items():
                # Get the id list for the target prop and value, or make it if it doesnt exist
                list_to_edit = self.indexes.get(prop_name).get(index_val)
                if list_to_edit is None:
                    self.indexes.get(prop_name).update({index_val: ids_to_add})
                else:
                    list_to_edit += ids_to_add

        # Update stored data
        self.entries.update(entries_update)


""" connect to the database """

def databaseConnect():
    conn_info = None

    conn_id_todelete = []

    global db_pool
    global db_pool_id

    # Iterate through open connections and find the currently active one.
    for pool_id in db_pool:
        conn_info_iter = db_pool.get(pool_id)

        if conn_info_iter['closed'] == True:
            if conn_info_iter['count'] <= 0:
                conn_id_todelete.append(pool_id)
        else:
            conn_info = conn_info_iter

    # Close and remove dead connections.
    if len(conn_id_todelete) > 0:
        for pool_id in conn_id_todelete:
            conn_info_iter = db_pool[pool_id]
            conn_info_iter['conn'].close()

            del db_pool[pool_id]

    # Create a new connection.
    if conn_info == None:
        db_pool_id += 1
        conn_info = {
        'conn': MySQLdb.connect(host = "localhost", user = "rfck-bot", passwd = "rfck" , db = ewcfg.database, charset = "utf8mb4"),
            'created': int(time.time()),
            'count': 1,
            'closed': False
        }
        db_pool[db_pool_id] = conn_info
    else:
        conn_info['count'] += 1

    return conn_info


""" close (maybe) the active database connection """


def databaseClose(conn_info):
    conn_info['count'] -= 1

    # Expire old database connections.
    if (conn_info['created'] + 60) < int(time.time()):
        conn_info['closed'] = True


"""
    Execute a given sql_query. (the purpose of this function is to minimize repeated code and keep functions readable)
"""


def execute_sql_query(sql_query = None, sql_replacements = None, fetchone = False):
    data = None
    cursor = None
    conn_info = None

    try:
        conn_info = databaseConnect()
        conn = conn_info.get('conn')
        cursor = conn.cursor()
        cursor.execute(sql_query, sql_replacements)
        if sql_query.lower().startswith("select"):
            data = cursor.fetchall() if not fetchone else cursor.fetchone()
        conn.commit()
    finally:
        # Clean up the database handles.
        if cursor is not None: cursor.close()
        if conn_info is not None: databaseClose(conn_info)

    return data


""" Locate the cache, compile all given identifying values, and get the entry with the given identification and type """


def get_cache_result(obj_type = None, obj = None, **kwargs):
    """
        Takes an object type and any given properties, or an object itself
        Returns False on failure to find, otherwise returns specified entry data

        Any unspecified keywords will be assumed to be unique properties, and a given object will be considered the
        an instance of the target object, and have its properties added as potential identifiers
    """

    # Setup for return, and grab the cache if it exists
    obj_cache = get_cache(obj_type = obj_type, obj = obj, create = False)

    # This ensures a proper type was passed
    if obj_cache is not False:
        # Use given object's properties as example of target object
        if obj is not None: kwargs.update(obj.__dict__)

        # Look for and return entry with values matching what was given.
        return obj_cache.get_entry(unique_vals=kwargs)

    # Return False if the type is not cached
    return False


def cache_data(obj_type = None, data = None, obj = None):
    """
        Takes an object's type and data, or the object itself. Will prioritize given "data" if mixed with an object.
        Returns True if it was successfully cached, and false if given incomplete or incompatible data.

        Will create a new cache if one does not yet exist for the given object type.
    """

    # Find or create the cache
    type_cache = get_cache(obj_type = obj_type, obj = obj, create = True)

    # Extracts the data from an object if that was passed in lieu of necessitating separating the values elsewhere
    data = obj.__dict__ if ((data is None) and (obj is not None)) else data

    # Get cache will return false if not passed a proper object type
    if type_cache is not False:
        # Attempt to save the given data in the cache of its type
        return type_cache.set_entry(data)

    # Indicate failure to find a cache
    return False


def remove_entry(obj_type = None, obj = None, **kwargs):
    """
        Takes the type of object or the object itself being targeted
        Returns True or False if the cached data was found and removed or not

        Extra keywords are assumed to be unique properties of the target data, as are all properties of a passed obj
    """

    # Attempt to find pre-existing cache of the specified type
    type_cache = get_cache(obj_type = obj_type, obj = obj, create = False)

    # If the cache was found, try to find and delete an entry with the given properties.
    if type_cache is not False:
        # if the entire object was given, use its properties for identification
        if obj is not None: kwargs.update(obj.__dict__)
        # attempt deletion and indicate success
        return type_cache.delete_entry(unique_vals = kwargs)

    # Return indicator of success
    return False


def get_cache(obj_type=None, obj = None, create=False):
    """
        Takes the type().__name__ of an object, or an object, and bool determining creation
        Returns a cache of the specified type if create, or if it already exists, otherwise False
    """

    # Allow for passing of entire objects in the place of having to pick over the data every time
    obj_type = type(obj).__name__ if ((obj_type is None) and (obj is not None)) else obj_type

    # Ensure a valid type was actually given
    if obj_type in enabled_caches:
        # Search through all caches
        for cache in caches:
            # Return the cache upon finding it
            if cache.entry_type == obj_type:
                return cache

        if create:
            # If no matching cache was found, create a new one and return it, unless specified otherwise
            return ObjCache(ew_obj_type=obj_type)

    # Return false if No cache was found or creatable
    return False
