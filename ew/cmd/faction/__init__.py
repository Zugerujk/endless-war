from ew.static import cfg as ewcfg
from . import factioncmds

cmd_map = {

    # Allow people to enlist
    ewcfg.cmd_vouch: factioncmds.vouch,
    ewcfg.cmd_vote: factioncmds.vote,
    ewcfg.cmd_hydraulicpress:factioncmds.hydraulicpress

}
