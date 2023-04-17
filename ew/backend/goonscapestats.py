import time
import math

from . import core as bknd_core
from ..static import cfg as ewcfg
from ew.utils.frontend import send_response

from ew.backend.questrecords import create_quest_record
from ew.backend.questrecords import fetch_quest_records
from ew.backend.item import item_create


class EwGoonScapeStat:

    def __init__(self, id_user, id_server, stat_name):

        self.id_user = id_user
        self.id_server = id_server
        self.stat = stat_name

        try:

            conn_info = bknd_core.databaseConnect()
            conn = conn_info.get('conn')
            cursor = conn.cursor()

            # Retrieve data of given stat
            cursor.execute("SELECT {}, {} FROM goonscape_stats WHERE id_user = %s AND id_server = %s".format(
                ewcfg.gs_stat_to_level_col.get(self.stat),
                ewcfg.gs_stat_to_xp_col.get(self.stat),
            ), (
                self.id_user,
                self.id_server,
            ))
            result = cursor.fetchone()

            if result != None:
                self.level = result[0]
                self.xp = result[1]
            else:
                # Create a new entry for the stat if no existing one was found
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

        finally:
            # Clean up the database handles.
            cursor.close()
            bknd_core.databaseClose(conn_info)


    def persist(self):
        bknd_core.execute_sql_query(
            "UPDATE goonscape_stats SET {} = %s, {} = %s WHERE id_user = %s AND id_server = %s".format(
                ewcfg.gs_stat_to_level_col.get(self.stat),
                ewcfg.gs_stat_to_xp_col.get(self.stat),
            ), (
                self.level,
                self.xp,
                self.id_user,
                self.id_server
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


    async def add_xp(self, value):
        level_up_message = None
        responses = []

        if value < 0:
            self.xp = max(0, self.xp + value)
            
            #check for level down cap at 99
            xp_level = min(99, self.xp_to_level(self.xp+1) - 1)
            start_level = self.level

            #if level decreased
            if start_level > xp_level:
                # Persist before waiting, please
                self.level = xp_level
            self.persist() 

            for x in range(start_level-1, xp_level-1,-1):

                line_1 = "YOU SUCK. YOU LOST A {stat} LEVEL! ".format(stat = self.stat.capitalize()) 
                length_1 = len(line_1)
                line_2 = "[Your {stat} level is now {level}.]".format(stat = self.stat.capitalize(), level = x).center(length_1)
                line_3 = "We hope you're enjoying your GoonScape members' experience so far. Interested in becoming a member? If so we've got a great offer for you:".center(length_1)
                line_4 = "[- 75% off your first month's membership.]".center(length_1)
                line_5 = "[- 12 additional spins on the Reel of Fortune]".center(length_1)
                line_6 = "[- 2,000 Slimecoin to spend on exclusive items.]".center(length_1)
                line_7 = "You'll also keep any days of trial membership remaining.".center(length_1)
                line_8 = "Hurry while this amazing offer lasts!".center(length_1)
                line_9 = ";I want to sign up.".center(length_1) +"<-"
                line_10 = ";I'm not ready yet.".center(length_1)


                level_up_message = f"```ini\n{line_1}\n{line_2}\n{line_3}\n\n{line_4}\n{line_5}\n{line_6}\n\n{line_7}\n{line_8}\n\n\n{line_9}\n{line_10}```\n"    

                responses.append(level_up_message)

        else: 
            self.xp += value

            #check for level up cap at 99
            xp_level = min(99, self.xp_to_level(self.xp) - 1)
            start_level = self.level

            #if level increased
            if start_level < xp_level:
                # Persist before waiting, please
                self.level = xp_level

            self.persist() 

            for x in range(start_level+1, xp_level+1):

                line_1 = "Congradulations, you just advanced a {stat} level.".format(stat = self.stat.capitalize()) 
                length_1 = len(line_1)
                line_2 = "[Your {stat} level is now {level}.]".format(stat = self.stat.capitalize(), level = x).center(length_1)
                line_3 = ";Click here to continue".center(length_1)


                level_up_message = f"```ini\n{line_1}\n{line_2}\n{line_3}\n```"    

                responses.append(level_up_message)

            if start_level < xp_level and self.level == 99:
                capes = await fetch_quest_records(self.id_server, "skill_cape", self.stat)
                if self.stat == ewcfg.goonscape_pee_stat:
                    for cape in capes:
                        if cape[1] == self.id_user: #the cape should already exist, so exit.
                            return responses
                placement = len(capes) + 1
                item_create( #making the skill cape
                    item_type=ewcfg.it_cosmetic,
                    id_user=self.id_user,
                    id_server=self.id_server,
                    item_props={
                        'id_cosmetic': '{skill}skillcape'.format(skill=self.stat),
                        'cosmetic_name': "{skill} cape".format(skill=self.stat.capitalize()),
                        'cosmetic_desc': ewcfg.gs_stat_to_cape_description.get(self.stat).format(user_id=self.id_user,placement=placement),
                        'str_onadorn': ewcfg.str_cape_onadorn,
                        'str_unadorn': ewcfg.str_cape_unadorn,
                        'str_onbreak': ewcfg.str_cape_onbreak,
                        'rarity': ewcfg.rarity_promotional,
                        'size': 0,
                        'attack':0,
                        'defense':0,
                        'speed':0,
                        'ability': None,
                        'durability': 42069, #man fuck this noise
                        'original_durability': 42069,
                        'fashion_style': ewcfg.style_skill,
                        'freshness': 1,
                        'adorned': 'true',
                        'soulbound': 'true'
                    }
                )
                await create_quest_record(int(time.time()), self.id_user, self.id_server, "skill_cape", self.stat)

        return responses
