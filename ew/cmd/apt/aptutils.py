import asyncio
import random
from copy import deepcopy

from ew.backend import item as bknd_item
from ew.backend import core as bknd_core
from ew.backend.apt import EwApartment
from ew.backend.item import EwItem
from ew.backend.market import EwStock
from ew.static import cfg as ewcfg
from ew.static import cosmetics
from ew.static import poi as poi_static
from ew.static import hue as hue_static
from ew.static import items as static_items
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import move as move_utils
from ew.utils import rolemgr as ewrolemgr
from ew.utils.combat import EwUser
from ew.utils.market import EwMarket
from ew.utils.slimeoid import EwSlimeoid


async def usekey(cmd, owner_user):
    owner_apartment = EwApartment(id_user=owner_user.id_user, id_server=cmd.guild.id)
    user_data = EwUser(member=cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)
    poi_dest = poi_static.id_to_poi.get(ewcfg.poi_id_apt + owner_apartment.poi)  # there isn't an easy way to change this, apologies for being a little hacky
    inv = bknd_item.inventory(id_user=cmd.message.author.id, id_server=cmd.guild.id)


    key = None
    for item_inv in inv:
        if "key to" in item_inv.get('name'):
            item_key_check = EwItem(id_item=item_inv.get('id_item'))
            if item_key_check.item_props.get("houseID") == str(owner_user.id_user):
                key = item_key_check

    if cmd.message.guild is None or not ewutils.channel_name_is_poi(cmd.message.channel.name):
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You must enter an apartment in a zone's channel.".format(cmd.tokens[0])))
    elif key == None:
        response = "You don't have a key for their apartment."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    elif owner_apartment.apt_class == ewcfg.property_class_c or (owner_apartment.apt_class in [ewcfg.property_class_a, ewcfg.property_class_b] and key.id_item == owner_apartment.key_2):
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Your key's not working at this new flat. Your roomates must've forgotten to upgrade apartments. Congratulations on the homelessness by the way.".format(cmd.tokens[0])))
    elif owner_apartment.poi != poi.id_poi:
        response = "Your key doesn't match an apartment here."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    else:
        move_utils.move_counter += 1
        move_current = ewutils.moves_active[cmd.message.author.id] = move_utils.move_counter
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You start walking toward the apartment."))

        await asyncio.sleep(20)

        if move_current == ewutils.moves_active[cmd.message.author.id]:
            user_data = EwUser(member=cmd.message.author)
            user_data.poi = poi_dest.id_poi
            user_data.visiting = owner_user.id_user
            user_data.persist()
            await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
            response = "You're in the apartment."

            try:
                await fe_utils.send_message(cmd.client, cmd.message.author, response)
            except:
                await fe_utils.send_message(cmd.client, fe_utils.get_channel(cmd.guild, poi_dest.channel), fe_utils.formatMessage(cmd.message.author, response))


# returns a price based on the stock with the biggest change
def getPriceBase(cmd):
    # based on stock success
    user_data = EwUser(member=cmd.message.author)  # market rates average to 1000. This fomula calculates prices to specification based on that amount.
    kfc = EwStock(stock='kfc', id_server=user_data.id_server)
    tcb = EwStock(stock='tacobell', id_server=user_data.id_server)
    hut = EwStock(stock='pizzahut', id_server=user_data.id_server)
    if abs(kfc.market_rate - 1000) > abs(tcb.market_rate - 1000) and abs(kfc.market_rate - 1000) > abs(hut.market_rate - 1000):
        return kfc.market_rate * 201
    elif abs(tcb.market_rate - 1000) > abs(hut.market_rate - 1000):
        return tcb.market_rate * 201
    else:
        return hut.market_rate * 201


def apt_max_compartment_capacity(user_data: EwUser, apt_data: EwApartment, compartment: str) -> int:
    max_capacity = ewcfg.apt_storage_base

    # Property Class Modifiers
    if apt_data.apt_class == ewcfg.property_class_b:
        max_capacity *= 2
    elif apt_data.apt_class == ewcfg.property_class_a:
        max_capacity *= 4
    elif apt_data.apt_class == ewcfg.property_class_s:
        max_capacity *= 8

    # Mutation Modifiers
    if ewcfg.mutation_id_packrat in user_data.get_mutations():
        max_capacity *= 2

    # Compartment Modifiers
    if compartment == ewcfg.compartment_id_bookshelf:
        max_capacity *= 3
    elif compartment == ewcfg.compartment_id_decorate:
        max_capacity *= 0.75
    elif compartment == ewcfg.compartment_id_closet:
        max_capacity *= 2

    return int(max_capacity)


def prepare_compartment_capacity(id_user, id_server, compartment) -> int:
    """ Why does this exist? As a nice little wrapper for all the behaviour for per-compartment commands. It's my refactor, I choose the jank! """
    user_data = EwUser(id_user=id_user, id_server=id_server)
    if user_data.visiting != "empty" and user_data.visiting is not None:
        apt_data = EwApartment(id_user=user_data.visiting, id_server=id_server)
    else:
        apt_data = EwApartment(id_user=id_user, id_server=id_server)

    max_capacity = apt_max_compartment_capacity(user_data, apt_data, compartment)

    return max_capacity


def apt_collection_look_str(id_server: int, id_item: int, show_capacity: bool = False) -> str:
    item = EwItem(id_item=id_item)
    collection_inv_id = "{}collection".format(id_item)

    # General collections will have italicized names
    if item.item_props.get('id_furniture') == "generalcollection":
        collection_name = "*{}*".format(item.item_props.get('furniture_name'))
        max_capacity = 10
    else:
        collection_name = item.item_props.get('furniture_name')
        max_capacity = 50

    response = "**The {} holds:\n**".format(collection_name)

    # Get the collection's inventory
    collection = bknd_item.inventory(id_server=id_server, id_user=collection_inv_id)

    # Get all the item names
    if collection:
        hammerspace = []
        for thing in collection:
            hammerspace.append(thing.get('name'))
        
        if hammerspace == []:
            response += "Nothing!"
        else:
            response += ewutils.formatNiceList(hammerspace)
            response = response + '.'

    # Specify capacity if requested
    if show_capacity:
        response += f"\n{collection_name} capacity: ({len(collection)}/{max_capacity})"

    return response


def apt_decorate_look_str(id_server: int, id_user: int, show_capacity: bool = False) -> str:
    furn_response = ""
    collections_placed = False
    furns = bknd_item.inventory(id_user=str(id_user) + ewcfg.compartment_id_decorate, id_server=id_server, item_type_filter=ewcfg.it_furniture)
    furniture_id_list = []
    collections_id_list = []
    for furn in furns:
        i = EwItem(furn.get('id_item'))
        # Collections are collected and handled in a separate area
        if i.item_props.get('id_furniture') in static_items.furniture_collection:
            collections_id_list.append(furn.get('id_item'))
            collections_placed = True
        else:
            furn_response += "{} ".format(i.item_props['furniture_look_desc'])
            furniture_id_list.append(i.item_props['id_furniture'])

        hue = hue_static.hue_map.get(i.item_props.get('hue'))
        if hue is not None and i.item_props.get('id_furniture') not in static_items.furniture_specialhue:
            furn_response += " It's {}. ".format(hue.str_name)
        elif i.item_props.get('id_furniture') in static_items.furniture_specialhue:
            if hue is not None:
                furn_response = furn_response.replace("-*HUE*-", hue.str_name)
            else:
                furn_response = furn_response.replace("-*HUE*-", "white")

    # FIXME Refactor this for the love of god
    if all(elem in furniture_id_list for elem in static_items.furniture_lgbt):
        furn_response += "\nThis is the most homosexual room you could possibly imagine. Everything is painted rainbow. A sign on your bedroom door reads \"FORNICATION ZONE\". There's so much love in the air that some dust mites set up a gay bar in your closet. It's amazing."
    if all(elem in furniture_id_list for elem in static_items.furniture_haunted):
        furn_response += "\nOne day, on a whim, you decided to say \"Levy Jevy\" 3 times into the mirror. Big mistake. Not only did it summon several staydeads, but they're so enamored with your decoration that they've been squatting here ever since."
    if all(elem in furniture_id_list for elem in static_items.furniture_highclass):
        furn_response += "\nThis place is loaded. Marble fountains, fully stocked champagne fridges, complementary expensive meats made of bizarre unethical ingredients, it's a treat for the senses. You wonder if there's any higher this place can go. Kind of depressing, really."
    if all(elem in furniture_id_list for elem in static_items.furniture_leather):
        furn_response += "\n34 innocent lives. 34 lives were taken to build the feng shui in this one room. Are you remorseful about that? Obsessed? Nobody has the base antipathy needed to peer into your mind and pick at your decisions. The leather finish admittedly does look fantastic, however. Nice work."
    if all(elem in furniture_id_list for elem in static_items.furniture_church):
        furn_response += "\n" + random.choice(ewcfg.bible_verses)
    if all(elem in furniture_id_list for elem in static_items.furniture_pony):
        furn_response += "\nWhen the Mane 6 combine their powers, kindness, generosity, loyalty, honesty, magic, and the other one, they combine to form the most powerful force known to creation: friendship. Except for slime. That's still stronger."
    if all(elem in furniture_id_list for elem in static_items.furniture_blackvelvet):
        furn_response += "\nLooking around just makes you want to loosen your tie a bit and pull out an expensive cigar. Nobody in this city of drowned rats and slimeless rubes can stop you now. You commit homicide...in style. Dark, velvety smooth style."
    if all(elem in furniture_id_list for elem in static_items.furniture_seventies):
        furn_response += "\nLook at all this vintage furniture. Didn't the counterculture that created all this shit advocate for 'peace and love'? Yuck. I hope you didn't theme your bachelor pad around that kind of shit and just bought everything for its retro aesthetic."
    if all(elem in furniture_id_list for elem in static_items.furniture_shitty):
        furn_response += "\nYou're never gonna make it. Look at all this furniture you messed up, do you think someday you can escape this? You're never gonna have sculptures like Stradivarius, or paintings as good as that one German guy. You're deluded and sitting on splinters. Grow up."
    if all(elem in furniture_id_list for elem in static_items.furniture_instrument):
        furn_response += "\nYou assembled the instruments. Now all you have to do is form a soopa groop and play loudly over other people acts next Slimechella. It's high time the garage bands of this city take over, with fresh homemade shredding and murders most foul. The world's your oyster. As soon as you can trust them with all this expensive equipment."
    if all(elem in furniture_id_list for elem in static_items.furniture_slimecorp):
        furn_response += "\nSUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP. SUBMIT TO SLIMECORP."
    if all(elem in furniture_id_list for elem in static_items.furniture_NMS):
        furn_response += "\nThis room just reeks of dorm energy. You've clearly pilfered some poor Neo Milwaukee State student's room just to make a hollow imitation of your college days. Unless you haven't had those yet, in which case, Good Luck Charlie."
    if all(elem in furniture_id_list for elem in static_items.furniture_hatealiens):
        furn_response += "\nWhoa, your flat is so futuristic! You've got LED lights hanging from every wall to show how far in the future you are compared to everyone else. They just don't get it."
    if all(elem in furniture_id_list for elem in static_items.furniture_hummels):
        furn_response += "\nYour apartment has severe elderly vibes, like a thick fog."

    market_data = EwMarket(id_server=id_server)
    clock_data = ewutils.weather_txt(market_data)
    clock_data = clock_data[16:20]
    furn_response = furn_response.format(time=clock_data)

    if show_capacity:
        max_capacity = prepare_compartment_capacity(id_user, id_server, compartment=ewcfg.compartment_id_decorate)
        furn_response += f"\nFurniture Capacity ({len(furns)}/{max_capacity})"

    # Handle collections
    for collection_id in collections_id_list:
        collection_response = apt_collection_look_str(id_server=id_server, id_item=collection_id, show_capacity=show_capacity)
        furn_response += "\n" + collection_response
    if collections_placed is True:
        furn_response += "\n*('!inspect' collections for more info)*"

    return furn_response


def apt_fridge_look_str(id_server: int, id_user: int, show_capacity: bool = False) -> str:
    response = "**The fridge contains:**\n"
    frids = bknd_item.inventory(id_user=str(id_user) + ewcfg.compartment_id_fridge, id_server=id_server)
    fridge_contents = []
    if frids:
        stacked_fridge_map = {}
        for frid in frids:
            if frid.get("name") in stacked_fridge_map:
                stacked_item = stacked_fridge_map.get(frid.get("name"))
                stacked_item["quantity"] += frid.get("quantity")
            else:
                stacked_fridge_map[frid.get("name")] = deepcopy(frid)
        item_names = stacked_fridge_map.keys()
        for item_name in item_names:
            # Get the stack's item data
            item = stacked_fridge_map.get(item_name)

            # Generate the stack's line in the response
            response_part = "{soulbound_style}{name}{soulbound_style}{quantity}".format(
                name=item.get('name'),
                soulbound_style=("**" if item.get('soulbound') else ""),
                quantity=(" **x{:,}**".format(item.get("quantity")) if (item.get("quantity") > 0) else "")
            )
            fridge_contents.append(response_part)
        response += ewutils.formatNiceList(fridge_contents)
        response += '.'
    else:
        response += "Nothing."

    if show_capacity:
        max_capacity = prepare_compartment_capacity(id_user, id_server, compartment=ewcfg.compartment_id_fridge)
        response += f"\nFridge Capacity: ({len(frids)}/{max_capacity})"

    return response


def apt_closet_look_str(id_server: int, id_user: int, show_capacity: bool = False) -> str:
    closet_resp = "**The closet contains:**\n"
    closet_contents = []
    poud_stack = 0

    closets = bknd_item.inventory(id_user=str(id_user) + ewcfg.compartment_id_closet, id_server=id_server)
    if closets:
        stacked_closet_map = {}
        for closet in closets:
            if closet.get("name") in stacked_closet_map:
                stacked_item = stacked_closet_map.get(closet.get("name"))
                stacked_item["quantity"] += closet.get("quantity")
            else:
                stacked_closet_map[closet.get("name")] = deepcopy(closet)
        item_names = stacked_closet_map.keys()
        for item_name in item_names:
            # Get the stack's item data
            item = stacked_closet_map.get(item_name)
            item_obj = EwItem(id_item=item.get('id_item'))
            if item_obj.id_item == ewcfg.item_id_slimepoudrin:
                poud_stack += 1
            # Generate the stack's line in the response
            response_part = "{soulbound_style}{name}{soulbound_style}{quantity}".format(
                name=item.get('name'),
                soulbound_style=("**" if item.get('soulbound') else ""),
                quantity=(" **x{:,}**".format(item.get("quantity")) if (item.get("quantity") > 0) else "")
            )
            closet_contents.append(response_part)
        if not closet_resp:
            closet_resp = "Nothing."
        else:
            closet_resp += ewutils.formatNiceList(closet_contents)
    else:
        closet_resp += "Nothing."

    response = ""
    response += closet_resp

    if show_capacity:
        max_capacity = prepare_compartment_capacity(id_user, id_server, compartment=ewcfg.compartment_id_closet)
        response += f"\nCloset Capacity: ({len(closets) - poud_stack}/{max_capacity})"

    return response


def apt_bookshelf_look_str(id_server: int, id_user: int, show_capacity: bool = False) -> str:
    response = ""
    shelves = bknd_item.inventory(id_user=str(id_user) + ewcfg.compartment_id_bookshelf, id_server=id_server)
    if shelves:
        response += "**The bookshelf contains:**\n"
        shelf_pile = []
        for shelf in shelves:
            shelf_pile.append(shelf.get('name'))
        response += ewutils.formatNiceList(shelf_pile)
        response = response + '.'

    # This is only done for the compartment-specific commands, so loading apt_model and user_model is relatively efficient
    if show_capacity:
        max_capacity = prepare_compartment_capacity(id_user, id_server, compartment=ewcfg.compartment_id_bookshelf)
        response += f"\nBookshelf Capacity: ({len(shelves)}/{max_capacity})"

    return response


def apt_slimeoid_look_str(id_server: int, id_user: int, show_capacity: bool = False) -> str:
    response = ""
    data = None
    id_user = str(id_user) + 'freeze'
    slimeoid_data = EwSlimeoid(id_user=str(id_user), id_server=id_server)

    if slimeoid_data:
        sql = f"SELECT {ewcfg.col_name} FROM slimeoids WHERE {ewcfg.col_id_user} = %s"
        data = bknd_core.execute_sql_query(sql, [id_user])

        if data:
            response += "In the freezer, you hear "
            iterate = 0
            for row in data:
                if iterate > 0:
                    response += ", "
                if iterate >= len(data) - 1 and len(data) > 1:
                    response += "and "
                response += row[0]
                iterate += 1
            response += " cooing to themselves."

    if show_capacity:
        response += f"\nFreezer Capacity: ({len(data)}/???)"

    return response
