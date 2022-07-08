from ew.static import hunting as static_hunt
from ew.utils import frontend as fe_utils
import random
from ew.static import cfg as ewcfg

#move: enemy move action
#talk: action on a !talk
#act: action every 3 seconds
#die: action when the enemy dies
#hit: action when the enemy gets hit

async def generic_npc_action(keyword = '', enemy = None, channel = None):
    npc_obj = static_hunt.active_npcs_map.get(enemy.enemyclass)

    if keyword == 'move':
        return await generic_move(enemy=enemy)
    elif keyword == 'act':
        return await generic_act(channel=channel, npc_obj=npc_obj, enemy=enemy)
    elif keyword == 'talk':
        return await generic_talk(channel=channel, npc_obj=npc_obj, enemy = enemy)
    elif keyword == 'hit':
        return await generic_hit(npc_obj=npc_obj, channel=channel, enemy=enemy)
    elif keyword == 'die':
        return await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='die', enemy = enemy)


async def chatty_npc_action(keyword = '', enemy = None, channel = None): #similar to the generic npc, but with loopable dialogue
    npc_obj = static_hunt.active_npcs_map.get(enemy.enemyclass)

    if keyword == 'move':
        return await generic_move(enemy=enemy)
    elif keyword == 'act':
        if random.randint(1, 5) == 2:
            return await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='loop', enemy = enemy)
    elif keyword == 'talk':
        return await generic_talk(channel=channel, npc_obj=npc_obj, enemy = enemy)
    elif keyword == 'hit':
        return await generic_hit(npc_obj=npc_obj, channel=channel, enemy=enemy)
    elif keyword == 'die':
        return await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='die', enemy = enemy)


async def generic_talk(channel, npc_obj, keyword_override = 'talk', enemy = None): #sends npc dialogue, including context specific and rare variants
    rare_keyword = "rare{}".format(keyword_override)
    location_keyword = '{}{}'.format(enemy.poi, keyword_override)

    if rare_keyword in npc_obj.dialogue.keys() and random.randint(1, 20) == 2:
        keyword_override = rare_keyword #rare dialogue has a 1 in 20 chance of firing

    potential_dialogue = npc_obj.dialogue.get(keyword_override)

    if location_keyword in npc_obj.dialogue.keys() and 'rare' not in keyword_override:
        potential_dialogue += npc_obj.dialogue.get(location_keyword)

    response = random.choice(potential_dialogue)
    name = "{}{}{}".format('**__', npc_obj.str_name.upper(), '__**')
    if response is not None:
        return await fe_utils.talk_bubble(response=response, name=name, image=npc_obj.id_profile, channel=channel)

async def generic_move(enemy = None): #moves within boundaries every 20 seconds or so
    if enemy.life_state == ewcfg.enemy_lifestate_alive:
        if random.randrange(20) == 0:
            resp_cont = enemy.move()
            if resp_cont != None:
                await resp_cont.post(delete_after=120)

async def generic_act(channel, npc_obj, enemy): #attacks when hostile. otherwise, if act or talk dialogue is available, the NPC will use it every so often.
    enemy_statuses = enemy.getStatusEffects()
    print('tick')
    if ewcfg.status_enemy_hostile_id in enemy_statuses:
        if any([ewcfg.status_evasive_id, ewcfg.status_aiming_id]) not in enemy_statuses and random.randrange(10) == 0:
            resp_cont = random.choice([enemy.dodge, enemy.taunt, enemy.aim])()
            print('aim')
        else:
            resp_cont = await enemy.kill()
            print('kill')

        if resp_cont is not None:
            await resp_cont.post()

    elif random.randrange(25) == 0:
        response = random.choice(npc_obj.dialogue.get('act'))
        if response is None:
            response = random.choice(npc_obj.dialogue.get('talk'))

        name = "{}{}{}".format("*__", npc_obj.str_name.upper(), "__*"),
        if response is not None:
            return await fe_utils.talk_bubble(response=response, name=name, image=npc_obj.image_profile, channel=channel)



async def generic_hit(channel, npc_obj, enemy, territorial = True, probability = 1): #territorial enemy that attacks when you do. if a line is prepared for it, talkbubble that line
    if ewcfg.status_enemy_hostile_id not in enemy.getStatusEffects() and territorial:
        enemy.applyStatus(id_status=ewcfg.status_enemy_hostile_id)
        await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='hit', enemy=enemy)
    else:
        if random.randint(1, probability) == 1:
            await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='hit', enemy=enemy)




