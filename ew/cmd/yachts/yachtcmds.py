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
import asyncio


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
            yacht.yacht_name = name
            yacht.id_server = user_data.id_server
            response = "I christen ye: The S.S. {}!".format(name)
            boat_poi = poi_static.id_to_poi.get("yacht")
            new_poi = '{}{}'.format('yacht', yacht.thread_id)
            poi_static.id_to_poi[new_poi] = boat_poi

            starting_message = await fe_utils.send_message(cmd.client, channel_slimesea, "S.S. {}".format(name))
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
            current_ship = EwYacht(id_server=user_data.id_server, id_thread=user_data.poi[5:])
            ships = yacht_utils.find_local_boats(name=name, current_coords=[current_ship.xcoord, current_ship.ycoord])
        else:
            ships = yacht_utils.find_local_boats(poi=user_data.poi, name=name)

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