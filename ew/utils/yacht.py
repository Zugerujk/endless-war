import ew.static.cfg as ewcfg
import math
from ..backend.yacht import EwYacht
from ..backend import core as bknd_core
import ew.static.poi as poi_static


try:
    from ew.cmd import debug as ewdebug
except:
    from ew.cmd import debug_dummy as ewdebug



async def boat_tick(id_server, tick_count):
    boats = bknd_core.execute_sql_query(
        "SELECT id_yacht from yachts where {direction} <> %s and {id_server} = %s".format(direction=ewcfg.col_direction, id_server=ewcfg.col_id_server),  ('sunk', id_server))
    for boat in boats:
        boat_obj = EwYacht(id_server=id_server, id_yacht=boat)

        #If the ship is moving in a direction, allow it to move until it hits an obstruction.
        if boat.direction == 'stop':
            boat_obj.speed = 0
        else:
            if tick_count == 1:
                spaces_to_advance = math.floor(boat_obj.speed / 2)
            else:
                spaces_to_advance = math.ceil(boat_obj.speed / 2)

            if boat.direction in ['north', 'west']:
                direction_to_advance = -1
            else:
                direction_to_advance = 1

            seacursor_x = boat_obj.xcoord
            seacursor_y = boat_obj.ycoord

            for x in range(spaces_to_advance):
                if boat.direction in['north', 'south']:
                    seacursor_y += direction_to_advance
                else:
                    seacursor_x += direction_to_advance

                if ewdebug.seamap[seacursor_y][seacursor_x] == -1:
                    boat_obj.xcoord = seacursor_x
                    boat_obj.ycoord = seacursor_y
                elif ewdebug.seamap[seacursor_y][seacursor_x] == 0 and ewdebug.seamap[boat_obj.ycoord][boat_obj.xcoord] == -1:
                    boat_obj.direction = 'stop'
                    boat_obj.flood = 0
                    boat_obj.speed = 0
                    #todo send a message to the boat indicating arrival at a destination
                elif ewdebug.seamap[seacursor_y][seacursor_x] in [3, 0]:
                    #todo set up a boat message telling the player they've hit a wall or island
                    break

        stats = boat_obj.getYachtStats()

        for stat in stats:
            if stat == 'flood' and ewdebug.seamap[boat_obj.ycoord][boat_obj.xcoord] != 0:
                boat_obj.flood += stat.quantity

        if boat_obj.flood > 100:
            #todo create a sink function that drowns anyone on a sunken ship
            pass
        boat_obj.persist()




async def find_local_boats(poi = None, name = None, id_server = None):
    boats = []
    query = "select {} from yachts where {} = %s and {} <> %s".format(ewcfg.col_thread_id, ewcfg.col_id_server, ewcfg.col_direction)
    data = bknd_core.execute_sql_query(query, (id_server, 'sunk'))

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
        else:
            poi_match = 1

        if poi_match == 1 and(name in yacht.yacht_name or name is None):
            boats.append(yacht)

    return boats


async def sink():
    pass