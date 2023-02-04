import time
import random
from copy import deepcopy

from ew.backend import item as bknd_item
from ew.backend import core as bknd_core
from ew.backend.item import EwItem
from ew.backend.market import EwMarket
from ew.backend.market import EwStock
from ew.backend.player import EwPlayer
from ew.backend.fish import EwRecord
from ew.backend.dungeons import EwGamestate
from ew.static import cfg as ewcfg
from ew.static import community_cfg as comm_cfg
from ew.static import poi as poi_static
from ew.static.fish import fish_map
try:
    from ew.static.rstatic import relic_map
except:
    from ew.static.rstatic_dummy import relic_map
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import market as market_utils
from ew.utils import rolemgr as ewrolemgr
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict

try:
    import ew.static.rstatic as relic_static
    import ew.cmd.debug as debug
except:
    import ew.static.rstatic_dummy as relic_static
    import ew.cmd.debug_dummy as debug

async def invest(cmd):
    """ player invests slimecoin in the market """
    user_data = EwUser(member = cmd.message.author)

    time_now = round(time.time())
    market_data = EwMarket(id_server = cmd.message.author.guild.id)

    if cmd.message.channel.name not in [ewcfg.channel_stockexchange, ewcfg.channel_stockexchange_p]: # or user_data.poi != ewcfg.poi_id_downtown:
        # Only allowed in the stock exchange.
        response = ewcfg.str_exchange_channelreq.format(currency = "SlimeCoin", action = "invest")
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if market_data.clock < 6 or market_data.clock >= 20:
        response = ewcfg.str_exchange_closed
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if user_data.time_lastinvest + ewcfg.cd_invest > time_now:
        # Limit frequency of investments.
        response = ewcfg.str_exchange_busy.format(action = "invest")
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if user_data.life_state == ewcfg.life_state_corpse:
        # Disallow invests from ghosts.
        response = "Your slimebroker can't confirm your identity while you're dead."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if user_data.life_state == ewcfg.life_state_kingpin:
        # Disallow investments by RF and CK kingpins.
        response = "You need that money to buy more videogames."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    else:
        value = None
        stock = None

        if cmd.tokens_count > 1:
            value = ewutils.getIntToken(cmd.tokens, allow_all = True)

            for token in cmd.tokens[1:]:
                if token.lower() in ewcfg.stocks:
                    stock = token.lower()
                    break


        if value != None:
            if value < 0:
                value = user_data.slimecoin
            if value <= 0:
                value = None

        if value != None:
            if stock != None:

                stock = EwStock(id_server = cmd.guild.id, stock = stock)
                # basic exchange rate / 1000 = 1 share
                exchange_rate = (stock.exchange_rate / 1000.0)

                cost_total = round(value * 1.05)

                # gets the highest value possible where the player can still pay the fee
                if value == user_data.slimecoin:
                    while cost_total > user_data.slimecoin:
                        value -= cost_total - value
                        cost_total = round(value * 1.05)

                # The user can only buy a whole number of shares, so adjust their cost based on the actual number of shares purchased.
                net_shares = round(value / exchange_rate)

                if user_data.slimecoin < cost_total:
                    response = "You don't have enough SlimeCoin. ({:,}/{:,})".format(user_data.slimecoin, cost_total)

                elif value > user_data.slimecoin:
                    response = "You don't have that much SlimeCoin to invest."

                elif net_shares == 0:
                    response = "You don't have enough SlimeCoin to buy a share in {stock}".format(stock = ewcfg.stock_names.get(stock.id_stock))

                else:
                    user_data.change_slimecoin(n = -cost_total, coinsource = ewcfg.coinsource_invest)
                    shares = market_utils.getUserTotalShares(id_server = user_data.id_server, stock = stock.id_stock, id_user = user_data.id_user)
                    shares += net_shares
                    market_utils.updateUserTotalShares(id_server = user_data.id_server, stock = stock.id_stock, id_user = user_data.id_user, shares = shares)
                    user_data.time_lastinvest = time_now

                    stock.total_shares += net_shares
                    response = "You invest {coin:,} SlimeCoin and receive {shares:,} shares in {stock}. Your slimebroker takes his nominal fee of {fee:,} SlimeCoin.".format(coin = value, shares = net_shares, stock = ewcfg.stock_names.get(stock.id_stock), fee = (cost_total - value))

                    user_data.persist()
                    stock.timestamp = round(time.time())
                    stock.persist()

            else:
                response = "That's not a valid stock name, please use a proper one, you cunt: {}".format(ewutils.formatNiceList(names = ewcfg.stocks))

        else:
            response = ewcfg.str_exchange_specify.format(currency = "SlimeCoin", action = "invest")

    # Send the response to the player.
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def withdraw(cmd):
    """ player withdraws slimecoin from the market """
    user_data = EwUser(member = cmd.message.author)

    time_now = round(time.time())
    market_data = EwMarket(id_server = cmd.message.author.guild.id)

    if market_data.clock < 6 or market_data.clock >= 20:
        response = ewcfg.str_exchange_closed
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if cmd.message.channel.name not in [ewcfg.channel_stockexchange, ewcfg.channel_stockexchange_p]:  #or user_data.poi != ewcfg.poi_id_downtown:
        # Only allowed in the stock exchange.
        response = ewcfg.str_exchange_channelreq.format(currency = "SlimeCoin", action = "withdraw")
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if user_data.life_state == ewcfg.life_state_corpse:
        # Disallow withdraws from ghosts.
        response = "Your slimebroker can't confirm your identity while you're dead."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    else:
        value = None
        stock = None

        if cmd.tokens_count > 1:
            value = ewutils.getIntToken(cmd.tokens[1:], allow_all = True)

            for token in cmd.tokens[1:]:
                if token.lower() in ewcfg.stocks:
                    stock = token.lower()
                    break


        if stock != None:
            stock = EwStock(id_server = cmd.guild.id, stock = stock)

            total_shares = market_utils.getUserTotalShares(id_server = user_data.id_server, stock = stock.id_stock, id_user = user_data.id_user)

            if value != None:
                if value < 0:
                    value = total_shares
                if value <= 0:
                    value = None

            if value != None:

                if value <= total_shares:
                    exchange_rate = (stock.exchange_rate / 1000.0)

                    shares = value
                    slimecoin = round(value * exchange_rate)

                    if user_data.time_lastinvest + ewcfg.cd_invest > time_now:
                        # Limit frequency of withdrawals
                        response = ewcfg.str_exchange_busy.format(action = "withdraw")
                    else:
                        user_data.change_slimecoin(n = slimecoin, coinsource = ewcfg.coinsource_withdraw)
                        total_shares -= shares
                        user_data.time_lastinvest = time_now
                        stock.total_shares -= shares

                        response = "You exchange {shares:,} shares in {stock} for {coins:,} SlimeCoin.".format(coins = slimecoin, shares = shares, stock = ewcfg.stock_names.get(stock.id_stock))
                        user_data.persist()
                        stock.timestamp = round(time.time())
                        stock.persist()
                        market_utils.updateUserTotalShares(id_server = user_data.id_server, stock = stock.id_stock, id_user = user_data.id_user, shares = total_shares)
                else:
                    response = "You don't have that many shares in {stock} to exchange.".format(stock = ewcfg.stock_names.get(stock.id_stock))
            else:
                response = ewcfg.str_exchange_specify.format(currency = "SlimeCoin", action = "withdraw")
        else:
            response = "That's not a valid stock name, please use a proper one, you cunt: {}".format(ewutils.formatNiceList(names = ewcfg.stocks))

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def redeem(cmd):
    """ player turns slimecoin into slime """
    user_data = EwUser(member = cmd.message.author)

    time_now = round(time.time())
    market_data = EwMarket(id_server = cmd.message.author.guild.id)

    if market_data.clock < 6 or market_data.clock >= 20:
        response = ewcfg.str_exchange_closed
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if user_data.time_lastinvest + ewcfg.cd_invest > time_now:
        response = ewcfg.str_exchange_busy.format(action = "redeem")

    if cmd.message.channel.name  not in [ewcfg.channel_stockexchange, ewcfg.channel_stockexchange_p]:  #or user_data.poi != ewcfg.poi_id_downtown:
        # Only allowed in the stock exchange.
        response = ewcfg.str_exchange_channelreq.format(currency = "SlimeCoin", action = "redeem")
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if user_data.life_state == ewcfg.life_state_corpse:
        # Disallow withdraws from ghosts.
        response = "Your slimebroker can't confirm your identity while you're dead."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    else:
        slimecoin_exchange_rate = 25000000000000 # 25 trillion slime

        redeem_value = round(user_data.slimecoin / slimecoin_exchange_rate)

        if redeem_value <= 0:
            response = "Sadly, you haven't made enough Slimecoin to reedeem any slime!"

        else:
            response = ""

            if user_data.life_state == ewcfg.life_state_enlisted:
                response = "After you dot all the i’s and cross all the t’s, you immediately send your Kingpin half of your earnings."
                role_boss = (ewcfg.role_copkiller if user_data.faction == ewcfg.faction_killers else ewcfg.role_rowdyfucker)
                kingpin = fe_utils.find_kingpin(id_server = cmd.guild.id, kingpin_role = role_boss)
                kingpin = EwUser(id_server=cmd.guild.id, id_user=kingpin.id_user)
                if kingpin:
                    kingpin.change_slimes(n = int(redeem_value / 2))
                    kingpin.persist()

            else:
                response = "Your slimebroker pulls a fast one on you and gets you to sign a waiver that lets SlimeCorp keep half of your supposedly redeemed slime. Damn."

            response += "You walk out with {:,}.".format(int(redeem_value / 2))
            user_data.slimes += int(redeem_value / 2)
            user_data.slimecoin = round(user_data.slimecoin % slimecoin_exchange_rate)
            user_data.persist()

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def donate(cmd):
    """ donate slime to slimecorp in exchange for slimecoin """
    user_data = EwUser(member = cmd.message.author)

    market_data = EwMarket(id_server = user_data.id_server)

    time_now = round(time.time())

    if user_data.poi == ewcfg.poi_id_themuseum:
       response = await museum_donate(cmd=cmd)
    elif user_data.poi == ewcfg.poi_id_slimecorphq:
        poi = poi_static.id_to_poi.get(user_data.poi)

        value = None
        if cmd.tokens_count > 1:
            value = ewutils.getIntToken(tokens = cmd.tokens, allow_all = True)

        if value != None:
            if value < 0:
                value = user_data.slimes
            if value <= 0:
                value = None

        if value != None and value < ewcfg.slimecoin_exchangerate:
            response = "You must volunteer to donate at least %d slime to receive compensation." % ewcfg.slimecoin_exchangerate

        elif value != None:
            # Amount of slime invested.
            cost_total = round(value)
            coin_total = round(value / ewcfg.slimecoin_exchangerate)

            if user_data.slimes < cost_total:
                response = "Acid-green flashes of light and bloodcurdling screams emanate from small window of SlimeCorp HQ. Unfortunately, you did not survive the procedure. Your body is dumped down a disposal chute to the sewers."
                market_data.donated_slimes += user_data.slimes
                market_data.persist()
                user_data.trauma = ewcfg.trauma_id_environment
                die_resp = await user_data.die(cause = ewcfg.cause_donation)
                await die_resp.post()
            else:
                # Do the transfer if the player can afford it.
                market_data.donated_slimes += cost_total
                market_data.persist()
                user_data.change_slimes(n = -cost_total, source = ewcfg.source_spending)
                user_data.change_slimecoin(n = coin_total, coinsource = ewcfg.coinsource_donation)

                # Persist changes
                user_data.persist()

                response = "You stumble out of a Slimecorp HQ vault room in a stupor. You don't remember what happened in there, but your body hurts and you've got {slimecoin:,} shiny new SlimeCoin in your pocket.".format(slimecoin = coin_total)

        else:
            response = ewcfg.str_exchange_specify.format(currency = "slime", action = "donate")

    elif user_data.poi == ewcfg.poi_id_slimeoidlab:

        poudrins = bknd_item.find_item(item_search = "slimepoudrin", id_user = cmd.message.author.id, id_server = cmd.guild.id if cmd.guild is not None else None, item_type_filter = ewcfg.it_item)

        if poudrins == None:
            response = "You have to own a poudrin in order to donate a poudrin. Duh."

        else:
            bknd_item.item_delete(id_item = poudrins.get('id_item'))  # Remove Poudrins
            market_data.donated_poudrins += 1
            market_data.persist()

            response = "You hand off one of your hard-earned poudrins to the front desk receptionist, who is all too happy to collect it. Pretty uneventful, but at the very least you’re glad donating isn’t physically painful anymore."

    else:
        response = "To donate slime, go to the SlimeCorp HQ in Downtown. To donate museum goods, go to the Museum in Ooze Gardens."

    # Send the response to the player.
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def museum_donate(cmd):
    dialogue_set = ewcfg.museum_dialogue.get(ewcfg.current_curator)

    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id)
    if item_sought:
        item_obj = EwItem(id_item=item_sought.get("id_item"))

        if (item_obj.item_type == ewcfg.it_relic or item_obj.template in relic_static.alt_relics):
            response = await relic_donate(item_obj.id_item, cmd, dialogue_set)

        elif item_obj.item_props.get('acquisition') == ewcfg.acquisition_fishing:
            response = await fish_donate(item_obj.id_item, cmd, dialogue_set)
        elif item_obj.item_props.get('id_furniture') == 'pictureframe':

            response = await art_donate(item_obj.id_item, cmd, dialogue_set)
        else:
            response = dialogue_set.get('odditem')
    else:
        response = "You don't have that item."

    #fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    return response


async def fish_donate(id_item, cmd, dialogue_set):
    item_obj = EwItem(id_item=id_item)
    length = item_obj.item_props.get('length')
    id_fish = item_obj.item_props.get('id_food')
    user_data = EwUser(member=cmd.message.author)

    if length is None:
        length = float((ewcfg.fish_size_range.get(item_obj.item_props.get('size'))[0] + ewcfg.fish_size_range.get(item_obj.item_props.get('size'))[1])/2)
        item_obj.item_props['length'] = length
        item_obj.persist()
    else:
        length = float(length)
    current_record = EwRecord(id_server=cmd.guild.id, record_type=id_fish)
    if current_record.record_amount > length:
        response = dialogue_set.get("smallfish")
    elif id_fish in user_data.get_bans():
        response = dialogue_set.get('cheatedfish').format(insult=random.choice(comm_cfg.curator_insults))
    elif item_obj.item_props.get('embiggened') == 'illegal' and random.choice([0, 1]) == 0:
        response = dialogue_set.get("caughtcheatfish").format(insult=random.choice(comm_cfg.curator_insults), fish=(item_obj.item_props.get('food_name').upper() if dialogue_set == ewcfg.museum_curator_dialogue.get('curator') else item_obj.item_props.get('food_name')))
        user_data.ban(faction=id_fish)
    else:
        aquarium = fe_utils.get_channel(server = cmd.guild, channel_name='aquarium')
        if current_record.id_post != "" and current_record.id_post is not None:
            old_message = await aquarium.fetch_message(int(current_record.id_post))
            await old_message.delete()
        current_record.record_amount = length
        if item_obj.item_props.get('embiggened') is not None:
            current_record.legality = 0


        current_record.id_user = cmd.message.author.id

        rawdesc = item_obj.item_props.get('food_desc')
        cleandesc = rawdesc[:rawdesc.rfind("It's")]

        player = EwPlayer(id_user=item_obj.id_owner, id_server=cmd.guild.id)
        museum_text = "-------------------------------------------------\n{}\nDonated by {}\n{}\nLENGTH:{} INCHES\n{}".format(item_obj.item_props.get('food_name').upper(), player.display_name, current_record.id_image, item_obj.item_props.get('length'), cleandesc)
        sent_message = await fe_utils.send_message(cmd.client, aquarium, museum_text)
        current_record.id_post = sent_message.id
        current_record.persist()

        slimes_awarded = 330000

        if length > 78:
            slimes_awarded *= 3

        user_data = EwUser(id_user=cmd.message.author.id, id_server=cmd.guild.id)
        if user_data.life_state == ewcfg.life_state_corpse:
            slimes_awarded *= -1
        user_data.change_slimes(n=slimes_awarded)
        user_data.persist()


        response = dialogue_set.get("fishdonate").format(item_obj.item_props.get('food_name'), slimes_awarded)
        bknd_item.item_delete(id_item = id_item)

    return response


async def relic_donate(id_item, cmd, dialogue_set):
    item_obj = EwItem(id_item=id_item)
    if item_obj.item_props.get('donated') is not None and item_obj.item_props.get('donated') != 0:
        response = dialogue_set.get("redonaterelic")
    else:
        item_obj.item_props['donated'] = 1
        item_obj.persist()

        relic_count = EwGamestate(id_server=cmd.guild.id, id_state='donated_relics')
        count = int(relic_count.value)
        count += 1
        relic_count.value = str(count)
        relic_count.persist()

        if item_obj.item_type != 'relic':
            item_obj.item_props['id_relic'] = "{}{}".format('_', item_obj.template)
        relic_obj = relic_static.relic_map.get(item_obj.item_props.get('id_relic'))
        payout = relic_obj.amount_yield
        player = EwPlayer(id_user=item_obj.id_owner, id_server=cmd.guild.id)

        if relic_obj.acquisition == 'zine':
            bknd_core.execute_sql_query("UPDATE books SET {genre} = 1 WHERE {title} = %s and {genre} = 11".format(title=ewcfg.col_title, genre=ewcfg.col_genre), (relic_obj.str_use, ))

        if relic_obj.str_use == relic_static.debug1:
            artplayer_obj = EwGamestate(id_server=cmd.guild.id, id_state='artplayer')
            id_artplayer = int(artplayer_obj.value)
            bknd_item.give_item(id_server=cmd.guild.id, id_user=id_artplayer, id_item=item_obj.id_item)
            return relic_obj.str_museum


        museum_text = "-------------------------------------------------\n{}\nDiscovered by {}\n-...-\n{}".format(relic_obj.str_name, player.display_name, relic_obj.str_museum)

        relic_channel = fe_utils.get_channel(server=cmd.guild, channel_name='relic-exhibits')
        sent_message = await fe_utils.send_message(cmd.client, relic_channel, museum_text)
        new_record = EwRecord(id_server=cmd.guild.id, record_type=item_obj.item_props.get('id_relic'))
        new_record.id_user = cmd.message.author.id
        new_record.id_post = str(sent_message.id)
        new_record.persist()

        user_data = EwUser(id_user=cmd.message.author.id, id_server=cmd.guild.id)
        if user_data.life_state == ewcfg.life_state_corpse:
            payout *= -1
        user_data.change_slimes(n=payout)
        user_data.persist()
        response = dialogue_set.get("donaterelic").format(relic_obj.str_name, payout)

    return response


async def art_donate(id_item, cmd, dialogue_set):
    item_obj = EwItem(id_item=id_item)

    if item_obj.item_props.get('furniture_desc') == 'https://cdn11.bigcommerce.com/s-cece8/images/stencil/1280x1280/products/305/1506/010420__10394.1343058001.jpg?c=2&imbypass=on':
        response = dialogue_set.get('spoons')

    else:
        #gamestate = EwGamestate(id_server=item_obj.id_server, id_state='artplayer')
        if 1 != None:

            if item_obj.item_props.get('title') is not None:
                new_record = EwRecord(id_server=cmd.guild.id, record_type = item_obj.item_props.get('title'))
                if new_record.id_user != -1:
                    return dialogue_set.get("artnametaken").format(insult=random.choice(comm_cfg.curator_insults))
                elif "::" in item_obj.item_props.get('title'):
                    return dialogue_set.get("colon")
                else:
                    new_record.id_user = item_obj.id_owner
                    new_record.legality  = 1
                    new_record.id_image = item_obj.item_props.get('furniture_desc')
                    new_record.persist()



                response = dialogue_set.get("deviantpost")


                player_obj = EwPlayer(id_user=item_obj.id_owner, id_server=cmd.guild.id)
                artserv = fe_utils.get_channel(server=cmd.guild, channel_name='deviant-splaart')
                post_text = "{}::\nBy {}\n\n{}".format(item_obj.item_props.get('title'), player_obj.display_name, item_obj.item_props.get('furniture_desc'))
                await fe_utils.send_message(cmd.client, artserv, post_text)
                bknd_item.item_delete(id_item)

            else:
                response = dialogue_set.get("notitleart").format(insult = random.choice(comm_cfg.curator_insults))
        else:
            response = '\"Sorry, we\'re not collecting donations from your kind at this time. Please refrain from stinking up the general vicinity.\"'
    return response


async def populate_image(cmd):
    """ Add art for records e.g. posts in the aquarium, relic exhibit, etc."""
    if 0 < ewrolemgr.check_clearance(member=cmd.message.author) < 4:
        if cmd.tokens_count != 4:
            response = "Invalid command. Try !addart <fish/relic> <title> <link>."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        else:
            type = cmd.tokens[1]
            item = cmd.tokens[2]
            link = cmd.tokens[3]

            if type == "relic":
                channel = fe_utils.get_channel(server=cmd.guild, channel_name='relic-exhibits')
            elif type == "fish":
                channel = fe_utils.get_channel(server=cmd.guild, channel_name='aquarium')
            else:
                response = "Invalid command. Try !addart <relic/art> <title> <link>"
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            if item in relic_static.alt_relics:
                item = "_" + item

            record = EwRecord(id_server=cmd.guild.id, record_type=item)

            record.id_image = link
            record.persist()
            message = await channel.fetch_message(int(record.id_post))

            response = "Added an image to the message."

            if '-...-' not in message.content:
                donor = EwPlayer(id_server=cmd.guild.id, id_user=record.id_user)
                if type == 'fish':
                    fishmap = fish_map.get(record.record_type)
                    if fishmap is not None:
                        museum_text = "-------------------------------------------------\n{}\nDonated by {}\n{}\nLENGTH:{} INCHES\n{}".format(
                            fishmap.str_name.upper(), donor.display_name, record.id_image,
                            record.record_amount, fishmap.str_desc)
                        message = await message.edit(content=museum_text)
                    else:
                        response = "Failed to add an image to the message."

                elif type == 'relic':
                    relicmap = relic_map.get(record.record_type)
                    if relicmap is not None:
                        museum_text = "-------------------------------------------------\n{}\nDiscovered by {}\n{}\n{}".format(relicmap.str_name, donor.display_name, record.id_image, relicmap.str_museum)
                        message = await message.edit(content=museum_text)
                    else:
                        response = "Failed to add an image to the message."

            else:
                message = await message.edit(content = message.content.replace("-...-", link))

            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    else:
        response = "The Curator doesn't trust you with his precious displays. Maybe you could get someone else to help you..."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def xfer(cmd):
    """ Transfer slimecoin between players """
    time_now = round(time.time())
    user_data = EwUser(member = cmd.message.author)


    if cmd.message.channel.name  not in [ewcfg.channel_stockexchange, ewcfg.channel_stockexchange_p]:
        # Only allowed in the stock exchange.
        response = ewcfg.str_exchange_channelreq.format(currency = "SlimeCoin", action = "transfer")
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if cmd.mentions_count != 1:
        # Must have exactly one target to send to.
        response = "Mention the player you want to send SlimeCoin to."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if user_data.time_lastinvest + ewcfg.cd_invest > time_now:
        # Limit frequency of transfers
        response = ewcfg.str_exchange_busy.format(action = "transfer slimecoin")
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if user_data.life_state == ewcfg.life_state_corpse:
        # Disallow transfers from ghosts.
        response = "Your slimebroker can't confirm your identity while you're dead."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    member = cmd.mentions[0]
    target_data = EwUser(member = member)

    if target_data.life_state == ewcfg.life_state_kingpin:
        # Disallow transfers to RF and CK kingpins.
        response = "You can't transfer SlimeCoin to a known criminal warlord."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    market_data = EwMarket(id_server = cmd.message.author.guild.id)

    if cmd.message.author.id == member.id:

        slimes_total = user_data.slimes
        slimes_drained = int(slimes_total * 0.1)
        slimes_todistrict = slimes_total - slimes_drained

        sewer_data = EwDistrict(district=ewcfg.poi_id_thesewers, id_server=user_data.id_server)
        sewer_data.change_slimes(n=slimes_drained)
        sewer_data.persist()

        district_data = EwDistrict(district=user_data.poi, id_server=cmd.guild.id)
        district_data.change_slimes(n=slimes_todistrict, source=ewcfg.source_killing, poi_name=user_data.poi)
        district_data.persist()

        # Set the id_killer to the player himself, remove his slime and slime poudrins.
        user_data.id_killer = cmd.message.author.id
        user_data.visiting = ewcfg.location_id_empty
        user_data.trauma = ewcfg.trauma_id_environment

        await user_data.die(cause = ewcfg.cause_suicide)

        return await fe_utils.send_response("Gaming the slimeconomy is punishable by death. FREE MARKET (TM) soldiers execute you immediately.", cmd)

    # Parse the slime value to send.
    value = None
    if cmd.tokens_count > 1:
        value = ewutils.getIntToken(tokens = cmd.tokens)

    if value != None:
        if value < 0:
            value = user_data.slimes
        if value <= 0:
            value = None

    if value != None:
        # Cost including the transfer fee.
        cost_total = round(value * 1.1)

        if user_data.slimecoin < cost_total:
            response = "You don't have enough SlimeCoin. ({:,}/{:,})".format(user_data.slimecoin, cost_total)
        else:
            # Do the transfer if the player can afford it.
            target_data.change_slimecoin(n = value, coinsource = ewcfg.coinsource_transfer)
            user_data.change_slimecoin(n = -cost_total, coinsource = ewcfg.coinsource_transfer)
            user_data.time_lastinvest = time_now

            # Persist changes
            response = "You transfer {slime:,} SlimeCoin to {target_name}. Your slimebroker takes his nominal fee of {fee:,} SlimeCoin.".format(slime = value, target_name = member.display_name, fee = (cost_total - value))

            target_data.persist()
            user_data.persist()
    else:
        response = ewcfg.str_exchange_specify.format(currency = "SlimeCoin", action = "transfer")

    # Send the response to the player.
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def rate(cmd):
    """ Show the current market exchange rate """

    response = ""

    if cmd.message.channel.name  not in [ewcfg.channel_stockexchange, ewcfg.channel_stockexchange_p]:
        # Only allowed in the stock exchange.
        response = "You must go to the Slime Stock Exchange to check the current stock exchange rates ."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    else:

        stock = ""

        if cmd.tokens_count > 0:
            stock = ewutils.flattenTokenListToString(cmd.tokens[1:])

        if stock in ewcfg.stocks:
            stock = EwStock(id_server = cmd.guild.id, stock = stock)
            response = "The current value of {stock} stocks is {cred:,} SlimeCoin per 1000 Shares.".format(stock = ewcfg.stock_names.get(stock.id_stock), cred = stock.exchange_rate)
        elif stock == "":
            for stock in ewcfg.stocks:
                stock = EwStock(id_server = cmd.guild.id, stock = stock)
                response += "\nThe current value of {stock} stocks is {cred:,} SlimeCoin per 1000 Shares.".format(stock = ewcfg.stock_names.get(stock.id_stock), cred = stock.exchange_rate)

        else:
            response = "That's not a valid stock name, please use a proper one, you cunt: {}".format(ewutils.formatNiceList(ewcfg.stocks))

        # Send the response to the player.
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def shares(cmd):
    """ Show player's shares in a stock """
    user_data = EwUser(member = cmd.message.author)

    stock = ""
    response = ""

    if cmd.tokens_count > 0:
        stock = ewutils.flattenTokenListToString(cmd.tokens[1:])

    if stock in ewcfg.stocks:
        response = get_user_shares_str(id_server = user_data.id_server, id_user = user_data.id_user, stock = stock)

    elif stock == "":
        for stock in ewcfg.stocks:
            response += "\n"
            response += get_user_shares_str(id_server = user_data.id_server, id_user = user_data.id_user, stock = stock)

    else:
        response = "That's not a valid stock name, please use a proper one, you cunt: {}".format(ewutils.formatNiceList(ewcfg.stocks))

    # Send the response to the player.
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def stocks(cmd):
    """ Show all interactable stocks in the market """

    if cmd.message.channel.name  not in [ewcfg.channel_stockexchange, ewcfg.channel_stockexchange_p]:
        # Only allowed in the stock exchange.
        response = "You must go to the Slime Stock Exchange to check the currently available stocks."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    else:

        response = "Here are the currently available stocks: {}".format(ewutils.formatNiceList(ewcfg.stocks))

    # Send the response to the player.
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def slimecoin(cmd):
    """ Show player's slimecoin balance """
    if cmd.mentions_count == 0:
        user_data = EwUser(member = cmd.message.author)
        coins = user_data.slimecoin
        response = "You have {:,} SlimeCoin.".format(coins)


    else:
        member = cmd.mentions[0]
        user_data = EwUser(member = member)
        coins = user_data.slimecoin
        response = "{} has {:,} SlimeCoin.".format(member.display_name, coins)

    # Send the response to the player.
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


def get_user_shares_str(id_server = None, stock = None, id_user = None):
    """ Used for !shares. """
    response = ""
    if id_server != None and stock != None and id_user != None:
        user_data = EwUser(id_server = id_server, id_user = id_user)
        stock = EwStock(id_server = id_server, stock = stock)
        shares = market_utils.getUserTotalShares(id_server = user_data.id_server, stock = stock.id_stock, id_user = user_data.id_user)
        shares_value = round(shares * (stock.exchange_rate / 1000.0))

        response = "You have {shares:,} shares in {stock}".format(shares = shares, stock = ewcfg.stock_names.get(stock.id_stock))

        #if user_data.poi == ewcfg.poi_id_downtown:
        response += ", currently valued at {coin:,} SlimeCoin.".format(coin = shares_value)
        #else:
        #	response += "."

    return response


async def trade(cmd):
    user_data = EwUser(member=cmd.message.author)

    user_trade = ewutils.active_trades.get(user_data.id_user)

    if user_trade != None and len(user_trade) > 0:
        if user_trade.get("state") > ewcfg.trade_state_proposed:

            stacking = False if 'nostack' in ewutils.flattenTokenListToString(cmd.tokens[1:]).lower() else True
            sort_by_name = True if 'name' in ewutils.flattenTokenListToString(cmd.tokens[1:]).lower() else False

            stacked_item_map = {}

            # print info about the current trade
            trade_partner = EwPlayer(id_user=user_trade.get("trader"), id_server=user_data.id_server)

            #print player's offers
            response = "Your offers:\n"
            items = ewutils.trading_offers.get(user_data.id_user) if not sort_by_name else sorted(ewutils.trading_offers.get(user_data.id_user), key=lambda item: item.get("name").lower)
            for item in items:
                if not stacking:
                    response_part = "{id_item}: {name} {quantity}\n".format(id_item=item.get("id_item"), name=item.get("name"), quantity=(" x{:,}".format(item.get("quantity")) if (item.get("quantity") > 1) else ""))

                    if len(response) + len(response_part) > 1492:
                        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                        response = ""

                    response += response_part

                else:
                    if item.get("name") in stacked_item_map:
                        stacked_item = stacked_item_map.get(item.get("name"))
                        stacked_item["quantity"] += item.get("quantity")
                    else:
                        stacked_item_map[item.get("name")] = deepcopy(item)

            if stacking:
                item_names = stacked_item_map.keys() if not sort_by_name else sorted(stacked_item_map.keys())

                for item_name in item_names:
                    item = stacked_item_map.get(item_name)
                    quantity = item.get('quantity')
                    response_part = "{soulbound_style}{name}{soulbound_style}{quantity}\n".format(
                        name=item.get('name'),
                        soulbound_style=("**" if item.get('soulbound') else ""),
                        quantity=(" **x{:,}**".format(quantity) if (quantity > 0) else "")
                    )

                    if len(response) + len(response_part) > 1492:
                        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                        response = ""

                    response += response_part

            if user_trade.get("state") == ewcfg.trade_state_complete:
                response_part = "**You are ready to complete the trade.**"

                if len(response) + len(response_part) > 1492:
                    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                    response = ""

                response += response_part

            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            #print partner's offers
            stacked_item_map = {}

            response = trade_partner.display_name + "'s offers:\n"
            items = ewutils.trading_offers.get(trade_partner.id_user) if not sort_by_name else sorted(ewutils.trading_offers.get(trade_partner.id_user), key=lambda item: item.get("name").lower)
            for item in items:
                if not stacking:
                    response_part = "{id_item}: {name} {quantity}\n".format(id_item=item.get("id_item"), name=item.get("name"), quantity=(" x{:,}".format(item.get("quantity")) if (item.get("quantity") > 1) else ""))

                    if len(response) + len(response_part) > 1492:
                        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                        response = ""

                    response += response_part

                else:
                    if item.get("name") in stacked_item_map:
                        stacked_item = stacked_item_map.get(item.get("name"))
                        stacked_item["quantity"] += item.get("quantity")
                    else:
                        stacked_item_map[item.get("name")] = deepcopy(item)

            if stacking:
                item_names = stacked_item_map.keys() if not sort_by_name else sorted(stacked_item_map.keys())

                for item_name in item_names:
                    item = stacked_item_map.get(item_name)
                    quantity = item.get('quantity')
                    response_part = "{soulbound_style}{name}{soulbound_style}{quantity}\n".format(
                        name=item.get('name'),
                        soulbound_style=("**" if item.get('soulbound') else ""),
                        quantity=(" **x{:,}**".format(quantity) if (quantity > 0) else "")
                    )

                    if len(response) + len(response_part) > 1492:
                        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                        response = ""

                    response += response_part

            if ewutils.active_trades.get(trade_partner.id_user).get("state") == ewcfg.trade_state_complete:
                response_part = '**They are ready to complete the trade.**'

                if len(response) + len(response_part) > 1492:
                    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                    response = ""

                response += response_part

            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    else:
        if cmd.mentions_count == 0:
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Who do you want to trade with?"))

        if cmd.mentions_count > 1:
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You can only trade with one person at a time."))

        trade_partner = EwUser(member=cmd.mentions[0])

        if user_data.id_user == trade_partner.id_user:
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Huh?"))

        if user_data.poi != trade_partner.poi:
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You must be in the same location as someone to trade with them."))

        if ewutils.active_trades.get(trade_partner.id_user) != None and len(ewutils.active_trades.get(trade_partner.id_user)) > 0:
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Wait for them to finish their business before trying to trade with them."))

        ewutils.active_trades[user_data.id_user] = {"state": ewcfg.trade_state_proposed, "trader": trade_partner.id_user}
        ewutils.active_trades[trade_partner.id_user] = {"state": ewcfg.trade_state_proposed, "trader": user_data.id_user}

        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.mentions[0], "{user} wants to trade with you. Do you {accept} or {refuse}?".format(user=cmd.message.author.display_name, accept=ewcfg.cmd_accept, refuse=ewcfg.cmd_refuse)))

        accepted = False

        try:
            member = cmd.mentions[0]
            msg = await cmd.client.wait_for('message', timeout = 30, check=lambda message: message.author == member and
                                                    message.content.lower() in [ewcfg.cmd_accept, ewcfg.cmd_refuse])

            if msg != None and msg.content.lower() == ewcfg.cmd_accept:
                accepted = True
        except:
            accepted = False

        if accepted:
            ewutils.active_trades[user_data.id_user] = {"state": ewcfg.trade_state_ongoing, "trader": trade_partner.id_user}
            ewutils.active_trades[trade_partner.id_user] = {"state": ewcfg.trade_state_ongoing, "trader": user_data.id_user}

            ewutils.trading_offers[user_data.id_user] = []

            ewutils.trading_offers[trade_partner.id_user] = []

            response = "You both head into a shady alleyway nearby to conduct your business."

        else:
            ewutils.active_trades[user_data.id_user] = {}
            ewutils.active_trades[trade_partner.id_user] = {}
            response = "They didn't respond in time."

        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def offer_item(cmd):
    user_data = EwUser(member=cmd.message.author)

    user_trade = ewutils.active_trades.get(user_data.id_user)

    if user_trade != None and len(user_trade) > 0 and user_trade.get("state") > ewcfg.trade_state_proposed:
        item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])

        try:
            item_id_int = int(item_search)
        except:
            item_id_int = None

        if item_search != None and len(item_search) > 0:
            item_sought = None

            inventory = bknd_item.inventory(
                id_user=user_data.id_user,
                id_server=user_data.id_server
            )

            for item in inventory:
                if (item.get('id_item') == item_id_int or item_search in ewutils.flattenTokenListToString(item.get('name'))) \
                    and item not in ewutils.trading_offers.get(user_data.id_user):
                    item_sought = item

            if item_sought:
                item = EwItem(id_item=item_sought.get("id_item"))

                if not item.soulbound or EwItem(id_item = item_sought.get('id_item')).item_props.get("context") == "housekey":

                    if item.id_item == user_data.weapon and user_data.weaponmarried:
                        response = "Unfortunately for you, the contract you signed before won't let you trade your partner away. You'll have to get your cuckoldry fix from somewhere else."
                        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

                    ewutils.trading_offers[user_data.id_user].append(item_sought)
                    response = "You add a {} to your offers.".format(item_sought.get("name"))

                    user_trade["state"] = ewcfg.trade_state_ongoing
                    ewutils.active_trades.get(user_trade.get("trader"))["state"] = ewcfg.trade_state_ongoing

                else:
                    response = "You can't trade soulbound items."
            else:
                if item_search:
                    response = "You don't have one."
        else:
            response = "Offer which item? (check **!inventory**)"
    else:
        response = "You need to be trading with someone to offer an item."

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def remove_offer(cmd):
    user_data = EwUser(member=cmd.message.author)

    user_trade = ewutils.active_trades.get(user_data.id_user)

    if user_trade != None and len(user_trade) > 0 and user_trade.get("state") > ewcfg.trade_state_proposed:
        item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])

        try:
            item_id_int = int(item_search)
        except:
            item_id_int = None

        if item_search != None and len(item_search) > 0:
            item_sought = None

            inventory = bknd_item.inventory(
                id_user=user_data.id_user,
                id_server=user_data.id_server
            )

            for item in inventory:
                if (item.get('id_item') == item_id_int or item_search in ewutils.flattenTokenListToString(item.get('name'))) \
                    and item in ewutils.trading_offers.get(user_data.id_user):
                    item_sought = item

            if item_sought:
                item = EwItem(id_item=item_sought.get("id_item"))

                ewutils.trading_offers[user_data.id_user].remove(item_sought)
                response = "You remove {} from your offers.".format(item_sought.get("name"))

                user_trade["state"] = ewcfg.trade_state_ongoing
                ewutils.active_trades.get(user_trade.get("trader"))["state"] = ewcfg.trade_state_ongoing

            else:
                if item_search:
                    response = "You don't have one."
        else:
            response = "Remove which offer? (check **!trade**)"
    else:
        response = "You need to be trading with someone to remove an offer."

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def complete_trade(cmd):
    user_data = EwUser(member=cmd.message.author)

    user_trade = ewutils.active_trades.get(user_data.id_user)

    if user_trade != None and len(user_trade) > 0 and user_trade.get("state") > ewcfg.trade_state_proposed:
        user_trade["state"] = ewcfg.trade_state_complete

        trader_id = user_trade.get("trader")
        if ewutils.active_trades.get(trader_id).get("state") != ewcfg.trade_state_complete:
            partner_player = EwPlayer(id_user=trader_id, id_server=user_data.id_server)
            response = "You tell {} that you're ready to finish the trade.".format(partner_player.display_name)

        else:
            trade_partner = EwUser(id_user=trader_id, id_server=user_data.id_server)

            #items this player is offering
            items_offered = {}

            #items the other player is offering
            trader_items_offered = {}

            for item in ewutils.trading_offers.get(user_data.id_user):
                if items_offered.get(item.get("item_type")) != None:
                    items_offered[item.get("item_type")] += 1
                else:
                    items_offered[item.get("item_type")] = 1

            for item in ewutils.trading_offers.get(trade_partner.id_user):
                if trader_items_offered.get(item.get("item_type")) != None:
                    trader_items_offered[item.get("item_type")] += 1
                else:
                    trader_items_offered[item.get("item_type")] = 1

            # check items currently held + items being given to the player - items the player is giving
            # check other user's inventory capacity
            trader_data = EwUser(id_user=trader_id, id_server=cmd.guild.id)
            for item_type in items_offered:

                inv_response = bknd_item.check_inv_capacity(user_data=trader_data, item_type=item_type, return_strings=True, pronoun='They', items_added=(items_offered[item_type] - trader_items_offered.get(item_type, 0)))
                if inv_response != "":
                    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, inv_response))

            # check own user's inventory capacity
            for item_type in trader_items_offered:
                inv_response = bknd_item.check_inv_capacity(user_data=user_data, item_type=item_type, return_strings=True, pronoun='You', items_added=(trader_items_offered.get(item_type) - items_offered.get(item_type, 0)))
                if inv_response != "":
                    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, inv_response))




            for item in list(ewutils.trading_offers.get(user_data.id_user)):
                if item.get("id_item") == user_data.weapon:
                    user_data.weapon = -1
                    user_data.persist()
                elif item.get("id_item") == user_data.sidearm:
                    user_data.sidearm = -1
                    user_data.persist()
                elif item.get("item_type") == ewcfg.it_cosmetic:
                    cosmetic = EwItem(id_item=item.get("id_item"))
                    cosmetic.item_props["adorned"] = 'false'
                    cosmetic.item_props["slimeoid"] = 'false'
                    cosmetic.persist()

                bknd_item.give_item(id_item=item.get("id_item"), id_user=trade_partner.id_user, id_server=trade_partner.id_server)

            for item in list(ewutils.trading_offers.get(trade_partner.id_user)):
                if item.get("id_item") == trade_partner.weapon:
                    trade_partner.weapon = -1
                    trade_partner.persist()
                elif item.get("id_item") == trade_partner.sidearm:
                    trade_partner.sidearm = -1
                    user_data.persist()
                elif item.get("item_type") == ewcfg.it_cosmetic:
                    cosmetic = EwItem(id_item=item.get("id_item"))
                    cosmetic.item_props["adorned"] = 'false'
                    cosmetic.item_props["slimeoid"] = 'false'
                    cosmetic.persist()

                bknd_item.give_item(id_item=item.get("id_item"), id_user=user_data.id_user, id_server=user_data.id_server)

            ewutils.active_trades[user_data.id_user] = {}
            ewutils.active_trades[trade_partner.id_user] = {}

            ewutils.trading_offers[user_data.id_user] = []
            ewutils.trading_offers[trade_partner.id_user] = []

            response = "You shake hands to commemorate another successful deal. That is their hand, right?"
    else:
        response = "You're not trading with anyone right now."

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def cancel_trade(cmd):
    user_trade = ewutils.active_trades.get(cmd.message.author.id)

    if user_trade != None and len(user_trade) > 0 and user_trade.get("state") > ewcfg.trade_state_proposed:
        ewutils.end_trade(cmd.message.author.id)
        response = "With your finely attuned business senses you realize they're trying to scam you and immediately call off the deal."
    else:
        response = "You're not trading with anyone right now."

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def bazaar_refresh(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return
    ewutils.logMsg(f"{cmd.message.author.display_name} force refreshed the bazaar.")
    await market_utils.refresh_bazaar(id_server=cmd.guild.id)


async def set_stock_value(cmd):
    """ Update a stock's exchange rate. """
    if not cmd.message.author.guild_permissions.administrator:
        return

    stock = None
    stock_new_value = None

    if len(cmd.tokens) >= 3:
        search_stock = cmd.tokens[1]
        if str.isnumeric(cmd.tokens[2]):
            stock_new_value = cmd.tokens[2]
        if search_stock in ewcfg.stocks:
            stock = EwStock(id_server=cmd.message.guild.id, stock=search_stock)
        else:
            return await fe_utils.send_response(f"Unrecognised stock. Try: {ewcfg.stocks}.", cmd)

    if stock is not None and stock_new_value is not None:
        old_value = stock.exchange_rate
        stock.exchange_rate = stock_new_value
        stock.timestamp = int(time.time())
        stock.persist()
        return await fe_utils.send_response(f"Updated {cmd.tokens[1]}'s stock value to be {stock_new_value} per 1000 shares instead of {old_value} per 1000.", cmd)
    else:
        return await fe_utils.send_response(f"Incorrect syntax. It's {cmd.tokens[0]} <stock_name> <new_rate>.", cmd)


async def set_stock_shares(cmd):
    """ Set a player's holdings of a certain stock to a certain quantity. """
    if not cmd.message.author.guild_permissions.administrator:
        return

    member = None
    stock = None
    stock_amount = None

    if len(cmd.tokens) >= 3:
        member = cmd.mentions[0]
        stock = cmd.tokens[2]
        if stock not in ewcfg.stocks:
            return await fe_utils.send_response(f"Unrecognised stock. Try: {ewcfg.stocks}.", cmd)
        if str.isnumeric(cmd.tokens[3]):
            stock_amount = cmd.tokens[3]

    if member and stock and stock_amount:
        old_holdings = market_utils.getUserTotalShares(id_server=cmd.message.guild.id, stock=stock, id_user=member.id)
        market_utils.updateUserTotalShares(id_server=cmd.message.guild.id, stock=stock, id_user=member.id, shares=stock_amount)

        return await fe_utils.send_response(f"Updated {member.display_name}'s holdings of {stock} stock from {old_holdings} to {stock_amount}.", cmd)
    else:
        return await fe_utils.send_response(f"Incorrect syntax. It's {cmd.tokens[0]} @user <stock_name> <share_amount>.", cmd)
