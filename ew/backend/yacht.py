import time
import random
from . import core as bknd_core
from ..static import cfg as ewcfg
from ew.utils import core as coreutils


class EwYacht():
    id_server = -1 #lol this is on everything
    yacht_name = '' #Name of the yacht
    thread_id = -1 #Identifier for the thread's name
    owner = -1 #User ID of the yacht's owner
    flood = 0 #Percentage of water the yacht is taking
    filth = 0 #Level of filth the boat currently holds
    helm = -1 #Player manning the helm
    cannon = -1 #Player manning the arms and belowdeck
    storehouse = -1 #Player manning the storehouse
    poopdeck = -1 #Player currently manning the poopdeck
    xcoord = -1 #Ship's x coordinate
    ycoord = -1 #Ship's y coordinate
    speed = 0 #Ship's speed
    direction = "" #Ship's orientation
    slimes = 0 #Slime the ship has in it

    def __init__(self, id_thread = None, id_server = None):

        self.id_server = id_server
        if id_server is not None and id_thread is not None:
            self.thread_id = id_thread
            try:
                conn_info = bknd_core.databaseConnect()
                conn = conn_info.get('conn')
                cursor = conn.cursor()

                # Retrieve object

                cursor.execute(
                    "SELECT {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} FROM yachts WHERE thread_id = %s AND id_server = %s".format(
                        ewcfg.col_name_yacht,
                        ewcfg.col_slimes,
                        ewcfg.col_id_user,
                        ewcfg.col_flood,
                        ewcfg.col_filth,
                        ewcfg.col_helm,
                        ewcfg.col_cannon,
                        ewcfg.col_storehouse,
                        ewcfg.col_poopdeck,
                        ewcfg.col_xcoord,
                        ewcfg.col_ycoord,
                        ewcfg.col_speed,
                        ewcfg.col_direction
                    ), (
                        self.thread_id,
                        self.id_server
                    ))
                result = cursor.fetchone()

                self.yacht_name = result[0]
                self.slimes = result[1]
                self.owner = result[2]
                self.flood = result[3]
                self.filth = result[4]
                self.helm = result[5]
                self.cannon = result[6]
                self.storehouse = result[7]
                self.poopdeck = result[8]
                self.xcoord = result[9]
                self.ycoord = result[10]
                self.speed = result[11]
                self.direction = result[12]

            finally:
                cursor.close()
                bknd_core.databaseClose(conn_info)


    def persist(self):
        try:
            conn_info = bknd_core.databaseConnect()
            conn = conn_info.get('conn')
            cursor = conn.cursor()

            # Save the object.
            cursor.execute(
                "REPLACE INTO yachts({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
                    ewcfg.col_id_server,
                    ewcfg.col_slimes,
                    ewcfg.col_name_yacht,
                    ewcfg.col_thread_id,
                    ewcfg.col_id_user,
                    ewcfg.col_flood,
                    ewcfg.col_filth,
                    ewcfg.col_helm,
                    ewcfg.col_cannon,
                    ewcfg.col_storehouse,
                    ewcfg.col_poopdeck,
                    ewcfg.col_xcoord,
                    ewcfg.col_ycoord,
                    ewcfg.col_speed,
                    ewcfg.col_direction

                ), (
                    self.id_server,
                    self.slimes,
                    self.yacht_name,
                    self.thread_id,
                    self.owner,
                    self.flood,
                    self.filth,
                    self.helm,
                    self.cannon,
                    self.storehouse,
                    self.poopdeck,
                    self.xcoord,
                    self.ycoord,
                    self.speed,
                    self.direction
                ))
        finally:
            # Clean up the database handles.
            cursor.close()
            bknd_core.databaseClose(conn_info)

    def getYachtStats(self): #because the stat quantity
        stats = []
        try:
            conn_info = bknd_core.databaseConnect()
            conn = conn_info.get('conn')
            cursor = conn.cursor()

            # Retrieve object

            cursor.execute(
                "SELECT {} FROM yacht_stats WHERE id_server = %s and thread_id = %s".format(
                    ewcfg.col_id_idstat
                ), (
                    self.id_server,
                    self.thread_id
                ))
            results = cursor.fetchall()

            for result  in results:
                result_obj = EwYachtStat(id_server=self.id_server, id_stat=result[0])
                stats.append(result_obj)
        finally:
            cursor.close()
            bknd_core.databaseClose(conn_info)
        return stats

    def change_slimes(self, n = 0, source = None):
        change = int(n)
        self.slimes += change

    async def get_thread(self):
        client = coreutils.get_client()
        server = client.get_guild(self.id_server)
        channel = await server.fetch_channel(self.thread_id)
        return channel

    def applyStat(self, stat_type, quantity = 0, target = 0):
        bknd_core.execute_sql_query("insert into yacht_stats({}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s)".format(
            ewcfg.col_thread_id,
            ewcfg.col_type_stat,
            'target',
            ewcfg.col_quantity,
            ewcfg.col_id_server),(
            self.thread_id,
            stat_type,
            target,
            quantity,
            self.id_server
        ))

    def clearStat(self, id_stat):
        bknd_core.execute_sql_query("delete from yacht_stats where {} = %s".format(
            ewcfg.col_id_idstat),(
            id_stat,
        ))

    def accumulate_filth(self, amount_filth = 1):
        self.filth += amount_filth
        self.persist()

    def filth_check(self):
        if random.randint(50, 150) > self.filth:
            return False
        return True

class EwYachtStat():
    thread_id = -1 #Name of the affected yacht
    id_stat = -1 #Unique value for the stat
    type_stat = "" #The stat in question
    target = 0 #Targeted yacht or player
    quantity = 0 #Necessary quantity value
    id_server = -1 # server id

    def __init__(self, id_stat, id_server):
        if id_server is not None and id_stat is not None:
            self.id_stat = id_stat
            self.id_server = id_server

        try:
            conn_info = bknd_core.databaseConnect()
            conn = conn_info.get('conn')
            cursor = conn.cursor()

            # Retrieve object

            cursor.execute(
                "SELECT {}, {}, {}, {} FROM yacht_stats WHERE id_stat = %s AND id_server = %s".format(
                    'target',
                    ewcfg.col_quantity,
                    ewcfg.col_type_stat,
                    ewcfg.col_thread_id
                ), (
                    self.id_stat,
                    self.id_server
                ))
            result = cursor.fetchone()
            if result is not None:
                self.target = result[0]
                self.quantity = result[1]
                self.type_stat = result[2]
                self.thread_id = result[3]

        finally:
            cursor.close()
            bknd_core.databaseClose(conn_info)


    def persist(self):
        try:
            conn_info = bknd_core.databaseConnect()
            conn = conn_info.get('conn')
            cursor = conn.cursor()

            # Save the object.
            cursor.execute(
                "REPLACE INTO yacht_stats({}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s)".format(
                    ewcfg.col_id_server,
                    ewcfg.col_thread_id,
                    ewcfg.col_id_stat,
                    'target',
                    ewcfg.col_quantity,
                    ewcfg.col_type_stat
                ), (
                    self.id_server,
                    self.thread_id,
                    self.id_stat,
                    self.target,
                    self.quantity,
                    self.type_stat

                ))
        finally:
            # Clean up the database handles.
            cursor.close()
            bknd_core.databaseClose(conn_info)

    def __eq__(self, other): #shout out to operator overloading dawg school was useful once
        if other == self.type_stat:
            return True
        else:
            return False

