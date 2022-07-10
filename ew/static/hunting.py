import random

from . import cfg as ewcfg
from ..model.hunting import EwAttackType
from ..model.hunting import EwNpc
from ew.utils import npcutils
from ew.static import poi_static

# Attacking type effects
def atf_fangs(ctn = None):
    # Reskin of dual pistols

    aim = (random.randrange(10) + 1)
    # ctn.sap_damage = 1

    if aim == (1 + int(10 * ctn.hit_chance_mod)):
        ctn.miss = True
        ctn.slimes_damage = 0
    elif aim == (10 - int(10 * ctn.crit_mod)):
        ctn.crit = True
        ctn.slimes_damage *= 2


def atf_talons(ctn = None):
    # Reskin of katana

    ctn.miss = False
    ctn.slimes_damage = int(0.85 * ctn.slimes_damage)
    # ctn.sap_damage = 0
    # ctn.sap_ignored = 10

    if (random.randrange(10) + 1) == (10 + int(10 * ctn.crit_mod)):
        ctn.crit = True
        ctn.slimes_damage *= 2.1


def atf_raiderscythe(ctn = None):
    # Reskin of scythe

    ctn.enemy_data.change_slimes(n=(-ctn.slimes_spent * 0.33), source=ewcfg.source_self_damage)
    ctn.slimes_damage = int(ctn.slimes_damage * 1.25)
    aim = (random.randrange(10) + 1)
    # ctn.sap_damage = 0
    # ctn.sap_ignored = 5

    if aim <= (2 + int(10 * ctn.hit_chance_mod)):
        ctn.miss = True
        ctn.slimes_damage = 0
    elif aim >= (9 - int(10 * ctn.crit_mod)):
        ctn.crit = True
        ctn.slimes_damage *= 2


def atf_gunkshot(ctn = None):
    # Reskin of rifle

    aim = (random.randrange(10) + 1)
    # ctn.sap_damage = 2

    if aim <= (2 + int(10 * ctn.hit_chance_mod)):
        ctn.miss = True
        ctn.slimes_damage = 0
    elif aim >= (9 - int(10 * ctn.crit_mod)):
        ctn.crit = True
        ctn.slimes_damage *= 2


def atf_tusks(ctn = None):
    # Reskin of bat

    aim = (random.randrange(21) - 10)
    # ctn.sap_damage = 3
    if aim <= (-9 + int(21 * ctn.hit_chance_mod)):
        ctn.miss = True
        ctn.slimes_damage = 0

    ctn.slimes_damage = int(ctn.slimes_damage * (1 + (aim / 10)))

    if aim >= (9 - int(21 * ctn.crit_mod)):
        ctn.crit = True
        ctn.slimes_damage = int(ctn.slimes_damage * 1.5)


def atf_molotovbreath(ctn = None):
    # Reskin of molotov

    dmg = ctn.slimes_damage
    ctn.slimes_damage = int(ctn.slimes_damage * 0.75)
    # ctn.sap_damage = 0
    # ctn.sap_ignored = 10

    aim = (random.randrange(10) + 1)

    # ctn.bystander_damage = dmg * 0.5

    if aim == (3 + int(10 * ctn.hit_chance_mod)):
        ctn.miss = True
        ctn.slimes_damage = 0

    elif aim == (10 - int(10 * ctn.crit_mod)):
        ctn.crit = True
        ctn.slimes_damage *= 2


def atf_armcannon(ctn = None):
    dmg = ctn.slimes_damage
    # ctn.sap_damage = 2

    aim = (random.randrange(20) + 1)

    if aim <= (2 + int(20 * ctn.hit_chance_mod)):
        ctn.miss = True

    if aim == (20 - int(20 * ctn.crit_mod)):
        ctn.crit = True
        ctn.slimes_damage *= 3


def atf_axe(ctn = None):
    ctn.slimes_damage *= 0.7
    aim = (random.randrange(10) + 1)

    if aim <= (4 + int(10 * ctn.hit_chance_mod)):
        ctn.miss = True

    if aim == (10 - int(10 * ctn.crit_mod)):
        ctn.crit = True
        ctn.slimes_damage *= 2


def atf_hooves(ctn = None):
    ctn.slimes_damage *= 0.4
    aim = (random.randrange(30) + 1)

    if aim <= (5 + int(30 * ctn.hit_chance_mod)):
        ctn.miss = True

    if aim > (25 - int(30 * ctn.crit_mod)):
        ctn.crit = True
        ctn.slimes_damage *= 2


def atf_body(ctn = None):
    ctn.slimes_damage *= 0.5
    aim = (random.randrange(10) + 1)

    if aim <= 2:
        ctn.miss = True

    if aim == 10:
        ctn.crit = True
        ctn.slimes_damage *= 2


def atf_smallclaws(ctn = None):
    chance = random.randrange(3)
    if chance <= 1:
        ctn.miss = True
    if chance == 2:
        strikes = random.randrange(5)
        ctn.strikes = strikes
        ctn.slimes_damage *= 0.05
    if chance == 3:
        ctn.slimes_damage *= 0.3
        ctn.crit = True


# All enemy attacking types in the game.
enemy_attack_type_list = [
    EwAttackType(  # 1
        id_type="fangs",
        str_crit="**Critical Hit!** {name_enemy} sinks their teeth deep into {name_target}!",
        str_miss="**{name_enemy} missed!** Their maw snaps shut!",
        # str_trauma_self = "You have bite marks littered throughout your body.",
        # str_trauma = "They have bite marks littered throughout their body.",
        str_kill="{name_enemy} opens their jaw for one last bite right on {name_target}'s juicy neck. **CHOMP**. Blood gushes out of their arteries and onto the ground. {emote_skull}",
        str_killdescriptor="mangled",
        str_damage="{name_target} is bitten on the {hitzone}!!",
        fn_effect=atf_fangs
    ),
    EwAttackType(  # 2
        id_type="talons",
        str_crit="**Critical hit!!** {name_target} is slashed across the chest!!",
        str_miss="**{name_enemy} missed!** Their wings flap in the air as they prepare for another strike!",
        # str_trauma_self = "A large section of scars litter your abdomen.",
        # str_trauma = "A large section of scars litter their abdomen.",
        str_kill="In a fantastic display of avian savagery, {name_enemy}'s talons grip {name_target}'s stomach, rip open their flesh and tear their intestines to pieces. {emote_skull}",
        str_killdescriptor="disembowled",
        str_damage="{name_target} has their {hitzone} clawed at!!",
        fn_effect=atf_talons
    ),
    EwAttackType(  # 3
        id_type="scythe",
        str_crit="**Critical hit!!** {name_target} is carved by the wicked curved blade!",
        str_miss="**MISS!!** {name_enemy}'s swings miss wide of the target!",
        # str_trauma_self = "You are wrapped tightly in bandages that hold your two halves together.",
        # str_trauma = "They are wrapped tightly in bandages that hold their two halves together.",
        str_kill="**SLASHH!!** {name_enemy}'s scythe cleaves the air, and {name_target} staggers. A moment later, {name_target}'s torso topples off their waist. {emote_skull}",
        str_killdescriptor="sliced in twain",
        str_damage="{name_target} is cleaved through the {hitzone}!!",
        fn_effect=atf_raiderscythe
    ),
    EwAttackType(  # 4
        id_type="gunkshot",
        str_crit="**Critical hit!!** {name_target} is covered in a thick, gelatenous ooze!",
        str_miss="**MISS!!** {name_enemy}'s gunk shot just barely missed the target!",
        # str_trauma_self = "Several locations on your body have decayed from the aftermath of horrific radiation.",
        # str_trauma = "Several locations on their body have decayed from the aftermath of horrific radiation.",
        str_kill="**SPLOOSH!!** {name_enemy}'s gunk shot completely envelops {name_target}, boiling their flesh alive in a radiation that rivals the Elephant's Foot. Nothing but a charred husk remains. {emote_skull}",
        str_killdescriptor="slimed on",
        str_damage="{name_target} is coated in searing, acidic radiation on their {hitzone}!!",
        fn_effect=atf_gunkshot
    ),
    EwAttackType(  # 5
        id_type="tusks",
        str_crit="**Critical hit!!** {name_target} is smashed hard by {name_enemy}'s tusks!",
        str_miss="**{name_enemy} missed!** Their tusks strike the ground, causing it to quake underneath!",
        # str_trauma_self = "You have one large scarred-over hole on your upper body.",
        # str_trauma = "They have one large scarred-over hole on their upper body.",
        str_kill="**SHINK!!** {name_enemy}'s tusk rams right into your chest, impaling you right through your back! Moments later, you're thrusted out on to the ground, left to bleed profusely. {emote_skull}",
        str_killdescriptor="pierced",
        str_damage="{name_target} has tusks slammed into their {hitzone}!!",
        fn_effect=atf_tusks
    ),
    EwAttackType(  # 6
        id_type="molotovbreath",
        # str_backfire = "**Oh the humanity!!** {name_enemy} tries to let out a breath of fire, but it combusts while still inside their maw!!",
        str_crit="**Critical hit!!** {name_target} is char grilled by {name_enemy}'s barrage of molotov breath!",
        str_miss="**{name_enemy} missed!** Their shot hits the ground instead, causing embers to shoot out in all directions!",
        # str_trauma_self = "You're wrapped in two layers of bandages. What skin is showing appears burn-scarred.",
        # str_trauma = "They're wrapped in two layers of bandages. What skin is showing appears burn-scarred.",
        str_kill="In a last ditch effort, {name_enemy} breathes in deeply for an extra powerful shot of fire. Before you know it, your body is cooked alive like a rotisserie chicken. {emote_skull}",
        str_killdescriptor="exploded",
        str_damage="{name_target} is hit by a blast of fire on their {hitzone}!!",
        fn_effect=atf_molotovbreath
    ),
    EwAttackType(  # 7
        id_type="armcannon",
        str_crit="**Critical hit!!** {name_target} has a clean hole shot through their chest by {name_enemy}'s bullet!",
        str_miss="**{name_enemy} missed their target!** The stray bullet cleaves right into the ground!",
        # str_trauma_self = "There's a deep bruising right in the middle of your forehead.",
        # str_trauma = "There's a deep bruising right in the middle of their forehead.",
        str_kill="{name_enemy} readies their crosshair right for your head and fires without hesitation. The force from the bullet is so powerful that when it lodges itself into your skull, it rips your head right off in the process. {emote_skull}",
        str_killdescriptor="sniped",
        str_damage="{name_target} has a bullet zoom right through their {hitzone}!!",
        fn_effect=atf_armcannon
    ),
    EwAttackType(  # 8
        id_type="axe",
        str_crit="**Critical hit!!** {name_target} is thoroughly cleaved by {name_enemy}'s axe!",
        str_miss="**{name_enemy} missed!** The axe gives a loud **THUD** as it strikes the earth!",
        # str_trauma_self = "There's a hefty amount of bandages covering the top of your head",
        # str_trauma = "There's a hefty amount of bandages covering the top of their head",
        str_kill="{name_enemy} lifts up their axe for one last swing. The wicked edge buries itself deep into your skull, cutting your brain in twain. {emote_skull}",
        str_killdescriptor="axed",
        str_damage="{name_target} is swung at right on their {hitzone}!!",
        fn_effect=atf_axe
    ),
    EwAttackType(  # 9
        id_type="hooves",
        str_crit="**Critical hit!!** {name_enemy} lays a savage hind-leg kick into {name_target}'s chest!",
        str_miss="**WHOOSH!** {name_enemy}'s hooves just barely miss you!",
        # str_trauma_self = "Your chest is somewhat concave.",
        # str_trauma = "Their chest is somewhat concave.",
        str_kill="{name_enemy} gallops right over your head, readying their hind legs just after landing. Before you can even ready your weapon, their legs are already planted right onto your chest. Your heart explodes. {emote_skull}",
        str_killdescriptor="stomped",
        str_damage="{name_target} is stomped all over their {hitzone}!!",
        fn_effect=atf_hooves
    ),
    EwAttackType(  # 10
        id_type="body",
        str_crit="**OOF!!** {name_enemy} lands a critical strike onto {name_target}'s torso with the sheer impact of their body weight!",
        str_miss="**MISS!** {name_enemy} flails their body around to try and attack {name_target}, but nothing happens...",
        # str_trauma_self = "Your have deep bruising on your torso.",
        # str_trauma = "They have deep bruising on their torso.",
        str_kill="{name_enemy} throws every once of force they can at you with your body. The impact is so strong that you're slammed into the ground, shattering your skull. {emote_skull}",
        str_killdescriptor="pushed around",
        str_damage="{name_target} gets bumped around a bit on their {hitzone}!",
        fn_effect=atf_body
    ),
    EwAttackType(  # 11
        id_type="amateur",
        str_crit="**AIIIIEEE!!** {name_enemy} screams in abject fear, lunging at {name_target}'s with a {civ_weapon} in hand! Fuck, they actually got you!",
        str_miss="**MISS!** {name_enemy} trips and falls facefirst on the ground. {name_target} is holding back their laughter at how goddamn stupid this all is.",
        # str_trauma_self = "Your have deep bruising on your torso.",
        # str_trauma = "They have deep bruising on their torso.",
        str_kill="{name_enemy} is thrown into an adrenaline rush! They brandish their {civ_weapon} and throw it in a perfect spiral, directly through {name_target}'s skull. {emote_skull}",
        str_killdescriptor="felled",
        str_damage="{name_enemy} bludgeons {name_target} in the {hitzone}! At least they try to...",
        fn_effect=atf_body
    ),
    EwAttackType(  # 11
        id_type="stomp",
        str_crit="**OH FUCK!** The titanoslime reels back onto its hind legs, stomping {name_target} deeper and deeper into the asphalt!",
        str_miss="**MISS!** {name_target} jumps barely out of the way of a stomp!",
        # str_trauma_self = "Your have deep bruising on your torso.",
        # str_trauma = "They have deep bruising on their torso.",
        str_kill="**CRUNCH!!** The titanoslime locks its teeth into your flesh, snapping you clean in half and swallowing all but your legs! You can feel the creatures stomach acid stinging on your face before you rapidly lose consciousness.{emote_skull}",
        str_killdescriptor="vored",
        str_damage="{name_enemy} swings it's car width legs full speed into {name_target}!",
        fn_effect=atf_tusks
    ),
    EwAttackType(  # 11
        id_type="stompn6",
        str_crit="**YIPPIE KI YAY MOTHER FUCKERS!!!** N6 pulls back the reins, reeling the Titanoslime up and stomping {name_target} deeper and deeper into the asphalt!",
        str_miss="**MISS!** {name_target} jumps barely out of the way of a stomp! You can hear N6 cursing from atop her steed.",
        # str_trauma_self = "Your have deep bruising on your torso.",
        # str_trauma = "They have deep bruising on their torso.",
        str_kill="N6 pulls out some kind of laser pistol and aims it directly at you. **FOOM!** You don't see the next moment because your eyes are now a fine powder. You bleed out the sockets for a few minutes before collapsing dead in the street.{emote_skull}",
        str_killdescriptor="disintegrated",
        str_damage="{name_enemy} swings it's car width legs full speed into {name_target}! N6 laughs and watches you eat shit on the pavement!",
        fn_effect=atf_tusks
    ),
    EwAttackType(  # 12
        id_type="gnash",
        str_crit="**GNASH GNASH GNASH!!!** The {name_enemy} opens it's mouth as wide it can go and chomps down on {name_target}! OOF!",
        str_miss="**MISS!** {name_target} barely sidesteps the {name_enemy}'s lunging bite!",
        str_kill="**GNASH!!!** The {name_enemy} catches you in it's mouth and flails you around a little, for effect. The world fades from view as the venom takes over. {emote_skull}",
        str_killdescriptor="gnashed",
        str_damage="{name_enemy} chomps into {name_target}! {name_target} is looking a little woozy!",
        fn_effect=atf_fangs
    ),
    EwAttackType(  # 13
        id_type="beak",
        str_crit="**PECK PECK PECK!!!** The {name_enemy} rips you to shreds! {name_target} is bleeding profusely!",
        str_miss="**SWOOSH!** {name_target} barely misses {name_enemy} and swoops around for another shot!",
        str_kill="**PECK PECK!!!** The {name_enemy} swoops at you with malice in their eyes. {name_target} never had a chance as their skin is ripped off, piece by piece. {emote_skull}",
        str_killdescriptor="pecked",
        str_damage="{name_enemy} pecks at {name_target}! They draw blood!",
        fn_effect=atf_talons
    ),
    EwAttackType(  # 14
        id_type="graspers",
        str_crit="**AAAAAHHHHHHH!!!** The {name_enemy} starts to wail as it twists and wrings slime out of your body! {name_target} breaks several bones!",
        str_miss="**WHOA!** You barely duck out of the way of {name_enemy}'s grasp!",
        str_kill="**RRRRRRIPPPP!!!** The {name_enemy} tears you in half! Actually it looks disappointed, {name_target} was a pretty interesting specimen. {emote_skull}",
        str_killdescriptor="strangled",
        str_damage="{name_enemy} constricts their graspers all over {name_target}! Creepy!",
        fn_effect=atf_body
    ),
    EwAttackType(  # 15
        id_type="raygun",
        str_crit="**PEWPEWPEW!!!** The {name_enemy} fires several shots right in the kisser! {name_target} is stunned and blinded!",
        str_miss="**PEW -SSSSSSS!** You barely dodge a laser blast! You hair's singed...",
        str_kill="**PEW -SSSSHhhhh.** The {name_enemy} finally hit its mark, {name_target} disintegrated into a pile of char and goo. {emote_skull}",
        str_killdescriptor="beamed",
        str_damage="{name_enemy} nails {name_target} with their laser pistol!",
        fn_effect=atf_gunkshot
    ),
    EwAttackType(  # 16
        id_type="feed",
        str_crit="**CRUNCH!!!** The {name_enemy} clutches {name_target}'s shouders and takes a bite from their neck! GET IT OFF GET IT OFF GET IT OFF!",
        str_miss="**WHOOSH-SMACK!** You jump out of the way of {name_enemy}'s lunge and kick them away!",
        str_kill="**GULP.** The {name_enemy} swallows you whole! {name_target} can feel a load of stomach acid on their face and then nothing. {emote_skull}",
        str_killdescriptor="eaten alive",
        str_damage="{name_enemy} bites {name_target} deep!",
        fn_effect=atf_fangs
    ),
    EwAttackType(  #17
        id_type="titanoslime",
        str_crit="NULL",
        str_miss="**MISS!** {name_target} barely jumps out of the way of {name_enemy}'s foot!",
        # str_trauma_self = "NULL",
        # str_trauma = "NULL,
        str_kill="**WRYYYYYYYY!!!!!** {name_enemy}'s collossal jowls slice {name_target} completely in half! As they lose conciousness, {name_target} can feel the burn of the acid on their face as they sink helplessly into its churning stomach. {emote_skull}",
        str_killdescriptor="vored",
        str_damage="{name_target} takes the brunt of {name_enemy}'s stomp!",
        str_groupattack="{name_enemy} tailsweeps a horde of gaiaslimeoids!",
        fn_effect=atf_tusks
    ),
EwAttackType(  #17
        id_type="police",
        str_crit="**POLICE BRUTALITY!** {name_enemy} knees {name_target} to the ground and fires 3 shots right to the head! ",
        str_miss="**WHOOSH** {name_target} ducks out of the way of {name_enemy}'s nightstick!",
        # str_trauma_self = "NULL",
        # str_trauma = "NULL,
        str_kill="**HE'S GOT A WEAPON!** {name_enemy} empties a whole clip into {name_target}'s soft juvenile head, absolutely shocked that they managed to not die this time. Guess we know what'll be on the news in a few days...",
        str_killdescriptor="vored",
        str_damage="{name_target} fires a warning shot into {name_enemy}'s {hitzone}!",
        fn_effect=atf_fangs #a pistol reskin of fangs which are a reskin of a pistol
    ),
]

#Values are sorted by the chance to the drop an item, and then the minimum and maximum amount of times to drop that item.

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
    dialogue = {"talk":["I'm a PI, bud. No need to get all panicky.", "I see your hands reaching into your pockets. A rookie like you shouldn't try anythin funny.", "At this point, getting killed's about as inconvenient as missing the train. You still shouldn't try it, squirt.", ""],
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
    starting_statuses=[],
    attacktype = 'police',
    condition = lambda user_data, enemy_data: True if user_data.crime > 1250000 else False
    #if the cop is trigger happy or if you're above a certain crime level
),
]

active_npcs_map = {}

for npc in npc_list:
    if npc.active:
        active_npcs_map[npc.id_npc] = npc





# A map of id_type to EwAttackType objects.
attack_type_map = {}

# Populate attack type map.
for attack_type in enemy_attack_type_list:
    attack_type_map[attack_type.id_type] = attack_type



