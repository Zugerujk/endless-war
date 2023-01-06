import random
import time
import math

from ew.backend import item as bknd_item
from ew.backend.farm import EwFarm
from ew.backend.item import EwItem
from ew.backend.market import EwMarket
from ew.static import cfg as ewcfg
from ew.static import farm as farm_static
from ew.static import food as static_food
from ew.static import poi as poi_static
from ew.static import items as static_items
from ew.static import vendors
from ew.static import weapons as static_weapons
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import item as itm_utils
from ew.utils import poi as poi_utils
from ew.utils import rolemgr as ewrolemgr
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict
from ew.utils.slimeoid import EwSlimeoid
from ew.utils.user import add_xp



""" Sow seeds that may eventually be !reaped. """


async def sow(cmd):
    user_data = EwUser(member=cmd.message.author)

    # check if the user has a farming tool equipped
    weapon_item = EwItem(id_item=user_data.weapon)
    weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))
    has_tool = False
    if weapon is not None:
        if ewcfg.weapon_class_farming in weapon.classes:
            has_tool = True

    # Checking availability of sow action
    if user_data.life_state != ewcfg.life_state_juvenile:
        response = "Only Juveniles of pure heart and with nothing better to do can farm."

    elif cmd.message.channel.name not in [ewcfg.channel_jr_farms, ewcfg.channel_og_farms, ewcfg.channel_ab_farms]:
        response = "The cracked, filthy concrete streets around you would be a pretty terrible place for a farm. Try again on more arable land."

    else:

        if user_data.poi == ewcfg.poi_id_jr_farms:
            farm_id = ewcfg.poi_id_jr_farms
        elif user_data.poi == ewcfg.poi_id_og_farms:
            farm_id = ewcfg.poi_id_og_farms
        else:  # if it's the farm in arsonbrook
            farm_id = ewcfg.poi_id_ab_farms

        farm = EwFarm(
            id_server=cmd.guild.id,
            id_user=cmd.message.author.id,
            farm=farm_id
        )

        if farm.time_lastsow > 0:
            response = "You’ve already sown something here. Try planting in another farming location. If you’ve planted in all three farming locations, you’re shit out of luck. Just wait, asshole."
        else:
            it_type_filter = None

            # gangsters can only plant poudrins
            if cmd.tokens_count > 1 and user_data.life_state == ewcfg.life_state_juvenile:
                item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])

                # if the item selected was a vegetable, use a food only filter in find_item
                for v in static_food.vegetable_list:
                    if item_search in v.id_food or item_search in v.str_name:
                        it_type_filter = ewcfg.it_food
                        break
            else:
                item_search = "slimepoudrin"

            item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None, item_type_filter=it_type_filter)

            if item_sought == None:
                response = "You don't have anything to plant! Try collecting a poudrin."
            else:
                is_item = False
                slimes_onreap = ewcfg.reap_gain
                item_data = EwItem(id_item=item_sought.get("id_item"))
                if item_data.item_type == ewcfg.it_item:
                    if item_data.item_props.get("id_item") == ewcfg.item_id_slimepoudrin:
                        vegetable = random.choice(static_food.vegetable_list)
                        slimes_onreap *= 2
                    elif item_data.item_props.get("context") == ewcfg.context_slimeoidheart:
                        vegetable = random.choice(static_food.vegetable_list)
                        slimes_onreap *= 2

                        slimeoid_data = EwSlimeoid(id_slimeoid=item_data.item_props.get("subcontext"))
                        slimeoid_data.delete()

                    else:
                        response = "The soil has enough toxins without you burying your trash here."
                        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                elif item_data.item_type == ewcfg.it_food:
                    food_id = item_data.item_props.get("id_food")
                    vegetable = static_food.food_map.get(food_id)
                    if ewcfg.vendor_farm not in vegetable.vendors:
                        response = "It sure would be nice if {}s grew on trees, but alas they do not. Idiot.".format(item_sought.get("name"))
                        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                    elif user_data.life_state != ewcfg.life_state_juvenile:
                        response = "You lack the knowledge required to grow {}.".format(item_sought.get("name"))
                        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

                elif item_data.item_type == ewcfg.it_cosmetic:
                    if item_data.item_props['id_cosmetic'] == 'scalp':
                        vegetable = static_items.item_map.get('evilstuds')
                        slimes_onreap *= 0.25
                        is_item = True
                    else:
                        response = "The soil has enough toxins without you burying your trash here."
                        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

                else:
                    response = "The soil has enough toxins without you burying your trash here."
                    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

                mutations = user_data.get_mutations()
                growth_time = ewcfg.crops_time_to_grow
                if user_data.life_state == ewcfg.life_state_juvenile: 
                    growth_time /= 2
                if ewcfg.mutation_id_greenfingers in mutations:
                    growth_time /= 1.5
              
                hours = int(growth_time / 60)
                minutes = int(growth_time % 60)

                str_growth_time = "{} hour{}{}".format(hours, "s" if hours > 1 else "", " and {} minutes".format(minutes) if minutes > 0 else "")

                # Sowing
                response = "You sow a {} into the fertile soil beneath you. It will grow in about {}.".format(item_sought.get("name"), str_growth_time)

                farm.time_lastsow = int(time.time() / 60)  # Grow time is stored in minutes.
                farm.time_lastphase = int(time.time())
                farm.slimes_onreap = slimes_onreap
                farm.phase = ewcfg.farm_phase_sow
                farm.action_required = ewcfg.farm_action_none
                farm.sow_life_state = user_data.life_state
                if is_item:
                    farm.crop = vegetable.id_item
                else:
                    farm.crop = vegetable.id_food
                if ewcfg.mutation_id_greenfingers in mutations:
                    if user_data.life_state == ewcfg.life_state_juvenile:
                        farm.sow_life_state = ewcfg.farm_life_state_juviethumb
                    else:
                        farm.sow_life_state = ewcfg.farm_life_state_thumb

                bknd_item.item_delete(id_item=item_sought.get('id_item'))  # Remove Poudrins

                farm.persist()

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" Reap planted crops. """


async def reap(cmd):
    user_data = EwUser(member=cmd.message.author)

    forcereap = False
    if cmd.tokens[0] == ewcfg.cmd_reap_alt:
        if cmd.message.author.guild_permissions.administrator:
            forcereap = True
        else:
            return

    response, responses = "", []
    levelup_response = ""
    mutations = user_data.get_mutations()
    poi = poi_static.id_to_poi.get(user_data.poi)

    # check if the user has a farming tool equipped
    weapon_item = EwItem(id_item=user_data.weapon)
    weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))
    has_tool = False
    if weapon is not None:
        if ewcfg.weapon_class_farming in weapon.classes:
            has_tool = True

    # Checking availability of reap action
    if user_data.life_state != ewcfg.life_state_juvenile:
        response = "Only Juveniles of pure heart and with nothing better to do can farm."
    elif cmd.message.channel.name not in [ewcfg.channel_jr_farms, ewcfg.channel_og_farms, ewcfg.channel_ab_farms]:
        response = "Do you remember planting anything here in this barren wasteland? No, you don’t. Idiot."
    else:

        if user_data.poi == ewcfg.poi_id_jr_farms:
            farm_id = ewcfg.poi_id_jr_farms
        elif user_data.poi == ewcfg.poi_id_og_farms:
            farm_id = ewcfg.poi_id_og_farms
        else:  # if it's the farm in arsonbrook
            farm_id = ewcfg.poi_id_ab_farms

        farm = EwFarm(
            id_server=cmd.guild.id,
            id_user=cmd.message.author.id,
            farm=farm_id
        )

        if farm.time_lastsow == 0:
            response = "You missed a step, you haven’t planted anything here yet."
        else:
            cur_time_min = time.time() / 60
            time_grown = cur_time_min - farm.time_lastsow

            if farm.phase != ewcfg.farm_phase_reap and not forcereap:
                response = "Patience is a virtue and you are morally bankrupt. Just wait, asshole."
            else:  # Reaping
                if (time_grown > ewcfg.crops_time_to_grow * 16) and not (forcereap == True or ewcfg.mutation_id_monplanto in mutations):  # about 2 days
                    response = "You eagerly cultivate your crop, but what’s this? It’s dead and wilted! It seems as though you’ve let it lay fallow for far too long. Pay better attention to your farm next time. You gain no slime."
                    farm.time_lastsow = 0  # 0 means no seeds are currently planted
                    farm.persist()
                else:
                    user_initial_level = user_data.slimelevel

                    slime_gain = farm.slimes_onreap
                    crop_gain = 0

                    controlling_faction = poi_utils.get_subzone_controlling_faction(user_data.poi, user_data.id_server)

                    if controlling_faction != "" and controlling_faction == user_data.faction:
                        slime_gain *= 2

                    if has_tool and weapon.id_weapon == ewcfg.weapon_id_hoe:
                        slime_gain *= 1.5

                    if has_tool and weapon.id_weapon == ewcfg.weapon_id_slimeringcan:
                        slime_gain *= 0.5

                    if ewcfg.mutation_id_greenfingers in mutations:
                        slime_gain *= 1.2

                    if user_data.poi == ewcfg.poi_id_jr_farms:
                        slime_gain = int(slime_gain / 4)

                    slime_gain = max(0, round(slime_gain))

                    response = "You reap what you’ve sown. Your investment has yielded {:,} slime, ".format(slime_gain)

                    # Determine if an item is found.
                    unearthed_item = False
                    unearthed_item_amount = 0

                    unearthed_item_chance = 50 / ewcfg.unearthed_item_rarity  # 1 in 30 chance

                    if ewcfg.mutation_id_lucky in mutations:
                        unearthed_item_chance *= 1.777   # 1 in ~17 chance

                    if has_tool and weapon.id_weapon == ewcfg.weapon_id_shovel:   # 1 in 6 chance
                        unearthed_item_chance *= 5

                    if random.random() < unearthed_item_chance:
                        unearthed_item = True
                        unearthed_item_amount = random.randint(1,4)

                    if unearthed_item == True:
                        item = random.choice(vendors.mine_results)
                        if has_tool and weapon.id_weapon == ewcfg.weapon_id_shovel:
                            # If there are multiple possible products, randomly select one.
                            # shovel buff item table
                            shovel_table = [
                            ewcfg.item_id_stick,
                            ewcfg.item_id_landmine,
                            ewcfg.item_id_oldboot,
                            ewcfg.item_id_tincan,]
                            item = static_items.item_map.get(random.choice(shovel_table))

                        item_props = itm_utils.gen_item_props(item)

                        if item is not None:

                            for creation in range(unearthed_item_amount):
                                bknd_item.item_create(
                                    item_type=item.item_type,
                                    id_user=cmd.message.author.id,
                                    id_server=cmd.guild.id,
                                    item_props=item_props
                                )

                        if unearthed_item_amount == 1:
                            response += "a {}, ".format(item.str_name)
                        elif unearthed_item_amount >= 2:
                            response += "{} {}s, ".format(unearthed_item_amount, item.str_name)

                    #  Determine what crop is grown.
                    if farm.crop == ewcfg.item_id_evil_material:
                        vegetable = static_items.item_map.get(farm.crop)
                    else:
                        vegetable = static_food.food_map.get(farm.crop)
                        
                    if vegetable is None:
                        vegetable = random.choice(static_food.vegetable_list)

                    item_props = itm_utils.gen_item_props(vegetable)

                    #  Create and give a bushel of whatever crop was grown, unless it's a metal crop.
                    if item_props.get('id_food') in [ewcfg.item_id_metallicaps, ewcfg.item_id_steelbeans, ewcfg.item_id_aushucks]:
                        metallic_crop_ammount = 1
                        if random.randrange(10) == 0:
                            metallic_crop_ammount = 5 if random.randrange(2) == 0 else 6

                        if has_tool and weapon.id_weapon == ewcfg.weapon_id_pitchfork:
                            metallic_crop_ammount *= 2
                        elif has_tool and weapon.id_weapon == ewcfg.weapon_id_slimeringcan:
                            metallic_crop_ammount = 0 

                        crop_gain = metallic_crop_ammount * 3

                        if metallic_crop_ammount > 0:
                            
                            for vcreate in range(metallic_crop_ammount):
                                bknd_item.item_create(
                                    id_user=cmd.message.author.id,
                                    id_server=cmd.guild.id,
                                    item_type=vegetable.item_type,
                                    item_props=item_props
                                )
                            if metallic_crop_ammount == 1:
                                response += "and a single {}!".format(vegetable.str_name)
                            else:
                                response += "and a bushel of {} {}!".format(metallic_crop_ammount,vegetable.str_name)
                        else:
                            poudrin_gain = random.randint(5,8)
                            item = random.choice(vendors.mine_results)
                            item_props = itm_utils.gen_item_props(item)
                            for vcreate in range(poudrin_gain):
                                bknd_item.item_create(
                                    id_user=cmd.message.author.id,
                                    id_server=cmd.guild.id,
                                    item_type=item.item_type,
                                    item_props=item_props
                                )
                            response += "\nThe {} collapses on the ground, having no structural support to even call it anything more than gunk. You got {} Slime Poudrins in trying, though.".format(vegetable.str_name, poudrin_gain)
                    
                    # if random.randrange(10) == 0:
                    # 	for vcreate in range(6):
                    # 		bknd_item.item_create(
                    # 			id_user=cmd.message.author.id,
                    # 			id_server=cmd.guild.id,
                    # 			item_type=vegetable.item_type,
                    # 			item_props=item_props
                    # 		)
                    #
                    # 	response += "and a bushel of {}!".format(vegetable.str_name)
                    # else:

                    # 	response += "and a bushel of... hey, what the hell! You didn't reap anything! Must've been some odd seeds..."
                    else:
                        unearthed_vegetable_amount = 3
                        if has_tool and weapon.id_weapon == ewcfg.weapon_id_pitchfork:
                            unearthed_vegetable_amount *= 2
                        elif has_tool and weapon.id_weapon == ewcfg.weapon_id_slimeringcan:
                            unearthed_vegetable_amount = 0

                        crop_gain = unearthed_vegetable_amount

                        if unearthed_vegetable_amount > 0:
                            for vcreate in range(unearthed_vegetable_amount):
                                bknd_item.item_create(
                                    id_user=cmd.message.author.id,
                                    id_server=cmd.guild.id,
                                    item_type=vegetable.item_type,
                                    item_props=item_props
                                )
                            if unearthed_vegetable_amount == 1:
                                response += "and a single {}!".format(vegetable.str_name)
                            else:
                                response += "and a bushel of {} {}!".format(unearthed_vegetable_amount,vegetable.str_name)
                        else:
                            poudrin_gain = random.randint(5,8)
                            item = random.choice(vendors.mine_results)
                            item_props = itm_utils.gen_item_props(item)
                            for vcreate in range(poudrin_gain):
                                bknd_item.item_create(
                                    id_user=cmd.message.author.id,
                                    id_server=cmd.guild.id,
                                    item_type=item.item_type,
                                    item_props=item_props
                                )
                            response += "\nThe {} collapses on the ground, having no structural support to even call it anything more than gunk. You got {} Slime Poudrins in trying, though.".format(vegetable.str_name, poudrin_gain)

                    levelup_response = user_data.change_slimes(n=slime_gain, source=ewcfg.source_farming)

                    was_levelup = True if user_initial_level < user_data.slimelevel else False

                    # Tell the player their slime level increased.
                    if was_levelup:
                        response += "\n\n" + levelup_response

                    user_data.hunger += ewcfg.hunger_perfarm
                    user_data.persist()

                    farm.time_lastsow = 0  # 0 means no seeds are currently planted
                    farm.persist()

                    #Goonscape Stat
                    xp_slime = round(slime_gain * 0.0230)
                    xp_crop = crop_gain * 1840

                    xp_yield = xp_slime + xp_crop
                    responses = await add_xp(cmd.message.author.id, cmd.message.guild.id, ewcfg.goonscape_farm_stat, xp_yield)

    respctn = fe_utils.EwResponseContainer(client=cmd.client, id_server=cmd.message.guild.id)
    respctn.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    for resp in responses: respctn.add_channel_response(cmd.message.channel, resp)
    await respctn.post()


async def check_farm(cmd):
    user_data = EwUser(member=cmd.message.author)

    response = ""
    levelup_response = ""
    mutations = user_data.get_mutations()

    # Checking availability of check farm action
    if user_data.life_state != ewcfg.life_state_juvenile:
        response = "Only Juveniles of pure heart and with nothing better to do can farm."
    elif cmd.message.channel.name not in [ewcfg.channel_jr_farms, ewcfg.channel_og_farms, ewcfg.channel_ab_farms]:
        response = "Do you remember planting anything here in this barren wasteland? No, you don’t. Idiot."
    else:
        if user_data.poi == ewcfg.poi_id_jr_farms:
            farm_id = ewcfg.poi_id_jr_farms
        elif user_data.poi == ewcfg.poi_id_og_farms:
            farm_id = ewcfg.poi_id_og_farms
        else:  # if it's the farm in arsonbrook
            farm_id = ewcfg.poi_id_ab_farms

        farm = EwFarm(
            id_server=cmd.guild.id,
            id_user=cmd.message.author.id,
            farm=farm_id
        )

        if farm.time_lastsow == 0:
            response = "You missed a step, you haven’t planted anything here yet."
        elif farm.action_required == ewcfg.farm_action_none:
            if farm.phase == ewcfg.farm_phase_reap:
                response = "Your crop is ready for the harvest."
            elif farm.phase == ewcfg.farm_phase_sow:
                response = "You only just planted the seeds. Check back later."
            else:
                if farm.slimes_onreap < ewcfg.reap_gain:
                    response = "Your crop looks frail and weak."
                elif farm.slimes_onreap < ewcfg.reap_gain + 3 * ewcfg.farm_slimes_peraction:
                    response = "Your crop looks small and generally unremarkable."
                elif farm.slimes_onreap < ewcfg.reap_gain + 6 * ewcfg.farm_slimes_peraction:
                    response = "Your crop seems to be growing well."
                else:
                    response = "Your crop looks powerful and bursting with nutrients."

        else:
            farm_action = farm_static.id_to_farm_action.get(farm.action_required)
            response = farm_action.str_check

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def cultivate(cmd):
    user_data = EwUser(member=cmd.message.author)

    response, responses = "", []
    levelup_response = ""
    mutations = user_data.get_mutations()

    # Checking availability of irrigate action

    if cmd.message.channel.name not in [ewcfg.channel_jr_farms, ewcfg.channel_og_farms, ewcfg.channel_ab_farms] and cmd.tokens[0].lower() == '!weed':
        rand1 = random.randrange(100)
        rand2 = random.randrange(5)
        response = ""
        if rand1 > 80:
            response = "**"
        for x in range(rand2 + 1):
            response += "Y"
        for x in range(rand2 + 1):
            response += "E"
        for x in range(rand2 + 1):
            response += "A"
        for x in range(rand2 + 1):
            response += "H"
        response += " BRO!"
        if rand1 > 80:
            response += "**"

    elif user_data.life_state != ewcfg.life_state_juvenile:
        response = "Only Juveniles of pure heart and with nothing better to do can tend to their crops."
    elif cmd.message.channel.name not in [ewcfg.channel_jr_farms, ewcfg.channel_og_farms, ewcfg.channel_ab_farms]:
        response = "Do you remember planting anything here in this barren wasteland? No, you don’t. Idiot."
    else:
        if user_data.poi == ewcfg.poi_id_jr_farms:
            farm_id = ewcfg.poi_id_jr_farms
        elif user_data.poi == ewcfg.poi_id_og_farms:
            farm_id = ewcfg.poi_id_og_farms
        else:  # if it's the farm in arsonbrook
            farm_id = ewcfg.poi_id_ab_farms

        farm = EwFarm(
            id_server=cmd.guild.id,
            id_user=cmd.message.author.id,
            farm=farm_id
        )

        farm_action = farm_static.cmd_to_farm_action.get(cmd.tokens[0].lower())

        if farm.time_lastsow == 0:
            response = "You missed a step, you haven’t planted anything here yet."
        elif farm.action_required != farm_action.id_action:
            response = farm_action.str_execute_fail
            farm.slimes_onreap -= ewcfg.farm_slimes_peraction
            farm.slimes_onreap = max(farm.slimes_onreap, 0)
            farm.persist()
        else:
            response = farm_action.str_execute
            # farm actions award more slime
            farm.slimes_onreap += ewcfg.farm_slimes_peraction * 2
            farm.action_required = ewcfg.farm_action_none
            farm.persist()
            xp_yield = 1150
            responses = await add_xp(cmd.message.author.id, cmd.message.guild.id, ewcfg.goonscape_farm_stat, xp_yield)

    respctn = fe_utils.EwResponseContainer(client=cmd.client, id_server=cmd.guild.id)
    respctn.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    for resp in responses: respctn.add_channel_response(cmd.message.channel, resp)
    return await respctn.post()


async def mill(cmd):
    user_data = EwUser(member=cmd.message.author)
    responses = []

    market_data = EwMarket(id_server=user_data.id_server)
    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None, item_type_filter=ewcfg.it_food)

    # Checking availability of milling
    if user_data.life_state != ewcfg.life_state_juvenile:
        response = "Only Juveniles of pure heart and with nothing better to do can mill their vegetables."
    elif cmd.message.channel.name not in [ewcfg.channel_jr_farms, ewcfg.channel_og_farms, ewcfg.channel_ab_farms]:
        response = "Alas, there doesn’t seem to be an official SlimeCorp milling station anywhere around here. Probably because you’re in the middle of the fucking city. Try looking where you reaped your vegetable in the first place, dumbass."

    # elif user_data.slimes < ewcfg.slimes_permill:
    # 	response = "It costs {} to !mill, and you only have {}.".format(ewcfg.slimes_permill, user_data.slimes)

    elif item_sought:
        items = []
        vegetable = EwItem(id_item=item_sought.get('id_item'))

        for result in vendors.mill_results:
            if type(result.ingredients) == str:
                if vegetable.item_props.get('id_food') != result.ingredients:
                    pass
                else:
                    items.append(result)
            elif type(result.ingredients) == list:
                if vegetable.item_props.get('id_food') not in result.ingredients:
                    pass
                else:
                    items.append(result)

        if len(items) > 0:
            item = random.choice(items)

            item_props = itm_utils.gen_item_props(item)

            bknd_item.item_create(
                item_type=item.item_type,
                id_user=cmd.message.author.id,
                id_server=cmd.guild.id,
                item_props=item_props
            )

            response = "You walk up to the official ~~SlimeCorp~~ Garden Gankers Milling Station and shove your irradiated produce into the hand-crank. You begin slowly churning them into a glorious, pastry goo. As the goo tosses and turns inside the machine, it solidifies, and after a few moments a {} pops out!".format(item.str_name)
            xp_yield = 1840
            responses = await add_xp(cmd.message.author.id, cmd.message.guild.id, ewcfg.goonscape_farm_stat, xp_yield)

            # market_data.donated_slimes += ewcfg.slimes_permill
            market_data.persist()

            bknd_item.item_delete(id_item=item_sought.get('id_item'))
            # user_data.change_slimes(n = -ewcfg.slimes_permill, source = ewcfg.source_spending)
            # user_data.slime_donations += ewcfg.slimes_permill
            user_data.persist()
        else:
            response = "You can only mill fresh vegetables! SlimeCorp obviously wants you to support local farmers."

    else:
        if item_search:  # if they didn't forget to specify an item and it just wasn't found
            response = "You don't have one."
        else:
            response = "Mill which item? (check **!inventory**)"

    respctn = fe_utils.EwResponseContainer(client=cmd.client, id_server=cmd.guild.id)
    respctn.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    for resp in responses: respctn.add_channel_response(cmd.message.channel, resp)
    return await respctn.post()
