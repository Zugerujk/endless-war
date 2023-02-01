import asyncio
from ew.backend import item as bknd_item
from ew.backend import core as bknd_core
from ew.backend.item import EwItem
from ew.backend.dungeons import EwGamestate
from ew.static import cfg as ewcfg
from ew.static import poi as poi_static
from ew.static import weapons as static_weapons
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
import ew.utils.cmd as cmd_utils
from ew.utils.combat import EwUser
from functools import partial

""" allow a juvie to join your gang """


async def vouch(cmd):
    user_data = EwUser(member=cmd.message.author)

    response = ""

    if user_data.faction == "":
        response = "You have to join a faction before you can vouch for anyone."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if cmd.mentions_count == 0:
        response = "Vouch for whom?"
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    member = cmd.mentions[0]
    vouchee_data = EwUser(member=member)

    if vouchee_data.poi != user_data.poi:
        response = "How do you pretend to vouch for that juvenile if you aren't with them, using a carrier pigeon? Go find them, dumbfuck!"
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if vouchee_data.faction == user_data.faction:
        response = "{} has already joined your faction.".format(member.display_name)
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    vouchers = vouchee_data.get_vouchers()

    if user_data.faction in vouchers:
        response = "A member of your faction has already vouched for {}.".format(member.display_name)
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    vouchee_data.vouch(faction=user_data.faction)

    response = "You place your undying trust in {}.".format(member.display_name)
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


# Not directly referenced. Cmd directs these commands to the apt or chest version
# Maybe these should be moved to item cmds
"""store items in a communal chest in your gang base"""

used_chest_poi_ids = []

async def store(cmd):
    if len(cmd.tokens) < 2:
        response = "{} what?".format(cmd.tokens[0])
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    user_data = EwUser(member=cmd.message.author)
    response = ""

    poi = poi_static.id_to_poi.get(user_data.poi)
    if poi.community_chest == None:
        response = "There is no community chest here."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    elif user_data.poi in used_chest_poi_ids:
        response = "You watch patiently as someone infront of you shits their entire stomach into the chest. They'll be done in a moment, try again then."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    else:
        if len(poi.factions) > 0 and user_data.faction not in poi.factions:
            response = "Get real, asshole. You haven't even enlisted into this gang yet, so it's not like they'd trust you with a key to their valuables."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if cmd.tokens[1] == 'all':
        cmd.tokens[1] = '100'

    multistow = 1
    startparse = 1

    items = []

    if cmd.tokens[1].isnumeric() and cmd.tokens_count > 2:
        startparse = 2
        multistow = int(cmd.tokens[1])
        if multistow > 100:
            multistow = 100

    item_search = ewutils.flattenTokenListToString(cmd.tokens[startparse:])

    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None)

    if item_sought:

        if not item_sought.get('soulbound'):
            items_had = 0
            loop_sought = item_sought.copy()

            item_cache = bknd_core.get_cache(obj_type="EwItem")

            chest_occupied = False
            if multistow > 1:
                chest_occupied = True
                used_chest_poi_ids.append(user_data.poi)
            try:
                while multistow > 0 and loop_sought is not None:
                    item = EwItem(id_item=loop_sought.get("id_item"))
                    item_search = ewutils.flattenTokenListToString(loop_sought.get('name'))
                    if item.item_type == ewcfg.it_weapon:
                        if user_data.weapon >= 0 and item.id_item == user_data.weapon:
                            if user_data.weaponmarried:
                                weapon = static_weapons.weapon_map.get(item.item_props.get("weapon_type"))
                                response = "Your cuckoldry is appreciated, but your {} will always remain faithful to you.".format(item_sought.get('name'))
                                if chest_occupied:
                                    used_chest_poi_ids.remove(user_data.poi)
                                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                            else:
                                user_data.weapon = -1
                                user_data.persist()
                        elif item.id_item == user_data.sidearm:
                            user_data.sidearm = -1
                            user_data.persist()

                    if item.item_type == ewcfg.it_cosmetic:
                        if "adorned" in item.item_props:
                            item.item_props["adorned"] = "false"
                        if "slimeoid" in item.item_props:
                            item.item_props["slimeoid"] = "false"

                    item.persist()
                    #bknd_item.give_item(id_item=loop_sought.get('id_item'), id_server=item.id_server, id_user=poi.community_chest)
                    items.append(int(loop_sought.get('id_item')))

                    cache_item = item_cache.get_entry(unique_vals={"id_item": int(loop_sought.get('id_item'))})
                    cache_item.update({'id_owner': poi.community_chest})
                    item_cache.set_entry(data=cache_item)

                    #= await event_loop.run_in_executor(None, item_cache.find_entries, criteria)
                    func = partial(bknd_item.find_item, item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None)
                    event_loop = asyncio.get_event_loop()
                    loop_sought = await event_loop.run_in_executor(None, func)

                    items_had += 1
                    multistow -= 1
            except:
                ewutils.logMsg("Failed to multi-stow {}. Error thrown.".format(item_sought).get("name"))
            if chest_occupied:
                used_chest_poi_ids.remove(user_data.poi)
            if items_had > 1:
                name_string = "{}(x{})".format(item_sought.get("name"), items_had)
            else:
                name_string = item_sought.get("name")

            bknd_item.give_item_multi(id_list=items, destination=poi.community_chest)
            response = "You store your {} in the community chest.".format(name_string)

        else:
            response = "You can't {} soulbound items.".format(cmd.tokens[0])
    else:
        if item_search:
            response = "You don't have one"
        else:
            response = "{} which item? (check **!inventory**)".format(cmd.tokens[0])

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


"""retrieve items from a communal chest in your gang base"""



async def take(cmd):
    if len(cmd.tokens) < 2:
        response = "{} what?".format(cmd.tokens[0])
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    user_data = EwUser(member=cmd.message.author)
    response = ""
    admin = 0
    if cmd.message.author.guild_permissions.administrator:
        admin = 1


    poi = poi_static.id_to_poi.get(user_data.poi)
    if poi.community_chest == None:
        response = "There is no community chest here."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    elif user_data.poi in used_chest_poi_ids:
        response = "Wait until the last bloke is done. Even thieves have to wait in line!"
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    else:
        if len(poi.factions) > 0 and user_data.faction not in poi.factions:
            response = "Get real, asshole. You haven't even enlisted into this gang yet, so it's not like they'd trust you with a key to their valubles."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    multisnag = 1
    startparse = 1
    if cmd.tokens[1] == 'all':
        cmd.tokens[1] = '100'

    if cmd.tokens[1].isnumeric() and cmd.tokens_count > 2:
        startparse = 2
        multisnag = int(cmd.tokens[1])
        if multisnag > 100:
            multisnag = 100

    item_search = ewutils.flattenTokenListToString(cmd.tokens[startparse:])

    item_sought = bknd_item.find_item(item_search=item_search, id_user=poi.community_chest, id_server=cmd.guild.id if cmd.guild is not None else None, admin = admin)

    items_snagged = 0
    item_list = []
    item_cache = bknd_core.get_cache(obj_type="EwItem")

    if item_sought:
        item_search = ewutils.flattenTokenListToString(item_sought.get('name'))
        loop_sought = item_sought.copy()

        chest_occupied = False
        if multisnag > 1:
            chest_occupied = True
            used_chest_poi_ids.append(user_data.poi)
        try:
            while multisnag > 0 and loop_sought is not None:
                if items_snagged == 0:
                    inv_response = bknd_item.check_inv_capacity(user_data=user_data, item_type=loop_sought.get('item_type'), return_strings=True, pronoun="You")

                    if inv_response != "":
                        if chest_occupied:
                            used_chest_poi_ids.remove(user_data.poi)
                        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, inv_response))

                    list_items = bknd_item.inventory(
                            id_user=cmd.message.author.id,
                            id_server=cmd.guild.id,
                            item_type_filter=loop_sought.get('item_type')
                        )



                    if loop_sought.get('item_type') == ewcfg.it_food:
                        food_items = bknd_item.inventory(
                            id_user=cmd.message.author.id,
                            id_server=cmd.guild.id,
                            item_type_filter=ewcfg.it_food
                        )

                        if user_data.get_food_capacity() - len(food_items) < multisnag:
                            multisnag = user_data.get_food_capacity() - len(food_items)
                            del food_items
                    elif loop_sought.get('item_type') == ewcfg.it_weapon:
                        weapons_held = bknd_item.inventory(
                            id_user=cmd.message.author.id,
                            id_server=cmd.guild.id,
                            item_type_filter=ewcfg.it_weapon
                        )

                        if user_data.life_state == ewcfg.life_state_corpse:
                            del weapons_held
                            response = "Ghosts can't hold weapons."
                            if chest_occupied:
                                used_chest_poi_ids.remove(user_data.poi)
                            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                        elif user_data.get_weapon_capacity() - len(weapons_held) < multisnag:
                            multisnag = user_data.get_weapon_capacity() - len(weapons_held)
                            del weapons_held

                    else:
                        other_items = bknd_item.inventory(
                            id_user=cmd.message.author.id,
                            id_server=user_data.id_server,
                            item_type_filter=loop_sought.get('item_type')
                        )
                        if ewcfg.generic_inv_limit - len(other_items) < multisnag:
                            multisnag = ewcfg.generic_inv_limit - len(other_items)
                            del other_items

                items_snagged += 1
                multisnag -= 1

                bknd_item.give_item(id_item=loop_sought.get('id_item'), id_server=user_data.id_server, id_user=user_data.id_user)
                item_list.append(loop_sought.get('id_item'))

                cache_item = item_cache.get_entry(unique_vals={"id_item": loop_sought.get('id_item')})
                cache_item.update({'id_owner': cmd.message.author.id})
                item_cache.set_entry(data=cache_item)


                #loop_sought = bknd_item.find_item(item_search=item_search, id_user=poi.community_chest, id_server=cmd.guild.id if cmd.guild is not None else None, admin=admin)

                func = partial(bknd_item.find_item, item_search=item_search, id_user=poi.community_chest,
                            id_server=cmd.guild.id if cmd.guild is not None else None, admin=admin)
                event_loop = asyncio.get_event_loop()
                loop_sought = await event_loop.run_in_executor(None, func)
        except:
            ewutils.logMsg("Failed to multi-snag {}. Error thrown.".format(item_sought).get("name"))
        if chest_occupied:
            used_chest_poi_ids.remove(user_data.poi)
        if items_snagged > 1:
            name_string = "{}(x{})".format(item_sought.get("name"), items_snagged)
        else:
            name_string = item_sought.get('name')

        response = "You retrieve a {} from the community chest.".format(name_string)

        del item_sought
    else:
        if item_search:
            response = "There isn't one here."
        else:
            response = "{} which item? (check **{}**)".format(cmd.tokens[0], ewcfg.cmd_communitychest)

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def vote(cmd):
    user_data = EwUser(member=cmd.message.author)
    gamestate = EwGamestate(id_state='votingtime', id_server=cmd.guild.id)


    if user_data.poi not in [ewcfg.poi_id_juviesrow, ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_copkilltown, ewcfg.poi_id_thesewers]:
        response = "You can't vote if you're not in a polling place. Go to a gang base, Juvies' Row, or the sewers to vote."
    elif gamestate.bit == 0:
        response = "They haven't opened up the polling places yet."
    elif cmd.mentions_count < 1:
        response = "You can't vote for nobody. What, were you planning to write in Deez Nuts?"
    else:
        target = cmd.mentions[0]
        results = bknd_core.execute_sql_query("SELECT 1 FROM votes WHERE id_server = %s AND id_user = %s and poi = %s".format(
                id_role=ewcfg.col_id_role,
                name=ewcfg.col_role_name
            ), (
                cmd.guild.id,
                user_data.id_user,
                user_data.poi
            ))
        if len(results) > 0:
            response = "You already voted here. The stupid motherfuckers over there won't let you stuff the ballot."
        else:
            try:
                bknd_core.execute_sql_query(
                    "REPLACE INTO votes ({id_server}, {poi}, {id_user}, {target}) VALUES (%s, %s, %s, %s)".format(
                        id_server=ewcfg.col_id_server,
                        poi=ewcfg.col_poi,
                        id_user=ewcfg.col_id_user,
                        target = "target"
                    ), (
                       user_data.id_server,
                        user_data.poi,
                        user_data.id_user,
                        target.id
                    ))
            except:
                ewutils.logMsg("Failed to write vote {} to database.".format(target.id))
            response = "You put in your vote for {}.".format(cmd.mentions[0].display_name)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response), delete_after=5)

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def hydraulicpress(cmd): #dammit if this worked i bet it would be fucking huge. i wish people didn't hate the idea so much
    state = EwGamestate(id_server=cmd.guild.id, id_state='hydraulicpress')
    #locked behind a gamestate that will remain off for the time being
    user_data = EwUser(member=cmd.message.author)
    if state.bit == 0:
        return await cmd_utils.fake_failed_command(cmd)
    else:
        if user_data.slimes < state.number:
            response = "You're too scrawny, the press won't fit your meager slimecount. Try again when you have {:,} slime or more.".format(state.number)
        elif cmd.mentions_count != 0:
            response = "You have to press the slime into someone."
        else:
            target = EwUser(member=cmd.mentions[0])

            if target.poi != user_data.poi:
                response = "You need to be in the same place."
            elif user_data.poi not in [ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_copkilltown, ewcfg.poi_id_juviesrow]:
                response = "You can't find a hydraulic press to use in here. The gang bases have some, you're pretty sure."
            elif target.slimes > 2000000:
                response = "They're too big, they won't fit in the press to receive your slime."
            elif user_data.life_state == ewcfg.life_state_corpse or target.life_state == ewcfg.life_state_corpse:
                response = "That seems pretty counterproductive..."
            else:

                target_1 = 2000000 - target.slimes
                target_2 = user_data.slimes - state.number
                final_target = min(target_1, target_2)

                q = "This will squeeze {:,} slime into {}. Hey, {}, do you !accept or !refuse it?".format(final_target, cmd.mentions[0].display_name, cmd.mentions[0].display_name)
                accept = await fe_utils.prompt(cmd=cmd, target=cmd.mentions[0], checktarget=True, question=q)
                user_data = EwUser(member=cmd.message.author)
                target = EwUser(member=cmd.mentions[0])

                target_1 = 2000000 - target.slimes
                target_2 = user_data.slimes - state.number
                final_target = min(target_1, target_2)

                if user_data.slimes < state.number or target.slimes > 2000000:
                    response = "Nice try, jackass."
                elif accept:
                    response = "You get under the press, and {} jumps into the receiver. \n\n**PSSSSHHHHHHHHSPLAAAAT!** You nearly feel your lungs pop under the pressure, but soon enough the process is complete. {} is {:,} slime richer!".format(cmd.mentions[0].display_name, cmd.mentions[0].display_name, final_target)
                    user_data.change_slimes(-final_target)
                    target.change_slimes(final_target)
                    user_data.persist()
                    target.persist()
                else:
                    response = "Huh, guess they're not biting. Their loss!"

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))



