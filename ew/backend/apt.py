from . import core as bknd_core
from ..static import cfg as ewcfg


class EwApartment:
    id_user = -1
    id_server = -1

    name = "a city apartment."
    description = "It's drafty in here! You briefly consider moving out, but your SlimeCoin is desperate to leave your pocket."
    poi = ""
    rent = 0
    apt_class = "c"
    num_keys = 0
    key_1 = 0
    key_2 = 0

    def __init__(
            self,
            id_user = None,
            id_server = None
    ):
        if (id_user != None and id_server != None):
            self.id_user = id_user
            self.id_server = id_server

            result = bknd_core.execute_sql_query(
                sql_query = "SELECT {}, {}, {}, {}, {}, {}, {}, {} FROM apartment WHERE id_user = %s and id_server = %s".format(
                    ewcfg.col_apt_name,
                    ewcfg.col_apt_description,
                    ewcfg.col_poi,
                    ewcfg.col_rent,
                    ewcfg.col_apt_class,
                    ewcfg.col_num_keys,
                    ewcfg.col_key_1,
                    ewcfg.col_key_2
                ),
                sql_replacements = (self.id_user, self.id_server),
                fetchone = True
            )

            if result != None:
                # Record found: apply the data to this object.
                self.name = result[0]
                self.description = result[1]
                self.poi = result[2]
                self.rent = result[3]
                self.apt_class = result[4]
                self.num_keys = result[5]
                self.key_1 = result[6]
                self.key_2 = result[7]
            elif id_server is not None and id_user is not None:
                # Create a new database entry if the object is missing.
                bknd_core.execute_sql_query(
                    sql_query = "REPLACE INTO apartment({}, {}, {}) VALUES(%s, %s, %s)".format(
                        ewcfg.col_id_user,
                        ewcfg.col_id_server,
                        ewcfg.col_poi
                    ), 
                    sql_replacements = (
                        self.id_user,
                        self.id_server,
                        self.poi
                    )
                )

    def persist(self):
        bknd_core.execute_sql_query(
            "REPLACE INTO apartment ({col_id_server}, {col_id_user}, {col_apt_name}, {col_apt_description}, {col_poi}, {col_rent}, {col_apt_class}, {col_num_keys}, {col_key_1}, {col_key_2}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
                col_id_server=ewcfg.col_id_server,
                col_id_user=ewcfg.col_id_user,
                col_apt_name=ewcfg.col_apt_name,
                col_apt_description=ewcfg.col_apt_description,
                col_poi=ewcfg.col_poi,
                col_rent=ewcfg.col_rent,
                col_apt_class=ewcfg.col_apt_class,
                col_num_keys=ewcfg.col_num_keys,
                col_key_1=ewcfg.col_key_1,
                col_key_2=ewcfg.col_key_2,

            ), (
                self.id_server,
                self.id_user,
                self.name,
                self.description,
                self.poi,
                self.rent,
                self.apt_class,
                self.num_keys,
                self.key_1,
                self.key_2

            ))
