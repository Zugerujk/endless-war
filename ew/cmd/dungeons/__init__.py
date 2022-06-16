from .dungeoncmds import tutorial_cmd
from ew.static import cfg as ewcfg
from . import dungeoncmds


cmd_map = {
    ewcfg.cmd_blurbcontext:dungeoncmds.display_blurb_context,
    ewcfg.cmd_addblurb:dungeoncmds.add_blurb,
    ewcfg.cmd_deleteblurb:dungeoncmds.delete_blurb,
    ewcfg.cmd_displayblurbs:dungeoncmds.displayblurbs



}