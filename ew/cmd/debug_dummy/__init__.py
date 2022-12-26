from ew.static import cfg as ewcfg
from . import debugcmds
from .debugcmds import *
from .debugutils import *

cmd_map = {

    # Inspect objects in a POI
    ewcfg.cmd_scrutinize: debugcmds.scrutinize,

    # debug commands
    # ewcfg.cmd_prefix + cmd_debug1: cmds.debug1,
    # ewcfg.cmd_prefix + cmd_debug2: cmds.debug2,
    # ewcfg.cmd_prefix + cmd_debug3: cmds.debug3,
    # ewcfg.cmd_prefix + cmd_debug4: cmds.debug4,
    # ewcfg.cmd_prefix + debug5: cmds.debug5,
    # ewcfg.cmd_prefix + cmd_debug6: cmds.debug6,
    # ewcfg.cmd_prefix + cmd_debug7: cmds.debug7,
    # ewcfg.cmd_prefix + cmd_debug8: cmds.debug8,

    ewcfg.cmd_prefix + cmd_debug9: debugcmds.debug9,

    ewcfg.cmd_changegamestate: debugcmds.change_gamestate,
    ewcfg.cmd_deletegamestate: debugcmds.delete_gamestate,
    ewcfg.cmd_display_states: debugcmds.display_states,
    # ewcfg.cmd_press_button: cmds.elevator_press,
    # ewcfg.cmd_call_elevator: cmds.elevator_call,

}
