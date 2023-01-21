import random

from ew.backend import item as bknd_item
from ew.backend.item import EwItem
from ew.backend.market import EwStock
from ew.static import cfg as ewcfg
from ew.static import poi as poi_static
import ew.static.items as static_items
from ew.static import weapons as wep_static
from ew.utils import frontend as fe_utils
from ew.utils import market as market_utils
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict


def gen_score_text(ew_id, slime_alias):
    user_data = EwUser(ew_id=ew_id)

    items = bknd_item.inventory(id_user=user_data.id_user, id_server=user_data.id_server, item_type_filter=ewcfg.it_item)

    poudrin_amount = bknd_item.find_poudrin(id_user=user_data.id_user, id_server=user_data.id_server)

    if user_data.life_state == ewcfg.life_state_grandfoe:
        # Can't see a raid boss's slime score.
        response = "{}'s power is beyond your understanding.".format(ew_id.display_name)
    else:
        # return somebody's score
        response = "{} currently has {:,} {}{}.".format(ew_id.display_name, user_data.slimes, slime_alias, (" and {} {} poudrin{}".format(poudrin_amount, slime_alias, ("" if poudrin_amount == 1 else "s")) if poudrin_amount > 0 else ""))

    return response


def item_off(id_item, id_server, item_name = "", is_flushed = False):
    item_obj = EwItem(id_item=id_item)
    districtmodel = EwDistrict(id_server=id_server, district=ewcfg.poi_id_slimesendcliffs)
    slimetotal = 0

    if item_obj.item_props.get('id_furniture') == 'sord':
        response = "You toss the sord off the cliff, but for whatever reason, the damn thing won't go down. It just keeps going up and up, as though gravity itself blocked this piece of shit jpeg artifact on Twitter. It eventually goes out of sight, where you assume it flies into the sun."
        if is_flushed:
            response = "You cram the sord in the toilet."
        bknd_item.item_delete(id_item=id_item)
    elif random.randrange(500) < 125 or item_obj.item_type in([ewcfg.it_questitem, item_obj.item_type == ewcfg.it_medal, ewcfg.it_relic])  or item_obj.item_props.get('rarity') == ewcfg.rarity_princeps or item_obj.item_props.get('id_cosmetic') == "soul" or item_obj.item_props.get('id_furniture') == "propstand" or item_obj.item_props.get('id_furniture') in static_items.furniture_collection or item_obj.item_props.get('acquisition') == 'relic':
        response = "You toss the {} off the cliff. It sinks into the ooze disappointingly.".format(item_name)
        if is_flushed:
            response = "You flush {} down the toilet. Off it goes..."
        if item_obj.item_props.get('id_item') in [ewcfg.item_id_oldboot, ewcfg.item_id_seaweed, ewcfg.item_id_tincan, ewcfg.item_id_slimepoudrin] or item_obj.item_props.get('acquisition') == ewcfg.acquisition_fishing:
            bknd_item.item_delete(id_item=id_item)
        else:
            bknd_item.give_item(id_item=id_item, id_server=id_server, id_user=ewcfg.poi_id_slimesea)

    elif random.randrange(500) < 498:
        response = "You toss the {} off the cliff. A nearby kraken swoops in and chomps it down with the cephalapod's equivalent of a smile. Your new friend kicks up some sea slime for you. Sick!".format(item_name)
        if is_flushed:
            response = "You flush {} down the toilet. Off it goes..."
        slimetotal = 2000 + random.randrange(10000)
        bknd_item.item_delete(id_item=id_item)

    else:
        response = "{} Oh fuck. FEEDING FRENZY!!! Sea monsters lurch down on the spoils like it's fucking christmas, and a ridiculous level of slime debris covers the ground. {}".format(ewcfg.emote_slime1, ewcfg.emote_slime1)
        if is_flushed:
            response = "You flush {} down the toilet. Off it goes..."
        slimetotal = 100000 + random.randrange(900000)

        bknd_item.item_delete(id_item=id_item)

    if not is_flushed:
        districtmodel.change_slimes(n=slimetotal)
        districtmodel.persist()
    return response




def location_commands(cmd, search_poi = None):
    user_data = EwUser(member=cmd.message.author)
    response = init_resp = "**CURRENT LOCATION**:"

    # Get either location searched or user location
    if search_poi is not None:
        poi = search_poi
    else:
        poi = user_data.poi
    poi_obj = poi_static.id_to_poi.get(poi)

    if poi_obj is not None:
        response = init_resp = "**{}**".format(poi_obj.str_name)

        # Unique-ish commands first
        if poi in [ewcfg.poi_id_nlacu, ewcfg.poi_id_neomilwaukeestate]:
            response += "\n" + ewcfg.universities_commands
        if ewcfg.district_unique_commands.get(poi) is not None:

            response += "\n" + ewcfg.district_unique_commands.get(poi)

        # Generic commands second
        if poi in [ewcfg.poi_id_mine, ewcfg.poi_id_mine_sweeper, ewcfg.poi_id_mine_bubble, ewcfg.poi_id_tt_mines,
                   ewcfg.poi_id_tt_mines_sweeper, ewcfg.poi_id_tt_mines_bubble, ewcfg.poi_id_cv_mines,
                   ewcfg.poi_id_cv_mines_sweeper, ewcfg.poi_id_cv_mines_bubble]:
            response += "\n" + ewcfg.mine_commands
        elif poi_obj.is_pier:
            response += "\n" + ewcfg.pier_commands
        elif poi_obj.is_transport_stop or poi_obj.is_transport:
            response += "\n" + ewcfg.transport_commands
        elif poi_obj.is_apartment:
            response += "\n" + ewcfg.apartment_commands
        elif poi in [ewcfg.poi_id_greencakecafe, ewcfg.poi_id_nlacu, ewcfg.poi_id_neomilwaukeestate, ewcfg.poi_id_glocksburycomics]:
            response += "\n" + ewcfg.zine_writing_places_commands
        elif poi in [ewcfg.poi_id_ab_farms, ewcfg.poi_id_og_farms, ewcfg.poi_id_jr_farms]:
            response += "\n" + ewcfg.farm_commands

        # Shops last
        if len(poi_obj.vendors) != 0:
            response += "\n" + ewcfg.shop_commands

    if response != init_resp:
        return response + "\n"
    else:
        return "No special commands for {}. Try \"!commands basic\" or \"!help\".".format(poi_obj.str_name if poi_obj is not None else user_data.poi)


def mutation_commands(cmd):
    response = "**CURRENT MUTATIONS:**"
    user_data = EwUser(member=cmd.message.author)
    mutations = user_data.get_mutations()
    for mutation in mutations:
        if ewcfg.mutation_unique_commands.get(mutation) is not None:
            response += "\n" + ewcfg.mutation_unique_commands.get(mutation)

    if response != "**CURRENT MUTATIONS:**":
        return (response + "\n")
    else:
        return "No special commands found for your mutations. Try \"!help mymutations\" or \"!commands allmutations\"."


def item_commands(cmd):
    response = "**IN YOUR INVENTORY:**"
    items_to_find = ewcfg.item_unique_commands.keys()
    items = bknd_item.inventory(id_user=cmd.message.author.id, id_server=cmd.guild.id)
    
    items_template_list = []
    
    items = list(map(lambda dat: {
        "template": dat.get("template"),
    }, items))    

    for item in items:
        items_template_list.append(item["template"])

    del items

    # Unique items
    for lookup in items_to_find:
        if lookup in items_template_list:
            response += "\n" + ewcfg.item_unique_commands.get(lookup)

    # yuck
    # Response and Instant-Use
    if any(item in (static_items.prank_items_instantuse_names + static_items.prank_items_response_names) for item in items_template_list):
        response += "\n" + ewcfg.item_group_commands.get("instantuse_response_pranks")
    # Trap pranks
    if any(item in static_items.prank_items_trap_names for item in items_template_list):
        response += "\n" + ewcfg.item_group_commands.get("trap_pranks")
    # Instruments
    if any(item in (static_items.furniture_instrument + ["whistle", "bass"]) for item in items_template_list):
        response += "\n" + ewcfg.item_group_commands.get("instruments")
    # Body spray
    if any(item in ["juviegradefuckenergybodyspray", "superduperfuckenergybodyspray", "gmaxfuckenergybodyspray"] for item in items_template_list):
        response += "\n" + ewcfg.item_group_commands.get("bodyspray")
    # Trading cards
    if any(item in ["tradingcardpack", "promotradingcardpack", "tcgboosterbox"] for item in items_template_list):
        response += "\n" + ewcfg.item_group_commands.get("tradingcards")
    # Wrapping Paper
    if any(item in static_items.wrap_items_names for item in items_template_list):
        response += "\n" + ewcfg.item_group_commands.get("wrappingpaper")
    

    if response != "**IN YOUR INVENTORY:**":
        return (response + "\n")
    else:
        return "No special commands found for items in your inventory. Try \"!commands allitems\"."


def holiday_commands(header = True):
    if header:
        response = "\n**EVENTS:**\n"
    else:
        response = ""
    if ewcfg.dh_active:
        return "{}{}".format(response, ewcfg.holidaycommands.get('doublehalloween'))
    elif ewcfg.slimernalia_active:
        return "{}{}".format(response, ewcfg.holidaycommands.get('slimernalia'))
    elif ewcfg.swilldermuk_active:
        return "{}{}".format(response, ewcfg.holidaycommands.get('swilldermuk'))

    else:
        return ''

""" used for !shares """


def get_user_shares_str(id_server = None, stock = None, id_user = None):
    response = ""
    if id_server != None and stock != None and id_user != None:
        user_data = EwUser(id_server=id_server, id_user=id_user)
        stock = EwStock(id_server=id_server, stock=stock)
        shares = market_utils.getUserTotalShares(id_server=user_data.id_server, stock=stock.id_stock, id_user=user_data.id_user)
        shares_value = round(shares * (stock.exchange_rate / 1000.0))

        response = "You have {shares:,} shares in {stock}".format(shares=shares, stock=ewcfg.stock_names.get(stock.id_stock))

        # if user_data.poi == ewcfg.poi_id_downtown:
        response += ", currently valued at {coin:,} SlimeCoin.".format(coin=shares_value)
        # else:
        #	response += "."

    return response

