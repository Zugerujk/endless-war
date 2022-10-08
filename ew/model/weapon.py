from ..static import cfg as ewcfg

""" A weapon object which adds flavor text to kill/shoot. """


class EwWeapon:
    item_type = "weapon"

    # A unique name for the weapon. This is used in the database and typed by
    # users, so it should be one word, all lowercase letters.
    id_weapon = ""

    # An array of names that might be used to identify this weapon by the player.
    alias = None  # []

    # Displayed when !equip-ping this weapon
    str_equip = ""

    # Displayed when this weapon is used for a !kill
    str_kill = ""

    # Displayed to the dead victim in the sewers. Brief phrase such as "gunned down" etc.
    str_killdescriptor = ""

    # Displayed when viewing the !trauma of another player.
    str_trauma = ""

    # Displayed when viewing the !trauma of yourself.
    str_trauma_self = ""

    # like str_weapon but without the article
    str_name = ""

    # Displayed when viewing the !weapon of another player.
    str_weapon = ""

    # Displayed when viewing the !weapon of yourself.
    str_weapon_self = ""

    # Same as weapon and weapon_self, but used when the player's weapon skill is max.
    str_weaponmaster = ""
    str_weaponmaster_self = ""

    # Displayed when a non-lethal hit occurs.
    str_damage = ""

    # Displayed when two players wielding the same weapon !spar with each other.
    str_duel = ""

    # Function that applies the special effect for this weapon.
    fn_effect = None  # []

    # Displayed when a weapon effect causes a critical hit.
    str_crit = ""

    # Displayed when a weapon effect causes a miss.
    str_miss = ""

    # Displayed when a weapon effect causes backfire damage
    str_backfire = ""

    # Displayed when !inspect-ing
    str_description = ""

    # Displayed when reloading
    str_reload = ""

    # Displayed when the weapon used it's last ammo
    str_reload_warning = ""

    # Displayed in a scalp's description.
    str_scalp = ""

    #Text when brandishing a weapon
    str_brandish = ""

    # Clip size
    clip_size = 0

    # Cost
    price = 0

    # Hard Cooldown
    cooldown = 0

    # Vendor
    vendors = None  # []

    # Classes the weapon belongs to
    classes = None  # []

    acquisition = "dojo"

    # Statistics metric
    stat = ""

    # sap needed to fire
    # sap_cost = 0

    # length of captcha you need to solve to fire
    captcha_length = 0

    # whether the weapon is a tool
    is_tool = 0

    # an array for storing extra string data for different tools
    tool_props = {}

    def __init__(
            self,
            id_weapon = "",
            alias = [],
            str_equip = "",
            str_kill: list = [],
            str_killdescriptor = "",
            str_trauma = "",
            str_trauma_self = "",
            str_name = "",
            str_weapon = "",
            str_weapon_self = "",
            str_damage = "",
            str_duel = "",
            str_weaponmaster = "",
            str_weaponmaster_self = "",
            fn_effect = None,
            str_crit = "",
            str_miss = "",
            str_backfire = "",
            str_description = "",
            str_reload = "",
            str_reload_warning = "",
            str_scalp = "",
            str_brandish = "",
            clip_size = 0,
            price = 0,
            cooldown = 0,
            vendors = [],
            classes = [],
            acquisition = "dojo",
            stat = "",
            # sap_cost = 0,
            captcha_length = 0,
            is_tool = 0,
            tool_props = None
    ):
        self.item_type = ewcfg.it_weapon

        self.id_weapon = id_weapon
        self.alias = alias
        self.str_equip = str_equip
        self.str_kill = str_kill
        self.str_killdescriptor = str_killdescriptor
        self.str_trauma = str_trauma
        self.str_trauma_self = str_trauma_self
        self.str_name = str_name
        self.str_weapon = str_weapon
        self.str_weapon_self = str_weapon_self
        self.str_damage = str_damage
        self.str_duel = str_duel
        self.str_weaponmaster = str_weaponmaster
        self.str_weaponmaster_self = str_weaponmaster_self
        self.fn_effect = fn_effect
        self.str_crit = str_crit
        self.str_miss = str_miss
        self.str_backfire = str_backfire
        self.str_description = str_description
        self.str_reload = str_reload
        self.str_reload_warning = str_reload_warning
        self.str_scalp = str_scalp
        self.str_brandish = str_brandish
        self.clip_size = clip_size
        self.price = price
        self.cooldown = cooldown
        self.vendors = vendors
        self.classes = classes
        self.acquisition = acquisition
        self.stat = stat
        # self.sap_cost = sap_cost
        self.captcha_length = captcha_length
        self.is_tool = is_tool
        self.tool_props = tool_props,
# self.str_name = self.str_weapon,
