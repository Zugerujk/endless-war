import time

from ew.static import cfg as ewcfg
from ew.utils import frontend as fe_utils
from ew.utils import stats as ewstats
from ew.utils import core as ewutils
from ew.utils.combat import EwUser
from ew.utils.user import add_xp

from .slimetwitterutils import format_player_tweet
from .slimetwitterutils import separate_id_from_slimetwitter_embed


async def tweet(cmd):
    user_data = EwUser(id_user=cmd.message.author.id, id_server=cmd.guild.id)

    if user_data.has_gellphone():

        if cmd.tokens_count < 2:
            if len(cmd.message.attachments) == 0:
                response = "Tweet what?"
                return await fe_utils.send_response(response, cmd)
            else:
                tweet_content = "\u200d"
        else:
            tweet_content = ' '.join("`{}`".format(token) if token.startswith("#") else token for token in cmd.tokens[1:])

        # embed limits
        if len(tweet_content) > 280:
            response = "Alright there bud, slow down a bit. No one's gonna read all that ({}/280).".format(len(tweet_content))
            return await fe_utils.send_response(response, cmd)

        tweet = format_player_tweet(cmd, user_data, tweet_content)

        channel = fe_utils.get_channel(server=cmd.guild, channel_name=ewcfg.channel_slimetwitter)

        fart = await fe_utils.send_message(cmd.client, channel, embed=tweet)
        await add_xp(cmd.message.author.id, cmd.guild.id, ewcfg.goonscape_clout_stat, 1300)
        
        if ewutils.DEBUG:
            await fart.add_reaction(ewcfg.emote_slimetwitter_like_debug)
            await fart.add_reaction(ewcfg.emote_slimetwitter_resplat_debug)
        else:
            await fart.add_reaction(ewcfg.emote_slimetwitter_like)
            await fart.add_reaction(ewcfg.emote_slimetwitter_resplat)




    else:
        response = "You need to have a gellphone to !tweet."
        return await fe_utils.send_response(response, cmd)


async def verification(cmd):
    user_data = EwUser(member=cmd.message.author)

    if user_data.poi == ewcfg.poi_id_slimecorphq:

        if user_data.verified:
            response = "*Huh? You're already verified! Get outta here you goofster!*"
            return await fe_utils.send_response(response, cmd)

        time_now = int(time.time())
        time_in_server = time_now - user_data.time_joined

        if time_in_server >= 60 * 60 * 24 * 180:  # 6 months

            lifetime_slime = ewstats.get_stat(user=user_data, metric=ewcfg.stat_lifetime_slimes)
            # you can use haunted slimes too cause we're nicer to ghosts than we should be
            lifetime_haunted = ewstats.get_stat(user=user_data, metric=ewcfg.stat_lifetime_slimeshaunted)

            if lifetime_slime > 1000000000 or lifetime_haunted > 100000000:

                user_data.verified = True
                user_data.persist()
                response = "*Alright, everything checks out. Congratulations, you're #verified now.*"  # TODO emote

            else:
                response = "*Yeah, sorry, looks but it like you don't love slime enough. Try getting some more slime, then come back. Freak.*"

                if user_data.life_state != ewcfg.life_state_corpse:
                    response += " ({current:,}/{needed:,} lifetime slime)".format(current=lifetime_slime, needed=1000000000)
                else:
                    response += " ({current:,}/{needed:,} lifetime slime haunted)".format(current=lifetime_haunted, needed=100000000)
        else:
            response = "*We can't just verify any random schmuck who wanders into our city, it'd be a bad look. Stick around for a while, then we'll consider verifying you.*"
    else:
        if user_data.poi == ewcfg.poi_id_stockexchange:
            response = "*Hey buddy, I think you got the wrong door, the HQ's two blocks down.*"
        else:
            response = "Only the Slimecorp employees at the HQ can get you verified on Slime Twitter."

    return await fe_utils.send_response(response, cmd)


async def quote_retweet(cmd):
    user_data = EwUser(id_user=cmd.message.author.id, id_server=cmd.guild.id)

    if user_data.has_gellphone():

        if cmd.tokens_count < 3:
            if cmd.tokens_count < 2:
                response = "You need to specify a message to resplat, dumbass. Use !quoteresplat <message id> <tweet>."
                return await fe_utils.send_response(response, cmd)
            elif len(cmd.message.attachments) == 0:
                response = "Resplat what?"
                return await fe_utils.send_response(response, cmd)
            else:
                tweet_content = "\u200d"
        else:
            tweet_content = ' '.join("`{}`".format(token) if token.startswith("#") else token for token in cmd.tokens[2:])

        if len(tweet_content) > 280:
            response = "Alright there bud, slow down a bit. No one's gonna read all that ({}/280).".format(len(tweet_content))
            return await fe_utils.send_response(response, cmd)

        #  Make sure to sQRT amirite
        # Separate Tweeter's original ID
        slime_twitter = fe_utils.get_channel(cmd.guild, ewcfg.channel_slimetwitter)
        message_qrt_id = cmd.tokens[1]
        try:
            og_qrt_message = await slime_twitter.fetch_message(message_qrt_id)
            embed = og_qrt_message.embeds[0]
            og_user_id = separate_id_from_slimetwitter_embed(embed=embed)
        except:
            response = "There was an issue processing your resplat. Try !quoteresplat <message id> <tweet>."
            return await fe_utils.send_response(response, cmd)

        tweet_content = "<@!{}> {}".format(og_user_id, tweet_content)
        tweet = format_player_tweet(cmd, user_data, tweet_content)

        channel = fe_utils.get_channel(server=cmd.guild, channel_name=ewcfg.channel_slimetwitter)

        fart = await fe_utils.send_message(cmd.client, channel, embed=tweet, reference=og_qrt_message)
        await add_xp(cmd.message.author.id, cmd.guild.id, ewcfg.goonscape_clout_stat, 1300)

        if ewutils.DEBUG:
            await fart.add_reaction(ewcfg.emote_slimetwitter_like_debug)
            await fart.add_reaction(ewcfg.emote_slimetwitter_resplat_debug)
        else:
            await fart.add_reaction(ewcfg.emote_slimetwitter_like)
            await fart.add_reaction(ewcfg.emote_slimetwitter_resplat)
