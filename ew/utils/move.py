import asyncio
import heapq
import math
import random
import time
from copy import deepcopy

from ew.backend import core as bknd_core
from ew.backend.dungeons import EwGamestate
from ew.static import cfg as ewcfg
from ew.static import poi as poi_static
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import poi as poi_utils
from ew.utils import rolemgr as ewrolemgr
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict

move_counter = 0

map_world = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 0
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 1
    [-1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 120, -3, -3, -3, -3, -2, 120, 0, 0, 0, 0, 0, 0, 0, 0, 120, -3, -3, -3, -3, -2, 120, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 2
    [-1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 60, -1, 60, -1, 60, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 60, -1, 60, -1, 60, -1, -1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 3
    [-1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1],  # 4
    [-1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 120, -1, -1, -1, -1, -1, -1, -1],  # 5
    [-1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 60, -1, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1],  # 6
    [-1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -2, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, 60, -1, -1, -1, -1, -1, -1, 60, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -3, -1, -1, -1, -1, -1, -1, -1],  # 7
    [-1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, 60, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -2, 30, 0, 0, 0, 0, 30, -2, 30, 0, 0, 0, 0, -1, -1, 60, -1, -1, -1, -1, -1, 60, -1, -1, -1, -1, -1, -1, -1],  # 8
    [-1, -1, -1, 120, -1, -1, -1, -1, -1, -1, -1, 0, 0, 30, -2, 30, 0, 0, 0, 0, 0, -1, 0, -1, -1, -1, 30, -1, -1, -1, 0, -1, -1, 30, -1, -1, -1, -1, 0, 0, 30, -2, 30, 0, 0, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1],  # 9
    [-1, -1, -1, -2, 60, 0, 0, 0, 0, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 60, -1, 0, 0, 0, 0, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, 30, -1, 0, -1, -1, -1, -1, -1, -1, -1],  # 10
    [-1, -1, -1, -3, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, 0, 30, -2, 30, 0, -1, -1, 0, -1, -1, 30, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -2, 60, 0, -1, -1, -1, -1, -1, -1, -1],  # 11
    [-1, -1, -1, -3, 60, 0, 0, 0, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, 0, 0, 0, -1, 30, -1, -1, -1, -1, 0, -1, -1, -2, 30, 0, 0, 0, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 12
    [-1, -1, -1, -3, -1, -1, -1, 0, -1, 0, -1, 30, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, 0, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 13
    [-1, -1, -1, -3, 60, 0, -1, 0, -1, 0, 60, -2, 30, 0, 0, 0, 0, 30, -2, -1, -1, -1, 0, -1, -1, -1, -1, 0, 0, -1, -1, -1, -1, -1, 0, 0, 30, -2, 30, 0, 0, 0, 0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 14
    [-1, -1, -1, 120, -1, 0, -1, 0, -1, -1, -1, 30, -1, -1, -1, 0, -1, -1, 30, -1, -1, -1, 0, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, 30, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 15
    [-1, -1, -1, 0, -1, 0, -1, 0, -1, -1, -1, 0, -1, -1, -1, 30, -1, -1, 0, -1, -1, -1, 0, 0, 0, 0, 0, 30, -2, 30, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 30, -2, 30, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 16
    [-1, -1, -1, 0, -1, 0, -1, 0, -1, 0, 0, 0, 0, 0, 30, -2, -1, -1, 0, -1, -1, -1, 30, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 17
    [-1, -1, -1, 0, -1, 0, -1, 0, -1, 30, -1, -1, -1, -1, -1, 30, -1, -1, 0, 0, 0, 30, -2, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 18
    [-1, -1, -1, 0, -1, 0, -1, 0, 60, -2, -1, -1, -1, -1, 0, 0, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, 0, -1, 0, 0, 0, 30, -2, 30, 0, 0, 0, 0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 19
    [-1, -1, -1, 0, -1, 0, -1, -1, -1, 30, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, 30, -1, 30, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 20
    [-1, -1, -1, 0, -1, 0, -1, -1, -1, 0, 0, 0, 0, 30, -2, 30, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 30, -2, -3, -3, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, 0, 0, 30, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 21
    [-1, -1, -1, 0, -1, 0, -1, -1, -1, 0, -1, -1, -1, -1, 30, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -3, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 22
    [-1, -1, -1, 0, -1, 0, -1, -1, -1, 0, -1, -1, -1, -1, 0, -1, 30, -1, -1, 0, -1, -1, -1, -1, 0, 0, 0, 0, 0, -1, -3, -1, -1, -1, -1, -1, 30, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 23
    [-1, -1, -1, 0, -1, 0, -1, -1, -1, 30, 30, 0, 0, 0, 0, 30, -2, -1, -1, 0, 30, -2, 30, 0, 0, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 24
    [-1, -1, -1, 0, -1, 0, 0, 0, 60, -2, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, 30, -1, -1, 0, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 25
    [-1, -1, -1, 0, -1, -1, -1, -1, -1, 30, 0, 0, 0, 30, -2, 30, 0, 30, -1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1, -2, 30, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 26
    [-1, -1, -1, 0, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, 60, -1, -1, -2, 30, 0, 0, 0, -1, -1, 30, -1, 0, 0, 0, 0, 30, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 27
    [-1, -1, -1, 0, -1, -1, 0, 0, 0, 60, -2, -1, -1, -1, 0, -1, -1, 60, -1, 0, -1, -1, 0, 30, -2, 30, 0, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 28
    [-1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, 30, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, 60, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 29
    [-1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, -2, 30, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 30
    [-1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, 60, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 31
    [-1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 32
    [-1, -1, -1, 0, -1, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, -1, 0, -1, -1, 0, 30, -2, 30, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 33
    [-1, -1, -1, 0, -1, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, -1, 60, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 34
    [-1, -1, -1, 0, -1, -1, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 35
    [-1, -1, -1, 0, -1, -1, 60, -1, 60, -1, 60, -1, -1, -1, -1, -1, -1, -1, -1, 60, -1, 60, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 36
    [-1, -1, -1, 0, 0, 120, -2, -3, -3, -3, -3, 120, 0, 0, 0, 0, 0, 0, 120, -2, -3, -3, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 37
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 38
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2],  # 39
]
map_width = len(map_world[0])
map_height = len(map_world)

sem_wall = -1
sem_city = -2
sem_city_alias = -3

landmarks = {}

"""
    Returns true if the specified point of interest is a PvP zone.
"""


def poi_is_pvp(poi_name = None):
    poi = poi_static.id_to_poi.get(poi_name)

    if poi != None:
        return poi.pvp

    return False


"""
    Directions and cost from coord to arrive at a destination.
"""


class EwPath:
    visited = None
    steps = None
    cost = 0
    iters = 0
    pois_visited = None

    def __init__(
            self,
            path_from = None,
            steps = [],
            cost = 0,
            visited = {},
            pois_visited = None
    ):
        if path_from != None:
            self.steps = deepcopy(path_from.steps)
            self.cost = path_from.cost
            self.visited = deepcopy(path_from.visited)
            self.pois_visited = deepcopy(path_from.pois_visited)
        else:
            self.steps = steps
            self.cost = cost
            self.visited = visited
            if pois_visited == None:
                self.pois_visited = set()
            else:
                self.pois_visited = pois_visited


"""
    Add coord_next to the path.
"""


def path_step(path, poi_next, cost_next, user_data, poi_end, landmark_mode = False):
    next_poi = poi_next

    # Observer always makes inaccessible False
    if inaccessible(user_data=user_data, poi=next_poi):
        return False
    else:
        # check if we already got the movement bonus/malus for this district
        if not poi_next.id_poi in path.pois_visited:
            # if the given next step hasn't been marked visited, do so
            path.pois_visited.add(next_poi.id_poi)
            # If user has a faction, and the next poi isnt the start or end
            if len(user_data.faction) > 0 and next_poi.id_poi != poi_end.id_poi and next_poi.id_poi != path.steps[0].id_poi:
                # Grab district data
                district = EwDistrict(
                    id_server=user_data.id_server,
                    district=next_poi.id_poi
                )

                # If district data is found and it is capped, add/sub the faction bonus to cost_next
                if district != None and len(district.controlling_faction) > 0:
                    if user_data.faction == district.controlling_faction:
                        cost_next -= ewcfg.territory_time_gain
                    else:
                        cost_next += ewcfg.territory_time_gain
                # Slimecorp gets a bonus in unclaimed territory
                elif user_data.faction == ewcfg.faction_slimecorp:
                    cost_next -= ewcfg.territory_time_gain

    # Add the given next step to the path
    path.steps.append(poi_next)

    # subtract the faction bonus if the cost allows for it
    if landmark_mode and cost_next > ewcfg.territory_time_gain:
        cost_next -= ewcfg.territory_time_gain

    # add the step's cost to the path cost
    path.cost += cost_next

    return True


"""
    Returns a new path including all of path_base, with the next step coord_next.
"""


def path_branch(path_base, poi_next, cost_next, user_data, poi_end, landmark_mode = False):
    # Create a copy of the base path
    path_next = EwPath(path_from=path_base)

    # Return None if the next step is inaccessible
    if path_step(path_next, poi_next, cost_next, user_data, poi_end, landmark_mode) == False:
        return None

    # Return the base path with its next poi, and the corresponding cost, added, and marked as visited
    return path_next


def score_map_from(
        poi_start = None,
        user_data = None,
        landmark_mode = False
):
    # Load all districts with infinite travel time
    score_golf = math.inf
    score_map = {}
    for poi in poi_static.poi_list:
        score_map[poi.id_poi] = score_golf

    # Initialize some variable names
    paths_walking = []
    poi_end = None

    # Get EwPoi of the given start district
    poi_start = poi_static.id_to_poi.get(poi_start)

    # Initialize an empty path beginning with the given district, marked as already visited
    path_base = EwPath(
        steps=[poi_start],
        cost=0,
        pois_visited={poi_start.id_poi},
    )

    # Add the base path to the list of paths
    paths_walking.append(path_base)

    # Repeat until No paths are being checked
    count_iter = 0
    while len(paths_walking) > 0:
        count_iter += 1

        paths_walking_new = []

        # Iterate through all paths to be walked
        for path in paths_walking:
            # Grab the known score (infinite to start) of the final step, and skip walking this path if its cost is greater
            step_last = path.steps[-1]
            score_current = score_map.get(step_last.id_poi)
            if path.cost >= score_current:
                continue

            # Set the mapped score of the last step to the path's cost
            score_map[step_last.id_poi] = path.cost

            # Grab the second to last step if there are 2 or more
            step_penult = path.steps[-2] if len(path.steps) >= 2 else None

            # Set the base path to the one currently being walked, and grab the neighbor ids of the last step
            path_base = path
            neighs = list(step_last.neighbors.keys())

            # If there is a second to last step, and it neighbors the last step, remove it from the neighbor list
            if step_penult != None and step_penult.id_poi in neighs:
                neighs.remove(step_penult.id_poi)

            # Loop each remaining neighbor
            num_neighbors = len(neighs)
            for i in range(num_neighbors):
                # Grabbing its EwPoi and travel cost from the last step
                neigh = poi_static.id_to_poi.get(neighs[i])
                neigh_cost = step_last.neighbors.get(neigh.id_poi)

                # Skip if it has no cost
                if neigh_cost == None:
                    continue

                # On all but the last neighbor in the loop
                if i < num_neighbors - 1:
                    # Create a new path with the neighbor appended, visited, and its cost (-10) added
                    branch = path_branch(path_base, neigh, neigh_cost, user_data, poi_end, landmark_mode)
                    if branch != None:  # if the branch *can* be made anyway
                        paths_walking_new.append(branch)

                # For the last neighbor
                else:
                    # directly add it to the base path
                    if path_step(path_base, neigh, neigh_cost, user_data, poi_end, landmark_mode):
                        paths_walking_new.append(path_base)

        # Set the paths to process equal to the list of the base path + neighbor, one path for each neighbor
        paths_walking = paths_walking_new

    # Return a dictionary of the cost to reach each district from the given starting point
    return score_map


def path_to(
        poi_start = None,
        poi_end = None,
        user_data = None
):
    # ewutils.logMsg("beginning pathfinding")
    # Map all districts with a starting score of infinite
    score_golf = math.inf
    score_map = {}
    for poi in poi_static.poi_list:
        score_map[poi.id_poi] = math.inf

    # Initialize some lists for later use/reference
    paths_finished = []
    paths_walking = []
    pois_adjacent = []

    # Grab the EwPoi of the start and destination
    poi_start = poi_static.id_to_poi.get(poi_start)
    poi_end = poi_static.id_to_poi.get(poi_end)

    # Initialize a path beginning at the given start district
    path_base = EwPath(
        steps=[poi_start],
        cost=0,
        pois_visited={poi_start.id_poi},
    )

    path_id = 0
    # Push a tuple of (Base Cost + LMH of base to destination, path id, and the base EwPath) onto the heap (paths_walking)
    heapq.heappush(paths_walking, (path_base.cost + landmark_heuristic(path_base, poi_end), path_id, path_base))
    path_id += 1

    # While there are paths to walk, do something to all of them, and track the number of iterations
    count_iter = 0
    while len(paths_walking) > 0:
        count_iter += 1

        # grab the smallest (By cost + landmark heuristic) path out of the list, removing it
        path_tuple = heapq.heappop(paths_walking)

        # Grab the EwPath out of the acquired tuple
        path = path_tuple[-1]

        # So long as there WAS a path to grab
        if path is not None:
            # Grab the final step in the path, and its known score
            step_last = path.steps[-1]
            score_current = score_map.get(step_last.id_poi)

            # Skip conditions
            if poi_end is not None and not poi_start.is_outskirts and not poi_end.is_outskirts and step_last.is_outskirts and poi_end.id_poi != 'temple' and poi_start.id_poi != 'temple':
                # do not go through outskirts if the start and destination aren't part of them
                continue
            if path.cost >= score_current:
                # if the total path cost exceeds the cost of the final step
                continue
            if user_data.life_state != ewcfg.life_state_corpse and (poi_end and poi_end.id_poi != step_last.id_poi == ewcfg.poi_id_thesewers):
                # if alive, and the destination EwPoi exists, is not the final step
                # can't route through the sewers unless you're dead
                continue

            # assign the path's cost as the score for the final step
            score_map[step_last.id_poi] = path.cost
            # ewutils.logMsg("visiting " + str(step_last))

            # Grab the second to last step if there is one
            step_penult = path.steps[-2] if len(path.steps) >= 2 else None

            # If a destination was passed
            if poi_end != None:
                # Arrived at the actual destination?
                if step_last.id_poi == poi_end.id_poi:
                    # If the final step of the current path is the destination
                    path_final = path
                    if path_final.cost < score_golf:
                        # if the cost is less than the lowest currently known, overwrite, and empty the finished paths
                        score_golf = path_final.cost
                        paths_finished = []
                    if path_final.cost <= score_golf:
                        # if the path is the fastest, or equivalent, add to the finished paths
                        paths_finished.append(path_final)
                    # Leave the "if path is not None" block
                    break
            # If no destination was given
            else:
                # Looking for adjacent points of interest.
                poi_adjacent = step_last
                # if the final step is not the starting poi, add it to the list of adjacent pois, and return to the beginning of the loop
                if poi_adjacent.id_poi != poi_start.id_poi:
                    pois_adjacent.append(poi_adjacent)
                    continue

            # Set the base path to the current path, and get the neighbors of the final step
            path_base = path
            neighs = list(step_last.neighbors.keys())

            # Don't go backwards and recompute from a neighbor you just came from, and computed
            if step_penult != None and step_penult.id_poi in neighs:
                neighs.remove(step_penult.id_poi)

            # iterate through all remaining neighbors
            num_neighbors = len(neighs)
            for i in range(num_neighbors):
                # Get the neighbor EwPoi, and its cost from the final step of the path
                neigh = poi_static.id_to_poi.get(neighs[i])
                neigh_cost = step_last.neighbors.get(neigh.id_poi)

                # If it has no listed cost, skip it
                if neigh_cost == None:
                    continue

                # Only if it isn't the last neighbor
                if i < num_neighbors - 1:
                    # Create a new path that goes to that neighbor, and throw it on the heap if it's accessible
                    branch = path_branch(path_base, neigh, neigh_cost, user_data, poi_end)
                    if branch != None:
                        heapq.heappush(paths_walking, (branch.cost + landmark_heuristic(branch, poi_end), path_id, branch))
                        path_id += 1
                # On the last neighbor
                else:
                    # If the path to the neighbor is accessible, make it the base path, and throw it on the heap
                    if path_step(path_base, neigh, neigh_cost, user_data, poi_end):
                        heapq.heappush(paths_walking, (path_base.cost + landmark_heuristic(path_base, poi_end), path_id, path_base))
                        path_id += 1

    # ewutils.logMsg("finished pathfinding")

    # If a destination was given
    if poi_end != None:
        path_true = None
        # Return the first finished path if there are any
        if len(paths_finished) > 0:
            path_true = paths_finished[0]
            path_true.iters = count_iter
        # Otherwise return None and log it
        if path_true is None:
            ewutils.logMsg("Could not find a path.")
        return path_true
    # if no destination was given, return all districts adjacent to the start district
    else:
        return pois_adjacent


def landmark_heuristic(path, poi_end):
    # If landmark cost maps are uninitialized or no destination is given, return zero
    if len(landmarks) == 0 or poi_end is None:
        return 0
    else:
        # Grab the last step of the given path
        last_step = path.steps[-1]
        # List the difference in cost from each landmark between the last step of the path and the destination
        scores = []
        for lm in landmarks:
            score_map = landmarks.get(lm)
            score_path = score_map.get(last_step.id_poi)
            score_goal = score_map.get(poi_end.id_poi)
            scores.append(abs(score_path - score_goal))

        # Return the maximum of the score differences
        return max(scores)


"""
    Debug method to draw the map, optionally with a path/route on it.
"""


def map_draw(path = None, coord = None):
    y = 0
    for row in map_world:
        outstr = ""
        x = 0

        for col in row:
            if col == sem_wall:
                col = "  "
            elif col == sem_city:
                col = "CT"
            elif col == sem_city_alias:
                col = "ct"
            elif col == 0:
                col = "██"
            elif col == 30:
                col = "[]"
            elif col == 20:
                col = "••"
            elif col == 60:
                col = "<>"
            elif col == 120:
                col = "=="

            if path != None:
                visited_set_y = path.visited.get(x)
                if visited_set_y != None and visited_set_y.get(y) != None:
                    col = "." + col[-1]

            if coord != None and coord == (x, y):
                col = "O" + col[-1]

            outstr += "{}".format(col)
            x += 1

        print(outstr)
        y += 1


def inaccessible(user_data = None, poi = None):
    if poi == None or user_data == None:
        return True

    if user_data.life_state == ewcfg.life_state_observer:
        return False

    source_poi = poi_static.id_to_poi.get(user_data.poi)

    # locks that inhibit a POI
    for lock in ewcfg.region_lock_states:
        if poi.id_poi == lock:
            for state in ewcfg.region_lock_states.get(lock):
                gamestate = EwGamestate(id_server=user_data.id_server, id_state=state)
                if gamestate.bit == 0:
                    return True

    shipstate = EwGamestate(id_server=user_data.id_server, id_state='shipstate')
    if ((shipstate.bit == 0) and (user_data.poi == 'ufoufo' or poi.id_poi == 'ufoufo')) or (poi.id_poi == 'ufoufo' and user_data.life_state == ewcfg.life_state_corpse):
        return True

    bans = user_data.get_bans()
    vouchers = user_data.get_vouchers()

    locked_districts_list = poi_utils.retrieve_locked_districts(user_data.id_server)

    if (
            len(poi.factions) > 0 and
            (set(vouchers).isdisjoint(set(poi.factions)) or user_data.faction != "") and
            user_data.faction not in poi.factions
    ) or (
            len(poi.life_states) > 0 and
            user_data.life_state not in poi.life_states
    ):
        return True
    elif (
            len(poi.factions) > 0 and
            len(bans) > 0 and
            set(poi.factions).issubset(set(bans))
    ):
        return True
    elif poi.id_poi in locked_districts_list and user_data.life_state not in [ewcfg.life_state_executive, ewcfg.life_state_lucky]:
        return True
    else:
        return False


"""
    Kicks idle players from subzones. Called every 15 minutes.
"""


async def kick(id_server):
    time_now = int(time.time() - ewcfg.time_kickout)
    # Gets data for all living players from the database
    all_living_players = bknd_core.execute_sql_query("SELECT {poi}, {id_user} FROM users WHERE id_server = %s AND {life_state} > 0 AND {time_last_action} < %s AND {time_lastenter} < %s".format(
        poi=ewcfg.col_poi,
        id_user=ewcfg.col_id_user,
        time_last_action=ewcfg.col_time_last_action,
        time_lastenter=ewcfg.col_time_lastenter,
        life_state=ewcfg.col_life_state
    ), (
        id_server,
        time_now,
        time_now
    ))

    client = ewutils.get_client()

    blockparty = EwGamestate(id_server=id_server, id_state='blockparty')
    party_poi = ''.join([i for i in blockparty.value if not i.isdigit()])
    if party_poi == 'outsidethe':
        party_poi = ewcfg.poi_id_711


    for player in all_living_players:
        try:
            poi = poi_static.id_to_poi[player[0]]
            id_user = player[1]
            

            # checks if the player should be kicked from the subzone and kicks them if they should.
            if poi.is_subzone and poi.id_poi not in [ewcfg.poi_id_thesphere, ewcfg.poi_id_thebreakroom]:
                
                # Don't load the user until we know that we need to
                user_data = EwUser(id_user=id_user, id_server=id_server)
                
                # Some subzones could potentially have multiple mother districts.
                # Make sure to get one that's accessible before attempting a proper kickout.
                mother_district_chosen = random.choice(poi.mother_districts)

                if inaccessible(user_data=user_data, poi=poi_static.id_to_poi.get(mother_district_chosen)):
                    # If the randomly chosen mother district is inaccessible, make one more attempt.
                    mother_district_chosen = random.choice(poi.mother_districts)
                else:
                    pass

                if not inaccessible(user_data=user_data, poi=poi_static.id_to_poi.get(mother_district_chosen)):

                    if user_data.poi != party_poi and user_data.life_state not in [ewcfg.life_state_kingpin, ewcfg.life_state_lucky, ewcfg.life_state_executive]:

                        server = ewcfg.server_list[id_server]
                        member_object = await fe_utils.get_member(server, id_user)

                        user_data.poi = mother_district_chosen
                        user_data.time_lastenter = int(time.time())

                        user_data.change_crime(n=50) # loitering:punishable by death

                        user_data.persist()
                        await ewrolemgr.updateRoles(client=client, member=member_object)
                        await user_data.move_inhabitants(id_poi=mother_district_chosen)
                        mother_district_channel = fe_utils.get_channel(server, poi_static.id_to_poi[mother_district_chosen].channel)
                        response = "You have been kicked out for loitering! You can only stay in a sub-zone and twiddle your thumbs for 1 hour at a time."
                        await fe_utils.send_message(client, mother_district_channel, fe_utils.formatMessage(member_object, response))
                        ewutils.logMsg('moved inactive player {} out of subzone {}. Last action: {}'.format(user_data.id_user, user_data.poi, user_data.time_last_action))
        except:
            ewutils.logMsg('failed to move inactive player out of subzone with poi {}: {}'.format(player[0], player[1]))


async def send_gangbase_messages(server_id, clock):
    # this can be added onto for events and such
    lucky_lucy = 0
    casino_response = "**Lucky Lucy has arrived!** Now's the time to make your fortune!"
    casino_end = "Aww, Lucy left."


    highnoon = 0


    response = ""
    #if clock == 3:
    #    response = "The police are probably asleep, the lazy fucks. It's a good time for painting the town!"
    #elif clock == 11:
    #    response = "Spray time's over, looks like the cops are back out. Fuck those guys."
    if random.randint(1, 50) == 2:
        lucky_lucy = 1


    if clock == 11:
        highnoon = 1
    if clock == 12:
        highnoon = 2


    client = ewutils.get_client()
    server = client.get_guild(server_id)
    channels = ewcfg.hideout_channels
    casino_channel = fe_utils.get_channel(server=server, channel_name=ewcfg.channel_casino)
    dueling_channel = fe_utils.get_channel(server=server, channel_name='hang-em-square')



    if response != "":
        for channel in channels:
            post_channel = fe_utils.get_channel(server, channel)
            await fe_utils.send_message(client, post_channel, response)
    if lucky_lucy == 1:
        pass #taking this out until we have a better method
        #await fe_utils.send_message(client, casino_channel, casino_response)
        #await asyncio.sleep(300)
        #await fe_utils.send_message(client, casino_channel, casino_end)


    if highnoon != 0:
        district = EwDistrict(district='hangemsquare', id_server=server_id)
        if len(district.get_players_in_district(min_slimes=0, life_states=[ewcfg.life_state_enlisted, ewcfg.life_state_juvenile, ewcfg.life_state_corpse], ignore_offline=True)) > 0:
            if highnoon == 1:
                response = "It's almost high noon..."
            else:
                response = "**DRAW!!!!**"
            await fe_utils.send_message(client, dueling_channel, response)



"""
    Find the cost to move through ortho-adjacent cells.
"""


# unused
def neighbors(coord):
    neigh = []

    if coord[1] > 0 and map_world[coord[1] - 1][coord[0]] != sem_wall:
        neigh.append((coord[0], coord[1] - 1))
    if coord[1] < (map_height - 1) and map_world[coord[1] + 1][coord[0]] != sem_wall:
        neigh.append((coord[0], coord[1] + 1))

    if coord[0] > 0 and map_world[coord[1]][coord[0] - 1] != sem_wall:
        neigh.append((coord[0] - 1, coord[1]))
    if coord[0] < (map_width - 1) and map_world[coord[1]][coord[0] + 1] != sem_wall:
        neigh.append((coord[0] + 1, coord[1]))

    return neigh
