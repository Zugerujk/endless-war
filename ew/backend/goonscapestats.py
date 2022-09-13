import time
import math

from . import core as bknd_core
from ..static import cfg as ewcfg
from ew.utils.frontend import send_response

from ew.backend.questrecords import create_quest_record


goonscape_mine_stat = "mining"
goonscape_fish_stat = "fishing"
goonscape_farm_stat = "farming"
goonscape_eat_stat = "feasting"




class EwGoonScapeStat:

    def __init__(self, id_user, id_server, stat_name):

        self.id_user = id_user
        self.id_server = id_server
        self.stat = stat_name


        try:

            conn_info = bknd_core.databaseConnect()
            conn = conn_info.get('conn')
            cursor = conn.cursor()

            # Retrieve object
            cursor.execute("SELECT {}, {} FROM goonscape_stats WHERE id_user = %s".format(
                self.stat + "_level",
                self.stat + "_xp",
            ), (self.id_user,))
            result = cursor.fetchone()

            if result != None:
                self.level = result[0]
                self.xp = result[1]
            else:
                #insert if there is no exiting row for user
                cursor.execute("INSERT INTO goonscape_stats({}, {}) VALUES(%s, %s)".format(
                    ewcfg.col_id_user, 
                    ewcfg.col_id_server
                ), (
                    self.id_user,
                    self.id_server,
                ))
                   
                conn.commit()
                
                self.level = 1
                self.xp = 0

            #bknd_core.cache_data(self)

        finally:
            # Clean up the database handles.
            cursor.close()
            bknd_core.databaseClose(conn_info)


    def persist(self):
        bknd_core.execute_sql_query(
            "UPDATE goonscape_stats SET {level_column} = %s, {xp_column} = %s WHERE id_user = %s".format(
                level_column=self.stat + "_level",
                xp_column=self.stat + "_xp",
            ), (
                self.level,
                self.xp,
                self.id_user,
            )
        )





    def equate(self, xp):
        return math.floor(xp + 300 * (2 ** (xp / 7.0)))

    def level_to_xp(self, level):
        return math.floor(
            sum((self.equate(lvl) for lvl in range(1, level))) / 4)

    def xp_to_level(self, xp):
        level = 1

        while self.level_to_xp(level) < xp:
            level += 1

        return level


    async def add_xp(self, value, channel):
        level_up_message = None

        if value <= 0:
            pass
        else: 
            self.xp += value

            #check for level up cap at 99
            xp_level = min(99, self.xp_to_level(self.xp) - 1)

            #if level increased
            if self.level < xp_level:


                
                for x in range(self.level+1, xp_level+1):

                    line_1 = "Congradulations, you just advanced a {stat} level.".format(stat = self.stat.capitalize()) 
                    length_1 = len(line_1)
                    line_2 = "[Your {stat} level is now {level}.]".format(stat = self.stat.capitalize(), level = x).center(length_1)
                    line_3 = ";Click here to continue".center(length_1)


                    level_up_message = f"```ini\n{line_1}\n{line_2}\n{line_3}\n```"    

                    await send_response(level_up_message, name = "no_name", channel = channel, format_name = False)         


                
                self.level = xp_level   

                if self.level == 99:
                    await create_quest_record(int(time.time()), self.id_user, self.id_server, "skill_cape", self.stat)

            self.persist()          
            

        return level_up_message






async def add_xp(id_user, id_server, channel, stat_name, xp_value):

    stat = EwGoonScapeStat(id_user, id_server, stat_name)
    await stat.add_xp(xp_value, channel)