import ew.backend.core as bknd_core
import datetime
import ew.static.cfg as ewcfg
from ew.static import mutations as static_mutations
import random
from ew.backend.dungeons import EwGamestate

active_mutations = []

stat_ranges = {
    'gamespeed':[1, 1],
    'decayrate':[1, 1],
    'slimegainrate':[1, 1],
    'fishrate':[1, 1],
    'minerate':[1, 1],
    'farmrate':[1, 1],
    'damagemultiplier':[1, 1]
}

def initialize_rotation(id_server):
    today = datetime.date.today()
    month = int(today.month)
    year = int(today.year)

    future_month = (month % 12) + 1
    future_year = year if month != 12 else year + 1

    current_rotation_data = bknd_core.execute_sql_query("select {id_mutation}, {context_num} from mut_rotations where {month} = %s and {year} = %s".format(
        id_mutation = ewcfg.col_id_mutation,
        context_num = ewcfg.col_id_context_num,
        month = ewcfg.col_id_month,
        year = ewcfg.col_id_year
    ),(month, year))

    future_rotation_data = bknd_core.execute_sql_query(
        "select {id_mutation}, {context_num} from mut_rotations where {month} = %s and {year} = %s".format(
            id_mutation=ewcfg.col_id_mutation,
            context_num=ewcfg.col_id_context_num,
            month=ewcfg.col_id_month,
            year=ewcfg.col_id_year
        ), (future_month, future_year))

    if len(current_rotation_data) == 0:
        current_rotation_data = insert_rotation(id_server=id_server, month=month, year=year),
    if len(future_rotation_data) == 0:
        future_rotation_data = insert_rotation(id_server=id_server, month = future_month, year = future_year)

    for mut in current_rotation_data:
        name = mut[0]
        modifier = mut[1]
        if name not in stat_ranges.keys():
            active_mutations.append(mut[0])
        else:
            if modifier == 1.00:
                pass
            elif name == 'gamespeed':
                gamestate = EwGamestate(id_server=id_server, id_state='endlessgraphite')
                gamestate.value = str(modifier)
                gamestate.persist()
            elif name == 'decayrate':
                gamestate = EwGamestate(id_server=id_server, id_state='endlesspumice')
                gamestate.number = int(modifier)
                gamestate.persist()
            elif name == 'damagemultiplier':
                ewcfg.global_damage_multiplier = modifier
            elif name == 'slimegainrate':
                ewcfg.global_slimegain_multiplier = modifier
            elif name == 'fishrate':
                ewcfg.fishgain_multiplier = modifier
            elif name == 'farmrate':
                ewcfg.farmgain_multiplier = modifier
            elif name == 'minerate':
                ewcfg.minegain_multiplier = modifier






def insert_rotation(id_server, month, year):
    selected_muts = create_rotation()
    returned_list = []
    for mut in selected_muts:

        contextnum = 1.00  # this is to reroll variables other than mutations. currently all multipliers are locked at 1
        if mut in stat_ranges.keys():
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



def create_rotation():
    all_mutations = []

    for mutation in static_mutations.mutations:
        all_mutations.append(mutation.id_mutation)

    random.shuffle(all_mutations)

    limited_list = int(len(all_mutations) * .66)

    selections = all_mutations[:limited_list]

    for stat in stat_ranges.keys():
        selections.append(stat)

    return selections

