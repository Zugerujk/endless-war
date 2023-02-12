
cmd_debug8 = "debug8"
cmd_debug9 = "debug9"
debug_state_1 = 'debugstate1'
debug_content_1= 'nothing to find, goons'
debugitem_set = []
debugpois = []
debugpiers = []
debugrecipes = []

debugitem = "debugitem"
debugroom = "debugroom"

debugfish_response = ""
debugfish_goal = 99999999999

theforbiddenoneoneone_desc = "slimexodia"
forbiddenstuffedcrust_eat = "it's a pizza. whatever."
forbiddenstuffedcrust_desc = "this sure looks like a pizza."

act_pois = {}

zone_bonus_flavor = {}


def initialize_gamestate(id_server):
    return


def reel_code():
    return None


def debug_code():
    return None


def act(cmd_obj, poi, content_tolower):
    return None


async def secret_context(user_data, item, cmd):
    return False

async def award_item(cmd, itemname = None, on_give = None, on_fail = None, on_runout = None, gamestate = None, marker_gamestate = None):
    return