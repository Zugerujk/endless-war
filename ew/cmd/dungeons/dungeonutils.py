import ew.static.cfg as ewcfg
# maps users to where they are in the tutorial
user_to_tutorial_state = {}
import ew.backend.core as bknd_core

import ew.utils.rolemgr as ewrolemgr

import ew.utils.frontend as ewfrontend
import ew.static.community_cfg as comm_cfg






def import_blurb(list = [], context = None, subcontext = None, subsubcontext = None):
    new_list = list
    if context is not None:
        query = "SELECT {col_id_blurb} from blurbs WHERE context = %s".format(col_id_blurb=ewcfg.col_id_blurb)

        if subcontext is not None:
            query += " AND {} = {}".format(ewcfg.col_id_subcontext, subcontext)
        if subsubcontext is not None:
            query += " AND {} = {}".format(ewcfg.col_id_subsubcontext, subsubcontext)

        data_chunk = bknd_core.execute_sql_query(query, (context,))

        for chunk in data_chunk:
            new_list.append(chunk[0])

    return new_list


def initialize_blurbs(id_server):
    comm_cfg.browse_list = import_blurb(list=comm_cfg.browse_list, context='browse')