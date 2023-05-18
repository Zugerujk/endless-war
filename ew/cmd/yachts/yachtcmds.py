import discord
import time
from ew.utils.combat import EwUser
import ew.backend.item as bknd_item
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

    docked_yachts = yacht_utils.find_local_boats(poi=ewcfg.poi_id_slimesend_pier, id_server=user_data.id_server)

    ownone = None
    for yacht_ in docked_yachts:
        if yacht_.owner == cmd.message.author.id:
            ownone = yacht_.yacht_name

    if user_data.poi != ewcfg.poi_id_capnalexyachtshack:
        response = "Nobody in NLACakaNM can afford to sell out yachts except for the Alexanders. Head over to the Yacht Shack and we can try this again."
    elif cmd.tokens_count < 2:
        response = "Laddy, you need a name for this vessel! I'm not a playwright here, son, do it yerself!"
        return await fe_utils.talk_bubble(response=response, name="**__SMITTY ALEXANDER__**", channel=cmd.message.channel, image="https://rfck.app/img/npc/albertalex.png")
    elif ownone is not None:
        response = "Ay, you already own a yacht, laddy! You have the {}, what do ya need another one fer?".format(ownone)
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
            yacht.xcoord = 27
            yacht.ycoord = 12
            yacht.direction = 'stop'
            yacht.yacht_name = "S.S. " + name
            yacht.id_server = user_data.id_server
            response = "I christen ye: The S.S. {}!".format(name)
            boat_poi = poi_static.id_to_poi.get("yacht")
            new_poi = '{}{}'.format('yacht', yacht.thread_id)
            poi_static.id_to_poi[new_poi] = boat_poi

            #starting_message = await fe_utils.send_message(cmd.client, channel_slimesea, "🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊")
            thread = await channel_slimesea.create_thread(name="S.S. {}".format(name), type=discord.ChannelType.private, invitable=False)

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

        if ships is None or len(ships) == 0:
            response = "There aren't any ships like that around here."
        else:
            selected_ship = None
            for ship in ships:
                if current_ship is not None and ship.thread_id == current_ship.thread_id:
                    pass
                else:
                    selected_ship = ship
            if selected_ship is not None:
                if ewdebug.seamap[selected_ship.ycoord][selected_ship.xcoord] != -1:
                    onland =  True
                else:
                    onland = False

                if user_data.poi[:5] == 'yacht' and selected_ship.thread_id == int(user_data.poi[5:]):
                    response = "You're already here, dumbass."
                else:
                    approved = False
                    if current_ship is None:
                        if selected_ship.owner == user_data.id_user or 'locked' not in selected_ship.getYachtStats():
                            approved = True
                        else:
                            response = "The entrance is locked up, it's no good."
                    else:
                        shipstats = current_ship.getYachtStats()
                        planked = False
                        for stat in shipstats:
                            if stat == 'gangplanked':
                                if stat.target == selected_ship.thread_id:
                                    planked = True

                        if not planked:
                            response = "You need to !gangplank then first, so you can cross."
                        elif onland and 'locked' in selected_ship.getYachtStats():
                            response = "The entrance is locked up, it's no good. Crossing via gangplank doesn't work either because you're not docked that closely."
                        else:
                            approved = True

                    if approved:
                        response = "You begin boarding the {}.".format(selected_ship.yacht_name)
                        move_utils.move_counter += 1
                        move_current = ewutils.moves_active[cmd.message.author.id] = move_utils.move_counter
                        if move_current == ewutils.moves_active[cmd.message.author.id]:
                            user_data = EwUser(member=cmd.message.author)
                            user_data.poi = "yacht{}".format(selected_ship.thread_id)
                            user_data.persist()
                            thread = await selected_ship.get_thread()
                            try:
                                if current_ship is not None:
                                    currentthread = await current_ship.get_thread()
                                    await currentthread.remove_user(cmd.message.author)
                            except:
                                ewutils.logMsg("Failed to remove thread.")

                            try:
                                await thread.add_user(user=cmd.message.author)
                            except:
                                ewutils.logMsg("Failed to add thread.")

                            try:
                                await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
                                await user_data.move_inhabitants(id_poi=user_data.poi)
                            except:
                                ewutils.logMsg("Failed to update roles.")


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
        yacht = yacht_utils.clear_station(id_server=cmd.guild.id, thread_id=yacht.thread_id, id_user=user_data.id_user)


        if yacht.filth_check() and ewutils.flattenTokenListToString(cmd.tokens[1:]) != 'poopdeck':
            response = "You slip on the poop deck and can't man anything! Which idiot forgot to swab?"
        else:
            if post == 'poopdeck':
                yacht.poopdeck = user_data.id_user
            elif post == 'helm':
                yacht.helm = user_data.id_user
            elif post == 'cannon':
                yacht.cannon = user_data.id_user
            elif post == 'storehouse':
                yacht.storehouse = user_data.id_user
            yacht.accumulate_filth()
            response = "You man the {}!".format(post)
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def avast(cmd):
    user_data = EwUser(member=cmd.message.author)
    extra_response = None
    printmap = True
    if user_data.poi[:5] != 'yacht':
        response = "Yeah, man, I like that antivirus software, too."
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        if yacht.storehouse == user_data.id_user or yacht.cannon == user_data.id_user:
            printmap = False

        if printmap:
            response = yacht_utils.draw_map(xcoord=yacht.xcoord, ycoord=yacht.ycoord, id_server=cmd.guild.id, radius=4)
        else:
            response = ""
        extra_response = "\n{} is currently ".format(yacht.yacht_name)

        if yacht.direction == 'stop':
            extra_response += "stopped."
        elif yacht.direction == 'sunk':
            extra_response += "sunk."
        else:
            extra_response += "headed {}.".format(yacht.direction)

        coords = yacht_utils.get_boat_coord_radius(xcoord=yacht.xcoord, ycoord=yacht.ycoord, radius=4)
        ships = yacht_utils.find_local_boats(current_coords=coords, id_server=cmd.guild.id)
        if len(ships) > 1:
            extra_response += "There are ships nearby: "
            shipnames = []
            for ship in ships:

                if int(ship.thread_id) != int(yacht.thread_id):
                    shipnames.append("the **{}**".format(ship.yacht_name))
            extra_response += "{}.".format(ewutils.formatNiceList(names=shipnames))

        stats = yacht.getYachtStats()
        flood_count = 0
        for stat in stats:
            if stat in ['gangplanked', 'harpooned']:
                attached_yacht = EwYacht(id_server=yacht.id_server, id_thread=stat.target)
                if attached_yacht.thread_id != yacht.thread_id:
                    extra_response += " You are {} to the {}.".format(stat.type_stat, attached_yacht.yacht_name)
            if stat == 'embalmed':
                extra_response += " You have embalmed your ship to prevent it from burning up."
            if stat == 'flood':
                flood_count += stat.quantity
            if stat == 'netcast':
                extra_response += " You lowered the treasure net."


        if flood_count > 50:
            extra_response += " There are so many holes in the ship it's lunacy it can even stay together."
        elif flood_count > 25:
            extra_response += " You're taking on way too much water. Basically, you're sunk already."
        elif flood_count > 15:
            extra_response += " The yacht's taking on water."
        elif flood_count > 10:
            extra_response += " There is a large hole in the boat."
        elif flood_count > 5:
            extra_response += " The boat's taking on a bit of water."

        if yacht.flood > 0:
            extra_response += " The ship is {}% flooded.".format(yacht.flood)
        if yacht.filth > 0:
            extra_response += " The ship's filth level is {}%.".format(yacht.filth)

        if ewdebug.seamap[yacht.ycoord][yacht.xcoord] == 0:
            extra_response += " You've docked on an island and can get off now."

    if response != "":
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    if extra_response is not None:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, extra_response))


async def setsail(cmd):
    user_data = EwUser(member=cmd.message.author)


    if user_data.poi[:5] != 'yacht':
        response = "You have to do that when you're on a yacht."
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        stats = yacht.getYachtStats()

        if "harpooned" in stats:
            response = "You're tied to another ship right now, no can do."
        elif yacht.helm != user_data.id_user:
            response = "You aren't at the helm!"
        elif yacht.filth_check():
            response = "The crew bumble around trying to shift course, but the poopdeck is too filthy! The fucking swabbies are slacking!"
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
            for stat in stats:
                if stat.type_stat == 'gangplanked':
                    yacht.clearStat(id_stat=stat.id_stat)

            yacht.accumulate_filth()
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

                    try:
                        if yacht is not None:
                            currentthread = await yacht.get_thread()
                            await currentthread.remove_user(cmd.message.author)
                    except:
                        ewutils.logMsg("Failed to remove thread.")

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
            response = "Captain Albert's words echoed in your head. \"You can't just load anything into these cannons, laddy. Smitty makes the fuckers out of balsa wood!\"\n\nTry a cannonball or a harpoon."
        elif yacht.filth_check():
            response = "You can't bring yourself to toss artillery on the ground, the filth down there will fuck up the cannons!"
        elif ('cannonball' in stats and cmd.tokens[1] == 'cannonball') or ('harpoon' in stats and cmd.tokens[1] == 'harpoon'):
            response = "They already have one. Don't go throwing shit around belowdeck, or the filth level's gonna go through the roof."
        elif user_data.id_user != yacht.storehouse:
            response = "You're nowhere near the storehouse, you can't find it!"
        else:
            yacht.applyStat(stat_type=cmd.tokens[1], quantity=0, target = 0)
            response = "{} tosses a {} cannon-ways!".format(cmd.message.author.display_name, cmd.tokens[1])
            yacht.accumulate_filth()

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
        elif yacht.filth_check():
            response = "You reach over to load the {}, but nearly concuss yourself slipping over the greasy floors. Somebody forgot to swab...".format(cmd.tokens[1])
        elif ('cannonball' not in stats and cmd.tokens[1] == 'cannonball') or (
                'harpoon' not in stats and cmd.tokens[1] == 'harpoon'):
            response = "You don't have one of those. Storehouse guy, chop chop!"
        elif user_data.id_user != yacht.cannon:
            response = "You're nowhere near the cannon, you can't do that!"
        else:
            response = None
            stat_sought = None
            for stat in stats:
                if stat == cmd.tokens[1] and stat.quantity == 1:
                    response = "You already loaded that in."
                    break
                elif stat == cmd.tokens[1] and stat.quantity == 0:
                    stat_sought = stat
            if response is None:
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
        elif yacht.filth_check():
            response = "The stink lines on the deck completely obscure your vision! Somebody swab the poop deack already..."
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
                yacht.accumulate_filth()
                stat_sought.target = target_ship.thread_id
                stat_sought.quantity = (target_ship.xcoord * 1000) + target_ship.ycoord #this creates a readable and distinct value for the coords locked into
                stat_sought.persist()
                response = "Aim for the {}, right between the eyes! Steady as she goes...".format(target_ship.yacht_name)

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def fire_cannon(cmd):
    user_data = EwUser(member=cmd.message.author)
    other_ship_response = ""
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
        elif yacht.filth_check():
            response = "The cabin is so rank with filth that the humidity dampens the fuse! Can't fire until you swab the deck."
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
                yacht.accumulate_filth()
                if aimed is False:
                    response = "BAM!..............splish!\nThe cannonball flies through the air, landing on sweet nothing! Aim faster next time, dumpass!"
                else:
                    other_ship_channel = target_ship.get_thread()
                    distance = math.sqrt((target_ship.xcoord-yacht.xcoord)**2 + (target_ship.ycoord-yacht.ycoord)**2)
                    #i just used the fucking pythagorean theorem to kill a man with cannonballs. yeah i bet you're jealous

                    if firetype == 'cannonball':

                        hit_chance = (-0.018 * (distance**2)) - (0.048 * distance) + 1.015
                        #i plotted the general results i wanted into a curve of best fit calculator and these were my results, go figure
                        random_pct = random.randint(0, 100)
                        if random_pct > int(hit_chance * 100):
                            response = "BAM!...........whoosh! You barely miss The {}!".format(target_ship.yacht_name)
                            other_ship_response = "...whoosh! Shit, a cannonball! We're under attack!"
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
                            other_ship_response = "BAM!............KKKKRRRRRAAAACKKKK! Your hull has been breached! The hole's{}!".format(hole_dict.get(holesize))

                            target_ship.applyStat(stat_type='flood', quantity=holesize, target=yacht.thread_id)
                    else:
                        if distance != 0:
                            response = "Harpoons don't reach that far. You have to be in the same area as them."
                        else:
                            target_ship.applyStat(stat_type="harpooned", quantity=5, target=yacht.thread_id)
                            yacht.applyStat(stat_type="harpooned", quantity=0, target=target_ship.thread_id)
                            response = "SHHHHINC! A harpoon sinks into the {}'s walls, locking your ship to theirs!".format(target_ship.yacht_name)
                            other_ship_response = "SHHHHINC! A harpoon sinks into the {}'s walls, locking their ship to yours!".format(target_ship.yacht_name)


    if other_ship_response != "":
        await fe_utils.send_message(cmd.client, other_ship_channel, fe_utils.formatMessage(cmd.message.author, other_ship_response))

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def gangplank(cmd):
    user_data = EwUser(member=cmd.message.author)
    target_name  = ' '.join(word for word in cmd.tokens[1:])

    if user_data.poi[:5] != 'yacht':
        response = "Plank was a member of Slimecorp, telemarketing division. He's probably pretty miffed you put him out of a job, so i doubt he's in a gang now."
    elif cmd.tokens_count < 2:
        response = "Be more specific, who are you trying to board?"
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        self_stats = yacht.getYachtStats()

        coord_me = [yacht.xcoord, yacht.ycoord]

        boats = yacht_utils.find_local_boats(current_coords=coord_me, id_server=cmd.guild.id, name=target_name)
        if len(boats) < 1:
            response = "There's nobody to gangplank with that name."
        elif yacht.filth_check():
            response = "You can't find the plank under all this filth. God dammit, where is that blasted thing!"
        else:
            chosen_boat = None
            for boat in boats:
                if boat.owner == yacht.owner:
                    continue
                else:
                    chosen_boat = boat
                    break

            if chosen_boat is None:
                response = "You can't gangplank yourself. Hey, somebody throw this guy overboard."
            elif chosen_boat.direction != yacht.direction or yacht.direction != 'stop':
                response = "One of you is still moving, you can't gangplank unless you're both stopped in the same place."
            elif "gangplanked" in self_stats:
                response = "You already gangplanked with somebody. You're a bit tied up at the moment."
            else:
                yacht.accumulate_filth()
                response = "You drop down the plank onto the {}!".format(chosen_boat.yacht_name)
                target_response = "Someone's boarding! It's the {}!".format(yacht.yacht_name)
                chosen_boat.applyStat(stat_type='gangplanked', target=yacht.thread_id)
                yacht.applyStat(stat_type='gangplanked', target=chosen_boat.thread_id)
                target_channel = await chosen_boat.get_thread()
                await fe_utils.send_message(cmd.client, target_channel,  target_response)

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))




async def seanet(cmd):
    user_data = EwUser(member=cmd.message.author)

    time_now = int(time.time())

    if user_data.poi[:5] != 'yacht':
        response = "You didn't find a net, so though you get ready to throw, I say no. Try it on a yacht."

    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        stats = yacht.getYachtStats()
        if yacht.direction != 'stop':
            response = "You can only do that when the boat's not moving."
        elif yacht.poopdeck != user_data.id_user:
            response = "If you're gonna scoop shit from the bottom of the sea, you'll need to be on the poop deck."
        elif yacht.filth_check():
            response = "Your sea net is already full. Too much chum and filth that SOMEBODY forgot to swab."
        elif 'netcast' in stats:
            chosen_stat = None
            for stat in stats:
                if stat == 'netcast':
                    chosen_stat=stat
                    break

            inventory_id = "slimesea_{}_{}".format(yacht.xcoord, yacht.ycoord)
            sea_inv = bknd_item.inventory(id_user=inventory_id, id_server=cmd.guild.id)
            response = "You pull up the net..."
            yacht.accumulate_filth()
            if time_now - 60 > chosen_stat.quantity and len(sea_inv) > 0:
                received_items = random.randint(0, len(sea_inv))
                random.shuffle(sea_inv)
                for x in range(received_items):
                    item_obj = bknd_item.EwItem(id_item=sea_inv[x].get('id_item'))
                    bknd_item.give_item(id_item=item_obj.id_item, id_user=user_data.poi, id_server=item_obj.id_server)
                    #item_obj.id_owner = user_data.poi
                    item_obj.persist()
                    response += "\nYou caught a {}!".format(sea_inv[x].get('name'))

                if received_items == 0:
                    response += "and nothing's in it."
            else:
                response = "You pull up the net...and nothing's in it."
        else:
            yacht.accumulate_filth()
            response = "You drop the salvage net into the depths of the Slime Sea."
            yacht.applyStat(stat_type='netcast', quantity=time_now)

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def swab(cmd):
    user_data = EwUser(member=cmd.message.author)
    if user_data.poi[:5] != 'yacht':
        response = "The landlubber term for that is !scrub, scrub."
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        if user_data.id_user != yacht.poopdeck:
            response = "Don't just !swab anything. It's gotta be when you're manned to the poop deck!"
        else:
            swab = -20
            if user_data.life_state == 1:
                swab *= 1.5
            yacht.filth = max(0, int(yacht.filth)+int(swab))
            yacht.persist()
            response = "**swab swab**"
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))



async def repair_ship(cmd):
    user_data = EwUser(member=cmd.message.author)
    if user_data.poi[:5] != 'yacht':
        response = "Fuck you, there aren't any ships in this game. Not even at Smitty's Yacht Shack I'm pretty sure."
    elif ewutils.active_restrictions.get(user_data.id_user) is not None and ewutils.active_restrictions.get(user_data.id_user) > 0:
        response = "You can't do that right now."
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        if user_data.id_user in [yacht.helm, yacht.poopdeck]:
            response = "You're aboveboard! Stop manning the helm or poop deck and you can go do that."
        elif yacht.filth_check():
            response = "Your hands keep slipping thanks to all the grease around here. Someone forgot to reduce the filth."
        else:
            totalrepair = 2
            stats = yacht.getYachtStats()
            response = "There aren't any holes to repair."
            if 'flood' in stats:
                ewutils.active_restrictions[user_data.id_user] = 6
                await asyncio.sleep(5)
                ewutils.active_restrictions[user_data.id_user] = 0
                stats = yacht.getYachtStats()
                for stat in stats:
                    if stat.type_stat == 'flood':
                        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
                        yacht.accumulate_filth()
                        if totalrepair >= stat.quantity:
                            yacht.clearStat(id_stat=stat.id_stat)
                        else:
                            stat.quantity -= totalrepair
                            stat.persist()
                        response = "You patch some scrap wood over the hole. You should be flooding a bit less now."
                        break

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))



async def scoop_ship(cmd):
    user_data = EwUser(member=cmd.message.author)
    if user_data.poi[:5] != 'yacht' and user_data.id_user != 412813074991415316:
        response = "Nah, you're not the scoop guy. That's someone else."
    elif user_data.poi[:5] != 'yacht':
        response = '**YEAHHHHH BRO!!!**'
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        if yacht.flood == 0:
            response = "There's no water in here."
        elif user_data.id_user in[yacht.helm, yacht.poopdeck]:
            response = "You're aboveboard! Stop manning the helm or poop deck and you can go do that."
        elif yacht.filth_check():
            response = "You try to scoop the water out from the {}, but all the grime from the unswabbed deck absorbed it all. This hasn't made you any safer from being weighed down into Davy Jones' locker, but you certainly can't scoop it out. Fucking swabbies.".format(yacht.yacht_name)
        else:
            response = ""
            totalscoop = 1
            if user_data.weapon != -1:
                equip = bknd_item.EwItem(id_item=user_data.weapon)
                if equip.template == ewcfg.weapon_id_slimeringcan:
                    totalscoop *= 2

            yacht.flood = max(0, yacht.flood-totalscoop)
            yacht.persist()

    if response != "":
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))



async def lock(cmd): #doubles as the ship unlock
    user_data = EwUser(member=cmd.message.author)
    if user_data.poi[:5] != 'yacht':
        response = "Your apartment is locked already. You're not stupid enough to leave it open to anyone, ever."
    else:
        yacht = EwYacht(id_server=cmd.guild.id, id_thread=int(user_data.poi[5:]))
        if user_data.id_user != yacht.owner:
            response = "It's not your yacht, you don't have the key. Funny idea, though."
        else:
            response = ""
            if cmd.tokens[0] == '!unlock':
                if 'locked' not in yacht.getYachtStats():
                    response = "It's already unlocked."
                else:
                    response = "You open the entry hatch to your vessel."
                    for stat in yacht.getYachtStats():
                        if stat.type_stat == 'locked':
                            yacht.clearStat(id_stat=stat.id_stat)
            elif cmd.tokens[1] == '!lock':
                if 'locked' in yacht.getYachtStats():
                    response = "It's already locked."
                else:
                    yacht.applyStat(stat_type='locked')
                    response = "You lock the entry hatch to the boat."
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def statstest(cmd):
    pass