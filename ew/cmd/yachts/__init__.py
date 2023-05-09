from ew.static import cfg
from . import yachtcmds

cmd_map = {
cfg.cmd_rentyacht:yachtcmds.rentyacht,
cfg.cmd_board:yachtcmds.board_ship,
cfg.cmd_avast:yachtcmds.avast,
cfg.cmd_man:yachtcmds.man,
cfg.cmd_setsail:yachtcmds.setsail,
cfg.cmd_unboard:yachtcmds.unboard,
cfg.cmd_gangplank:yachtcmds.gangplank,
cfg.cmd_firecannon:yachtcmds.fire_cannon,
cfg.cmd_aim:yachtcmds.aim_ship,
cfg.cmd_stock_ammo:yachtcmds.stock,
cfg.cmd_loadcannon:yachtcmds.load,
cfg.cmd_aimship:yachtcmds.aim_ship,
cfg.cmd_swab:yachtcmds.swab,
cfg.cmd_scoop:yachtcmds.scoop_ship,
cfg.cmd_fixship:yachtcmds.repair_ship
}



apt_dm_cmd_map = {

}