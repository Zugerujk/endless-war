from . import cfg as ewcfg
from . import cosmetics
from . import fish as static_fish
from . import food as static_food
from . import items as static_items
from . import weapons
try:
    import ew.static.rstatic as static_relic
except:
    import ew.static.rstatic_dummy as static_relic


# A map of vendor names to their items.
vendor_inv = {}

it_to_map = {
    ewcfg.it_item: static_items.item_map,
    ewcfg.it_food: static_food.food_map,
    ewcfg.it_weapon: weapons.weapon_map,
    ewcfg.it_furniture: static_items.furniture_map,
    ewcfg.it_cosmetic: cosmetics.cosmetic_map,
    ewcfg.it_relic: static_relic.relic_map
}

# Populate item map, including all aliases.
for item in static_items.item_list:
    # Add item to its vendors' lists.
    for vendor in item.vendors:
        vendor_list = vendor_inv.get(vendor)

        if vendor_list == None:
            vendor_list = []
            vendor_inv[vendor] = vendor_list

        vendor_list.append(item.id_item)

# Populate food map, including all aliases.
for food in static_food.food_list:
    # Add food to its vendors' lists.
    for vendor in food.vendors:
        vendor_list = vendor_inv.get(vendor)

        if vendor_list == None:
            vendor_list = []
            vendor_inv[vendor] = vendor_list

        vendor_list.append(food.id_food)

# Populate fish map, including all aliases.
for fish in static_fish.fish_list:
    # Add fish to its vendors' lists.
    for vendor in fish.vendors:
        vendor_list = vendor_inv.get(vendor)

        if vendor_list == None:
            vendor_list = []
            vendor_inv[vendor] = vendor_list

        vendor_list.append(fish.id_fish)

# Populate cosmetic map.
for cosmetic in cosmetics.cosmetic_items_list:

    # Add cosmetics to its vendors' lists.
    for vendor in cosmetic.vendors:
        vendor_list = vendor_inv.get(vendor)

        if vendor_list == None:
            vendor_list = []
            vendor_inv[vendor] = vendor_list

        vendor_list.append(cosmetic.id_cosmetic)

for furniture in static_items.furniture_list:
    for vendor in furniture.vendors:
        vendor_list = vendor_inv.get(vendor)
        if vendor_list == None:
            vendor_list = []
            vendor_inv[vendor] = vendor_list
        vendor_list.append(furniture.id_furniture)

# Populate weapon map, including all aliases.
for weapon in weapons.weapon_list:
    for vendor in weapon.vendors:
        vendor_list = vendor_inv.get(vendor)

        if vendor_list == None:
            vendor_list = []
            vendor_inv[vendor] = vendor_list

        vendor_list.append(weapon.id_weapon)

#Populate relic map
for relic in static_relic.relic_list:
    for vendor in relic.vendors:
        vendor_list = vendor_inv.get(vendor)

        if vendor_list == None:
            vendor_list = []
            vendor_inv[vendor] = vendor_list

        vendor_list.append(relic.id_relic)

# List of items you can obtain via milling.
mill_results = []

# Gather all items that can be the result of milling.
for m in static_items.item_list:
    if m.acquisition == ewcfg.acquisition_milling:
        mill_results.append(m)
    else:
        pass

for m in static_food.food_list:
    if m.acquisition == ewcfg.acquisition_milling:
        mill_results.append(m)
    else:
        pass

for m in cosmetics.cosmetic_items_list:
    if m.acquisition == ewcfg.acquisition_milling:
        mill_results.append(m)
    else:
        pass

# List of items you can obtain via appraisal.
appraise_results = []

# Gather all items that can be the result of bartering.
for a in static_items.item_list:
    if a.acquisition == ewcfg.acquisition_bartering:
        appraise_results.append(a)
    else:
        pass

for a in static_food.food_list:
    if a.acquisition == ewcfg.acquisition_bartering:
        appraise_results.append(a)
    else:
        pass

for a in cosmetics.cosmetic_items_list:
    if a.acquisition == ewcfg.acquisition_bartering:
        appraise_results.append(a)
    else:
        pass

# List of items you can obtain via smelting.
smelt_results = []

# Gather all items that can be the result of smelting.
for s in static_items.item_list:
    if s.acquisition == ewcfg.acquisition_smelting:
        smelt_results.append(s)
    # So poudrins can be smelted with 2 royalty poudrins (this is obviously half-assed but i can't think of a better solution)
    elif s.id_item == ewcfg.item_id_slimepoudrin:
        smelt_results.append(s)
    else:
        pass

for s in static_food.food_list:
    if s.acquisition == ewcfg.acquisition_smelting:
        smelt_results.append(s)
    else:
        pass

for s in cosmetics.cosmetic_items_list:
    if s.acquisition == ewcfg.acquisition_smelting:
        smelt_results.append(s)
    else:
        pass

for s in weapons.weapon_list:
    if s.acquisition == ewcfg.acquisition_smelting:
        smelt_results.append(s)
    else:
        pass

for s in static_items.furniture_list:
    if s.acquisition == ewcfg.acquisition_smelting:
        smelt_results.append(s)
    else:
        pass

# List of items you can obtain via mining.
mine_results = []

# Gather all items that can be the result of mining.
for m in static_items.item_list:
    if m.acquisition == ewcfg.acquisition_mining:
        mine_results.append(m)
    else:
        pass

for m in static_food.food_list:
    if m.acquisition == ewcfg.acquisition_mining:
        mine_results.append(m)
    else:
        pass

for m in cosmetics.cosmetic_items_list:
    if m.acquisition == ewcfg.acquisition_mining:
        mine_results.append(m)
    else:
        pass
