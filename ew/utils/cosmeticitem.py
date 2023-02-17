from ew.backend import core as bknd_core
from ew.backend import item as bknd_item
from ew.backend.item import EwItem
from ew.static import cfg as ewcfg
from ew.static import cosmetics as cosmetics_static
from ew.utils import core as ewutils
from ew.utils.item import gen_item_props


async def dedorn_all_costumes():
    costume_count = 0
    # Grab costumes from the cache if enabled
    item_cache = bknd_core.get_cache(obj_type = "EwItem")
    if item_cache is not False:
        # separate search criteria for adorned or slimeoided
        p1 = {"context": "costume", "adorned": "true"}
        p2 = {"context": "costume", "slimeoid": "true"}
        # compile both results
        costumes_data = item_cache.find_entries(criteria={"item_props": p1})
        costumes_data += item_cache.find_entries(criteria={"item_props": p2})

        # Build a list that'll be handled in the same way
        costumes = list(map(lambda dat: dat.get("id_item"), costumes_data))
    else:
        costumes = bknd_core.execute_sql_query("SELECT id_item FROM items_prop WHERE name = 'context' AND value = 'costume' AND id_item IN (SELECT id_item FROM items_prop WHERE (name = 'adorned' OR name = 'slimeoid') AND value = 'true')")

    for costume_id in costumes:
        costume_item = EwItem(id_item=costume_id)

        costume_item.item_props['adorned'] = 'false'
        costume_item.item_props['slimeoid'] = 'false'

        costume_item.persist()

        costume_count += 1

    ewutils.logMsg("Dedorned {} costumes after full moon ended.".format(costume_count))


def get_cosmetic_max_durability(item_data: EwItem) -> int:
    """ Determine the max durability of a cosmetic item. """
    # Special item_props override comes first
    if item_data.item_props.get("original_durability"):
        return int(item_data.item_props["original_durability"])

    # Souls and scalps have preset durabilities and don't appear in the cosm map
    if item_data.item_props['id_cosmetic'] == 'soul':
        return ewcfg.soul_durability
    if item_data.item_props['id_cosmetic'] == 'scalp':
        return ewcfg.generic_scalp_durability

    # If there's no special rules, just look up the durability in the cosmetics list
    cosmetic_definition = cosmetics_static.cosmetic_map.get(item_data.item_props["id_cosmetic"])
    if cosmetic_definition:
        max_durability = cosmetic_definition.durability
    else:
        # Otherwise use the base cosmetic durability
        if item_data.item_props.get('rarity') == ewcfg.rarity_princeps:
            # Princeps have a different base durability for reasons
            max_durability = ewcfg.base_durability * 100
        else:
            max_durability = ewcfg.base_durability

    return max_durability


def repair_cosmetic(item_data: EwItem, new_durability: int = None) -> EwItem:
    """ Repair a cosmetic to its original durability. """
    if new_durability is None:
        new_durability = get_cosmetic_max_durability(item_data)

    item_data.item_props["durability"] = new_durability

    return item_data


def update_cosmetic(item_data: EwItem) -> EwItem:
    """ Update a cosmetic to the current item definition in the code base. """
    # TODO: Update cosmetics to save less properties. Do we really need to keep saving stats if they aren't coming back?
    cosm_def = cosmetics_static.cosmetic_map.get(item_data.item_props["id_cosmetic"])
    if cosm_def is None:
        ewutils.logMsg(f"WARNING: Couldn't find cosmetic definition under {item_data.item_props['id_cosmetic']} for item id {item_data.id_item}.")
        return item_data
    # TODO no. 2: Eventually refactor this into a simpler update_item. Probably as part of a wider item_props refactor.
    cosm_props = gen_item_props(cosm_def)
    item_data.item_props.update(cosm_props)

    return item_data


def restyle_cosmetic(item_data: EwItem, new_style: str) -> EwItem:
    """ Change a cosmetic item's style property."""
    if new_style not in ewcfg.fashion_styles:
        return item_data

    item_data.item_props["fashion_style"] = new_style

    return item_data


async def has_cosmetic(user_data, search_cosmetic: int | str, ignore_adorned = False, ignore_slimeoid = False, rarity = None) -> EwItem | None:
    """ See if a player has a matching cosmetic. """
    cosmetic_items = bknd_item.inventory(
        id_user=user_data.id_user,
        id_server=user_data.id_server,
        item_type_filter=ewcfg.it_cosmetic
    )

    item_sought = None
    item_data = None
    item_from_slimeoid = None

    search_id = int(search_cosmetic) if search_cosmetic.isnumeric() else -2

    for item in cosmetic_items:
        item_props = item["item_props"]
        if item.get('id_item') == search_id or search_cosmetic in ewutils.flattenTokenListToString(item.get('name')):

            if rarity and item_props.get('rarity') != rarity:
                continue

            if item_props.get('adorned') and ignore_adorned:
                continue

            if item_props.get('slimeoid') and ignore_slimeoid:
                continue

            if item_from_slimeoid is None and item_props.get("slimeoid") == 'true':
                item_from_slimeoid = item
                continue
            else:
                item_sought = item
                break

    if item_sought is None:
        item_sought = item_from_slimeoid

    if item_sought is not None:
        item_data = EwItem(id_item=item_sought["id_item"])

    return item_data
