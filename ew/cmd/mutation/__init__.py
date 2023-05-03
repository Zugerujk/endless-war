from ew.static import cfg as ewcfg
from . import mutationcmds

cmd_map = {

    # Setting mutations
    ewcfg.cmd_chemo: mutationcmds.chemo,
    ewcfg.cmd_graft: mutationcmds.graft,

    # Mutation only Cmds
    ewcfg.cmd_preserve: mutationcmds.preserve,
    ewcfg.cmd_stink: mutationcmds.waft,
    ewcfg.cmd_track: mutationcmds.track_oneeyeopen,
    ewcfg.cmd_shakeoff: mutationcmds.shakeoff,
    ewcfg.cmd_clench: mutationcmds.clench,
    ewcfg.cmd_bleedout: mutationcmds.bleedout,
    ewcfg.cmd_piss: mutationcmds.piss,
    ewcfg.cmd_fursuit: mutationcmds.fursuit,
    ewcfg.cmd_devour: mutationcmds.devour,
    ewcfg.cmd_longdrop: mutationcmds.longdrop,
    ewcfg.cmd_skullbash: mutationcmds.skullbash,
    ewcfg.cmd_slap: mutationcmds.slap,
    ewcfg.cmd_thirdeye: mutationcmds.tracker,
    ewcfg.cmd_currentrotation: mutationcmds.display_current_rotation,
    # Debug commands
    ewcfg.cmd_forcegraft: mutationcmds.forcegraft,
    ewcfg.cmd_forcechemo: mutationcmds.forcechemo,
    ewcfg.cmd_nextrotation:mutationcmds.display_current_rotation,
    ewcfg.cmd_add_mut_rotation:mutationcmds.add_rotation_mut,
    ewcfg.cmd_clear_mut_rotation:mutationcmds.drop_rotation_mut,
    ewcfg.cmd_change_rotation_stat:mutationcmds.change_rotation_stat
}

apt_dm_cmd_map = {

    # !stink
    ewcfg.cmd_stink: mutationcmds.waft,

    # !bleedout
    ewcfg.cmd_bleedout: mutationcmds.bleedout,

    # more oeo
    ewcfg.cmd_track: mutationcmds.track_oneeyeopen,

    # preserve
    ewcfg.cmd_preserve: mutationcmds.preserve,

    # clench your cheeks
    ewcfg.cmd_clench: mutationcmds.clench,

    # piss on the floor
    ewcfg.cmd_piss: mutationcmds.piss,

    ewcfg.cmd_longdrop: mutationcmds.longdrop,

    ewcfg.cmd_thirdeye: mutationcmds.tracker,
    ewcfg.cmd_nextrotation:mutationcmds.display_current_rotation

}
