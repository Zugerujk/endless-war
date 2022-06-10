import ew.static.cfg as ewcfg
# maps users to where they are in the tutorial
user_to_tutorial_state = {}
import ew.backend.core as bknd_core
from ew.utils import cmd as cmd_utils
import ew.utils.rolemgr as ewrolemgr
from ew.backend.dungeons import EwBlurb
import ew.utils.frontend as ewfrontend
import ew.static.community_cfg as comm_cfg


async def add_blurb(cmd):
    if not 0 < ewrolemgr.check_clearance(member=cmd.message.author) < 4:
        return await cmd_utils.fake_failed_command(cmd)

    if len(cmd.tokens) > 5 or len(cmd.tokens) < 3:
        response = "The syntax is !addblurb \"blurb\" \"context\" \"subcontext\" \"subsubcontext\" Only the first context is required."
    else:
        blurb_obj = EwBlurb()
        blurb_obj.id_server = cmd.guild.id
        blurb_obj.blurb = cmd.tokens[1]
        blurb_obj.context = cmd.tokens[2]
        if len(cmd.tokens) > 3:
            blurb_obj.subcontext = cmd.tokens[3]
        if len(cmd.tokens) > 4:
            blurb_obj.subsubcontext = cmd.tokens[4]
        blurb_obj.persist()
        list_to_update = comm_cfg.blurb_context_map.get(blurb_obj.context)
        list_to_update.append(blurb_obj.blurb)
        response = "Added a blurb."

    await ewfrontend.send_message(cmd.client, cmd.message.channel,ewfrontend.formatMessage(cmd.message.author, response))




async def displayblurbs(cmd):
    if not 0 < ewrolemgr.check_clearance(member=cmd.message.author) < 4:
        return await cmd_utils.fake_failed_command(cmd)

    context = None
    subcontext = None
    subsubcontext = None


    if len(cmd.tokens) > 1:
        context = cmd.tokens[1]
    if len(cmd.tokens) > 2:
        subcontext = cmd.tokens[2]
    if len(cmd.tokens) > 3:
        subsubcontext = cmd.tokens[3]

    if context is not None:
        query = "SELECT {col_id_id_blurb}, {col_id_blurb} from blurbs".format(col_id_blurb=ewcfg.col_id_blurb, col_id_id_blurb=ewcfg.col_id_id_blurb)

        if context is not None:
            query += " WHERE {} = {}".format(ewcfg.col_id_context, context)
        if subcontext is not None:
            query += " AND {} = {}".format(ewcfg.col_id_subcontext, subcontext)
        if subsubcontext is not None:
            query += " AND {} = {}".format(ewcfg.col_id_subsubcontext, subsubcontext)

        data_chunk = bknd_core.execute_sql_query(query, (context,))


        response = ""
        for data in data_chunk:
            response += "Blurb {}: starting in {}\n".format(data[0], data[1][0:15])

        await ewfrontend.send_message(cmd.client, cmd.message.channel, ewfrontend.formatMessage(cmd.message.author, response))


async def display_blurb_context(cmd):
    response = comm_cfg.context_guide
    await ewfrontend.send_message(cmd.client, cmd.message.channel, ewfrontend.formatMessage(cmd.message.author, response))


async def delete_blurb(cmd):
    to_delete = cmd.tokens[1]
    checked = EwBlurb(id_server=cmd.guild.id)
    if checked.context != "" and checked.context != None:
        query = "DELETE from blurbs WHERE {col_id_blurb} = %s".format(col_id_blurb=ewcfg.col_id_blurb)
        bknd_core.execute_sql_query(query, (to_delete,))
        response = "Done."
    else:
        response = "No such blurb."
    await ewfrontend.send_message(cmd.client, cmd.message.channel, ewfrontend.formatMessage(cmd.message.author, response))


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
