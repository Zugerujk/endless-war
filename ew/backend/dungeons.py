from . import core as bknd_core

from ..static import cfg as ewcfg
from ..utils import core as ewutils


class EwGamestate():
    # server id, duh
    id_server = -1

    # name of the state
    id_state = ""

    # setting of the state, on or off
    bit = True

    # additional value for unique states
    value = ""

    #numerical value

    number = 0

    def __init__(
            self,
            id_state = None,
            id_server = None
    ):

        if id_server is not None and id_state is not None:
            self.id_server = id_server
            self.id_state = id_state
            try:
                data = bknd_core.execute_sql_query("SELECT {col_bit}, {col_value}, {col_number} FROM gamestates WHERE {id_server} = %s AND {id_state} = %s".format(

                    id_state=ewcfg.col_id_state,
                    id_server=ewcfg.col_id_server,
                    col_bit=ewcfg.col_bit,
                    col_value=ewcfg.col_value,
                    col_number=ewcfg.col_number

                ), (
                    self.id_server,
                    self.id_state
                ))
                # Retrieve data if the object was found
                if len(data) > 0:
                    self.id_state = id_state
                    self.bit = data[0][0]
                    self.value = data[0][1]
                    self.number = data[0][2]
                else:
                    self.bit = None

            except:
                ewutils.logMsg("Failed to retrieve gamestate {} from database.".format(self.id_state))

    def persist(self):
        bknd_core.execute_sql_query(
            "REPLACE INTO gamestates ({id_server}, {id_state},  {col_bit}, {col_value}, {col_number}) VALUES (%s, %s, %s, %s, %s)".format(
                id_server=ewcfg.col_id_server,
                id_state=ewcfg.col_id_state,
                col_bit=ewcfg.col_bit,
                col_value=ewcfg.col_value,
                col_number=ewcfg.col_number
            ), (
                self.id_server,
                self.id_state,
                self.bit,
                self.value,
                self.number
            ))


class EwBlurb():
    id_server = -1,

    id_blurb = 0 #a numerical identifier for blurbs

    blurb = "", #the flavor text itself

    context = "" #what the blurb is associated with, i.e. bazaar_distractions, browse lists, etc.

    subcontext = "" #specific limitations or attributes the blurb might have, zone flavor might list specific districts here

    subsubcontext = "" #any other criteria for a blurb to appear. maybe you only see some text while high

    active = 1 #whether a blurb gets pulled or not

    dateadded = None #when the blurb is added

    def __init__(
            self,
            id_blurb = None,
            id_server = None
    ):

        if id_server is not None and id_blurb is not None:
            self.id_server = id_server
            self.id_blurb = id_blurb
            try:
                data = bknd_core.execute_sql_query("SELECT {col_blurb}, {col_context}, {col_subcontext}, {col_subsubcontext}, {col_active}, {col_dateadded} FROM blurbs WHERE {id_server} = %s AND {col_id_id_blurb} = %s".format(

                    col_id_id_blurb = ewcfg.col_id_id_blurb,
                    col_blurb = ewcfg.col_id_blurb,
                    col_context = ewcfg.col_id_context,
                    col_subcontext = ewcfg.col_id_subcontext,
                    col_subsubcontext = ewcfg.col_id_subsubcontext,
                    col_active = ewcfg.col_id_active,
                    col_dateadded = ewcfg.col_id_dateadded,
                    id_server = ewcfg.col_id_server

                ), (
                    self.id_server,
                    self.id_blurb
                ))
                # Retrieve data if the object was found
                if len(data) > 0:
                    self.id_blurb = id_blurb
                    self.blurb = data[0][0]
                    self.context = data[0][1]
                    self.subcontext = data[0][2],
                    self.subsubcontext = data[0][3],
                    self.active = data[0][4],
                    self.dateadded=data[0][5]
                else:
                    self.bit = None

            except:
                ewutils.logMsg("Failed to retrieve blurb {} from database.".format(self.id_blurb))

    def persist(self):
        bknd_core.execute_sql_query(
            "REPLACE INTO blurbs ({col_id_server}, {col_id_id_blurb}, {col_blurb}, {col_context}, {col_subcontext}, {col_subsubcontext}, {col_active}, {col_dateadded}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)".format(
                col_id_id_blurb=ewcfg.col_id_id_blurb,
                col_blurb=ewcfg.col_id_blurb,
                col_context=ewcfg.col_id_context,
                col_subcontext=ewcfg.col_id_subcontext,
                col_subsubcontext=ewcfg.col_id_subsubcontext,
                col_active=ewcfg.col_id_active,
                col_dateadded=ewcfg.col_id_dateadded,
                col_id_server=ewcfg.col_id_server
            ), (
                self.id_server,
                self.id_blurb,
                self.blurb,
                self.context,
                self.subcontext,
                self.subsubcontext,
                self.active,
                self.dateadded
            ))