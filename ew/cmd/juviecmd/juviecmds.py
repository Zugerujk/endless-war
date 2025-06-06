"""
    Commands and utilities related to Juveniles.
"""
import math
import random
import time

from ew.backend import item as bknd_item
from ew.backend import worldevent as bknd_worldevent
from ew.backend.item import EwItem
from ew.backend.market import EwMarket
from ew.backend.worldevent import EwWorldEvent
from ew.static import cfg as ewcfg
from ew.static import food as static_food
from ew.static import items as static_items
from ew.static import poi as poi_static
from ew.static import vendors
from ew.static import weapons as static_weapons
from ew.static import hunting as static_hunt
from ew.static import npc as static_npc
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import combat as cmbt_utils
from ew.utils import item as itm_utils
from ew.utils import poi as poi_utils
from ew.utils import rolemgr as ewrolemgr
from ew.utils import combat as cmbt_utils
from ew.utils import stats as ewstats
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict
from ew.utils.frontend import EwResponseContainer
from ew.utils.user import add_xp
from . import juviecmdutils
from .juviecmdutils import create_mining_event
from .juviecmdutils import gen_scavenge_captcha
from .juviecmdutils import get_mining_yield_by_grid_type
from .juviecmdutils import init_grid
from .juviecmdutils import mismine
from .juviecmdutils import print_grid
from ew.backend.dungeons import EwGamestate

try:
    import ew.cmd.debug as ewdebug
    from ew.static.rstatic import digup_relics
    from ew.static.rstatic import relic_map
    from ew.static.rstatic import question_map

except:
    import ew.cmd.debug_dummy as ewdebug
    from ew.static.rstatic_dummy import digup_relics
    from ew.static.rstatic_dummy import relic_map
    from ew.static.rstatic_dummy import question_map

async def crush(cmd):
    member = cmd.message.author
    user_data = EwUser(member=member)
    resp_cont = EwResponseContainer(id_server=cmd.guild.id)
    response = ""  # if it's not overwritten
    crush_slimes = ewcfg.crush_slimes

    command = "crush"
    if cmd.tokens[0] == (ewcfg.cmd_prefix + 'crunch'):
        command = "crunch"

    if user_data.life_state == ewcfg.life_state_corpse:
        response = "Alas, your ghostly form cannot {} anything. Lame.".format(command)
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    item_sought = bknd_item.find_item(item_search=item_search, id_user=user_data.id_user, id_server=user_data.id_server)

    if item_sought:
        sought_id = item_sought.get('id_item')
        item_data = EwItem(id_item=sought_id)

        response = "The item doesn't have !{} functionality".format(command)  # if it's not overwritten

        if item_data.item_props.get("id_item") == ewcfg.item_id_slimepoudrin:
            # delete a slime poudrin from the player's inventory
            bknd_item.item_delete(id_item=sought_id)

            levelup_response = user_data.change_slimes(n=crush_slimes, source=ewcfg.source_crush)
            user_data.persist()

            response = "You {} the hardened slime crystal with your bare teeth.\nYou gain {} slime. Sick, dude!!".format(command, crush_slimes)

            if len(levelup_response) > 0:
                response += "\n\n" + levelup_response

        elif item_data.item_props.get("id_item") == ewcfg.item_id_royaltypoudrin:
            # delete a royalty poudrin from the player's inventory
            bknd_item.item_delete(id_item=sought_id)
            crush_slimes = 5000

            levelup_response = user_data.change_slimes(n=crush_slimes, source=ewcfg.source_crush)
            user_data.persist()

            response = "You {} your hard-earned slime crystal with your bare teeth.\nYou gain {} slime. Ah, the joy of writing!".format(command, crush_slimes)

            if len(levelup_response) > 0:
                response += "\n\n" + levelup_response

        elif item_data.item_props.get("id_food") in static_food.vegetable_to_cosmetic_material.keys():
            bknd_item.item_delete(id_item=sought_id)

            crop_name = item_data.item_props.get('food_name')
            # Turn the crop into its proper cosmetic material item.
            cosmetic_material_id = static_food.vegetable_to_cosmetic_material[item_data.item_props.get("id_food")]
            new_item = static_items.item_map.get(cosmetic_material_id)

            new_item_type = ewcfg.it_item
            if new_item != None:
                new_name = new_item.str_name
                new_item_props = itm_utils.gen_item_props(new_item)
            else:
                ewutils.logMsg("ERROR: !crunch failed to retrieve proper cosmetic material for crop {}.".format(item_data.item_props.get("id_food")))
                new_name = None
                new_item_props = None

            generated_item_id = bknd_item.item_create(
                item_type=new_item_type,
                id_user=cmd.message.author.id,
                id_server=cmd.guild.id,
                item_props=new_item_props
            )

            response = "You {} your {} in your mouth and spit it out to create some {}!!".format(command, crop_name, new_name)

        elif item_data.item_props.get("id_food") in static_food.candy_ids_list:

            bknd_item.item_delete(id_item=sought_id)
            item_name = item_data.item_props.get('food_name')

            if float(getattr(item_data, "time_expir", 0)) < time.time():
                response = "The {} melts disappointingly in your hand...".format(item_name)

            else:
                gristnum = random.randrange(2) + 1
                gristcount = 0

                response = "You crush the {} with an iron grip. You gain {} piece(s) of Double Halloween Grist, as well as 11,000 Double Slimernalia XP!".format(item_name, gristnum)
                XPresponse = await add_xp(user_data.id_user, user_data.id_server, ewcfg.goonscape_dslimernalia_stat, 11000)
                if XPresponse != "":
                    resp_cont.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, XPresponse))

                while gristcount < gristnum:
                    grist = static_items.item_map.get(ewcfg.item_id_doublehalloweengrist)
                    grist_props = itm_utils.gen_item_props(grist)

                    bknd_item.item_create(
                        item_type=grist.item_type,
                        id_user=cmd.message.author.id,
                        id_server=cmd.message.guild.id,
                        item_props=grist_props
                    )

                    gristcount += 1

        elif item_data.item_props.get("id_item") == ewcfg.item_id_negapoudrin:

            # Delete a negapoudrin from the player's inventory
            bknd_item.item_delete(id_item=sought_id)
            crush_slimes = -1000000

            # Kill player if they have less than 1 million slime
            if user_data.slimes < 1000000:
                die_resp = await user_data.die(cause=ewcfg.cause_crushing)
                resp_cont.add_response_container(die_resp)

                response = "You {} your hard-earned slime crystal with your bare teeth.\nAs the nerve endings in your teeth explode, you realize you bit into a negapoudrin! You writhe on the ground as slime gushes from all of your orifices. You fucking die. {}".format(command, ewcfg.emote_slimeskull)

            # Remove 1 million slime from the player
            else:
                levelup_response = user_data.change_slimes(n = crush_slimes, source = ewcfg.source_crush)
                user_data.persist()

                response = "You {} your hard-earned slime crystal with your bare teeth.\nAs the nerve endings in your teeth explode, you realize you bit into a negapoudrin! You writhe on the ground as slime gushes from all of your orifices.".format(command)
            
                if len(levelup_response) > 0:
                    response += "\n\n" + levelup_response

        # If the item is a negaslimeoidheart
        elif item_data.item_props.get("context") == ewcfg.context_negaslimeoidheart:
            
            # Delete a core from the player's inventory
            bknd_item.item_delete(id_item=sought_id)
            crush_slimes = -1000000

            # Kill player if they have less than 1 million slime
            if user_data.slimes < 1000000:
                die_resp = await user_data.die(cause=ewcfg.cause_crushing)
                resp_cont.add_response_container(die_resp)
                
                response = "You {} the Negaslimeoid core with your bare teeth.\nAs the nerve endings in your teeth explode, you recoil in pain! You writhe on the ground as slime gushes from all of your orifices. You fucking die. {}".format(command, ewcfg.emote_slimeskull)

            # Remove 1 million slime from the player
            else:
                levelup_response = user_data.change_slimes(n = crush_slimes, source = ewcfg.source_crush)
                user_data.persist()

                # Give the player a negative dye
                bknd_item.item_create(
                    item_type=ewcfg.it_item,
                    id_user=cmd.message.author.id,
                    id_server=cmd.guild.id,
                    item_props={
                        'context': 'dye',
                        'item_name': '||Negative Dye||',
                        'item_desc': 'A small vial of ||negative dye||.',
                        'id_item': 'negativedye'
                                }
                )

                response = "You {} the Negaslimeoid core with your bare teeth.\nAs the nerve endings in your teeth explode, you recoil in pain! You writhe on the ground as slime gushes from all of your orifices. \n\nFrom within the Negaslimeoid's core, you recover a sample of ||Negative Dye||! This piece here is pretty rare, so don't waste it!".format(command)
            
                if len(levelup_response) > 0:
                    response += "\n\n" + levelup_response


    else:
        if item_search:  # if they didnt forget to specify an item and it just wasn't found
            response = "You don't have one."
        else:
            response = "{} which item? (check **!inventory**)".format(command)

    # Send the response to the player.
    resp_cont.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    await resp_cont.post()


""" player enlists in a faction/gang """


async def enlist(cmd):
    user_data = EwUser(member=cmd.message.author)

    user_slimes = user_data.slimes
    time_now = int(time.time())
    bans = user_data.get_bans()
    vouchers = user_data.get_vouchers()

    if user_data.life_state == ewcfg.life_state_corpse:
        response = "You're dead, bitch."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    elif ewutils.active_restrictions.get(user_data.id_user) != None and ewutils.active_restrictions.get(user_data.id_user) > 0:
        response = "You can't do that right now."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    elif user_slimes < ewcfg.slimes_toenlist:
        response = "You need to mine more slime to rise above your lowly station. ({}/{})".format(user_slimes, ewcfg.slimes_toenlist)
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if cmd.tokens_count > 1:
        desired_faction = cmd.tokens[1].lower()
    else:
        response = "Which faction? Say '{} {}', '{} {}', or '{} {}'.".format(ewcfg.cmd_enlist, ewcfg.faction_killers, ewcfg.cmd_enlist, ewcfg.faction_rowdys, ewcfg.cmd_enlist, ewcfg.faction_slimecorp)
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if desired_faction == ewcfg.faction_killers:
        if ewcfg.faction_killers in bans:
            response = "You are banned from enlisting in the {}.".format(ewcfg.faction_killers)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        elif ewcfg.faction_killers not in vouchers and user_data.faction != ewcfg.faction_killers:
            response = "You need a current gang member's permission to join the {}.".format(ewcfg.faction_killers)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        elif user_data.life_state in [ewcfg.life_state_enlisted, ewcfg.life_state_kingpin] and user_data.faction == ewcfg.faction_killers:
            response = "You are already enlisted in the {}! Look, your name is purple! Get a clue, idiot.".format(user_data.faction)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        elif user_data.faction == ewcfg.faction_rowdys or user_data.faction == ewcfg.faction_slimecorp:
            response = "Traitor! You can only {} in the {}, you treacherous cretin. Ask for a {} if you're that weak-willed.".format(ewcfg.cmd_enlist, user_data.faction, ewcfg.cmd_pardon)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        # elif user_data.poi not in [ewcfg.poi_id_copkilltown]:
        #	response = "How do you want to enlist in a gang's forces without even being in their headquarters? Get going to Cop Killtown, bitch."
        #	return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        else:
            response = "Enlisting in the {}.".format(ewcfg.faction_killers)
            if user_data.race == ewcfg.race_clown:
                user_data.race = ewcfg.race_humanoid
            user_data.life_state = ewcfg.life_state_enlisted
            user_data.faction = ewcfg.faction_killers
            user_data.time_lastenlist = time_now + ewcfg.cd_enlist
            for faction in vouchers:
                user_data.unvouch(faction)
            user_data.persist()
            await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)

    elif desired_faction == ewcfg.faction_rowdys:
        if ewcfg.faction_rowdys in bans:
            response = "You are banned from enlisting in the {}.".format(ewcfg.faction_rowdys)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        if ewcfg.faction_rowdys not in vouchers and user_data.faction != ewcfg.faction_rowdys:
            response = "You need a current gang member's permission to join the {}.".format(ewcfg.faction_rowdys)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        elif user_data.life_state in [ewcfg.life_state_enlisted, ewcfg.life_state_kingpin] and user_data.faction == ewcfg.faction_rowdys:
            response = "You are already enlisted in the {}! Look, your name is pink! Get a clue, idiot.".format(user_data.faction)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        elif user_data.faction == ewcfg.faction_killers or user_data.faction == ewcfg.faction_slimecorp:
            response = "Traitor! You can only {} in the {}, you treacherous cretin. Ask for a {} if you're that weak-willed.".format(ewcfg.cmd_enlist, user_data.faction, ewcfg.cmd_pardon)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        # elif user_data.poi not in [ewcfg.poi_id_rowdyroughhouse]:
        #	response = "How do you want to enlist in a gang's forces without even being in their headquarters? Get going to the Rowdy Roughhouse, bitch."
        #	return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        else:
            response = "Enlisting in the {}.".format(ewcfg.faction_rowdys)
            user_data.life_state = ewcfg.life_state_enlisted
            user_data.faction = ewcfg.faction_rowdys
            user_data.time_lastenlist = time_now + ewcfg.cd_enlist

            for faction in vouchers:
                user_data.unvouch(faction)
            user_data.persist()
            await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)

    elif desired_faction == ewcfg.faction_slimecorp:
        response = "Sorry, pal. That ship has sailed."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    else:
        response = "That's not a valid gang you can enlist in, bitch."

    # Send the response to the player.
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def renounce(cmd):
    user_data = EwUser(member=cmd.message.author)

    if user_data.life_state == ewcfg.life_state_corpse:
        response = "You're dead, bitch."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    elif user_data.life_state != ewcfg.life_state_enlisted:
        response = "What exactly are you renouncing? Your lackadaisical, idyllic life free of vice and violence? You aren't actually currently enlisted in any gang, dumbass."

    elif user_data.poi not in [ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_copkilltown, ewcfg.poi_id_thebreakroom]:
        response = "To turn in your badge, you must return to your soon-to-be former gang base."

    else:
        renounce_fee = int(user_data.slimes) / 2
        user_data.change_slimes(n=-renounce_fee)
        faction = user_data.faction
        user_data.life_state = ewcfg.life_state_juvenile
        user_data.weapon = -1
        user_data.sidearm = -1
        user_data.persist()
        response = "You are no longer enlisted in the {}, but you are not free of association with them. Your former teammates immediately begin to beat the shit out of you, knocking {} slime out of you before you're able to get away.".format(faction, renounce_fee)
        await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" mine for slime (or endless rocks) """


async def mine(cmd):
    market_data = EwMarket(id_server=cmd.message.author.guild.id)
    user_data = EwUser(member=cmd.message.author)

    mutations = user_data.get_mutations()

    responses = []
    resp_ctn = EwResponseContainer(client=cmd.client, id_server=cmd.guild.id)
    response = ""

    # Kingpins can't mine.
    if user_data.life_state == ewcfg.life_state_kingpin or user_data.life_state == ewcfg.life_state_grandfoe:
        return

    # ghosts cant mine (anymore)
    if user_data.life_state == ewcfg.life_state_corpse:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You can't mine while you're dead. Try {}.".format(ewcfg.cmd_revive)))

    # Enlisted players only mine at certain times.
    if user_data.life_state == ewcfg.life_state_enlisted:
        if user_data.faction == ewcfg.faction_rowdys and (market_data.clock < 8 or market_data.clock > 17):
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Rowdies only mine in the daytime. Wait for full daylight at 8am.".format(ewcfg.cmd_revive)))

        if user_data.faction == ewcfg.faction_killers and (market_data.clock < 20 and market_data.clock > 5):
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Killers only mine under cover of darkness. Wait for nightfall at 8pm.".format(ewcfg.cmd_revive)))

    # Mine only in the mines, and only in the mining channel.
    if cmd.message.channel.name in ewcfg.mining_channels and user_data.poi in juviecmdutils.mines_map:

        # Hunger check
        if user_data.hunger >= user_data.get_hunger_max():
            return await mismine(cmd, user_data, "exhaustion")

        else:
            grid_cont = None
            grid_type = ""
            toolused = "nothing"
            goonscape = False
            
            world_events = bknd_worldevent.get_world_events(id_server=cmd.guild.id)
            mining_type = ewcfg.mines_mining_type_map.get(user_data.poi)

            # If the user has a weapon equipped, check to see if it's a mining tool.
            if user_data.weapon >= 0:
                weapon_item = EwItem(id_item=user_data.weapon)
                weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))
                if (weapon.id_weapon == ewcfg.weapon_id_pickaxe or weapon.id_weapon == ewcfg.weapon_id_diamondpickaxe):
                    toolused = ewcfg.weapon_id_pickaxe
                elif weapon.id_weapon == ewcfg.weapon_id_sledgehammer:
                    toolused = ewcfg.weapon_id_sledgehammer
                elif weapon.id_weapon == ewcfg.weapon_id_shovel:
                    toolused = ewcfg.weapon_id_shovel

            if mining_type != "":
                # Check if the mine has a grid container. If not, initialize one.
                if user_data.id_server not in juviecmdutils.mines_map.get(user_data.poi): # The POI key will return another dict. The dict will be empty, unless there's an active grid, in which case the id_server will act as a key.
                    init_grid(user_data.poi, user_data.id_server)

                # Get the mine's grid container
                grid_cont = juviecmdutils.mines_map.get(user_data.poi).get(user_data.id_server)

                # Double check that the grid is the right kind!
                grid_type = ewcfg.grid_type_by_mining_type.get(mining_type)
                if grid_type != grid_cont.grid_type:
                    init_grid(user_data.poi, user_data.id_server)
                    grid_cont = juviecmdutils.mines_map.get(user_data.poi).get(user_data.id_server)

            # Create mine_action container
            mine_action = juviecmdutils.EwMineAction(user_data=user_data,
                                                     valid=False,
                                                     hunger_cost_multiplier=1,
                                                     toolused=toolused,
                                                     response=response,
                                                     unearthed_item_chance=1/ewcfg.unearthed_item_rarity,  # 1/1500
                                                     value_mod=1,  # Var for determining other random calcs
            )
            
            # Check for a mine collapse
            juviecmdutils.check_for_minecollapse(cmd, world_events, mine_action)
            
            # Do the calcs for !mine, return the updated mine_action container
            if mine_action.collapse == False and mine_action.valid == False:
                mine_action = get_mining_yield_by_grid_type(cmd, mine_action, grid_cont)
            
            # If !mine would result in nothing, send its response
            if mine_action.valid == False:
                response = mine_action.response
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            # If !mine doesn't result in a collapse, run worldevent checks and bonus checks
            if mine_action.collapse == False and mine_action.slime_yield != 0:
                
                # Check to create a mining event
                create_mining_event(cmd, mine_action, mutations, grid_type)

                # Check for currently-running world events
                juviecmdutils.check_for_mining_world_events(world_events, mine_action)

                # ZZZZT ZZZZT shovel check ZZZZT ZZZZT
                if toolused == ewcfg.weapon_id_shovel and mine_action.user_data.life_state != ewcfg.life_state_juvenile and cmd.tokens[0] == '!dig':
                    poi = poi_static.id_to_poi.get(mine_action.user_data.poi)
                    juviecmdutils.dig_hole(cmd, mine_action, poi)

                # Check to unearth an item
                juviecmdutils.unearth_item(cmd, mine_action, mutations)

            # If there WAS an uncleared collapse, do the flavor text and calcs for that
            if mine_action.collapse == True:
                mine_action = juviecmdutils.mine_collapse(mine_action, mutations, id_user=None)
                
                # Change user slime
                if mine_action.user_data.slimes > 0:
                    mine_action.user_data.change_slimes(n=-(mine_action.user_data.slimes * mine_action.collapse_penalty))


            # Do final slime calcs & give slime
            elif mine_action.slime_yield > 0:
                # Capped district check
                controlling_faction = poi_utils.get_subzone_controlling_faction(mine_action.user_data.poi, mine_action.user_data.id_server)
                if controlling_faction != "" and controlling_faction == mine_action.user_data.faction:
                    mine_action.slime_yield *= 2
                # Tool & Juvie lifestate check
                if mine_action.toolused in [ewcfg.weapon_id_pickaxe] or (ewcfg.slimernalia_active and mine_action.toolused in [ewcfg.weapon_id_sledgehammer]):
                    mine_action.slime_yield *= 2
                elif mine_action.user_data.life_state == ewcfg.life_state_juvenile:
                    mine_action.slime_yield *= 2
                mine_action.slime_yield = int(float(mine_action.slime_yield) * float(ewcfg.minegain_multiplier_dt[user_data.id_server]) * float(ewcfg.global_slimegain_multiplier_dt[user_data.id_server]))

                # Add the multiplier-free bonus yield, make sure it's not negative!!!!
                mine_action.slime_yield += mine_action.bonus_slime_yield
                mine_action.slime_yield = max(0, round(mine_action.slime_yield))
                
                # Increase slime
                mine_action.response += mine_action.user_data.change_slimes(n=mine_action.slime_yield, source=ewcfg.source_mining)
                if ewutils.DEBUG_OPTIONS['slimegainchecker'] == True:
                    f = open("minefile.txt", "a")
                    f.write("{},{},{}\n".format(int(time.time()), cmd.message.author.id, mine_action.slime_yield))

                goonscape = True

            # Take hunger from user
            hunger_cost_mod = ewutils.hunger_cost_mod(mine_action.user_data.slimelevel)
            hunger_cost = int(hunger_cost_mod) * mine_action.hunger_cost_multiplier
            mine_action.user_data.hunger += int(hunger_cost)
            
            # Liiiitle bit extra
            extra_hunger = hunger_cost - int(hunger_cost)  # extra is the fractional part of hunger_cost if it's not an integer
            if extra_hunger > 0: 
                # there's an x% chance that an extra stamina is deducted, where x is the fractional part of hunger_cost_mod in percent (times 100)
                if random.randint(1, 100) <= extra_hunger * 100:
                    mine_action.user_data.hunger += ewcfg.hunger_permine
            
            # Persist user_data :pleading:
            user_data.persist()

            # Handle Goonscape stats
            if goonscape:
                xp_yield = max(1, round(mine_action.slime_yield * 0.0077))
                
                responses = await add_xp(cmd.message.author.id, cmd.message.guild.id, ewcfg.goonscape_mine_stat, xp_yield)

            response = mine_action.response
            # Handle response container
            if len(response) > 1 or len(responses) > 0:
                resp_ctn.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                for resp in responses: resp_ctn.add_channel_response(cmd.message.channel, resp)
                await resp_ctn.post()
            
            # Add grid print or make a new grid, at the very end <3 
            if mine_action.grid_effect == 1:
                await print_grid(cmd, mine_action.user_data.poi, grid_cont)
            elif mine_action.grid_effect == 2:
                init_grid(mine_action.user_data.poi, mine_action.user_data.id_server)

                grid_cont = juviecmdutils.mines_map.get(mine_action.user_data.poi).get(mine_action.user_data.id_server)

                await print_grid(cmd, mine_action.user_data.poi, grid_cont)

            return

    else:
        return await mismine(cmd, user_data, "channel")



"""Talk with someone. Oh god, somebody answer."""

async def talk(cmd):
    user_data = EwUser(member = cmd.message.author)
    if cmd.mentions_count > 0:
        target_data = EwUser(member = cmd.mentions[0])
        if target_data.poi == user_data.poi:
            if target_data.id_user != user_data.id_user:
                response = random.choice(ewcfg.pvp_dialogue).format(cmd.mentions[0].display_name)
            else:
                response = "This is quite sad, you know that right?"
        else:
            response = "You strike up a conversation with- oh. They're not here. You miss {}...".format(cmd.mentions[0].display_name)

        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    elif user_data.poi in ewcfg.vendor_dialogue.keys() and cmd.tokens_count == 1:
        response = random.choice(ewcfg.vendor_dialogue.get(user_data.poi))
        thumbnail = ewcfg.vendor_thumbnails.get(user_data.poi)[1]
        rawname = ewcfg.vendor_thumbnails.get(user_data.poi)[0]
        name = "{}{}{}".format("*__", rawname, "__*")
        return await fe_utils.talk_bubble(response = response, name = name, image = thumbnail, channel = cmd.message.channel)

    elif cmd.tokens_count > 1:
        huntedenemy = " ".join(cmd.tokens[1:]).lower()
        checked_npc = cmbt_utils.find_enemy(enemy_search = huntedenemy, user_data=user_data)

        if checked_npc is None:
            response = "You can't seem to find them here. They're just a figment of your imagination."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        elif checked_npc.enemytype != ewcfg.enemy_type_npc:
            response = "What is this, Endless Kiss and Make Up? Stop talking to battle fodder and stab that fucker!" #get some generic enemy dialogue at some point
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        elif ewutils.DEBUG_OPTIONS.get('alternate_talk'):
            npc_obj = static_npc.active_npcs_map.get(checked_npc.enemyclass)
            await npc_obj.func_ai(keyword='move', enemy=checked_npc, channel=cmd.message.channel)
        else:
            npc_obj = static_npc.active_npcs_map.get(checked_npc.enemyclass)
            await npc_obj.func_ai(keyword='talk', enemy = checked_npc, channel = cmd.message.channel, user_data=user_data)

    else: #No tokens, no mentions, just the bare command
        response = "There's nobody living here who would talk to you."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

""" mine for slime (or endless rocks) """


async def flag(cmd):
    market_data = EwMarket(id_server=cmd.message.author.guild.id)
    user_data = EwUser(member=cmd.message.author)
    mutations = user_data.get_mutations()

    response = ""
    # Kingpins can't mine.
    if user_data.life_state == ewcfg.life_state_kingpin or user_data.life_state == ewcfg.life_state_grandfoe:
        return  

    # ghosts cant mine (anymore)
    if user_data.life_state == ewcfg.life_state_corpse:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You can't mine while you're dead. Try {}.".format(ewcfg.cmd_revive)))

    # Enlisted players only mine at certain times.
    if user_data.life_state == ewcfg.life_state_enlisted:
        if user_data.faction == ewcfg.faction_rowdys and (market_data.clock < 8 or market_data.clock > 17) and ewcfg.mutation_id_lightminer not in mutations:
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Rowdies only mine in the daytime. Wait for full daylight at 8am.".format(ewcfg.cmd_revive)))

        if user_data.faction == ewcfg.faction_killers and (market_data.clock < 20 and market_data.clock > 5) and ewcfg.mutation_id_lightminer not in mutations:
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Killers only mine under cover of darkness. Wait for nightfall at 8pm.".format(ewcfg.cmd_revive)))

    # Mine only in the mines.
    if cmd.message.channel.name in ewcfg.mining_channels:

        if user_data.hunger >= user_data.get_hunger_max():
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You've exhausted yourself from mining. You'll need some refreshment before getting back to work."))

        else:
            # hunger_cost_mod = ewutils.hunger_cost_mod(user_data.slimelevel)
            # extra = hunger_cost_mod - int(hunger_cost_mod)  # extra is the fractional part of hunger_cost_mod

            mining_type = ewcfg.mines_mining_type_map.get(user_data.poi)

            if mining_type != ewcfg.mining_type_minesweeper:
                response = "What do you think you can flag here?"
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            if user_data.poi not in juviecmdutils.mines_map:
                response = "You can't mine here! Go to the mines in Juvie's Row, Toxington, or Cratersville!"
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
            elif user_data.id_server not in juviecmdutils.mines_map.get(user_data.poi):
                init_grid(user_data.poi, user_data.id_server)

            grid_cont = juviecmdutils.mines_map.get(user_data.poi).get(user_data.id_server)
            grid = grid_cont.grid

            grid_type = ewcfg.grid_type_by_mining_type.get(mining_type)
            if grid_type != grid_cont.grid_type:
                init_grid(user_data.poi, user_data.id_server)
                grid_cont = juviecmdutils.mines_map.get(user_data.poi).get(user_data.id_server)
                grid = grid_cont.grid

            row = -1
            col = -1
            if cmd.tokens_count < 2:
                response = "Please specify which Minesweeper vein to flag."
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            for token in cmd.tokens[1:]:

                coords = token.lower()
                if col < 1:

                    for char in coords:
                        if char in ewcfg.alphabet:
                            col = ewcfg.alphabet.index(char)
                            coords = coords.replace(char, "")
                if row < 1:
                    try:
                        row = int(coords)
                    except:
                        row = -1

            row -= 1

            if row not in range(len(grid)) or col not in range(len(grid[row])):
                response = "Invalid Minesweeper vein."


            elif grid[row][col] == ewcfg.cell_empty_marked:
                grid[row][col] = ewcfg.cell_empty

            elif grid[row][col] == ewcfg.cell_mine_marked:
                grid[row][col] = ewcfg.cell_mine

            elif grid[row][col] == ewcfg.cell_empty_open:
                response = "This vein has already been mined dry."

            elif grid[row][col] == ewcfg.cell_mine:
                grid[row][col] = ewcfg.cell_mine_marked

            elif grid[row][col] == ewcfg.cell_empty:
                grid[row][col] = ewcfg.cell_empty_marked

            await print_grid(cmd, user_data.poi, grid_cont)


    else:
        response = "You can't mine here! Go to the mines in Juvie's Row, Toxington, or Cratersville!"

    if len(response) > 0:
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" scavenge for slime """


async def scavenge(cmd):
    market_data = EwMarket(id_server=cmd.message.author.guild.id)
    user_data = EwUser(member=cmd.message.author)
    mutations = user_data.get_mutations()

    time_now = int(time.time())
    response = ""

    time_since_last_scavenge = time_now - user_data.time_lastscavenge

    # Kingpins can't scavenge.
    if user_data.life_state == ewcfg.life_state_kingpin or user_data.life_state == ewcfg.life_state_grandfoe:
        return

    # ghosts cant scavenge
    if user_data.life_state == ewcfg.life_state_corpse:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "What would you want to do that for? You're a ghost, you have no need for such lowly materialistic possessions like slime. You only engage in intellectual pursuits now. {} if you want to give into your base human desire to see numbers go up.".format(ewcfg.cmd_revive)))
    # currently not active - no cooldown
    if time_since_last_scavenge < ewcfg.cd_scavenge:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Slow down, you filthy hyena."))

    if user_data.poi == ewcfg.poi_id_slimesea:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You consider diving down to the bottom of the sea to grab some sick loot, but quickly change your mind when you {}.".format(random.choice(ewcfg.sea_scavenge_responses))))

    # Scavenge only in location channels
    if ewutils.channel_name_is_poi(cmd.message.channel.name) == True:
        if user_data.hunger >= user_data.get_hunger_max():
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You are too exhausted to scrounge up scraps of slime off the street! Go get some grub!"))
        else:

            if juviecmdutils.scavenge_combos.get(user_data.id_user) == None:
                juviecmdutils.scavenge_combos[user_data.id_user] = 0

            combo = juviecmdutils.scavenge_combos.get(user_data.id_user)

            district_data = EwDistrict(district=user_data.poi, id_server=cmd.message.author.guild.id)

            if user_data.poi != juviecmdutils.scavenge_locations.get(user_data.id_user):
                juviecmdutils.scavenge_combos[user_data.id_user] = 0
                combo = 0

            user_initial_level = user_data.slimelevel
            # add scavenged slime to user
            if ewcfg.mutation_id_trashmouth in mutations:
                combo += 5

            juviecmdutils.scavenge_locations[user_data.id_user] = user_data.poi

            time_since_last_scavenge = min(max(1, time_since_last_scavenge), ewcfg.soft_cd_scavenge)

            # scavenge_mod = 0.003 * (time_since_last_scavenge ** 0.9)
            scavenge_mod = 0.005 * combo

            if (ewcfg.mutation_id_whitenationalist in mutations or ewcfg.mutation_id_airlock in mutations) and market_data.weather == "snow":
                scavenge_mod *= 1.5

            if ewcfg.mutation_id_airlock in mutations and market_data.weather == "snow":
                scavenge_mod *= 1.5

            if ewcfg.mutation_id_webbedfeet in mutations:
                district_slimelevel = len(str(district_data.slimes))
                scavenge_mod *= max(1, min(district_slimelevel - 3, 4))

            scavenge_yield = math.floor(scavenge_mod * district_data.slimes)

            if district_data.slimes < scavenge_yield:
                scavenge_yield = district_data.slimes

            levelup_response = user_data.change_slimes(n=scavenge_yield, source=ewcfg.source_scavenging)
            district_data.change_slimes(n=-1 * scavenge_yield, source=ewcfg.source_scavenging)
            if district_data.slimes < 0:
                district_data.slimes = 0
            district_data.persist()

            if levelup_response != "":
                response += levelup_response + "\n\n"
            # response += "You scrape together {} slime from the streets.\n\n".format(scavenge_yield)
            if cmd.tokens_count > 1:

                item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
                has_comboed = False

                if juviecmdutils.scavenge_combos.get(user_data.id_user) > 0 and (time_now - user_data.time_lastscavenge) < 60:
                    if juviecmdutils.scavenge_captchas.get(user_data.id_user).lower() == item_search.lower():
                        juviecmdutils.scavenge_combos[user_data.id_user] += 1
                        new_captcha = gen_scavenge_captcha(n=juviecmdutils.scavenge_combos.get(user_data.id_user), user_data=user_data)
                        response += "New captcha: **" + ewutils.text_to_regional_indicator(new_captcha) + "**"
                        if ewcfg.mutation_id_webbedfeet in mutations:
                            response += "\nYour flippers pick up {:,} slime.".format(scavenge_yield)
                        juviecmdutils.scavenge_captchas[user_data.id_user] = new_captcha
                        has_comboed = True

                        if ewcfg.mutation_id_dumpsterdiver in mutations:
                            has_comboed = False
                            item_search = item_search[random.randrange(len(item_search))]

                    else:
                        juviecmdutils.scavenge_combos[user_data.id_user] = 0

                if not has_comboed:
                    loot_resp = itm_utils.item_lootspecific(
                        user_data=user_data,
                        item_search=item_search
                    )

                    if loot_resp != "":
                        response = loot_resp + "\n\n" + response

            else:
                loot_multiplier = 1.0 + bknd_item.get_inventory_size(owner=user_data.poi, id_server=user_data.id_server)
                loot_chance = loot_multiplier / ewcfg.scavenge_item_rarity
                if ewcfg.mutation_id_dumpsterdiver in mutations:
                    loot_chance *= 10
                if random.random() < loot_chance:
                    loot_resp = itm_utils.item_lootrandom(
                        user_data
                    )

                    if loot_resp != "":
                        response += loot_resp + "\n\n"

                juviecmdutils.scavenge_combos[user_data.id_user] = 1
                new_captcha = gen_scavenge_captcha(n=1, user_data=user_data)
                response += "New captcha: **" + ewutils.text_to_regional_indicator(new_captcha) + "**"
                if ewcfg.mutation_id_webbedfeet in mutations:
                    response += "\nYour flippers pick up {:,} slime.".format(scavenge_yield)
                juviecmdutils.scavenge_captchas[user_data.id_user] = new_captcha

            # Fatigue the scavenger.
            hunger_cost_mod = ewutils.hunger_cost_mod(user_data.slimelevel)
            extra = hunger_cost_mod - int(hunger_cost_mod)  # extra is the fractional part of hunger_cost_mod

            user_data.hunger += ewcfg.hunger_perscavenge * int(hunger_cost_mod)
            if extra > 0:  # if hunger_cost_mod is not an integer
                # there's an x% chance that an extra stamina is deducted, where x is the fractional part of hunger_cost_mod in percent (times 100)
                if random.randint(1, 100) <= extra * 100:
                    user_data.hunger += ewcfg.hunger_perscavenge

            user_data.time_lastscavenge = time_now

            user_data.persist()

            if not response == "":
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    else:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You'll find no slime here, this place has been picked clean. Head into the city to try and scavenge some slime."))


""" LOL """




""" Gender :3 """

async def identify(cmd):
    user_data = EwUser(member=cmd.message.author)
    gender = cmd.message.content[(len(ewcfg.cmd_identify)):].strip()

    if gender == "":
        response = "Cool. Noted. Enjoy your lack of gender, slime."
        user_data.gender = ""
        user_data.persist()
    elif gender in ewcfg.curse_words:
        response = "Hey, no matter what, you're still a juvenile. **NO SWEARS**."
    elif "\n" in gender:
        response = "No fucking line breaks! WTF!"    
    elif len(gender) > 16:
        response = "Fucking god, your gender **CANNOT** be longer than that. Sorry, them's the rules."
    elif gender == "boy":
        response = "Radical! Enjoy your gender, slimeboi."
        user_data.gender = "boi"
        user_data.persist()
    elif gender == "girl":
        response = "Radical! Enjoy your gender, slimegorl."
        user_data.gender = "gorl"
        user_data.persist()
    elif gender == "ancient obelisk":
        response = "You can't have that gender. It's mine."
    else:
        response = "Radical! Enjoy your gender, slime{}.".format(gender)
        user_data.gender = gender
        user_data.persist()

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def scrub(cmd):
    user_data = EwUser(member=cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)
    district = EwDistrict(id_server=cmd.guild.id, district=poi.id_poi)

    if user_data.life_state != ewcfg.life_state_juvenile:
        response = "You wouldn't stoop that low. Only Juvies would be that needlessly obedient."
    elif not poi.is_capturable:
        response = "No need to scrub, scrub. The gangs don't really mark up this place."
    elif district.capture_points == 0:
        response = "{} is clean. Good job, assuming you actually did anything.".format(poi.str_name)
    elif district.all_neighbors_friendly():
        response = "You're too deep into enemy territory. Scrub here and you might wet yourself."
    else:
        if random.randint(0, 2) == 0:
            district.change_capture_points(progress=-1, actor=ewcfg.actor_decay)
            district.persist()
        user_data.change_crime(n = -1)
        user_data.persist()
        response = "-"

    if response != "-":
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def hole_depth(cmd):
    user_data = EwUser(member = cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)

    if poi.mother_districts[0] not in['cratersville', 'juviesrow', 'toxington']:
        response = "Well, I never!"
    else:
        mother_poi = poi_static.id_to_poi.get(poi.mother_districts[0])
        gamestate = EwGamestate(id_server=cmd.guild.id, id_state= '{}hole'.format(poi.mother_districts[0]))
        current_depth = float(gamestate.value)/3000

        response = "The hole in {} is {:.2f} feet deep.".format(mother_poi.str_name, current_depth)
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def hall_question(cmd):
    user_data = EwUser(member = cmd.message.author)
    gamestate = EwGamestate(id_state='hall_counter', id_server=cmd.guild.id)
    if user_data.poi != 'doorsofthesludgenant':
        response = "I'm not answering your questions. Stop being a little bitch and ask bullets instead."
    else:
        hallNum = int(gamestate.value)
        if question_map.get(hallNum)[0] == '?':
            response = "The stone head isn't responding to anything. Maybe it's out of ancient voodo batteries or something."
        else:
            response = "{} {}".format("The stone head starts talking:",question_map.get(hallNum)[0])

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def hall_answer(cmd):
    user_data = EwUser(member=cmd.message.author)
    gamestate = EwGamestate(id_state='hall_counter', id_server=cmd.guild.id)

    input = ewutils.flattenTokenListToString(cmd.tokens[1:])

    if user_data.poi != 'doorsofthesludgenant':
        response = "I didn't ask you anything, knuckledragger. Don't speak unless spoken to."
    elif user_data.life_state == ewcfg.life_state_corpse:
        response = "The stone head pays no attention. It get channeled by way too many dead things to single you out."
    else:

        hallNum = int(gamestate.value)
        if question_map.get(hallNum)[0] == '?':
            response = "The stone head isn't responding to anything. Maybe it needs to charge its ancient voodo batteries or something."
        elif input == "" or input is None:
            response = "Answer what? You need to !answer <youranswer>."
        elif input.upper() in question_map.get(hallNum)[1]:
            hallNum += 1
            response = "Nice, that's it! Another door opens."
            if question_map.get(hallNum)[0] == '?':
                reward = relic_map.get(question_map.get(hallNum)[1])
                reward_props = itm_utils.gen_item_props(reward)
                bknd_item.item_create(
                    item_type=ewcfg.it_relic,
                    id_server=user_data.id_server,
                    id_user='doorsofthesludgenant',
                    item_props=reward_props
                )
                response += "\n\n A {} is behind this door! Jackpot!".format(reward_props.get('relic_name'))
                if (hallNum + 1) in question_map.keys(): #advance to the next question if it exists
                    hallNum += 1
            if question_map.get(hallNum)[0] != '?':
                response += " Next question: {}".format(question_map.get(hallNum)[0])

            response = response.format(question_map.get(hallNum)[0])


            gamestate.value = "{}".format(hallNum)
            gamestate.persist()

        else: #deduct a slime penalty for answering wrong
            damage = random.randrange(10000, 250000)
            if user_data.slimes > damage:
                dealt_string = "loses {} slime!".format(damage)
                user_data.change_slimes(n=-damage)
                user_data.persist()
            else:
                dealt_string = "gets vaporized!"
                await user_data.die(cause=ewcfg.cause_praying)

            response = "**WRYYYYYYYYY!!!** The stone head reels back and fires a bone hurting beam! Ouch, right in the {hitzone}! {player} {dealt_string}".format(hitzone = random.choice(cmbt_utils.get_hitzone().aliases), player = cmd.message.author.display_name, dealt_string=dealt_string)

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

#2 rallies can't go on at once with this design, maybe revise if that idea materializes
async def claim(cmd):
    user_data = EwUser(member=cmd.message.author)
    world_events = bknd_worldevent.get_world_events(id_server=user_data.id_server, active_only=True)
    response = ""
    for id_event in world_events:
        if world_events.get(id_event) == ewcfg.event_type_rally:
            event = bknd_worldevent.EwWorldEvent(id_event=id_event)

            if event.time_activate + (60 * 30) >= int(time.time()):

                if event.event_props.get('poi') == user_data.poi and event.event_props.get(str(user_data.id_user)) is None:
                    event.event_props[str(user_data.id_user)] = '1'
                    response = "You checked into the rally as security. Be the last one standing to claim your prize..."
                    event.persist()
                elif event.event_props.get('poi') == user_data.poi:
                    response = "You already did that."
                else:
                    response = "Wrong place, dumpass."
                break

            else:
                district = EwDistrict(id_server=cmd.guild.id, district=event.event_props.get('poi'))
                if district is not None:
                    if district.name != user_data.poi:
                        response = "There's no rally here."
                    elif district.controlling_faction == 'rabble' or len(district.get_players_in_district()) + len(district.get_enemies_in_district()) > 1:
                        response = "You're not done, there are violent people and/or subhumans around here that are still alive."
                    elif event.event_props.get(str(user_data.id_user)) is None:
                        response = "You're just pretending like you're part of security. Get outta here."
                    elif event.event_props.get('relic') == 'claimed':
                        response = 'Too late, bud. Someone already took payment.'
                    else:

                        relic_id = event.event_props.get('relic')
                        map_entry = relic_map.get(relic_id)
                        event.event_props['relic'] = 'claimed'
                        event.persist()
                        await ewdebug.award_item(cmd, itemname=relic_id, on_give='')
                        response = "You outlasted them all. Yes, paydirt! You get the {}!".format(map_entry.str_name)
                else:
                    response = ""
                break
        else:
            response = "There's no rally here."

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

