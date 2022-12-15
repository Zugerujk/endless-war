""" Utility functions for recording statistics in the database """

from . import event as evt_utils
from . import core as ewutils
from ..backend import core as bknd_core
from ..static import cfg as ewcfg


def get_stat(id_server = None, id_user = None, user = None, metric = None):
    """ Look up a user statistic by user object or server and user IDs  """
    if (id_user == None) and (id_server == None):
        if (user != None):
            id_server = user.id_server
            id_user = user.id_user

    try:
        conn_info = bknd_core.databaseConnect()
        conn = conn_info.get('conn')
        cursor = conn.cursor()

        cursor.execute("SELECT {value} FROM stats WHERE {metric} = %s AND {id_server} = %s AND {id_user} = %s".format(
            value=ewcfg.col_stat_value,
            metric=ewcfg.col_stat_metric,
            id_server=ewcfg.col_id_server,
            id_user=ewcfg.col_id_user
        ), (
            metric,
            id_server,
            id_user
        ))

        db_result = cursor.fetchone()

        if db_result is None:
            # stop flooding db pls
            # set_stat(id_server=id_server, id_user=id_user, metric=metric, value=0)
            result = 0
        else:
            result = db_result[0]

        conn.commit()
    finally:
        # Clean up the database handles.
        cursor.close()
        bknd_core.databaseClose(conn_info)

    return result


def set_stat(id_server = None, id_user = None, user = None, metric = None, value = 0):
    """ Overwrite a user statistic by user object or server and user IDs  """
    if (id_user == None) and (id_server == None):
        if (user != None):
            id_server = user.id_server
            id_user = user.id_user

    # If set to the delete value, delete it
    if value == 0:
        # Delete them instead
        bknd_core.execute_sql_query(
            "DELETE FROM stats WHERE {id_server} = %s AND {id_user} = %s AND {metric} = %s".format(
                id_server=ewcfg.col_id_server,
                id_user=ewcfg.col_id_user,
                metric=ewcfg.col_stat_metric,
            ), (
                id_server,
                id_user,
                metric
            )
        )
    else:
        bknd_core.execute_sql_query("REPLACE INTO stats({id_server}, {id_user}, {metric}, {value}) VALUES(%s, %s, %s, %s)".format(
            id_server=ewcfg.col_id_server,
            id_user=ewcfg.col_id_user,
            metric=ewcfg.col_stat_metric,
            value=ewcfg.col_stat_value
        ), (
            id_server,
            id_user,
            metric,
            value
        ))

    evt_utils.process_stat_change(id_server=id_server, id_user=id_user, metric=metric, value=value)


def change_stat(id_server = None, id_user = None, user = None, metric = None, n = 0):
    """ Increase/Decrease a stat by a given value """
    if (id_user == None) and (id_server == None) and (user != None):
        id_server = user.id_server
        id_user = user.id_user

    if (id_user == None) or (id_server == None):
        return

    old_value = get_stat(id_server=id_server, id_user=id_user, metric=metric)
    if old_value + n >= 9223372036854775807:
        total = 9223372036854775807
    else:
        total = old_value + n

    # I'll rewrite stats later but for now we're going a little jank
    # Usually this would be in evt_utils but because of how it's been coded
    # global festivity tracking needs to go here instead
    if metric == ewcfg.stat_festivity:
        change_stat(id_server, -1, metric=ewcfg.stat_festivity_global, n=n)

    set_stat(id_server=id_server, id_user=id_user, metric=metric, value=total)


def increment_stat(id_server = None, id_user = None, user = None, metric = None):
    change_stat(id_server=id_server, id_user=id_user, user=user, metric=metric, n=1)


def track_maximum(id_server = None, id_user = None, user = None, metric = None, value = 0):
    """ Update a user statistic only if the new value is higher. return True if change occurred """
    if (id_user == None) and (id_server == None):
        if (user != None):
            id_server = user.id_server
            id_user = user.id_user

    old_value = get_stat(id_server=id_server, id_user=id_user, metric=metric)
    if old_value < value:
        set_stat(id_server=id_server, id_user=id_user, metric=metric, value=value)


def clear_on_death(id_server = None, id_user = None):
    """ Set to zero stats that need to clear on death """
    # We gotta clean the list up as otherwise SQL gets quite mad
    format_clear_stats = ewutils.formatNiceList(ewcfg.stats_clear_on_death, ",")
    format_clear_stats = format_clear_stats.replace(" ", "")

    # Delete them instead
    bknd_core.execute_sql_query(
        'DELETE FROM stats WHERE {id_server} = %s AND {id_user} = %s AND FIND_IN_SET("{metric}", "{clear_stats}")'.format(
            id_server=ewcfg.col_id_server,
            id_user=ewcfg.col_id_user,
            metric=ewcfg.col_stat_metric,
            clear_stats=format_clear_stats
        ), (
            id_server,
            id_user
        )
    )


def clean_stats(id_server) -> int:
    """ Remove all redundant stats with a value of 0 from the database. Could be lengthy. """
    # First grab the number
    outcome = bknd_core.execute_sql_query(
        'SELECT COUNT(*) FROM stats WHERE {id_server} = %s AND {stat_value} = 0'.format(
            id_server=ewcfg.col_id_server,
            stat_value=ewcfg.col_stat_value
        ), (
            id_server,
        )
    )
    # Then delete 'em all
    bknd_core.execute_sql_query(
        'DELETE FROM stats WHERE {id_server} = %s AND {stat_value} = 0'.format(
            id_server=ewcfg.col_id_server,
            stat_value=ewcfg.col_stat_value
        ), (
            id_server,
        )
    )

    return outcome[0][0]
