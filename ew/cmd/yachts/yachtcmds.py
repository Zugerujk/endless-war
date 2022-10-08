from ew.utils.combat import EwUser
from ew.utils import frontend as fe_utils
import ew.static.cfg as ewcfg
from ew.backend.yacht import EwYacht

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
        accepted = await fe_utils.prompt(cmd=cmd, target = cmd.message.author, question = "", wait_time = 30, accept_command = 'accept', decline_command = 'refuse', checktarget = False)

        if accepted:
            user_data.change_slimecoin(n=-ewcfg.yachtprice, coinsource=ewcfg.coinsource_spending)
            user_data.persist()
            thread_id = 0 #todo learn thread creation and assign ship ID to thread ID
            yacht = EwYacht(id_server=cmd.guild.id, id_yacht=None)
            yacht.id_yacht = thread_id
            yacht.owner = cmd.message.author.id
            yacht.xcoord = 26
            yacht.ycoord = 5
            yacht.yacht_name = name
            yacht.thread_id = thread_id
            yacht.persist()
            response = "I christen ye: The S.S. {}!".format(name)
            return await fe_utils.talk_bubble(response=response, name="**__SMITTY ALEXANDER__**", channel=cmd.message.channel, image="https://rfck.app/img/npc/albertalex.png")
