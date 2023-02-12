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
        poi_list = [ewcfg.poi_id_711, ewcfg.poi_id_poudrinalley, ewcfg.poi_id_oozegardens, ewcfg.poi_id_wreckington, ewcfg.poi_id_glocksbury, ewcfg.poi_id_krakbay, ewcfg.poi_id_downtown, ewcfg.poi_id_greenlightdistrict, ewcfg.poi_id_smogsburg],  # list of locations an NPC roams in
        dialogue = {"talk":["...", "Feeling kind of thirsty..."],
                    "give":["Thanks, buddy! I'll take it, but honestly I'd rather have something to drink."],
                    "loop":["...", "Feeling kind of thirsty..."]},  # list of dialogue an npc can use
        func_ai = npcutils.drinkster_npc_action,  # function the enemy's AI uses
        image_profile = "https://rfck.app/npc/drinkster_thumb.png",  # image link to add to dialogue embeds
        defaultslime = 2036231,
        defaultlevel = 22,
        slimeoid_name = "Orange Crush",
        rewards = [
        {ewcfg.item_id_slimepoudrin: [75, 5, 6]}
        ],
        starting_statuses=[ewcfg.status_enemy_juviemode_id, ewcfg.status_enemy_trainer_id]
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
        description = "What an insufferable prick. Nobody asked for his opinion.",
        poi_list = [ewcfg.poi_id_crookline],  # list of locations an NPC roams in
        dialogue = {"talk":["Go away", "They won't let me inside Splatify", "Quiet, I'm listening to the tracks"],
                    "loop":["Not good", "Behemoth edits are played out 👎👎👎👎","Dances With White Girls 😂","This sounds like you just learned how to make riddims sounds yesterday","Too bad its not over 2min. Or else id put you in my highly banger populated playlist “dubstep 2022” maybe next time kid","Half decent","My ears are bleeding profusely","snorts fentanyl line* This actually better than your last failure of a EP. You will never be as good as aweminus. And if NSD was still active you wouldnt be good enough to be on it. Not even hating guy. You just lack originality.","your EP was a total bust. Not one song got over 1k likes. And you most likely paid that idiot kill feed to repost this garbag. You need yur money back,This is so bad. Like what are you doing?????","Sheeesh the beginning of ghis mix was ass. But these 2 last songs making up for it","This is half decent, but your lack of creativity didnt allow you to strech this track beyond 3 minutes. Nice try kid."],
                    "die":["EVERY TIME"],
                    "give":["Still not good.", "I'll take that but I really don't see how it won't be just the same old thing."]},  # list of dialogue an npc can use
        func_ai = npcutils.candidate_action,  # function the enemy's AI uses
        image_profile = "https://cdn.discordapp.com/attachments/886372560135143424/994106498038890526/unknown-18.png",  # image link to add to dialogue embeds
        defaultslime = 200,
        defaultlevel = 1,
        rarity=7,
        rewards = [
        {ewcfg.item_id_oldcd: [100, 1, 1],
         }, #"bobocuatroscalp":[100, 1, 1]
        ],
        starting_statuses=[ewcfg.status_enemy_barren_id, '5leveltrainer', ewcfg.status_enemy_trainer_id],

    ),
EwNpc(
    id_npc = "juviemiku",
    active = True,
    str_name = "Juvie Miku",
    description = "She's...well, she's definitely Juvie. A little *too* juvie.",
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
    image_profile = "https://rfck.app/npc/juviemiku_thumb.png", # "I'll illustrate one soon" - not final
    defaultslime = 160000,
    defaultlevel = 20,
    rewards = [
    {ewcfg.item_id_slimepoudrin: [75, 1, 3]},
    {'earbuds': [60, 1, 1]},
    {'rollerblades': [5, 1, 1]},
    {ewcfg.weapon_id_bass: [5, 1, 1]}
    ],
    starting_statuses=[ewcfg.status_enemy_barren_id, '1leveltrainer', ewcfg.status_enemy_trainer_id] #Killable, probably shouldn't drop slime?
),
EwNpc(
    id_npc = "shortsguy",
    active = True,
    str_name = "Shorts Guy",
    description = "Some people get into gang violence. Others are drawn to the stock market or maybe fishing. This goddamn idiot found shorts in the bodega one day and it's been love ever since.",
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
    starting_statuses=[ewcfg.status_enemy_barren_id, ewcfg.status_enemy_trainer_id, '2leveltrainer', ewcfg.status_enemy_trainer_id] # Didn't specify whether hostile or not - considering the guy in Pokemon is, I'd assume so?
),
EwNpc(
    id_npc = "carrottop",
    active = True,
    str_name = "Carrot Top",
    description = "The weakest of the Garden Gankers. They grunt a big game but they're basically free slime.",
    poi_list = poi_static.capturable_districts,
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
    rarity=1,
    rewards = [
    {'carrottopsmohawk': [100, 1, 1]},
    {ewcfg.item_id_slimepoudrin: [50, 1, 4]},
    {'quesarito': [30, 1, 3]},
    {"crop": [80, 2, 5]},
    ],
    starting_statuses=['4leveltrainer', ewcfg.status_enemy_trainer_id] # DOES drop slime. You SHOULD kill Carrot Top.
),
EwNpc(
    id_npc = "pork",
    active = True,
    str_name = "Pork, NLACPD",
    description = "Good thing you spotted in time. This isn't any old officer. This guy's got a sadist streak a million miles wide.",
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["Howdy, there.", "Don't you just love that sound when you asphyxiate some perp? Good times...", "Golly, I'm so hungry could eat a whole person.", "You seen any of these gang types around?"],
                "loop":["hrm...", "I'm hungry.", "Whew-wee.", "I could go for some blood. Good drinkin'..."],
                "hit":["NLACPD! Hold it!", "Kill 'em dead!", "Shucks! He's got a weapon!"],
                "die":["Ergh. Call in a squad, chief, I'm spent. Bring some donuts to the office, too."],
                "give":["What a morsel..."]
                },
    func_ai = npcutils.police_npc_action,
    image_profile = "https://rfck.app/npc/pork.png",
    defaultslime = 6911000,
    defaultlevel = 50,
    rarity=7,
    rewards = [
    {"jellyfilleddoughnut": [100, 2, 3],
     "officercopbadge":[100, 1, 1]}
    ],
    starting_statuses=['7leveltrainer', ewcfg.status_enemy_trainer_id],
    attacktype = 'police',
    condition = lambda user_data, enemy_data: True if user_data.crime > 10000 or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False,
    slimeoid_name='Chocolate Donut',
    is_threat=True
    #if the cop is trigger happy or if you're above a certain crime level
),
EwNpc(
    id_npc = "riot",
    active = True,
    str_name = "Riot, NLACPD",
    description = "A fresh-faced officer with a penchant for destruction. Do you recognize the voice under there? Nah, can't be.",
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["WHO ARE YOU?", "IM GONNA RIP THESE CRIMINALS' FINGERS OFF. JUST NEED TO FIND ONE.", "I CAN SMELL THAT JUSTICE IN THE AIR. SMELLS LIKE GUNPOWDER.", "CAN YOU LEAVE FOR A SEC? I WANT TO KICK SOMETHING REAL QUICK."],
                "loop":["IT'S HOT IN THIS SUIT...", "DO I GET TO KILL YOU? NO, MAYBE LATER.", "HEY DISPATCH, THIS IS RIOT. DID I LEAVE MY TASER BACK THERE? ACTUALLY, FORGET IT. I DON'T NEED THAT."],
                "hit":["RED ALERT!", "ZUCK THIS FUCKING HOOD RAT!!", "GRAAAHH!!"],
                "die":["CALLING FOR BACKUP! DISPATCH BETTER FUCKIN' HURRY!"],
                "give":["GIMME THAT!"]
                },
    func_ai = npcutils.police_npc_action,
    image_profile = "https://rfck.app/npc/riot.png",
    defaultslime = 4911000,
    defaultlevel = 50,
    rarity=7,
    rewards = [
    {"jellyfilleddoughnut": [50, 1, 1],
    "gasmask":[50, 1, 1],
     "heavymetalarmor":[20, 1, 1],
     "officercopbadge":[100, 1, 1]}
    ],
    starting_statuses=['5leveltrainer', ewcfg.status_enemy_trainer_id],
    attacktype = 'police',
    is_threat=True,
    condition = lambda user_data, enemy_data: True if user_data.crime > 1000 or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False,

    #if the cop is trigger happy or if you're above a certain crime level
),
EwNpc(
    id_npc = "sleuth",
    active = True,
    str_name = "Sleuth, NLACPD",
    description = "A well known police detective that goes way back with the department. It's NLACakaNM, so he has plenty to keep himself occupied.",
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["I'm a PI, bud. No need to get all panicky.", "I see your hands reaching into your pockets. A rookie like you shouldn't try anythin funny.", "At this point, getting killed's about as inconvenient as missing the train. You still shouldn't try it, squirt.", "This city..."],
                "loop":["This might be easier if they gave me some god damn forensic supplies.", "Dispatch, there's someone over here. They're looking at me funny.", "Can't believe they put me on homicide desk. It's not relevant no more."],
                "hit":["Now you've done it, punk!", "Bilge rat!", "Get back here!"],
                "die":["Son of a bitch. To dispatch, come to my location. Somebody got me..."],
                "give":["What, this some sorta clue?"]
                },
    func_ai = npcutils.police_npc_action,
    image_profile = "https://rfck.app/npc/sleuth.png",
    defaultslime = 5911000,
    defaultlevel = 50,
    is_threat=True,
    rarity=7,
    rewards = [
    {"jellyfilleddoughnut": [20, 1, 1],
    "revolver":[50, 1, 1],
     "trenchcoat":[50, 1, 1],
     "officercopbadge":[100, 1, 1]}
    ],
    starting_statuses=['6leveltrainer', ewcfg.status_enemy_trainer_id],
    attacktype = 'police',
    condition = lambda user_data, enemy_data: True if user_data.crime > 25000 or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False,
    #if the cop is trigger happy or if you're above a certain crime level
),
EwNpc(
    id_npc = "mrc",
    active = True,
    str_name = "Mr. C, NLACPD Chief of Police",
    description = 'The city\'s Chief of Police. Not much is known about them, but you hear they\'re pretty intimidating. You might not get this chance again, you should gank this sonavabitch!',
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["..."],
                "hit":["You'll regret this."],
                "die":["Dispatch, send all available high level officers. We need to make an example of someone."],
                "give":["We'll have our officers look over this."]
                },
    func_ai = npcutils.police_chief_npc_action,
    image_profile = "https://rfck.app/npc/mrc.png",
    defaultslime = 3000000,
    defaultlevel = 100,
    is_threat=True,
    rarity=1,
    rewards = [
    {
     "officercopbadge":[100, 1, 1]}
    ],
    starting_statuses=[ewcfg.status_enemy_barren_id, '9leveltrainer', ewcfg.status_enemy_trainer_id],
    attacktype = 'police',
    condition = lambda user_data, enemy_data: True if user_data.crime > 1250000 else False,

    #if the cop is trigger happy or if you're above a certain crime level
),
EwNpc(
    id_npc = "slimesmackenzie",
    active = True,
    str_name = "Slimes MacKenzie", # Knockoff of beloved Slurms MacKenzie, which is a knockoff of Spuds MacKenzie
    description = 'MacKenzie\'s here, guys. It\'s a real party now.',
    poi_list = [ewcfg.poi_id_vagrantscorner, ewcfg.poi_id_speakeasy, ewcfg.poi_id_assaultflatsbeach, ewcfg.poi_id_beachresort],
    dialogue = {"talk":["Hey, you want some cocktails? I'm pretty sure I can break into my quad-G GGGGramp's stash.", "Man, this place is a lot hotter than back home. If I wasn't slime I'd be melting.", "SLIME, my dude!!!", "Let's party!", "Slimmy slime slime slozzle!", "Hey you want some cocktails Im pretty sure I can break into Gramps stash in Vagrants Corner.", "Man this place is a lot hotter than back home if I wasn’t slime I’m pretty sure I’d be melting", "I am not saying my fucking catchphrase simp!", "Hey I heard you got the tier three sub from some sandwich shop…I’ll give you an autograph if you give me it.", "Did you know the speak easy also turns into a boat. Yeah me either.", "Check out the tiki bar out in grand toronto when you get the chance dude!"],
                "raretalk":["I'm gonna go lie down.", "I'm not saying my fucking catchphrase."],
                "hit":["HUK---", "HYEHK-", "OW! WHAT THE FUCKS WRONG WITH YOU!"],
                "die":["Party on, contest winners. Party on.", "Oh…No…B R O…"],
                "thekingswifessonspeakeasytalk":["Did you know this speakeasy used to be a boat? Yeah, me neither."]
                },
    func_ai = npcutils.generic_npc_action,
    image_profile = "https://cdn.discordapp.com/attachments/994241049012748399/998319239469486120/SLIMEZ.png", # Another with no PFP given so here's a placeholder
    defaultslime = 1500000,
    defaultlevel = 10,
    rewards = [
    {ewcfg.item_id_slimepoudrin: [80, 1, 3]},
    {'pairofsunglasses': [50, 1, 1]},
    {'bitchenergy': [100, 1, 2]},
    {'slimynipple': [50, 1, 1]}
    ],
    starting_statuses = [ewcfg.status_enemy_barren_id, '2leveltrainer', ewcfg.status_enemy_trainer_id]
),
EwNpc(
    id_npc = "recalcitrantfawn",
    active = True,
    str_name = "RF",
    description = 'This little guy made a big splash in the Rowdys when they first joined up. They ended up getting Consort in record time thanks to the inexplicable appearance of a bunch of  consort-themed fetch quests. If you kill him? Oh boy, he\'ll really lose his marbles.',
    poi_list = [ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_cratersville, ewcfg.poi_id_wreckington, ewcfg.poi_id_poudrinalley],
    dialogue = {"talk":["!!!", "👋",  "🤙", "()*RF gives you a high five.*"],
                "loop":["()*RF just checked a trash can. Can't jump in there, too full.*", "()*RF is anxious and jumping around! You must've caught them by suprise.*", "()*RF seems distracted by that brick over there*", "()*RF does a little happy dance.*"],
                "rowdyroughhouseloop": ["RF looks at the top of the Rowdy Roughhouse with a sense of pride."],
                "outsidethe711loop": ["RF repeatedly presses the button to the fuck energy machine."],
                "hit":["RF gears up for battle."],
                "die":["*It looks like RF really wasn't cut out to be a Rowdy.* {}".format(ewcfg.emote_slimeskull)]
                },
    func_ai = npcutils.condition_hostile_action,
    image_profile = "https://rfck.app/npc/rf1.png",
    defaultslime = 6479,
    defaultlevel = 32,
    is_threat=True,
    rewards = [
    {'rfconsortmarble': [100, 1, 1]}
    ],
    starting_statuses = ['4leveltrainer', ewcfg.status_enemy_trainer_id],
    condition= lambda user_data, enemy_data: True if (user_data.faction == 'killers' and user_data.life_state == ewcfg.life_state_enlisted) or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False #attacks killers, or anyone when hostile
),
EwNpc(
    id_npc = "pinkerton",
    active = True,
    str_name = "Pinkerton",
    description = "A disheveled homeless man wearing a tarp cloak over ruined body armor. Pinkerton was once a member of the NLACakaNMPD's Vandal Squad, thuggish brutes who disguised as homeless people to get the drop on poor, innocent graffiti artists. Decades of slime-fueled gang violence have made him a shell of his former self.",
    poi_list = poi_static.capturable_districts, # Change to whatever ew\static\poi is imported as
    dialogue = {"talk":["()*Pinkerton barks some incomprehensible nonsense that may have once been police radio shorthand. You slowly back away so as not to anger him further.*", "()*You think Pinkerton lost the ability to speak long ago.*"],
                "loop":["()*Pinkerton peers out from a back alley, suspiciously eyeing passersby.*", "()*Pinkerton is busying himself with a broken radio, trying to call backup that has long since disappeared.*", "()*Pinkerton's eye twitches, his hand tentatively reaching for his piece.*"],
                "hit":["HYARGH-!!", "RRGH-", "()*Pinkerton snaps to attention, readying his revolver*"],
                "rarehit":["()*Pinkerton lets out a bestial roar, lunging to grab and throw you in a perfect-arch German suplex!*"],
                "die":["()*The last of the Vandal Squad falls.*"]
                },
    func_ai = npcutils.generic_npc_action,
    image_profile = "https://cdn.discordapp.com/attachments/927511712473702411/996283670631546931/rivers_cuomo_pinkerton.png", # No PFP given again
    defaultslime = 1900000,
    defaultlevel = 23,
    is_threat=True,
    rewards = [
    {ewcfg.item_id_slimepoudrin: [100, 2, 6]},
    {'pairofsunglasses': [100, 1, 1]},
    {'reinforcedkfcbucket': [5, 1, 1]},
    {ewcfg.item_id_454casullround: [80, 1, 1]},
    {'crop': [100, 1, 3]}
    ],
    starting_statuses = ['6leveltrainer', ewcfg.status_enemy_trainer_id],
    ),
EwNpc(
    id_npc = "johnny",
    active = True,
    str_name = "Johnny",
    description = "The biggest poser in all of NLACakaNM. He claims to be the kingpin of his own gang and is always trying to rope people into doing him favors as a means of entry.",
    poi_list = [ewcfg.poi_id_vagrantscorner, ewcfg.poi_id_assaultflatsbeach, ewcfg.poi_id_slimesend],
    dialogue = {"first":["Hey there slick. Runnin' a little low on the sweet sweet skune ain'tcha? Don't you worry slick, big bro Johnny's gotcha covered. I'm just gonna need to you to get me a poudrin. Get me that and I might just slide you a cool 100 slime. Quite the charitable offer if you ask me. It's a real dime-a-dozen deal slick, you can trust me on that."], #note that the 'first' command is not actually functional
                "talk":["H-Hey, quit staring at me like that! I don't want any trouble, slick. Just leave me alone!", "I-I’m sorry I got in your way! H-Here, look, a poudrin! It's yours - you can have it! Just please don't hurt me!", "Munchy and Ben? Yeah, I know those guys. We go WAY back - I was totally a mentor figure to them. Just uh... don't ask anyone about that. And don't mention my name either!", "HEY! Watch it! Do have any idea how much effort it takes to keep my hairdo from falling to pieces? Fuck up the 'do and you're on thin ice!", "One of these days slick, I'm totally gonna rule this city. It'll be me sitting on a diamond-studded golden throne with, like, 12 slime girls at my feet. And you, uh... you can be the guy that shines my Yeezys!", "You're not gonna believe it, but some asshole was talking shit about my sick-ass 'do earlier! Yeah, I totally punched all of their teeth out. Yup! Every single one!"],
                "hit":["H-Hey, I'm sorry if I did something that upset you slick. Honest! Just please don't do that again, alright?"],
                "die":["What the fuck, slick..."]
                },
    func_ai = npcutils.generic_npc_action,
    image_profile = "https://cdn.discordapp.com/attachments/927511712473702411/996335418293362688/placeholderjohnny.png", # PFP in progress, placeholder
    defaultslime = 10000,
    defaultlevel = 1,
    rewards = [
    {ewcfg.item_id_slimepoudrin: [100, 1, 2]},
    {'jeans': [70, 1, 1]},
    {'dogtag': [70, 1, 1]},
    {ewcfg.weapon_id_katana: [15, 1, 1]}
    ],
    starting_statuses = ['6leveltrainer', ewcfg.status_enemy_trainer_id]
    ),
EwNpc(
    id_npc = "chad",
    active = True,
    str_name = "Chad", # Full name "Alpha Chad"
    poi_list = [ewcfg.poi_id_krakbay, ewcfg.poi_id_poudrinalley, ewcfg.poi_id_cratersville],
    dialogue = {"talk":["Look alive there, pal!", "We're all gonna make it, or so I've been told."],
                "hit":["Well, looks like things are going that way.", "Let's do this."],
                "die":["Back to the sauce I go..."],
                },
    func_ai = npcutils.condition_hostile_action,
    image_profile = "https://cdn.discordapp.com/attachments/976385581498138624/998073766477312020/kimblychadnpc.png",
    defaultslime = 2560000,
    is_threat=True,
    defaultlevel = 40,
    rewards = [
    {ewcfg.item_id_slimepoudrin: [100, 3, 5]},
    {'cookingapron': [70, 1, 1]},
    {'crop': [100, 1, 3]}
    ],
    starting_statuses = ['5leveltrainer', ewcfg.status_enemy_trainer_id],
    condition=lambda user_data, enemy_data: True if (user_data.faction == 'killers' and user_data.life_state == ewcfg.life_state_enlisted) or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False
    # attacks killers, or anyone when hostile
),
EwNpc(
    id_npc = "tips",
    active = True,
    str_name = "Tips", # Full name "Tips Fedora"
    poi_list = [ewcfg.poi_id_toxington, ewcfg.poi_id_gatlingsdale, ewcfg.poi_id_maimridge],
    dialogue = {"talk":["Nothing like a nice, long smoke on a big tall building, or walking around town, or sitting at home staring at your ceiling, or... Wait, what was I talking about again?"],
                "hit":["Heh, you're gonna regret this. I'm a master of the blade."],
                "die":["T-There was spaghetti in my controller..."],
                },
    func_ai = npcutils.condition_hostile_action,
    image_profile = "https://media.discordapp.net/attachments/976385581498138624/998073766682824704/kimblytipsnpc.png",
    defaultslime = 2560000,
    defaultlevel = 40,
    is_threat=True,
    rewards = [
    {ewcfg.item_id_slimepoudrin: [100, 3, 5]},
    {'packofluckyslimes': [70, 1, 1]},
    {'crop': [100, 1, 3]}
    ],
    starting_statuses = ['5leveltrainer', ewcfg.status_enemy_trainer_id],
    condition=lambda user_data, enemy_data: True if (user_data.faction == 'rowdys' and user_data.life_state == ewcfg.life_state_enlisted) or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False
),
EwNpc(
    id_npc = "kimbly",
    active = True,
    str_name = "Kimbly", # Full name "Kimbly Loksed"
    poi_list = [ewcfg.poi_id_smogsburg],
    dialogue = {"first":["Wha- Oh hey there!"],
                "talk":["Is there always supposed to be this much slime on the streets? "],
                "hit":["Oh jeez! Looks like I'll have to deal you a hand!"],
                "die":["Someone... Please check on my plushies..."],
                },
    func_ai = npcutils.generic_npc_action,
    image_profile = "https://cdn.discordapp.com/attachments/976385581498138624/998073766909313144/kimblynpc.png",
    defaultslime = 1550000,
    defaultlevel = 35,
    rewards = [
    {ewcfg.item_id_gameguide: [100, 1, 1]},
    {'crop': [100, 2, 5]}
    ],
    starting_statuses = [ewcfg.status_enemy_barren_id, '3leveltrainer', ewcfg.status_enemy_trainer_id],
),
EwNpc(
    id_npc = "juvieman",
    active = True,
    str_name = "Juvieman",
    description = "A Juvie blessed with a unique mutation - Slimernalia powers all year round! They use these powers to protect Juvies in need.  Praise Phoebus, truly.",
    poi_list = [ewcfg.poi_id_endlesswar, ewcfg.poi_id_downtown, ewcfg.poi_id_greenlightdistrict, ewcfg.poi_id_juviesrow],
    dialogue = {"talk":["Hail fair citizen! Fine day for a jaunt around town, is it not?", "Keep an eye out for that nefarious Staydeadman!", "Keeping these streets safe, one scumbag at a time...", "It's tough work, but someone's gotta do it...", "Green's my favorite color!", "Need something?"],
                "raretalk":["Remember to stock up on bodyspray, young Juve.", "Don't be afraid to use the Juvie signal if you're ever in trouble!", "I trust that you're not planning anything nefarious, citizen?"],
                "hit":["So you've chosen violence, then? Very well!", "I'll shield that with my body!", "**WHO THE HECK DO YOU THINK I AM!?**"],
                "rarehit":["Are you working with that nefarious Staydeadman!?"],
                "die":["**UP, UP, RUN AWAYYYYYYYYY!**"],
                "give":["Thank you, fair citizen!"]
                },
    func_ai = npcutils.juvieman_action,
    image_profile = "https://cdn.discordapp.com/attachments/982703096616599602/996615981407408249/unknown.png",
    defaultslime = 30000000,
    defaultlevel = 99,
    rarity=7,
    is_threat=True,
    attacktype = 'juvieman',
    rewards = [
    {ewcfg.item_id_slimepoudrin: [100, 6, 9]},
    {ewcfg.weapon_id_juvierang: [50, 1, 1]},
    ],
    starting_statuses = [ewcfg.status_enemy_barren_id, '9leveltrainer', ewcfg.status_enemy_trainer_id],
    condition= lambda user_data, enemy_data: True if user_data.life_state != 1 and ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False

),
EwNpc(
    id_npc = "marty",
    active = False,
    str_name = "Marty",
    description = "He's a two-faced fellow, but he means well, we promise. He runs a construction company over in Wreckington.",
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":[],
                "loop":[],
                "hit":[],
                "die":[],
                "give":[]
                },
    func_ai = npcutils.marty_action,
    image_profile = "",
    defaultslime = 3000000,
    defaultlevel = 50,
    rewards = [
    {}
    ],
    starting_statuses=['7leveltrainer', ewcfg.status_enemy_trainer_id],
    rarity=7
    #if the cop is trigger happy or if you're above a certain crime level
),
EwNpc(
    id_npc = "herb",
    active = True,
    str_name = "Herb",
    description = "He's your typical politician. Can't even take a good bullet to the face.",
    poi_list = [ewcfg.poi_id_downtown, ewcfg.poi_id_krakbay, ewcfg.poi_id_smogsburg, ewcfg.poi_id_poudrinalley, ewcfg.poi_id_charcoalpark, ewcfg.poi_id_oozegardens],
    dialogue = {"talk":["Please clap.", "Hi there! Uhh, you're actually the only person at this rally, so...", "Hey, I don't like the look on your face. Are you gonna hurt me?", "I know my jokes are trite, OK? I have a glandular problem."],
                "loop":["I see a vision for this city free of runaway slime, where violence is a thing of the past.", "Vote for me, and ensure Mr. Spin's money isn't wasted!", "Don't be afraid everyone! Nobody is out to hurt you, things are beginning to change!"],
                "hit":["Hah! That one didn't even hurt."],
                "die":["AIEEEEEEEE!!!!", "Security! SECURITY!!!", "AAAGHHHH NOT AGAIN!", "MY LUMBAGO!", "PLEASE STOP I LOOK UNELECTABLE!"],
                "give":["Thanks for the donation! I assure you it won't go to waste!", "Eheheheh..."]
                },
    func_ai = npcutils.candidate_action,
    image_profile = "https://rfck.app/npc/herb_pfp.png",
    defaultslime = 20,
    defaultlevel = 1,
    rarity=3,
    slimeoid_name='Fortunate Son',
    rewards = [
    {"necktie":[100, 1, 1]}
    ],
    starting_statuses=['1leveltrainer', ewcfg.status_enemy_trainer_id],

),
EwNpc(
    id_npc = "n11",
    active = True,
    str_name = "Mr. Musset, Formerly N11",
    description = "A former Slimecorp employee. Are you gonna put aside your differences here? Personally, I'd fawgeddabowdhit.",
    poi_list = [ewcfg.poi_id_brawlden, ewcfg.poi_id_wreckington, ewcfg.poi_id_cratersville, ewcfg.poi_id_poudrinalley, ewcfg.poi_id_toxington, ewcfg.poi_id_charcoalpark],
    dialogue = {"talk":["Hey dere.", "I'm comin ta change things. Public woiks, that kinda thing.", "Look at dis wise guy ova ere! They just waltz outta prison, so why are we's even funding dis? Seems like a big waste.", "We was a bit too extreme back in dah day, but I don't do dat anymore."],
                "loop":["Vote for dis guy! Ruben Musset oughta brighten up da government!", "I'm ya guy, I promise. I know Slimecorp, I can regulate Slimecorp.", "Musset for mayor, ya never felt gayer! And youse all know I'm talkin about the happy meaning."],
                "hit":["Oh no ya don't.", "Come on!"],
                "die":["Shoulda known.", "Asassinated, my foot! Come back ere!", "Can't zuck me, not no more...", "SEE DIS, PEOPLE? YOU DON'T HAFTA DIE LIKE DIS!"],
                "give":["Ey, buddy. Dat means a lot.", "Do I recognize you, kid? Anyhow, I 'preciate dat."]
                },
    func_ai = npcutils.candidate_action,
    image_profile = "https://rfck.app/npc/n11reformed.png",
    defaultslime = 4000000,
    defaultlevel = 55,
    rarity=3,
    attacktype = ewcfg.weapon_id_brassknuckles,
    slimeoid_name = 'Lil\' Bruiser',
    rewards = [
    {
     ewcfg.weapon_id_brassknuckles:[20, 1, 1]}
    ],
    starting_statuses=['6leveltrainer', ewcfg.status_enemy_trainer_id],
),
EwNpc(
    id_npc = "mozz",
    active = True,
    str_name = "Mozz",
    description = "Eww. Looks like somebody smelted a stuffed crust pizza wrong. Better let the thing just go about its business.",
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["()It starts to snarl at you! Oh shit!", "WRYYYYYYYYYY!"],
                "loop":["()*slurp smack* ", "AJAJAJA!!", "*munch munch*", "...", "WRYYYYYYYYYY! *Yawn...*"],
                "hit":["!!", "HCK!"],
                "die":["()The creature melts into a pizza puddle on the ground...", "WEHHHHHHH!"],
                "give":["()Mozz takes your spoiled food and runs away with it!"]
                },
    func_ai = npcutils.mozz_action,
    image_profile = "https://rfck.app/npc/mozz.png",
    defaultslime = 9999000,
    defaultlevel = 1,
    rarity=5,
    is_threat=True,
    attacktype = 'pizzagraspers',
    rewards = [
    {ewcfg.item_id_octuplestuffedcrust:[100, 1, 1],
     ewcfg.item_id_quadruplestuffedcrust:[100, 2, 4],
     ewcfg.item_id_doublestuffedcrust:[100, 2, 4]}
    ],
    starting_statuses=[ewcfg.status_enemy_tanky_id, ewcfg.status_enemy_dodgy_id, ewcfg.status_enemy_barren_id],
),
EwNpc(
    id_npc = "slox",
    active = True,
    str_name = "Slox",
    description = "It's a harmless little creature that just enjoys resting with its friend under the Poudrin Alley bridge.",
    poi_list = [ewcfg.poi_id_poudrinalley],
    dialogue = {"talk":["Prrrr...."],
                "loop":["*yawn* ", "Prrrr...."],
                "hit":["!!", "RRRRR!"],
                "die":["()The slox ragdolls to the ground. Why are you so cruel?"],
                "give":["()The slox takes your gift and brings it back to their resting place to share it with their friend."]
                },
    func_ai = npcutils.slox_action,
    image_profile = "https://rfck.app/npc/sloxes_f.png",
    defaultslime = 300,
    attacktype = 'slox',
    defaultlevel = 1,
    rarity=5,
    rewards = [
    {'sloxpendant':[1, 1, 1]} #good luck.
    ],
    starting_statuses=["buddyslox"],
),
EwNpc(
    id_npc = "dojomaster",
    active = True,
    str_name = "Dojo Master",
    description = "He's the master of all weapons. He seems to be in a zen-like state right now.",
    poi_list = [ewcfg.poi_id_southsleezeborough, ewcfg.poi_id_dojo],
    dialogue = {"talk":["ダンクウィートを切るのに大鎌を使わないで！」", "「恐怖の匂いを嗅ぐことを学ぶには、足から始めなければならない。」", "「軍風ダイハック #590: 自分の額の真ん中から少なくとも 180 度離れたところに銃を向けてください。」", "軍実の格言その16 一直線に弾丸をたくさん打てば相手は斬り切れない", "「格闘術のヒント #4306: 刀をたたむと、より簡単に財布に収まります。」"],
                "loop":["「警備員の皆さん、両生類を入れるのはやめてください。」 *昼食に戻り、箸でハエを捕る*", "「私と一緒に剣の練習をしに来てください。それで海峡を泳ぐことは決してありません。そして、フランス人はあなたの恐怖を嗅ぐでしょう。」", "「若い頃、リボルバーを研いで刃にしようとしたことがありますが、発砲するとうまくいきませんでした。これを教訓にして、武器に走り書きをやめてください。」"],
                "hit":["結構。私はあなたの挑戦を受け入れます。", "私に来てください！"],
                "die":["私を倒すには素晴らしいスキルが必要でした。あなたの熟達ぶりは、あなたのスタンスに表れています。次回まで。"],
                "give":["テグン道の格言 7: 見知らぬ人からの好意は、血で返す覚悟がない限り受け入れてはならない。ありがとう、私の息子。"]
                },
    func_ai = npcutils.dojomaster_action,
    image_profile = "https://rfck.app/npc/dojomaster.png",
    defaultslime = 15000000,
    attacktype = ewcfg.enemy_attacktype_dojoman,
    defaultlevel = 99,
    rarity=1,
    is_threat=True,
    slimeoid_name='蒸気船たかはし',
    rewards = [
    {ewcfg.weapon_id_brassknuckles:[100, 1, 1],
     ewcfg.weapon_id_scythe:[100, 1, 1],
     ewcfg.weapon_id_dualpistols:[100, 1, 1],
     ewcfg.weapon_id_bat:[100, 1, 1],
     ewcfg.weapon_id_garrote:[100, 1, 1],
     ewcfg.weapon_id_katana:[100, 1, 1],
     ewcfg.weapon_id_yoyo:[100, 1, 1],
     ewcfg.weapon_id_molotov:[100, 1, 1],
     ewcfg.weapon_id_broadsword:[100, 1, 1],
     ewcfg.weapon_id_nunchucks:[100, 1, 1]}
    ],
    starting_statuses=[ewcfg.status_enemy_dodgy_id, '9leveltrainer', ewcfg.status_enemy_trainer_id],
),
EwNpc(
    id_npc = "queenofengland",
    active = True,
    str_name = "Her Late Majesty Queen Elizabeth",
    description = 'She\'s fallen on hard times ever since...well, you know.',
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["Hi there, sir, may I inquire about bus fare?", "I just need one small favor...", "Hello! Thanks for talking to me finally.", "I'm going to bother you now."],
                "loop":["Cash?", "Can I have some cash?", "Hi, hey! Cash!", "Do you speak British?", "Cash, please?", "I want 100 po- I mean slime.", "Ca-ca-cash?", "May I have another poudrin?", "Alms for the poor?", "Alms for the pudgy?", "I'm not the Queen, I'm different. I need some cash for the train.", "Cash!", "Cash??", "CASH.", "Cash...", "Cash... 🥺", "I need some cash, good sir...🧐🧐🧐"],
                },
    func_ai = npcutils.needy_npc_action,
    image_profile = "https://rfck.app/npc/slimequeen.png",
    defaultslime = 15,
    defaultlevel = 1,
    str_juviemode = "You decide to just kill the Queen to get her off your back, but you decide the only thing more annoying than her is causing an international incident. Christ alive, she's just gonna spend it on alcohol anyway.",
    slimeoid_name = "Oliver Twist",
    rewards = [
    {ewcfg.item_id_slimepoudrin: [80, 1, 3]},
    ],
    starting_statuses = [ewcfg.status_enemy_juviemode_id, '1leveltrainer', ewcfg.status_enemy_trainer_id]
),
EwNpc(
    id_npc = "thenoid",
    active = True,
    str_name = "The Noid",
    description = "It's obvious, just avoid the Noid. Don't touch it.",
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["AVOOOOOID THE NOOOOOID!", "WHEEEE!", "ANFMXKAKNCNAEJD"],
                "loop":["HEHAHAHAHAHAHAHA!", "NOID!", "()https://s3-prod.adage.com/s3fs-public/20210429%29_Noid_3x2.jpg", "()https://static.wikia.nocookie.net/noid/images/a/ae/Mrgreen_dab_base.png/revision/latest/scale-to-width-down/250?cb=20180705000434", "()https://static.wikia.nocookie.net/noid/images/8/89/Mrgreen_angry_base.png/revision/latest?cb=20180705000425", "()I'M GONNA SAY PENIS!", "()https://images-ext-2.discordapp.net/external/iJ1Gv0mAX2KsSrzwPosYNgkcJAf-fvdYkuhcsmLYOQI/https/media.tenor.com/3vy4MVq4ms4AAAPo/breaking-bad-pizza.mp4", "()https://images-ext-2.discordapp.net/external/BMYY--1kwHktu4BXMEg0uOevsJxXa-SlxH6SJ2HcuyY/%3Fcid%3D73b8f7b1b5606a879da93500c3cae5f2de6109a01b9882f7%26rid%3Dgiphy.mp4%26ct%3Ds/https/media4.giphy.com/media/XbhTOfqVoIrlMIQhHZ/giphy.mp4", "()https://static.wikia.nocookie.net/noid/images/f/f0/Mrgreen_surprised_base.png/revision/latest?cb=20180705000456", "()https://cdn.discordapp.com/attachments/431240644464214017/1072654857015677028/image.png", "()https://tenor.com/view/pizza-fail-funny-drop-cooking-gif-23785565", "DOMINOS OR BUST", "YOU CAN'T AVOID ME!", "()https://tenor.com/view/pizza-party-oddly-soothing-serenity-now-pizza-lost-gif-5500152", "()https://tenor.com/view/pizza-pizza-party-gif-10580277", "I AM A CLUMSY LONG EARED MAN."],
                },
    func_ai = npcutils.needy_npc_action,
    image_profile = "https://compote.slate.com/images/fd2f8338-ec23-479f-bd89-f405909bf2d0.jpg",
    defaultslime = 15,
    defaultlevel = 1,
    slimeoid_name = "peperoni",
    rewards = [
    {"meatlovers": [80, 1, 3]},
    ],
    starting_statuses = ['7leveltrainer', ewcfg.status_enemy_trainer_id]
),
]

active_npcs_map = {}
spawn_probability_list = []


for npc in npc_list:
    if npc.active:
        active_npcs_map[npc.id_npc] = npc
        #print(npc.rarity)
        for x in range(min(npc.rarity, 10)): #the rarity determines frequency in the list, and thus spawn frequency, capped at 10
            spawn_probability_list.append(npc.id_npc)