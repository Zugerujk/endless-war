from ew.static import cfg as ewcfg
from ew.utils import frontend as fe_utils


# Returns a user's life state/gang color as a discord.Colour object
def get_tweet_color(user_data):
    if user_data.life_state < 2:
        color = ewcfg.tweet_color_by_lifestate.get(user_data.life_state)
    else:
        color = ewcfg.tweet_color_by_faction.get(user_data.faction)

    if color is None:
        color = None
    else:
        color = fe_utils.discord.Colour(int(color, 16))

    return color


# Returns a discord embed formatted like a slime tweet.
def format_generic_tweet(author, 
                         tweet_content, 
                         profile = "https://archive.org/download/discordprofilepictures/discordblue.png", 
                         checkmark = False, 
                         embed_color = ewcfg.tweet_color_by_lifestate[ewcfg.life_state_juvenile], 
                         attachment = "",):
    # Create the embed
    tweet = fe_utils.discord.Embed()

    # Format the embed
    tweet.set_thumbnail(url=profile)
    tweet.description = "{author}{checkmark}".format(author=author, checkmark=ewcfg.emote_verified if checkmark else "")
    tweet.color = embed_color
    tweet.add_field(name='\u200b', value=tweet_content)

    # Add the attachment
    if attachment != "":
        print("fart")
        tweet.set_image(url=attachment)

    return tweet


# Returns a discord embed formatted like a slime tweet, with properties autofilled.
def format_player_tweet(cmd, user_data, content=""):
    
    profile = cmd.message.author.display_avatar.url  # PFP
    author =  "<@!{}>".format(cmd.message.author.id)  # User
    checkmark = True if user_data.verified else False  # Verification
    tweet_content = content  # Content of tweet
    embed_color = get_tweet_color(user_data)  # Embed color

    attachment = ""
    if len(cmd.message.attachments) > 0:
        attachment = cmd.message.attachments[0].url

    return format_generic_tweet(profile=profile, author=author, checkmark=checkmark, tweet_content=tweet_content, embed_color=embed_color, attachment=attachment)


