from ew.static import cfg as ewcfg
from . import cosmeticcmds

cmd_map = {

    # Smoke a cosmetic. preferably a cigarette
    ewcfg.cmd_smoke: cosmeticcmds.smoke,

    # Vape a vape
    ewcfg.cmd_vape: cosmeticcmds.vape,
    ewcfg.cmd_vapealt1: cosmeticcmds.vape,

    # Wearing cosmetics
    ewcfg.cmd_adorn: cosmeticcmds.adorn,
    ewcfg.cmd_dedorn: cosmeticcmds.dedorn,
    ewcfg.cmd_dedorn_alt1: cosmeticcmds.dedorn,

    # Reworking/fixing
    ewcfg.cmd_sew: cosmeticcmds.sew,
    ewcfg.cmd_retrofit: cosmeticcmds.retrofit,
    ewcfg.cmd_bespoke: cosmeticcmds.bespoke,
    ewcfg.cmd_bespoke_alt1: cosmeticcmds.bespoke,

    # Dyeing
    ewcfg.cmd_dyecosmetic: cosmeticcmds.dye,
    ewcfg.cmd_dyecosmetic_alt1: cosmeticcmds.dye,
    ewcfg.cmd_dyecosmetic_alt2: cosmeticcmds.dye,
    ewcfg.cmd_dyecosmetic_alt3: cosmeticcmds.dye,

    # admins manipulate/make items
    ewcfg.cmd_balance_cosmetics: cosmeticcmds.balance_cosmetics,

}

apt_dm_cmd_map = {

    # Smoke a cosmetic. preferably a cigarette
    ewcfg.cmd_smoke: cosmeticcmds.smoke,

    # Vape a vape
    ewcfg.cmd_vape: cosmeticcmds.vape,
    
    # Wearing cosmetics
    ewcfg.cmd_adorn: cosmeticcmds.adorn,
    ewcfg.cmd_dedorn: cosmeticcmds.dedorn,
    ewcfg.cmd_dedorn_alt1: cosmeticcmds.dedorn,

    # Dyeing
    ewcfg.cmd_dyecosmetic: cosmeticcmds.dye,
    ewcfg.cmd_dyecosmetic_alt1: cosmeticcmds.dye,
    ewcfg.cmd_dyecosmetic_alt2: cosmeticcmds.dye,
    ewcfg.cmd_dyecosmetic_alt3: cosmeticcmds.dye,

}
