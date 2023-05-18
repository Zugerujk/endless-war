from ew.static import cfg as ewcfg
from ew.static import poi as poi_static
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import rolemgr as ewrolemgr
from ew.utils.combat import EwUser
from ew.cmd.dungeons import dungeonutils
from ..backend import core as bknd_core
from ew.static import npc as npc_static
from ew.static import community_cfg as commcfg
from ew.static import weapons as static_weapons

def format_tutorial_response(scene):
    response = scene.text
    if scene.dungeon_state:
        response += "\n\nWhat do you do?\n\n**>options: "
        options = []
        for path in scene.options.keys():
            options.append("{}{}".format(ewcfg.cmd_prefix, path))
        response += ewutils.formatNiceList(names=options, conjunction="or")
        response += "**"

    return response


async def begin_tutorial(member):
    user_data = EwUser(member=member)
    dungeonutils.user_to_tutorial_state[user_data.id_user] = 0

    scene = poi_static.dungeon_tutorial[0]

    if scene.poi != None:
        user_data.poi = scene.poi
    if scene.life_state != None:
        user_data.life_state = scene.life_state

    user_data.persist()

    await ewrolemgr.updateRoles(client=ewutils.get_client(), member=member)

    response = format_tutorial_response(scene)
    poi_def = poi_static.id_to_poi.get(user_data.poi)
    channels = [poi_def.channel]
    return await fe_utils.post_in_channels(member.guild.id, fe_utils.formatMessage(member, response), channels)



def load_npc_blurbs():
    npcblurbs = bknd_core.execute_sql_query("SELECT {col_id_id_blurb}, {col_id_blurb}, {col_subcontext}, {col_subsubcontext} from blurbs where context = %s".format(
        col_id_blurb=ewcfg.col_id_blurb,
        col_id_id_blurb=ewcfg.col_id_id_blurb,
        col_subcontext=ewcfg.col_id_subcontext,
        col_subsubcontext=ewcfg.col_id_subsubcontext), ('npc',))



    npc_map = npc_static.active_npcs_map

    for blurb in npcblurbs:
        npc = npc_map.get(blurb[2])
        if npc is not None:
            current_dialogue_tree = npc.dialogue.get(blurb[3])
            if current_dialogue_tree is None:
                try:
                    npc.dialogue[blurb[3]] = [blurb[1]]
                except Exception as e:
                    ewutils.logMsg('Error loading blurb:{}'.format(e))
            else:
                try:
                    npc.dialogue[blurb[3]].append(blurb[1])
                except Exception as e:
                    ewutils.logMsg('Error loading blurb:{}'.format(e))



def import_blurb_list(keyword = '', default_list = None):
    if default_list is None:
        default_list = []
    blurb_import = bknd_core.execute_sql_query("select {col_id_blurb} from blurbs where context = %s".format(
        col_id_blurb = ewcfg.col_id_blurb
        ), (keyword,))

    for blurb in blurb_import:
        try:
            default_list.append(blurb[0])
        except Exception as e:
            ewutils.logMsg('Error loading blurb:{}'.format(e))

    return default_list


def load_other_blurbs():
    for context in commcfg.blurb_context_map.keys():
        try:
            commcfg.blurb_context_map[context] = import_blurb_list(keyword=context, default_list=commcfg.blurb_context_map.get(context))
        except Exception as e:
            ewutils.logMsg('Error loading blurb group:{}'.format(e))



    districtblurbs = bknd_core.execute_sql_query(
        "SELECT {col_id_id_blurb}, {col_id_blurb}, {col_subcontext} from blurbs where context = %s".format(
            col_id_blurb=ewcfg.col_id_blurb,
            col_id_id_blurb=ewcfg.col_id_id_blurb,
            col_subcontext=ewcfg.col_id_subcontext), ('district',))

    for poi in poi_static.poi_list:
        commcfg.district_blurbs[poi.id_poi] = ['Your eyes glaze over from sniffing too much paint thinner. You can\'t see a thing.']
    for blurb in districtblurbs:
        try:
            commcfg.district_blurbs[blurb[2]].append(blurb[1])
        except Exception as e:
            ewutils.logMsg('Error loading blurb:{}'.format(e))

    vendorblurbs = bknd_core.execute_sql_query(
        "SELECT {col_id_id_blurb}, {col_id_blurb}, {col_subcontext} from blurbs where context = %s".format(
            col_id_blurb=ewcfg.col_id_blurb,
            col_id_id_blurb=ewcfg.col_id_id_blurb,
            col_subcontext=ewcfg.col_id_subcontext), ('vendor',))

    for blurb in vendorblurbs:
        try:
            ewcfg.vendor_dialogue[blurb[2]].append(blurb[1])
        except Exception as e:
            ewutils.logMsg('Error loading blurb:{}'.format(e))

    vendororderblurbs = bknd_core.execute_sql_query(
        "SELECT {col_id_id_blurb}, {col_id_blurb}, {col_subcontext} from blurbs where context = %s".format(
            col_id_blurb=ewcfg.col_id_blurb,
            col_id_id_blurb=ewcfg.col_id_id_blurb,
            col_subcontext=ewcfg.col_id_subcontext), ('vendororder',))

    for blurb in vendororderblurbs:
        try:
            ewcfg.vendor_order_dialogue[blurb[2]].append(blurb[1])
        except Exception as e:
            ewutils.logMsg('Error loading blurb:{}'.format(e))

    brandishblurbs = bknd_core.execute_sql_query(
        "SELECT {col_id_id_blurb}, {col_id_blurb}, {col_subcontext} from blurbs where context = %s".format(
            col_id_blurb=ewcfg.col_id_blurb,
            col_id_id_blurb=ewcfg.col_id_id_blurb,
            col_subcontext=ewcfg.col_id_subcontext), ('brandish',))

    for blurb in brandishblurbs:
        try:
            static_weapons.weapon_map[blurb[2]].str_brandish.append(blurb[1])
        except Exception as e:
            ewutils.logMsg('Error loading blurb:{}'.format(e))

    killtextblurbs = bknd_core.execute_sql_query(
        "SELECT {col_id_id_blurb}, {col_id_blurb}, {col_subcontext} from blurbs where context = %s".format(
            col_id_blurb=ewcfg.col_id_blurb,
            col_id_id_blurb=ewcfg.col_id_id_blurb,
            col_subcontext=ewcfg.col_id_subcontext), ('killtext',))

    for blurb in killtextblurbs:
        try:
            static_weapons.weapon_map[blurb[2]].str_kill.append(blurb[1])
        except Exception as e:
            ewutils.logMsg('Error loading blurb:{}'.format(e))