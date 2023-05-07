import ew.backend.core as bknd_core
import datetime
import ew.static.cfg as ewcfg
from ew.static import mutations as static_mutations
import random
from ew.backend.dungeons import EwGamestate
import time

active_mutations = {}

stat_ranges = {
    'gamespeed':[1, 1, 'Game Speed: {}x\n'],
    'decayrate':[1, 1, 'Decay Rate" LV {}\n'],
    'slimegainrate':[1, 1, 'Slimegain Multiplier: {}x\n'],
    'fishrate':[1, 1, 'Fishing Slimegain: {}x\n'],
    'minerate':[1, 1, 'Mining Slimegain: {}x\n'],
    'farmrate':[1, 1, 'Farming Slimegain: {}x\n'],
    'damagemultiplier':[1, 1, 'Damage Multiplier: {}x\n']
}

default_variables = {
    'slimegainrate': ewcfg.global_slimegain_multiplier,
    'fishrate': ewcfg.fishgain_multiplier,
    'minerate': ewcfg.minegain_multiplier,
    'farmrate': ewcfg.farmgain_multiplier,
    'damagemultiplier': ewcfg.global_damage_multiplier
}


def initialize_rotation(id_server):
    today = datetime.date.today()
    month = int(today.month)
    year = int(today.year)
    active_mutations[id_server] = []
    future_month = (month % 12) + 1
    future_year = year if month != 12 else year + 1




    current_rotation_data = bknd_core.execute_sql_query("select {id_mutation}, {context_num} from mut_rotations where {month} = %s and {year} = %s and {id_server} = %s".format(
        id_mutation = ewcfg.col_id_mutation,
        context_num = ewcfg.col_id_context_num,
        month = ewcfg.col_id_month,
        year = ewcfg.col_id_year,
        id_server=ewcfg.col_id_server
    ),(month, year, id_server))

    future_rotation_data = bknd_core.execute_sql_query(
        "select {id_mutation}, {context_num} from mut_rotations where {month} = %s and {year} = %s and {id_server} = %s".format(
            id_mutation=ewcfg.col_id_mutation,
            context_num=ewcfg.col_id_context_num,
            month=ewcfg.col_id_month,
            year=ewcfg.col_id_year,
            id_server=ewcfg.col_id_server
        ), (future_month, future_year, id_server))

    if len(current_rotation_data) == 0:

        current_rotation_data = insert_rotation(id_server=id_server, month=month, year=year)
    if len(future_rotation_data) == 0:
        insert_rotation(id_server=id_server, month = future_month, year = future_year, isFuture=1)

    for mut in current_rotation_data:
        name = mut[0]
        modifier = mut[1]


        if name not in stat_ranges.keys():
            active_mutations[id_server].append(mut[0])
        else:

            if name == 'damagemultiplier':
                ewcfg.global_damage_multiplier_dt[id_server] = modifier
            elif name == 'slimegainrate':
                ewcfg.global_slimegain_multiplier_dt[id_server] = modifier
            elif name == 'fishrate':
                ewcfg.fishgain_multiplier_dt[id_server] = modifier
            elif name == 'farmrate':
                ewcfg.farmgain_multiplier_dt[id_server] = modifier
            elif name == 'minerate':
                ewcfg.minegain_multiplier_dt[id_server] = modifier
            elif modifier == 1.00:
                pass
            elif name == 'gamespeed':
                gamestate = EwGamestate(id_server=id_server, id_state='endlessgraphite')
                gamestate.value = str(modifier)
                gamestate.persist()
            elif name == 'decayrate':
                gamestate = EwGamestate(id_server=id_server, id_state='endlesspumice')
                gamestate.number = int(modifier)
                gamestate.persist()

    inclause = "{}{}{}".format("('" , "','".join(active_mutations[id_server]), "')")

    bknd_core.execute_sql_query(
        "delete from mutations where {mutation} not in {inclause} and {id_server} = %s".format(
            mutation=ewcfg.col_id_mutation,
            inclause = inclause,
            id_server=ewcfg.col_id_server
        ), (id_server, ))





def insert_rotation(id_server, month, year, isFuture = 0):
    selected_muts = create_rotation(id_server=id_server, isFuture=isFuture)
    returned_list = []
    for mut in selected_muts:

        contextnum = 1.00  # this is to reroll variables other than mutations. currently all multipliers are locked at 1
        if mut in stat_ranges.keys():
            if mut in default_variables.keys():
                contextnum = default_variables.get(mut)
            if random.randint(1, 10) == 1:
                range = stat_ranges.get(mut)
                contextnum = round(random.uniform(range[0], range[1]), 2)

        returned_list.append([mut, contextnum])
        bknd_core.execute_sql_query(
            "insert into mut_rotations({id_server}, {id_month}, {id_year}, {mutation}, {context_num}) values(%s, %s, %s, %s, %s)".format(
                id_server=ewcfg.col_id_server,
                id_month=ewcfg.col_id_month,
                id_year=ewcfg.col_id_year,
                mutation=ewcfg.col_id_mutation,
                context_num=ewcfg.col_id_context_num
            ), (id_server,
                month,
                year,
                mut,
                contextnum))
    return returned_list



def create_rotation(id_server, isFuture = 0):
    all_mutations = []
    time_now = int(time.time())
    random_seed_mut = random.Random(id_server)
    random_seed_mut.seed(id_server + time_now + isFuture)
    locked_muts = []

    locked_rotation_data = bknd_core.execute_sql_query(
        "select {id_mutation} from mut_rotations where {month} = %s and {year} = %s and {id_server} = %s".format(
            id_mutation=ewcfg.col_id_mutation,
            context_num=ewcfg.col_id_context_num,
            month=ewcfg.col_id_month,
            year=ewcfg.col_id_year,
            id_server=ewcfg.col_id_server
        ), (0, 0, id_server))

    for lock in locked_rotation_data:
        locked_muts.append(lock[0])

    for mutation in static_mutations.mutations:
        if mutation.id_mutation not in locked_muts:
            all_mutations.append(mutation.id_mutation)

    random_seed_mut.shuffle(all_mutations)

    limited_list = int(len(all_mutations) * .66) - len(locked_rotation_data)

    selections = all_mutations[:limited_list]

    for stat in stat_ranges.keys():
        selections.append(stat)

    selections.extend(locked_muts)

    return selections

