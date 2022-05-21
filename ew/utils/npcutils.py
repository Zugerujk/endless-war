from ew.static import hunting as static_hunt
from ew.utils import frontend as fe_utils
import random
from ew.static import cfg as ewcfg

async def generic_npc_action(keyword = '', enemy = None, channel = None):
    npc_obj = static_hunt.active_npcs_map.get(enemy.enemyclass)

    if keyword == 'move':
        return await generic_move(enemy=enemy)
    elif keyword == 'act':
        pass
    elif keyword == 'talk':
        return await generic_talk(channel=channel, npc_obj=npc_obj)

async def generic_talk(channel, npc_obj):

    response = random.choice(npc_obj.dialogue.get('talk'))
    name = "{}{}{}".format('**__', npc_obj.str_name.upper(), '__**')
    return await fe_utils.talk_bubble(response=response, name=name, image=npc_obj.id_profile, channel=channel)

async def generic_move(enemy = None):
    if enemy.life_state == ewcfg.enemy_lifestate_alive:
        if random.randrange(20) == 0:
            resp_cont = enemy.move()
            if resp_cont != None:
                await resp_cont.post(delete_after=120)

async def generic_act(channel, npc_obj, enemy):
    enemy_statuses = enemy.getStatusEffects()

    if ewcfg.status_enemy_hostile_id in enemy_statuses:
        resp_cont = await enemy.kill()
    elif any([ewcfg.status_evasive_id, ewcfg.status_aiming_id]) not in enemy_statuses and random.randrange(10) == 0:
        resp_cont = random.choice([enemy.dodge, enemy.taunt, enemy.aim])()
    else:
        response = random.choice(npc_obj.dialogue.get('act'))
        if response is None:
            response = random.choice(npc_obj.dialogue.get('talk'))

        name = "{}{}{}".format("*__", npc_obj.str_name.upper(), "__*"),

        return await fe_utils.talk_bubble(response=response, name=name, image=npc_obj.image_profile, channel=channel)

    await resp_cont.post()