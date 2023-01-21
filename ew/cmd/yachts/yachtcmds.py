import discord
from ew.utils.combat import EwUser

import ew.static.cfg as ewcfg
from ew.backend.yacht import EwYacht
from ew.utils import frontend as fe_utils
from ew.utils import yacht as yacht_utils
import ew.static.poi as poi_static
from ew.utils import core as ewutils
import ew.utils.rolemgr as ewrolemgr
import ew.utils.move as move_utils
import math
import random
import asyncio

try:
    from ew.cmd import debug as ewdebug
except:
    from ew.cmd import debug_dummy as ewdebug




async def rentyacht(cmd):
    user_data = EwUser(member=cmd.message.author)
    question = "You'll need {} SlimeCoin to set sail. Whaddya say, laddy? !accept or !refuse?".format(ewcfg.yachtprice)

    name = ' '.join(word for word in cmd.tokens[1:])

    if user_data.poi != ewcfg.poi_id_capnalexyachtshack:
        response = "Nobody in NLACakaNM can afford to sell out yachts except for the Alexanders. Head over to the Yacht Shack and we can try this again."
    elif cmd.tokens_count < 2:
        response = "Laddy, you need a name for this vessel! I'm not a playwright here, son, do it yerself!"
        return await fe_utils.talk_bubble(response=response, name="**__SMITTY ALEXANDER__**", channel=cmd.message.channel, image="https://rfck.app/img/npc/albertalex.png")

    elif user_data.slimecoin < ewcfg.yachtprice:
        response = "Ay, laddy. You'll need more coin than that to rob me of this ere girl."
        return await fe_utils.talk_bubble(response=response, name="**__SMITTY ALEXANDER__**", channel=cmd.message.channel, image = "https://rfck.app/img/npc/albertalex.png")
    else:
        accepted = await fe_utils.prompt(cmd=cmd, target = cmd.message.author, question = question, wait_time = 30, accept_command = 'accept', decline_command = 'refuse', checktarget = False)
        user_data = EwUser(member=cmd.message.author)

        if accepted and user_data.slimecoin > ewcfg.yachtprice:
            channel_slimesea = fe_utils.get_channel(server=cmd.guild, channel_name=ewcfg.channel_slimesea)

            user_data.change_slimecoin(n=-ewcfg.yachtprice, coinsource=ewcfg.coinsource_spending)
            user_data.persist()
            yacht = EwYacht()
            yacht.owner = cmd.message.author.id
            yacht.xcoord = 26
            yacht.ycoord = 5
            yacht.direction = 'stop'
            yacht.yacht_name = "S.S. " + name
            yacht.id_server = user_data.id_server
            response = "I christen ye: The S.S. {}!".format(name)
            boat_poi = poi_static.id_to_poi.get("yacht")
            new_poi = '{}{}'.format('yacht', yacht.thread_id)
            poi_static.id_to_poi[new_poi] = boat_poi

            starting_message = await fe_utils.send_message(cmd.client, channel_slimesea, "🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊")
            thread = await channel_slimesea.create_thread(name="S.S. {}".format(name), message=starting_message, type=discord.ChannelType.private, invitable=False)

            yacht.thread_id = thread.id
            yacht.persist()
            return await fe_utils.talk_bubble(response=response, name="**__SMITTY ALEXANDER__**", channel=cmd.message.channel, image="https://rfck.app/npc/albertalex.png")

        else:
            response = "Oh, pooer soul. Go whale around with the rest of the urchins, lad."
            return await fe_utils.talk_bubble(response=response, name="**__SMITTY ALEXANDER__**", channel=cmd.message.channel, image="https://rfck.app/npc/albertalex.png")

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))



async def board_ship(cmd):
    user_data = EwUser(member=cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)

    name = ' '.join(word for word in cmd.tokens[1:])

    if not poi.is_dock:
        response = "There are no ships here."

    elif cmd.tokens_count == 1:
        response = "Specify the ship you want to get on."

    else:
        current_ship = None
        if user_data.poi[:5] == 'yacht':
            current_ship = EwYacht(id_server=user_data.id_server, id_thread=int(user_data.poi[5:]))
            ships = yacht_utils.find_local_boats(name=name, current_coords=[current_ship.xcoord, current_ship.ycoord], id_server=cmd.guild.id)
        else:
            ships = yacht_utils.find_local_boats(poi=user_data.poi, name=name, id_server=cmd.guild.id)

        if ships == []:
            response = "There aren't any ships like that around here."
        else:
            selected_ship = None
            for ship in ships:
                if current_ship is not None and ship.thread_id == current_ship.thread_id:
                    pass
                else:
                    selected_ship = ship
            if selected_ship is not None:
                #todo set up gangplank restrictions
                if selected_ship.direction != 'stop':
                    response = "Fuck, they just took off."
                else:
                    response = "You begin boarding the {}.".format(selected_ship.yacht_name)
                    move_utils.move_counter += 1
                    move_current = ewutils.moves_active[cmd.message.author.id] = move_utils.move_counter
                    if move_current == ewutils.moves_active[cmd.message.author.id]:
                        user_data = EwUser(member=cmd.message.author)
                        user_data.poi = "yacht{}".format(selected_ship.thread_id)
                        user_data.persist()
                        await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
                        await user_data.move_inhabitants(id_poi=user_data.poi)


            else:
                response = "There's no ship like that to board."

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def man(cmd):
    user_data = EwUser(member=cmd.message.author)

    if user_data.poi[:5] != 'yacht':
        response = "You can't just command a man into your life. You have to woo him gently."
    elif cmd.tokens_count == 1:
        response = "You have to man a specific post. Try 'poopdeck', 'helm', 'cannon', or 'storehouse'."
    elif ewutils.flattenTokenListToString(cmd.tokens[1:]) not in['poopdeck', 'helm', 'cannon', 'storehouse']:
        response = "That's not a thing, cap'n. Try 'poopdeck', 'helm', 'cannon', or 'storehouse'."
    else:
        post = ewutils.flattenTokenListToString(cmd.tokens[1:])
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        yacht_utils.clear_station(id_server=cmd.guild.id, thread_id=yacht.thread_id, id_user=user_data.id_user)

        if post == 'poopdeck':
            yacht.poopdeck = user_data.id_user
        elif post == 'helm':
            yacht.helm = user_data.id_user
        elif post == 'cannon':
            yacht.cannon = user_data.id_user
        elif post == 'storehouse':
            yacht.storehouse = user_data.id_user
        yacht.persist()
        response = "You man the {}!".format(post)
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def avast(cmd):
    user_data = EwUser(member=cmd.message.author)

    if user_data.poi[:5] != 'yacht':
        response = "Yeah, man, I like that antivirus software, too."
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        if yacht.storehouse == user_data.id_user or yacht.cannon == user_data.id_user:
            response = "You can't see anything, you're not aboveboard!"
        else:
            response = yacht_utils.draw_map(xcoord=yacht.xcoord, ycoord=yacht.ycoord, id_server=cmd.guild.id, radius=6)
            response += "\n{} is currently "

            if yacht.direction == 'stop':
                response += "stopped."
            elif yacht.direction == 'sunk':
                response += "sunk."
            else:
                response += "headed {}.".format(yacht.direction)

            if ewdebug.seamap[yacht.ycoord][yacht.xcoord] == 0:
                response += " You've docked on an island and can get off now."


    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def setsail(cmd):
    user_data = EwUser(member=cmd.message.author)

    if user_data.poi[:5] != 'yacht':
        response = "You have to do that when you're on a yacht."
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        if yacht.helm != user_data.id_user:
            response = "You aren't at the helm!"
        elif cmd.tokens_count == 1:
            response = "Which direction?"
        elif cmd.tokens[1] not in ['north', 'east', 'south', 'west', 'up', 'down', 'left', 'right', 'stop']:
            response = "Not a direction, squickface!"
        else:
            yacht.speed = max(1, yacht.speed)
            if cmd.tokens[1] in ['north', 'up']:
                yacht.direction = 'north'
                response = "Set course due north!"
            elif cmd.tokens[1] in ['south', 'down']:
                yacht.direction = 'south'
                response = 'Anchors aweigh, south we go!'
            elif cmd.tokens[1] in ['east', 'right']:
                yacht.direction = 'east'
                response = "Time to go FUCKING EAST!"
            elif cmd.tokens[1] in ['west', 'left']:
                yacht.direction = 'west'
                response = "Moving west, unfurl the sails!"
            elif cmd.tokens[1] in ['stop']:
                yacht.direction = 'stop'
                yacht.speed = 0
                response = 'Drop anchor!'
            else:
                response = ""
            yacht.persist()
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def unboard(cmd):
    user_data = EwUser(member = cmd.message.author)

    if user_data.poi[:5] != 'yacht':
        response = "You gotta get boarded first."
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        if ewdebug.seamap[yacht.ycoord][yacht.xcoord] == -1:
            resp_cont = fe_utils.EwResponseContainer(client=cmd.client, id_server=user_data.id_server)

            user_data.poi = ewcfg.poi_id_slimesea
            user_data.trauma = ewcfg.trauma_id_environment
            die_resp = await user_data.die(cause=ewcfg.cause_drowning)
            resp_cont.add_response_container(die_resp)
            await resp_cont.post()
            response = "{} jumps over the railing of the yacht and promptly drowns in the slime sea.".format(cmd.message.author.display_name)
        elif ewdebug.seamap[yacht.ycoord][yacht.xcoord] == 3:
            response = "Holy shit dude, that's not even supposed to happen. You're like, Tony Hawking the map right now."
        else:
            exit_poi = ""
            for dock in poi_static.docks:
                dock_obj = poi_static.id_to_poi.get(dock)
                for coord in dock_obj.coord:
                    if coord[0] == yacht.xcoord and coord[1] == yacht.ycoord:
                        exit_poi = dock
                        break
                if exit_poi != "":
                    break
            if exit_poi == "":
                response = "The cliffs are too steep here. Looks like we can't head for land."
            else:
                response = "LAND HO!"
                move_utils.move_counter += 1
                move_current = ewutils.moves_active[cmd.message.author.id] = move_utils.move_counter
                if move_current == ewutils.moves_active[cmd.message.author.id]:
                    user_data = EwUser(member=cmd.message.author)
                    user_data.poi = exit_poi
                    user_data.persist()
                    await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
                    await user_data.move_inhabitants(id_poi=user_data.poi)

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def stock(cmd):
    user_data = EwUser(member=cmd.message.author)
    if user_data.poi[:5] != 'yacht':
        response = "You must be thinking of \"!stocks\"."
    elif cmd.tokens_count < 2:
        response = "Stock what? Either a cannonball or a harpoon."
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        stats = yacht.getYachtStats()

        if cmd.tokens[1] not in['harpoon', 'cannonball']:
            response = "Captain Albert's words echoed in your head. \"You can't just load anything into these cannons, laddy. Smitty makes them out of balsa wood!\"\n\nTry a cannonball or a harpoon."

        elif ('cannonball' in stats and cmd.tokens[1] == 'cannonball') or ('harpoon' in stats and cmd.tokens[1] == 'harpoon'):
            response = "They already have one. Don't go throwing shit around belowdeck, or the filth level's gonna go through the roof."
        elif user_data.id_user != yacht.storehouse:
            response = "You're nowhere near the storehouse, you can't find it!"
        else:
            yacht.applyStat(stat_type=cmd.tokens[1], quantity=0, target = 0)
            response = "{} tosses a {} cannon-ways!".format(cmd.message.author.display_name, cmd.tokens[1])

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def load(cmd):
    user_data = EwUser(member=cmd.message.author)
    if user_data.poi[:5] != 'yacht':
        response = "Hey wait, I thought we were trying to forget about the cum jar."
    elif cmd.tokens_count < 2:
        response = "Load what? Either a cannonball or a harpoon."
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        stats = yacht.getYachtStats()

        if cmd.tokens[1] not in ['harpoon', 'cannonball']:
            response = "Captain Albert's words echoed in your head. \"You can't just load anything into these cannons, laddy. Smitty makes them out of balsa wood!\"\n\nTry a cannonball or a harpoon."

        elif ('cannonball' not in stats and cmd.tokens[1] == 'cannonball') or (
                'harpoon' not in stats and cmd.tokens[1] == 'harpoon'):
            response = "You don't have one of those. Storehouse guy, chop chop!"
        elif user_data.id_user != yacht.cannon:
            response = "You're nowhere near the cannon, you can't do that!"
        else:
            stat_sought = None
            for stat in stats:
                if stat == cmd.tokens[1]:
                    stat_sought = stat
                    break
            if stat_sought is not None and stat_sought.quantity != 0:
                response = "You already loaded that in."
            else:
                stat_sought.quantity += 1
                stat_sought.persist()
                response = "{} drops a {} into place!".format(cmd.message.author.display_name, cmd.tokens[1])

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def aim_ship(cmd):
    user_data = EwUser(member=cmd.message.author)
    if user_data.poi[:5] != 'yacht':
        response = "Just aim normally. If you're gonna larp as a pirate, be one first."
    elif cmd.tokens_count < 2:
        response = "Who are you aiming at?"
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        stats = yacht.getYachtStats()

        if yacht.helm != user_data.id_user:
            response = "You can't steer the ship to aim if you're not at the helm!"
        else:

            if 'aim' not in stats:
                yacht.applyStat(stat_type='aim')

            stats = yacht.getYachtStats()
            stat_sought = None
            for stat in stats:
                if stat == 'aim':
                    stat_sought = stat
                    break

            name = ' '.join(word for word in cmd.tokens[1:])
            coords = yacht_utils.get_boat_coord_radius(xcoord=yacht.xcoord, ycoord=yacht.ycoord, radius=4)

            targets = yacht_utils.find_local_boats(current_coords=coords, id_server=user_data.id_server, name =name)
            target_ship = None
            for target in targets:
                if target.thread_id == yacht.thread_id:
                    continue
                else:
                    target_ship = target

            if target_ship is None:
                response = "There's nothing to aim at with that name out here. Nothing important, at least."

            else:
                stat_sought.target = target_ship.thread_id
                stat_sought.quantity = (target_ship.xcoord * 1000) + target_ship.ycoord #this creates a readable and distinct value for the coords locked into
                stat_sought.persist()
                response = "Aim for the {}, right between the eyes! Steady as she goes...".format(target_ship.yacht_name)

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def fire_cannon(cmd):
    user_data = EwUser(member=cmd.message.author)
    if user_data.poi[:5] != 'yacht':
        response = "What, like in a crowded theater? Sounds like fun."
    elif cmd.tokens_count < 2:
        response = "Fire what? You could do a cannon or a harpoon."
    elif cmd.tokens[1] not in ["cannon", "cannonball", "harpoon"]:
        response = "You can only fire the cannon or a harpoon."
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        stats = yacht.getYachtStats()
        firetype = cmd.tokens[1].replace("cannon", "cannonball")

        if yacht.cannon != user_data.id_user:
            response = "You need to be near the cannon to fire it."

        else:
            loaded = False
            aimed = False
            target_ship = None

            for stat in stats:
                if stat == 'aim':
                    target_ship = EwYacht(id_server=yacht.id_server, id_thread=stat.target)
                    if (target_ship.xcoord * 1000) + target_ship.ycoord == stat.quantity:
                        aimed = True
                elif stat == firetype:
                    if stat.quantity > 0:
                        loaded = True
                        yacht.clearStat(id_stat=stat.id_stat)

            if loaded is False:
                response = "It's not loaded."
            else:
                if aimed is False:
                    response = "BAM!..............splish!\nThe cannonball flies through the air, landing on sweet nothing! Aim faster next time, dumpass!"
                else:
                    distance = math.sqrt((target_ship.xcoord-yacht.xcoord)**2 + (target_ship.ycoord-yacht.ycoord)**2)
                    #i just used the fucking pythagorean theorem to kill a man with cannonballs. yeah i bet you're jealous

                    if firetype == 'cannonball':

                        hit_chance = (-0.018 * (distance**2)) - (0.048 * distance) + 1.015
                        #i plotted the general results i wanted into a curve of best fit calculator and these were my results, go figure
                        random_pct = random.randint(0, 100)
                        if random_pct > int(hit_chance * 100):
                            response = "BAM!...........whoosh! You barely miss The {}!".format(target_ship.yacht_name)
                        else:
                            holesize =  int(7-distance)
                            hole_dict = {
                                1:" puny",
                                2:" downright mediocre",
                                3:"...well, actually it's pretty average",
                                4:" looking leaky as fuck",
                                5:" pretty big",
                                6:" huge",
                                7:" titanic, laddy!"
                            }

                            response = "BAM!............KKKKRRRRRAAAACKKKK! Their hull has been breached! The hole is{}!".format(hole_dict.get(holesize))

                            target_ship.applyStat(stat_type='flood', quantity=holesize, target=yacht.thread_id)
                    else:
                        if distance != 0:
                            response = "Harpoons don't reach that far. You have to be in the same area as them."
                        else:
                            target_ship.applyStat(stat_type="harpooned", quantity=5, target=yacht.thread_id)
                            yacht.applyStat(stat_type="harpooned", quantity=5, target=yacht.thread_id)
                            response = "SHHHHINC! A harpoon sinks into the {}'s walls, locking your ship to theirs!".format(target_ship.yacht_name)
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))





async def statstest(cmd):
    pass