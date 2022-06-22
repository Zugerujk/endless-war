import asyncio
import random

from . import core as ewutils
from .combat import EwEnemy
from .combat import EwUser
from .district import EwDistrict
from .frontend import EwResponseContainer
from .slimeoid import EwSlimeoid
from ..backend import core as bknd_core
from ..backend import hunting as bknd_hunt
from ..backend import item as bknd_item
from ..backend import worldevent as bknd_worldevent
from ..backend.worldevent import EwWorldEvent
from ..backend.item import EwItem
from ..backend.market import EwMarket
from ..backend.player import EwPlayer
from ..static import cfg as ewcfg
from ..static import poi as poi_static
from ..static import weather as weather_static
from ..utils import frontend as fe_utils

"""
	Coroutine that continually calls weather_tick; is called once per server, and not just once globally
"""


async def weather_tick_loop(id_server):
    interval = ewcfg.weather_tick_length
    while not ewutils.TERMINATE:
        await asyncio.sleep(interval)
        await weather_tick(id_server=id_server)


""" Bleed slime for all users """


async def weather_tick(id_server = None):
    if id_server != None:
        try:
            market_data = EwMarket(id_server=id_server)
            
            if market_data.weather == ewcfg.weather_sunny:
                exposed_pois = []
                exposed_pois.extend(poi_static.capturable_districts)
                exposed_pois.extend(poi_static.outskirts)
                exposed_pois = tuple(exposed_pois)

                users = bknd_core.execute_sql_query(
                    "SELECT id_user FROM users WHERE id_server = %s AND {poi} IN %s AND {life_state} > 0".format(
                        poi=ewcfg.col_poi,
                        life_state=ewcfg.col_life_state
                    ), (
                        id_server,
                        exposed_pois

                    ))
                for user in users:
                    try:
                        user_data = EwUser(id_user=user[0], id_server=id_server)
                        if user_data.life_state == ewcfg.life_state_kingpin:
                            continue
                        else:
                            mutations = user_data.get_mutations()
                            if ewcfg.mutation_id_airlock in mutations:
                                user_data.hunger -= min(user_data.hunger, 5)
                    except:
                        ewutils.logMsg("Error occurred in weather tick for server {}".format(id_server))

            world_events = bknd_worldevent.get_world_events(id_server=id_server)

            for id_event in world_events:
                if world_events.get(id_event) in [ewcfg.event_type_firestorm, ewcfg.event_type_radiation_storm, ewcfg.event_type_tornado]:
                    event_data = EwWorldEvent(id_event=id_event)
                    

        # bknd_worldevent.delete_world_event(id_event=id_event)

        except:
            ewutils.logMsg("Error occurred in weather tick for server {}".format(id_server))

async def weather_cycle(id_server = None):
    market_data = EwMarket(id_server)
    
    # Potentially change the weather
    if random.randrange(3) == 0:
            pattern_count = len(weather_static.weather_list)

            if pattern_count > 1:
                weather_old = market_data.weather

                # if random.random() < 0.4:
                # 	market_data.weather = ewcfg.weather_bicarbonaterain

                # Randomly select a new weather pattern. Try again if we get the same one we currently have.
                while market_data.weather == weather_old:
                    pick = random.randrange(len(weather_static.weather_list))
                    market_data.weather = weather_static.weather_list[pick].name
                    market_data.persist()
            # Log message for statistics tracking.
            ewutils.logMsg("The weather changed. It's now {}.".format(market_data.weather))