#Values are sorted by the chance to the drop an item, and then the minimum and maximum amount of times to drop that item.
from ..model.hunting import EwAttackType
from ..model.hunting import EwNpc
from . import cfg as ewcfg


from ew.utils import npcutils
from . import poi as poi_static

npc_list = [
    EwNpc(
        id_npc="thedrinkster",  # unique id for each npc
        active = False,  # whether an npc spawns
        str_name = "The Drinkster",  # Name of the NPC
        poi_list = [ewcfg.poi_id_711, ewcfg.poi_id_poudrinalley],  # list of locations an NPC roams in
        dialogue = {"talk":["heyyyy. stupid hoser pucknick bitches. i'm gonna steal your drink. huehuehuehuehuehuehuehue"]},  # list of dialogue an npc can use
        func_ai = npcutils.generic_npc_action,  # function the enemy's AI uses
        image_profile = "https://www.cupholdersplus.com/mm5/graphics/00000001/BD-Shorty-Drinkster-Bench-Seat-Console-Fiesta_540x540.jpg",  # image link to add to dialogue embeds
        defaultslime = 200,
        defaultlevel = 1,
        rewards = [
        {ewcfg.item_id_slimepoudrin: [75, 5, 6]},
        {ewcfg.rarity_patrician: [20, 1, 1]},
        {ewcfg.item_id_monsterbones: [100, 1, 3]},
        ]
    ),
EwNpc(
        id_npc="thehostiledrinkster",  # unique id for each npc
        active = False,  # whether an npc spawns
        str_name = "The Hostile Drinkster",  # Name of the NPC
        poi_list = [ewcfg.poi_id_downtown],  # list of locations an NPC roams in
        dialogue = {"talk":["heyyyy. stupid hoser pucknick bitches. i'm gonna steal your drink. huehuehuehuehuehuehuehue"],
                    "hit":["FUCK YOU YOU MADE ME SPILL MY DRINK!"],
                    "die": ["OH SHIT"]},  # list of dialogue an npc can use
        func_ai = npcutils.generic_npc_action,  # function the enemy's AI uses
        image_profile = "https://www.cupholdersplus.com/mm5/graphics/00000001/BD-Shorty-Drinkster-Bench-Seat-Console-Fiesta_540x540.jpg",  # image link to add to dialogue embeds
        defaultslime = 200,
        defaultlevel = 1,
        rewards = [
        {ewcfg.item_id_slimepoudrin: [75, 5, 6]},
        {ewcfg.rarity_patrician: [20, 1, 1]},
        {ewcfg.item_id_monsterbones: [100, 1, 3]},
        ],
        starting_statuses=[ewcfg.status_enemy_barren_id, ewcfg.status_enemy_hostile_id]
    ),
EwNpc(
        id_npc="bobocuatro",  # unique id for each npc
        active = True,  # whether an npc spawns
        str_name = "Bobo Cuatro",  # Name of the NPC
        poi_list = [ewcfg.poi_id_crookline],  # list of locations an NPC roams in
        dialogue = {"talk":["Go away", "They won't let me inside Splatify", "Quiet, I'm listening to the tracks"],
                    "loop":["Not good", "Behemoth edits are played out 👎👎👎👎","Dances With White Girls 😂","This sounds like you just learned how to make riddims sounds yesterday","Too bad its not over 2min. Or else id put you in my highly banger populated playlist “dubstep 2022” maybe next time kid","Half decent","My ears are bleeding profusely","snorts fentanyl line* This actually better than your last failure of a EP. You will never be as good as aweminus. And if NSD was still active you wouldnt be good enough to be on it. Not even hating guy. You just lack originality.","your EP was a total bust. Not one song got over 1k likes. And you most likely paid that idiot kill feed to repost this garbag. You need yur money back,This is so bad. Like what are you doing?????","Sheeesh the beginning of ghis mix was ass. But these 2 last songs making up for it","This is half decent, but your lack of creativity didnt allow you to strech this track beyond 3 minutes. Nice try kid."],
                    "die":["EVERY TIME"]},  # list of dialogue an npc can use
        func_ai = npcutils.chatty_npc_action,  # function the enemy's AI uses
        image_profile = "https://cdn.discordapp.com/attachments/886372560135143424/994106498038890526/unknown-18.png",  # image link to add to dialogue embeds
        defaultslime = 200,
        defaultlevel = 1,
        rewards = [
        {ewcfg.item_id_oldcd: [100, 1, 1]},
        ],
        starting_statuses=[ewcfg.status_enemy_barren_id]
    ),
EwNpc(
    id_npc = "juviemiku",
    active = True,
    str_name = "Juvie Miku",
    poi_list = [ewcfg.poi_id_downtown, ewcfg.poi_id_greenlightdistrict, ewcfg.poi_id_juviesrow, ewcfg.poi_id_vagrantscorner, ewcfg.poi_id_slimesend, ewcfg.poi_id_slimesendcliffs],
    dialogue = {"talk":["...", "..?", "..!", "👋"],
                "loop":[":notes:Hmm hmm hmmmm!!:notes:", ":notes:La dee da!:notes:", ":notes:Do do dooo!!:notes:", ":notes:Dum de bum!:notes:"],
                "rareloop":["*Miku is beginning to sing!* \nhttps://www.youtube.com/watch?v=NocXEwsJGOQ"],
                "hit":["!?!"],
                "die":["Aieeeeee!!"],
                "downtownloop":["*Miku ponders the Limecorp sign.*"],
                "greenlightdistrictloop":["*Miku is gleefully shopping.*"],
                "slimesendcliffsloop":["*Noticing the ocean waves, Miku frantically scrambles for land.*"]},
    func_ai = npcutils.chatty_npc_action,
    image_profile = "https://cdn.discordapp.com/attachments/431238867459375145/832804357731778620/Miku_02.png", # "I'll illustrate one soon" - not final
    defaultslime = 160000,
    defaultlevel = 20,
    rewards = [
    {ewcfg.item_id_slimepoudrin: [75, 1, 3]},
    {'earbuds': [60, 1, 1]},
    {'rollerblades': [5, 1, 1]},
    {ewcfg.weapon_id_bass: [5, 1, 1]}
    ],
    starting_statuses=[ewcfg.status_enemy_barren_id] #Killable, probably shouldn't drop slime?
),
EwNpc(
    id_npc = "shortsguy",
    active = True,
    str_name = "Shorts Guy",
    poi_list = [ewcfg.poi_id_maimridge, ewcfg.poi_id_toxington, ewcfg.poi_id_astatineheights, ewcfg.poi_id_arsonbrook, ewcfg.poi_id_brawlden, ewcfg.poi_id_littlechernobyl],  # list of locations an NPC roams in
    dialogue = {"talk":["Shorts are so comfortable and easy to wear. Why don't you try wearing some?", "I've bought about 10 pairs of shorts today. Want one?", "It's the perfect kind of day to go for a walk in some nice shorts.", "Shorts, shorts, shorts, can't get enough of them!", "Trying my best to make shorts into a fashion craze.", "Mama always said life is like a fresh pair of shorts."],
                "hit":["You're just jealous of my shorts!"],
                "die":["Not the shorts!"]},
    func_ai = npcutils.generic_npc_action,
    image_profile = "https://cdn.discordapp.com/attachments/927511712473702411/994771357940334684/unknown.png", # Mischief said "I'll come up with one later" so I took creative liberty
    defaultslime = 28561,
    defaultlevel = 13,
    rewards = [
    {ewcfg.item_id_slimepoudrin: [75, 1, 2]},
    {'shorts': [50, 1, 1]},
    {'shortshorts': [50, 1, 1]},
    {'shortshortshorts': [50, 1, 1]},
    {'autographedshorts': [10, 1, 1]}
    ],
    starting_statuses=[ewcfg.status_enemy_barren_id, ewcfg.status_enemy_trainer_id, '2leveltrainer'] # Didn't specify whether hostile or not - considering the guy in Pokemon is, I'd assume so?
),
EwNpc(
    id_npc = "carrottop",
    active = True,
    str_name = "Carrot Top",
    poi_list = [],
    dialogue = {"talk":["Hey dude. Or, uh, dudette. I actually can't see that well.", "Ignore me, loser. Just on official Ganker business.", "HECK!!!!!"],
                "loop":["ARGH!!!", "EUGHHH!!!", "Rgh...", "hmmmmmRRRR..."],
                "rareloop":["ARGH!!! UGHH!!!!!!! I'm getting bullied on slime twitter!!!"],
                "hit":["WHAT THE HELL!!!", "AUUUGHGHHH!!!", "EHHHHGHHH!!!!"],
                "die":["OWWUGUGHH..."],
                },
    func_ai = npcutils.chatty_npc_action,
    image_profile = "https://images-ext-2.discordapp.net/external/MkXZ4qyh3Ean3vEtPIE59Owa-I1Hhehdvkp2JO7g8mA/%3Fformat%3Dpng%26name%3Dsmall/https/pbs.twimg.com/media/FAqiED_WEAER7p4",
    defaultslime = 100000,
    defaultlevel = 17,
    rewards = [
    {'carrottopsmohawk': [100, 1, 1]},
    {ewcfg.item_id_slimepoudrin: [50, 1, 4]},
    {'quesarito': [30, 1, 3]},
    {"crop": [80, 2, 5]},
    ],
    starting_statuses=[] # DOES drop slime. You SHOULD kill Carrot Top.
),
EwNpc(
    id_npc = "pork",
    active = True,
    str_name = "Pork, NLACPD",
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["Howdy, there.", "Don't you just love that sound when you asphyxiate some perp? Good times...", "Golly, I'm so hungry could eat a whole person.", "You seen any of these gang types around?"],
                "loop":["hrm...", "I'm hungry.", "Whew-wee.", "I could go for some blood. Good drinkin'..."],
                "hit":["NLACPD! Hold it!", "Kill 'em dead!", "Shucks! He's got a weapon!"],
                "die":["Ergh. Call in a squad, chief, I'm spent. Bring some donuts to the office, too."],
                },
    func_ai = npcutils.police_npc_action,
    image_profile = "https://rfck.app/img/npc/pork.png",
    defaultslime = 6911000,
    defaultlevel = 50,
    rewards = [
    {"jellyfilleddoughnut": [100, 2, 3],
     "officercopbadge":[100, 1, 1]}
    ],
    starting_statuses=[],
    attacktype = 'police',
    condition = lambda user_data, enemy_data: True if user_data.crime > 10000 or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False
    #if the cop is trigger happy or if you're above a certain crime level
),
EwNpc(
    id_npc = "riot",
    active = True,
    str_name = "Riot, NLACPD",
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["WHO ARE YOU?", "IM GONNA RIP THESE CRIMINALS' FINGERS OFF. JUST NEED TO FIND ONE.", "I CAN SMELL THAT JUSTICE IN THE AIR. SMELLS LIKE GUNPOWDER.", "CAN YOU LEAVE FOR A SEC? I WANT TO KICK SOMETHING REAL QUICK."],
                "loop":["IT'S HOT IN THIS SUIT...", "DO I GET TO KILL YOU? NO, MAYBE LATER.", "HEY DISPATCH, THIS IS RIOT. DID I LEAVE MY TASER BACK THERE? ACTUALLY, FORGET IT. I DON'T NEED THAT."],
                "hit":["RED ALERT!", "ZUCK THIS FUCKING HOOD RAT!!", "GRAAAHH!!"],
                "die":["CALLING FOR BACKUP! DISPATCH BETTER FUCKIN' HURRY!"],
                },
    func_ai = npcutils.police_npc_action,
    image_profile = "https://rfck.app/img/npc/riot.png",
    defaultslime = 4911000,
    defaultlevel = 50,
    rewards = [
    {"jellyfilleddoughnut": [50, 1, 1],
    "gasmask":[50, 1, 1],
     "heavymetalarmor":[20, 1, 1],
     "officercopbadge":[100, 1, 1]}
    ],
    starting_statuses=[],
    attacktype = 'police',
    condition = lambda user_data, enemy_data: True if user_data.crime > 1000 or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False
    #if the cop is trigger happy or if you're above a certain crime level
),
EwNpc(
    id_npc = "sleuth",
    active = True,
    str_name = "Sleuth, NLACPD",
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["I'm a PI, bud. No need to get all panicky.", "I see your hands reaching into your pockets. A rookie like you shouldn't try anythin funny.", "At this point, getting killed's about as inconvenient as missing the train. You still shouldn't try it, squirt.", "This city..."],
                "loop":["This might be easier if they gave me some god damn forensic supplies.", "Dispatch, there's someone over here. They're looking at me funny.", "Can't believe they put me on homicide desk. It's not relevant no more."],
                "hit":["Now you've done it, punk!", "Bilge rat!", "Get back here!"],
                "die":["Son of a bitch. To dispatch, come to my location. Somebody got me..."],
                },
    func_ai = npcutils.police_npc_action,
    image_profile = "https://rfck.app/img/npc/sleuth.png",
    defaultslime = 5911000,
    defaultlevel = 50,
    rewards = [
    {"jellyfilleddoughnut": [20, 1, 1],
    "revolver":[50, 1, 1],
     "trenchcoat":[50, 1, 1],
     "officercopbadge":[100, 1, 1]}
    ],
    starting_statuses=[],
    attacktype = 'police',
    condition = lambda user_data, enemy_data: True if user_data.crime > 25000 or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False
    #if the cop is trigger happy or if you're above a certain crime level
),
EwNpc(
    id_npc = "mrc",
    active = True,
    str_name = "Mr. C, NLACPD Chief of Police",
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["..."],
                "hit":["You'll regret this."],
                "die":["Dispatch, send all available high level officers. We need to make an example of someone."],
                },
    func_ai = npcutils.police_chief_npc_action,
    image_profile = "https://rfck.app/img/npc/mrc.png",
    defaultslime = 3000000,
    defaultlevel = 100,
    rewards = [
    {
     "officercopbadge":[100, 1, 1]}
    ],
    starting_statuses=[ewcfg.status_enemy_barren_id],
    attacktype = 'police',
    condition = lambda user_data, enemy_data: True if user_data.crime > 1250000 else False
    #if the cop is trigger happy or if you're above a certain crime level
),
EwNpc(
    id_npc = "slimesmackenzie",
    active = True,
    str_name = "Slimes MacKenzie", # Knockoff of beloved Slurms MacKenzie, which is a knockoff of Spuds MacKenzie
    poi_list = [ewcfg.poi_id_vagrantscorner, ewcfg.poi_id_speakeasy, ewcfg.poi_id_assaultflatsbeach, ewcfg.poi_id_beachresort],
    dialogue = {"talk":["Hey, you want some cocktails? I'm pretty sure I can break into my quad-G GGGGramp's stash.", "Man, this place is a lot hotter than back home. If I wasn't slime I'd be melting.", "SLIME, my dude!!!", "Let's party!", "Slimmy slime slime slozzle!"],
                "raretalk":["I'm gonna go lie down.", "I'm not saying my fucking catchphrase."],
                "hit":["HUK---", "HYEHK-"],
                "die":["Party on, contest winners. Party on."],
                "thekingswifessonspeakeasytalk":["Did you know this speakeasy used to be a boat? Yeah, me neither."]
                },
    func_ai = npcutils.generic_npc_action,
    image_profile = "https://cdn.discordapp.com/attachments/927511712473702411/995441965548195841/slimes_mackenzie.png", # Another with no PFP given so here's a placeholder
    defaultslime = 1500000,
    defaultlevel = 40,
    rewards = [
    {ewcfg.item_id_slimepoudrin: [80, 1, 3]},
    {'pairofsunglasses': [50, 1, 1]},
    {'bitchenergy': [100, 1, 2]},
    {'slimynipple': [50, 1, 1]}
    ],
    starting_statuses = [ewcfg.status_enemy_barren_id]
),
EwNpc(
    id_npc = "recalcitrantfawn",
    active = True,
    str_name = "RF",
    poi_list = [ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_cratersville, ewcfg.poi_id_wreckington, ewcfg.poi_id_poudrinalley],
    dialogue = {"talk":["!!!", "👋",  "🤙", "*RF gives you a high five.*"],
                "loop":["*RF just checked a trash can. Can't jump in there, too full.*", "*RF is anxious and jumping around! You must've caught them by suprise.*", "*RF seems distracted by that brick over there*", "*RF does a little happy dance.*"],
                "rowdyroughhouseloop": ["RF looks at the top of the Rowdy Roughhouse with a sense of pride."],
                "outsidethe711loop": ["RF repeatedly presses the button to the fuck energy machine."],
                "hit":["RF gears up for battle."],
                "die":["*It looks like RF really wasn't cut out to be a Rowdy.* {}".format(ewcfg.emote_slimeskull)]
                },
    func_ai = npcutils.condition_hostile_action,
    image_profile = "https://rfck.app/img/npc/rf1.png",
    defaultslime = 6479,
    defaultlevel = 47,
    rewards = [
    {'rfconsortmarble': [100, 1, 1]}
    ],
    starting_statuses = [],
    condition= lambda user_data, enemy_data: True if (user_data.faction == 'killers' and user_data.life_state == ewcfg.life_state_enlisted) or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False #attacks killers, or anyone when hostile
)
]

active_npcs_map = {}

for npc in npc_list:
    if npc.active:
        active_npcs_map[npc.id_npc] = npc