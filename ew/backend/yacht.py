
class EwYacht():
    id_yacht = -1 #ID of the yacht
    yacht_name = '' #Name of the yacht
    thread_id = -1 #Identifier for the thread's name
    owner = -1 #User ID of the yacht's owner
    flood = 0 #Percentage of water the yacht is taking
    filth = 0 #Level of filth the boat currently holds
    helm = -1 #Player manning the helm
    cannon = -1 #Player manning the arms and belowdeck
    storehouse = -1 #Player manning the storehouse
    poopdeck = -1 #Player currently manning the poopdeck


class EwYachtStat():
    id_yacht = -1 #Name of the affected yacht
    id_stat = "" #The stat in question
    target = 0 #Targeted yacht or player
    quantiy = "" #Necessary quantity value