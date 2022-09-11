from . import core as bknd_core
from ..static import cfg as ewcfg

#this needs system expansion later
#when npcs get added i will add the ways to pull from the database and use records
#important to have record creation for now to track who wins skill capes first

class EwQuestRecord:
    def __init__(self, time_stamp, id_user, id_server, record_type, record_data):
        self.time_stamp = time_stamp
        self.id_user = id_user
        self.id_server = id_server
        self.record_type = record_type
        self.record_data = record_data



async def create_quest_record(_time_stamp, _id_user, _id_server, _record_type, _record_data):
    bknd_core.execute_sql_query(
        "INSERT INTO quest_records({time_stamp}, {id_user}, {id_server}, {record_type}, {record_data}) VALUES(%s, %s, %s, %s, %s)".format(
            time_stamp = ewcfg.col_time_stamp,
            id_user = ewcfg.col_id_user, 
            id_server = ewcfg.col_id_server,
            record_type = ewcfg.col_record_type,
            record_data = ewcfg.col_record_data,
        ), (
            _time_stamp, 
            _id_user, 
            _id_server, 
            _record_type, 
            _record_data
        )
    )

