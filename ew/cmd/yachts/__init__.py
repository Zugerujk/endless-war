from ew.static import cfg
from . import yachtcmds

cmd_map = {
cfg.cmd_rentyacht:yachtcmds.rentyacht,
cfg.cmd_board:yachtcmds.board_ship,
cfg.cmd_avast:yachtcmds.avast,
cfg.cmd_man:yachtcmds.man,
cfg.cmd_setsail:yachtcmds.setsail
}



apt_dm_cmd_map = {

}