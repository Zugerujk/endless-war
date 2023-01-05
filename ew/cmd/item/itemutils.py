import sys

from ew.backend import core as bknd_core
from ew.backend import item as bknd_item
from ew.backend.item import EwItem
from ew.static import cfg as ewcfg
from ew.utils import core as ewutils
from ew.utils.combat import EwUser
from ew.static.weapons import weapon_list
"""
    Drop item into current district.
"""


def item_drop(
        id_item = None,
        other_poi = None
):
    try:
        item_data = EwItem(id_item=id_item)
        user_data = EwUser(id_user=item_data.id_owner, id_server=item_data.id_server)
        if other_poi == None:
            dest = user_data.poi
        else:
            dest = other_poi

        if item_data.item_type == ewcfg.it_cosmetic:
            item_data.item_props["adorned"] = "false"
        item_data.persist()
        bknd_item.give_item(id_user=dest, id_server=item_data.id_server, id_item=item_data.id_item)
    except Exception as e:
        ewutils.logMsg("Failed to drop item {}: {}.".format(id_item, e))


def get_fish_collection(id_item, id_server):
    item = EwItem(id_item=id_item)
    # Checks whether the collection is in an apartment "decorate" inventory or the player's inventory
    if 'decorate' not in str(item.id_owner):
        return 'It\'s a large aquarium, built for whole schools of fish. You can\'t see what\'s inside because you\'re nearly killing yourself carrying it.'

    # Create string for the "id_user" corresponding to the collection.  
    id_item_col = "{}collection".format(id_item)

    fish_inv = bknd_item.inventory(id_server=id_server, id_user=id_item_col)

    response = ""

    if len(fish_inv) == 0:
        return "Look at all these- wait, you don't have any fish in here."
    elif len(fish_inv) == 1:
        response += "There's just one fish in here. It's feeling very loved."
    elif len(fish_inv) < 6:
        response += "It's pretty spacious in here!"
    elif len(fish_inv) < 43:
        response += "Look at all these fish!"
    else:
        response += "This thing is packed!"

    response += " There's "

    fish_arr = []

    for fish in fish_inv:
        fish_item = EwItem(fish.get('id_item'))
        length = fish_item.item_props.get('length')
        # If the fish doesn't have a length, generate it a random average length
        if length is None:
            length = float((ewcfg.fish_size_range.get(fish_item.item_props.get('size'))[0] + ewcfg.fish_size_range.get(fish_item.item_props.get('size'))[1]) / 2)
            fish_item.item_props['length'] = length
            fish_item.persist()
        # Add the fish's name and length to a list
        fish_arr.append("a {} ({} in)".format(fish.get('name'), length))

    # Create a response, formatting a nice-looking sentence from the fish name/length list.
    response += "{}{}".format(ewutils.formatNiceList(names=fish_arr), ".")
    return response


def get_scalp_collection(id_item, id_server):
    item = EwItem(id_item=id_item)
    # Checks whether the collection is in an apartment "decorate" inventory or the player's inventory
    if 'decorate' not in str(item.id_owner):
        return 'It\'s a scalp board, detailing the people you\'ve eliminated. Somehow, show and tell in public seems like a bad idea.'

    # Create string for the "id_user" corresponding to the collection.
    id_item_col = "{}collection".format(id_item)

    scalp_inv = bknd_item.inventory(id_server=id_server, id_user=id_item_col)
    response = "You take a gander at all these marks.\n             __**SHIT LIST**__:"

    if len(scalp_inv) == 0:
        return "Soon. This board will fill someday."

    for scalp in scalp_inv:
        scalp_item = EwItem(scalp.get('id_item'))
        # Get the name and kill description from the scalp's item_props
        victim_name = scalp_item.item_props.get('cosmetic_name').replace('\'s scalp', '').capitalize()
        victim_death = scalp_item.item_props.get('cosmetic_desc').replace('A scalp.', '')
        for weapon in weapon_list:
            # If the scalp's kill description matches a weapon, replace that with the weapon's kill descriptor (ie. "Gunned down")
            if weapon.str_scalp == victim_death:
                victim_death = "{}{}".format(weapon.str_killdescriptor.capitalize(), '.')
                break
        response += "\n~~{}~~     *{}*".format(victim_name, victim_death)

    return response


def get_soul_collection(id_item, id_server):
    item = EwItem(id_item=id_item)
    # Checks whether the collection is in an apartment "decorate" inventory or the player's inventory
    if 'decorate' not in str(item.id_owner):
        return 'It\'s a soul cylinder. You can\'t really tell whose soul is whose. You\'ve been carrying this thing around and all the souls are jostled and queasy.'

    # Create string for the "id_user" corresponding to the collection.
    id_item_col = "{}collection".format(id_item)

    soul_inv = bknd_item.inventory(id_server=id_server, id_user=id_item_col)

    if len(soul_inv) == 0:
        return "No souls. Just ask anyone."

    response = "You look into the cylinder to check how the souls are doing.\n\n"
    for soul in soul_inv:
        # Get the user_data from the soul's corresponding user
        soul_item = EwItem(id_item=soul.get('id_item'))
        soul_user = EwUser(id_server=id_server, id_user=soul_item.item_props.get('user_id')) 
        # If the user doesn't have a defined race, set it to humanoid
        if soul_user.race is None or soul_user.race == '':
            soul_user.race = ewcfg.race_humanoid #do not persist this!

        # Change flavor text based on the soul's race
        soul_text = ewcfg.defined_races.get(soul_user.race).get('soul_behavior')
        soul_name = soul_item.item_props.get('cosmetic_name')
        response += "{} {}\n".format(soul_name, soul_text)

    return response


def get_weapon_collection(id_item, id_server):
    item = EwItem(id_item=id_item)
    # Checks whether the collection is in an apartment "decorate" inventory or the player's inventory
    if 'decorate' not in str(item.id_owner):
        return "It's a weapon rack. You can't admire its splendor while it's on your back, though."

    # Create string for the "id_user" corresponding to the collection.
    id_item_col = "{}collection".format(id_item)
    weapon_inv = bknd_item.inventory(id_server=id_server, id_user=id_item_col)

    if len(weapon_inv) == 0:
        return "There are no weapons in here. Arms are meant to be used, not preserved."

    response = "You take a look at the archive of your violent history...\n\n"

    for wep in weapon_inv:
        # Get the weapon's stats, based on its props
        weapon_item = EwItem(id_item=wep.get('id_item'))
        kills = weapon_item.item_props.get('totalkills', 0)
        backfires = weapon_item.item_props.get('totalsuicides', 0)
        name = weapon_item.item_props.get('weapon_name')
        # If the weapon doesn't have a unique name, give it a generic descriptor
        if name is None or name == '':
            name = 'Generic {}'.format(weapon_item.item_props.get('weapon_type'))

        response += "{}: {} KILLS{}\n".format(name, kills, ", {} BACKFIRES".format(backfires) if backfires > 0 else "")

    return response


def get_crop_collection(id_item, id_server):
    item = EwItem(id_item=id_item)
    # Checks whether the collection is in an apartment "decorate" inventory or the player's inventory
    if 'decorate' not in str(item.id_owner):
        return "It's a greenhouse, built small enough to carry around (uncomfortably). Your unwieldy grip means you can't sus out what plants are inside."

    # Create string for the "id_user" corresponding to the collection.
    id_item_col = "{}collection".format(id_item)

    crop_inv = bknd_item.inventory(id_server=id_server, id_user=id_item_col)

    if len(crop_inv) == 0:
        return "There's no crops inside this portable greenhouse. Maybe they're potted instead?"

    response = "You glance at the Greenhouse. Inside, there's "

    crop_arr = []

    for crop in crop_inv:
        crop_icon = ewcfg.emote_blank
        # Get crop's type and name
        crop_item = EwItem(crop.get('id_item'))
        crop_type = crop_item.item_props.get('id_food')
        crop_name = crop_item.item_props.get('food_name')
        # If the crop isn't None, get its matching emote
        if crop_type is not None:
            crop_icon = ewcfg.crop_icon_map.get(crop_type)
        
        # Add crop to a list with its emote
        crop_arr.append("a {} {}".format(crop_name, crop_icon))

    # Create a response, formatting a nice-looking sentence from the crop name/emote list
    response += "{}{}".format(ewutils.formatNiceList(names=crop_arr), ".")
    return response


def get_general_collection(id_item, id_server):
    item = EwItem(id_item=id_item)
    # Checks whether the collection is in an apartment "decorate" inventory or the player's inventory
    if 'decorate' not in str(item.id_owner):
        return "It's a multi-item display case. Best viewed when placed."

    # Create string for the "id_user" corresponding to the collection.
    id_item_col = "{}collection".format(id_item)
    item_inv = bknd_item.inventory(id_server=id_server, id_user=id_item_col)

    if len(item_inv) == 0:
        return "There's nothing in here at the moment."

    response = "You examine your preserved collection. Inside is "
    item_arr = []

    for gen_item in item_inv:
        # Add item to a list with its ID
        item_arr.append("a {} ({})".format(gen_item.get('name'), gen_item.get('id_item')))

    # Create a response, formatting a nice-looking sentence from the item name/ID list
    response += "{}{}".format(ewutils.formatNiceList(names=item_arr), ".")

    return response