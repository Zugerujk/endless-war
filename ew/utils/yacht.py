import ew.static.cfg as ewcfg
import math
from ..backend.yacht import EwYacht
from ..backend import core as bknd_core
import ew.static.poi as poi_static
from ew.utils import core as coreutils
from ew.utils.district import EwDistrict
from ew.utils.combat import EwUser
import ew.utils.frontend as fe_utils
try:
    from ew.cmd import debug as ewdebug
except:
    from ew.cmd import debug_dummy as ewdebug


def load_boats_to_poi(id_server):
    boats = bknd_core.execute_sql_query(
        "SELECT thread_id from yachts where {direction} <> %s and {id_server} = %s".format(direction=ewcfg.col_direction, id_server=ewcfg.col_id_server), ('sunk', id_server))
    boat_poi = poi_static.id_to_poi.get('yacht')
    print("LOADING BOATS")
    for boat in boats:
        print('{}{}'.format('yacht', boat[0]))
        poi_static.id_to_poi['{}{}'.format('yacht', boat[0])] = boat_poi
        #boat_obj = EwYacht(id_server=id_server, id_thread=boat)



async def boat_tick(id_server, tick_count):
    boats = bknd_core.execute_sql_query(
        "SELECT thread_id from yachts where {direction} <> %s and {id_server} = %s".format(direction=ewcfg.col_direction, id_server=ewcfg.col_id_server),  ('sunk', id_server))
    for boat in boats:
        boat_obj = EwYacht(id_server=id_server, id_thread=boat[0])

        #If the ship is moving in a direction, allow it to move until it hits an obstruction.
        if boat_obj.direction == 'stop':
            boat_obj.speed = 0
        else:
            if tick_count == 1:
                spaces_to_advance = math.floor(boat_obj.speed / 2)
            else:
                spaces_to_advance = math.ceil(boat_obj.speed / 2)

            if boat_obj.direction in ['north', 'west']:
                direction_to_advance = -1
            else:
                direction_to_advance = 1

            seacursor_x = boat_obj.xcoord
            seacursor_y = boat_obj.ycoord
            response = ""
            if boat_obj.direction in ['north', 'south', 'east', 'west'] and boat_obj.helm != -1:
                player = EwUser(id_user=boat_obj.helm, id_server=id_server)
                if player.poi == "yacht{}".format(boat_obj.thread_id):
                    response += draw_map(xcoord=boat_obj.xcoord, ycoord=boat_obj.ycoord, id_server=boat_obj.id_server, radius=4)

            for x in range(spaces_to_advance):
                if boat_obj.direction in['north', 'south']:
                    seacursor_y += direction_to_advance
                else:
                    seacursor_x += direction_to_advance

                if ewdebug.seamap[seacursor_y][seacursor_x] == -1:
                    boat_obj.xcoord = seacursor_x
                    boat_obj.ycoord = seacursor_y
                    if response != "":
                        await fe_utils.send_message(None, boat_obj.get_thread(), response)
                elif ewdebug.seamap[seacursor_y][seacursor_x] == 0 and ewdebug.seamap[boat_obj.ycoord][boat_obj.xcoord] == -1:
                    boat_obj.xcoord = seacursor_x
                    boat_obj.ycoord = seacursor_y
                    boat_obj.direction = 'stop'
                    boat_obj.flood = 0
                    boat_obj.speed = 0
                    response += "LAND HO! Looks like we've arrived at an island."
                    await fe_utils.send_message(None, boat_obj.get_thread(), response)
                    break
                elif ewdebug.seamap[seacursor_y][seacursor_x] in [3, 0]:
                    response += "The {} suddenly stops. Did we hit something?".format(boat_obj.yacht_name)
                    await fe_utils.send_message(None, boat_obj.get_thread(), response)
                    break

        stats = boat_obj.getYachtStats()

        for stat in stats:
            if stat == 'flood' and ewdebug.seamap[boat_obj.ycoord][boat_obj.xcoord] != 0:
                boat_obj.flood += stat.quantity

        if boat_obj.flood > 100:
            #todo detect the killer and parse that in too
            await sink(thread_id=boat_obj.thread_id, id_server=id_server)
        boat_obj.persist()




def find_local_boats(poi = None, name = None, id_server = None, current_coords = None):
    boats = []
    query = "select {} from yachts where {} = %s and {} <> %s".format(ewcfg.col_thread_id, ewcfg.col_id_server, ewcfg.col_direction)
    data = bknd_core.execute_sql_query(query, (id_server, 'sunk'))
    if current_coords is not None:
        if type(current_coords[0]) == int:
            current_coords = [current_coords]

    for id in data:
        yacht = EwYacht(id_server=id_server, id_thread=id[0])
        poi_match = 0
        if poi is not None:
            poi = poi_static.id_to_poi.get(poi)
            if poi.coord is None:
                continue

            else:
                for coord in poi.coord:
                    if yacht.xcoord == coord[0] and yacht.ycoord == coord[1]:
                        poi_match = 1
                        break
        elif current_coords is not None:
            for coord in current_coords:
                if yacht.xcoord == coord[0] and yacht.ycoord == coord[1]:
                    poi_match = 1
                    break
        else:
            poi_match = 1
        if poi_match == 1 and(name is None or coreutils.flattenTokenListToString(name) in coreutils.flattenTokenListToString(yacht.yacht_name)):
            boats.append(yacht)

    return boats


def clear_station(id_user, thread_id, id_server):
    yacht = EwYacht(id_thread=thread_id, id_server=id_server)
    if id_user == yacht.poopdeck:
        yacht.poopdeck = -1
    if id_user == yacht.storehouse:
        yacht.storehouse = -1
    if id_user == yacht.cannon:
        yacht.cannon = -1
    if id_user == yacht.helm:
        yacht.helm = -1
    yacht.persist()


async def sink(thread_id, id_server, killer_yacht = None):

    sunk_yacht = EwYacht(id_server=id_server, id_thread=thread_id)
    sunk_yacht.direction = 'sunk'
    sunk_yacht.speed = 0
    sunk_yacht.helm = -1
    sunk_yacht.poopdeck = -1
    sunk_yacht.storehouse = -1
    sunk_yacht.cannon = -1

    total_yield = 0
    if sunk_yacht.slimes > 0:
        total_yield += sunk_yacht.slimes

    sunk_yacht.change_slimes(n=-sunk_yacht.slimes)

    district_data = EwDistrict(id_server=id_server, district='yacht')
    players = district_data.get_players_in_district(poi_name="yacht{}".format(thread_id))

    sunk_yacht.persist()

    for player in players:
        player_obj = EwUser(id_user=player, id_server=id_server)
        if player_obj.slimes > 0:
            total_yield += player_obj.slimes

        if player_obj.life_state != ewcfg.life_state_corpse:
            player_obj.change_slimes(n=-player_obj.slimes)
            player_obj.poi = "{}_{}_{}".format(ewcfg.poi_id_slimesea, sunk_yacht.xcoord, sunk_yacht.ycoord) #get items to sink to this region specifically
            await player_obj.die(cause=ewcfg.cause_shipsink, updateRoles=True)

    if killer_yacht is not None:
        killer_yacht_obj = EwYacht(id_server=id_server, id_thread=killer_yacht)
        if total_yield > 0:
            killer_yacht_obj.change_slimes(n=total_yield)
            killer_yacht_obj.persist()
    else:
        sewer_district = EwDistrict(id_server=sunk_yacht.id_server, district=ewcfg.poi_id_thesewers)
        sewer_district.change_slimes(n=total_yield)
        sewer_district.persist()



def draw_map(xcoord, ycoord, id_server, radius = 4 ):
    center_x = min(max(xcoord, 5), ewdebug.max_right_bound - 4)
    center_y = min(max(ycoord, 5), ewdebug.max_lower_bound - 4)
    search_coords = []
    for x in range(-radius, radius+1):
        for y in range(-radius, radius+1):
            search_coords.append([center_x + x, center_y + y])

    boats = find_local_boats(id_server=id_server, current_coords=search_coords)

    response = ''

    map_key = {
        -1: '🟦',  # blue
        3: '⬛',  # black
        0: '🟩'  # green

    }

    for y in range(-radius, radius+1):
        response += '\n'
        for x in range(-radius, radius+1):
            letter = map_key.get(ewdebug.seamap[y + center_y][x + center_x])
            for boat in boats:
                if boat.ycoord == y + center_y and boat.xcoord == x + center_x:
                    letter = '⛵'
            response += letter

    return response