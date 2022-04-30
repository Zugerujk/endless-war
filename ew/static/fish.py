import json
import os
from re import M

from ..model.fish import EwFish

# All the fish, baby!
fish_list = [
    EwFish(
        id_fish = "arsonfish",
        str_name = "Arsonfish",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "Its scales are so hot, you continuously toss the fish upwards to avoid getting burned.",
        slime = None,
    ),
    EwFish(
        id_fish = "moldfish",
        str_name = "Mold Fish",
        rarity = "common",
        catch_time = None,
        catch_weather = "foggy",
        str_desc = "It's said to have the memory capacity of 16 GB.",
        slime = None,
    ),
    EwFish(
        id_fish = "neonjuvie",
        str_name = "Neon Juvie",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "Pretty Juviecore.",
        slime = None,
    ),
    EwFish(
        id_fish = "clouttrout",
        str_name = "Clout Trout",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "This fish has the eyes of a winner.",
        slime = None,
    ),
    EwFish(
        id_fish = "slimekoi",
        str_name = "Slimekoi",
        rarity = "common",
        catch_time = None,
        catch_weather = "sunny",
        str_desc = "Slimekoi is a level 3 slimeboi.",
        slime = None,
    ),
    EwFish(
        id_fish = "deadkoi",
        str_name = "Deadkoi",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "Deadkoi is a level 3 deadboi.",
        slime = None,
    ),
    EwFish(
        id_fish = "slimesmelt",
        str_name = "Slime Smelt",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "It could sure use a bath.",
        slime = None,
    ),
    EwFish(
        id_fish = "hardboiledturtle",
        str_name = "Hard Boiled Turtle",
        rarity = "common",
        catch_time = None,
        catch_weather = "rainy",
        str_desc = "This radical dude doesn't take shit from anyone.",
        slime = None,
    ),
    EwFish(
        id_fish = "oozesalmon",
        str_name = "Ooze Salmon",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "You wonder how good it would taste on a bagel.",
        slime = None,
    ),
    EwFish(
        id_fish = "toxicpike",
        str_name = "Toxic Pike",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "Don't let it bite you.",
        slime = None,
    ),
    EwFish(
        id_fish = "slimymullet",
        str_name = "Slimy Mullet",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "You have some trouble keeping it in your grip.",
        slime = None,
    ),
    EwFish(
        id_fish = "scabgrabbers",
        str_name = "Scab Grabbers",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "Make sure you don't let one of these fuckers latch onto a wound.",
        slime = None,
    ),
    EwFish(
        id_fish = "thugfish",
        str_name = "Thugfish",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "These fish are known for being the bullies you find within all fish schools.",
        slime = None,
    ),
    EwFish(
        id_fish = "globfish",
        str_name = "Glob Fish",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "Its really sticky and smells like sulfur. Kinda nasty.",
        slime = None,
    ),
    EwFish(
        id_fish = "largebonedlionfish",
        str_name = "Large-Boned Lionfish",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "These fish evolved to have less meat in order to avoid fishers. Didn't work, clearly.",
        slime = None,
    ),
    EwFish(
        id_fish = "palemunch",
        str_name = "Pale Munch",
        rarity = "common",
        catch_time = "day",
        catch_weather = None,
        str_desc = "This fish looks like it needs some sleep.",
        slime = None,
    ),
    EwFish(
        id_fish = "pinksnapper",
        str_name = "Pink Snapper",
        rarity = "common",
        catch_time = "day",
        catch_weather = None,
        str_desc = "Quite Rowdycore.",
        slime = None,
    ),
    EwFish(
        id_fish = "killifish",
        str_name = "Killifish",
        rarity = "common",
        catch_time = "night",
        catch_weather = None,
        str_desc = "Apparently there are 1270 different species of Killifish.",
        slime = None,
    ),
    EwFish(
        id_fish = "barbeln8",
        str_name = "Barbel N8",
        rarity = "common",
        catch_time = "night",
        catch_weather = None,
        str_desc = "It looks like it could run a shady corporation.",
        slime = None,
    ),
    EwFish(
        id_fish = "killercod",
        str_name = "Killer Cod",
        rarity = "common",
        catch_time = "night",
        catch_weather = None,
        str_desc = "Quite Killercore.",
        slime = None,
    ),
    EwFish(
        id_fish = "jellyturkeyfish",
        str_name = "Jelly Turkey Fish",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "You nearly prick your finger on one of the many venomous spines on its back.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "modelopole",
        str_name = "Modelopole",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "UH-OH, IT'S MODELOPOLE TIME!",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "corpsecarp",
        str_name = "Corpse Carp",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "It smells like a rotting fish.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "thrash",
        str_name = "Thrash",
        rarity = "common",
        catch_time = "day",
        catch_weather = None,
        str_desc = "Pretty Rowdycore.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "snakeheadtrout",
        str_name = "Snakehead Trout",
        rarity = "common",
        catch_time = "night",
        catch_weather = "sunny",
        str_desc = "It has the body of a trout and the head of a snake. Heavy fuckin' metal.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "dab",
        str_name = "Dab",
        rarity = "common",
        catch_time = "night",
        catch_weather = None,
        str_desc = "Pretty Killercore.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "jarocephalopod",
        str_name = "Jar O' Cephalopod",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "It looks content in there.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "cruna",
        str_name = "Cruna",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "You've heard that these taste great in salads.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "neoneel",
        str_name = "Neon Eel",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "Its slippery body is bathed in a bright green glow.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "slimesquid",
        str_name = "Slime Squid",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "Apparently these things have three hearts.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "gar",
        str_name = "Gar",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "You have the strange urge to wrestle this fish into submission. You almost resist it.",
        slime = None,
    ),
    EwFish(
        id_fish = "lee",
        str_name = "Lee",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = "sunny",
        str_desc = "Oh shit, it's Lee!",
        slime = None,
    ),
    EwFish(
        id_fish = "greengill",
        str_name = "Greengill",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "Its gills ooze out some green stuff if you squeeze it.",
        slime = None,
    ),
    EwFish(
        id_fish = "italiansnapper",
        str_name = "Italian Snapper",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "You think you can hear this fish murmur some inarticulate Italian noises on occasion.",
        slime = None,
    ),
    EwFish(
        id_fish = "piranhoid",
        str_name = "Piranhoid",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "This fish is said to occasionally jump out of the water and bite unsuspecting slimeoids.",
        slime = None,
    ),
    EwFish(
        id_fish = "torrentfish",
        str_name = "Torrentfish",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = "foggy",
        str_desc = "This fish looks like it doesn't pay for ANY of its anime.",
        slime = None,
    ),
    EwFish(
        id_fish = "transbeam",
        str_name = "Trans Bream",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "If you remain in this city for long enough, you'll become one too (If you haven't already).",
        slime = None,
    ),
    EwFish(
        id_fish = "char",
        str_name = "Char",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "These fish migrated south after the North Pole was nuked.",
        slime = None,
    ),
    EwFish(
        id_fish = "devfish",
        str_name = "Devfish",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "This fish looks quite tired of your bullshit.",
        slime = None,
    ),
    EwFish(
        id_fish = "flarp",
        str_name = "Flarp",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "It's a carp that's really flexible.",
        slime = None,
    ),
    EwFish(
        id_fish = "arcticbluelip",
        str_name = "Arctic Blue Lip",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = "snow",
        str_desc = "Holy shit, this fish is cold.",
        slime = None,
    ),
    EwFish(
        id_fish = "neomilwaukianmittencrab",
        str_name = "Neo-Milwaukian Mitten Crab",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = "snow",
        str_desc = "Known for their furry claws, Mitten Crabs were considered an invasive species, but eventually people stopped caring about that because they had bigger fish to fry (metaphorically, of course).",
        slime = None,
    ),
    EwFish(
        id_fish = "yellowslash",
        str_name = "Yellow Slash",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "This fish is the successor to Classic Milwaukee's Yellow Perch.",
        slime = None,
    ),
    EwFish(
        id_fish = "nuclearbream",
        str_name = "Nuclear Bream",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = "sunny",
        str_desc = "Not to be confused with BREEAM, although this fish looks like its in the mood for assessing shit.",
        slime = None,
    ),
    EwFish(
        id_fish = "flopfish",
        str_name = "Flop Fish",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "It's floppin'.",
        slime = None,
    ),
    EwFish(
        id_fish = "cardboardcrab",
        str_name = "Cardboard Crab",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "It reminds you of your last meal at Red Mobster because that shit sure as hell tasted like cardboard heyoooo!",
        slime = None,
    ),
    EwFish(
        id_fish = "straubling",
        str_name = "Straubling",
        rarity = "uncommon",
        catch_time = "day",
        catch_weather = None,
        str_desc = "No relation.",
        slime = None,
    ),
    EwFish(
        id_fish = "holykrakerel",
        str_name = "Holy Krakerel",
        rarity = "uncommon",
        catch_time = "night",
        catch_weather = None,
        str_desc = "It looks bovine-adjacent.",
        slime = None,
    ),
    EwFish(
        id_fish = "magicksdorado",
        str_name = "magicksDorado",
        rarity = "uncommon",
        catch_time = "night",
        catch_weather = None,
        str_desc = "No relation.",
        slime = None,
    ),
    EwFish(
        id_fish = "iridescentsnapper",
        str_name = "Iridescent Snapper",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = "sunny",
        str_desc = "Its scales change color if you shake it. Fun.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "barredkatanajaw",
        str_name = "Barred Katana Jaw",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "Its stripes make it look vaguely Japanese.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "souroctopus",
        str_name = "Sour Octopus",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "It would rather be in a jar",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "mace",
        str_name = "Mace",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "These fish are called Mud Carps in Nu Hong Kong.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "croach",
        str_name = "Croach",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "He's from out of town.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "thalamuscaranx",
        str_name = "Thalamus Caranx",
        rarity = "uncommon",
        catch_time = "night",
        catch_weather = None,
        str_desc = "Finally, a worthy fish emerges.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "fuckshark",
        str_name = "Fuck Shark",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "You recall reading that this thing has the same nutritional value as SUPER WATER FUCK ENERGY.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "seajuggalo",
        str_name = "Sea Juggalo",
        rarity = "uncommon",
        catch_time = "day",
        catch_weather = None,
        str_desc = "This motherfucker definitely has some sick fuckin' musical taste.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "bufferfish",
        str_name = "Bufferfish",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "This fish has the ability to lag out predators in order to get away.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "arijuana",
        str_name = "Arijuana",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = "sunny",
        str_desc = "These fish are banned from the USA.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "piranhaha",
        str_name = "Piranhaha",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "Its toothy smile gives you the creeps. You don't want to know why it's laughing.",
        slime = None,
    ),
    EwFish(
        id_fish = "plebefish",
        str_name = "Plebefish",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "God. This fucking nerd. It just doesn't fucking GET it.",
        slime = None,
    ),
    EwFish(
        id_fish = "galaxyfrog",
        str_name = "Galaxy Frog",
        rarity = "rare",
        catch_time = None,
        catch_weather = "rainy",
        str_desc = "It's a big fuckin' color-changing frog.",
        slime = None,
    ),
    EwFish(
        id_fish = "gillboss",
        str_name = "Gill Boss",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "Gaslight, gatekeep, Gill Boss.",
        slime = None,
    ),
    EwFish(
        id_fish = "catboyfish",
        str_name = "Catboyfish",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "Oh no.",
        slime = None,
    ),
    EwFish(
        id_fish = "gooper",
        str_name = "Gooper",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "These fish are able to suck prey into their mouths like vacuums.",
        slime = None,
    ),
    EwFish(
        id_fish = "blacklimesalmon",
        str_name = "Black Lime Salmon",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "Kinda smells like Black Limes.",
        slime = None,
    ),
    EwFish(
        id_fish = "kinkfish",
        str_name = "Kinkfish",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "This fish looks like it's down to get wacky.",
        slime = None,
    ),
    EwFish(
        id_fish = "easysardines",
        str_name = "Easy Sardines",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "In terms of difficulty, this little bitch looks real low on the rungs.",
        slime = None,
    ),
    EwFish(
        id_fish = "mertwink",
        str_name = "Mertwink",
        rarity = "rare",
        catch_time = None,
        catch_weather = "snow",
        str_desc = "Rejoice, horndogs.",
        slime = None,
    ),
    EwFish(
        id_fish = "grandclam",
        str_name = "Grand Clam",
        rarity = "rare",
        catch_time = None,
        catch_weather = "snow",
        str_desc = "This clam has a sporty look to it.",
        slime = None,
    ),
    EwFish(
        id_fish = "bigtopoctopus",
        str_name = "Big Top Octopus",
        rarity = "rare",
        catch_time = "day",
        catch_weather = None,
        str_desc = "It kinda looks like a circus tent.",
        slime = None,
    ),
    EwFish(
        id_fish = "solarfrog",
        str_name = "Solar Frog",
        rarity = "rare",
        catch_time = "day",
        catch_weather = "sunny",
        str_desc = "Don't stare at it!",
        slime = None,
    ),
    EwFish(
        id_fish = "sweetfish",
        str_name = "Sweet Fish",
        rarity = "rare",
        catch_time = "day",
        catch_weather = None,
        str_desc = "Also known as Gillanaks.",
        slime = None,
    ),
    EwFish(
        id_fish = "lunarfrog",
        str_name = "Lunar Frog",
        rarity = "rare",
        catch_time = "night",
        catch_weather = "sunny",
        str_desc = "It's said to control the waves of the Slime Sea.",
        slime = None,
    ),
    EwFish(
        id_fish = "angerfish",
        str_name = "Angerfish",
        rarity = "rare",
        catch_time = None,
        catch_weather = "sunny",
        str_desc = "It doesn't look very happy to be here.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "nibblefish",
        str_name = "Nibblefish",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "It looks hungry.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "sourfish",
        str_name = "Sour Fish",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "It gives you an oddly cynical gaze.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "stunfisk",
        str_name = "Stunfisk",
        rarity = "rare",
        catch_time = None,
        catch_weather = "rainy",
        str_desc = "Its hide is so tough it can be stepped on by a pink whale without being injured.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "relicanth",
        str_name = "Relicanth",
        rarity = "rare",
        catch_time = None,
        catch_weather = "rainy",
        str_desc = "It doesn't have teeth.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "fantaray",
        str_name = "Fanta Ray",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "You consider licking it to see if it actually tastes like soda.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "slimewatergoby",
        str_name = "Slimewater Goby",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "This little fucko hates fun.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "uncookedkingpincrab",
        str_name = "Kingpin Crab",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "It reminds you of your last meal at Red Mobster.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "clownfish",
        str_name = "Clownfish",
        rarity = "rare",
        catch_time = "day",
        catch_weather = None,
        str_desc = "Its face kinda looks like a clown if you squint.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "seasaint",
        str_name = "Seasaint",
        rarity = "rare",
        catch_time = "night",
        catch_weather = None,
        str_desc = "It has a beanie on.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "anglershark",
        str_name = "Angler Shark",
        rarity = "rare",
        catch_time = "night",
        catch_weather = "foggy",
        str_desc = "It has a little poudrin on its head.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "doublestuffedflounder",
        str_name = "Double-Stuffed Flounder",
        rarity = "promo",
        catch_time = None,
        catch_weather = None,
        str_desc = "No one out-Flounders this fish.",
        slime = None,
    ),
    EwFish(
        id_fish = "seacolonel",
        str_name = "Sea Colonel",
        rarity = "promo",
        catch_time = None,
        catch_weather = None,
        str_desc = "This fish definitely looks like it dropped out of high school.",
        slime = None,
    ),
    EwFish(
        id_fish = "marlinsupreme",
        str_name = "Marlin Supreme",
        rarity = "promo",
        catch_time = None,
        catch_weather = None,
        str_desc = "Live mas.",
        slime = None,
    ),
    EwFish(
        id_fish = "universefrog",
        str_name = "Universe Frog",
        rarity = "promo",
        catch_time = None,
        catch_weather = "sunny",
        str_desc = "It's a huge fuckin' color-changing frog.",
        slime = None,
    ),
    EwFish(
        id_fish = "regiarapaima",
        str_name = "Regiarapaima",
        rarity = "promo",
        catch_time = None,
        catch_weather = "rainy",
        str_desc = "Regigigas sends his regards.",
        slime = None,
    ),
    EwFish(
        id_fish = "mermaid",
        str_name = "Mermaid",
        rarity = "secret",
        catch_time = None,
        catch_weather = None,
        str_desc = "Holy shit, what the fuck? It's actually real? You caught a fucking mermaid! Has that ever even happened before? That's actually pretty impressive, I'm proud of you. You should show it to that one guy in the Speakeasy.",
        slime = None,
    ),
    EwFish(
        id_fish = "octohuss",
        str_name = "Octohuss",
        rarity = "promo",
        catch_time = None,
        catch_weather = None,
        str_desc = "Don't let it near a horse. Or a drawing tablet.",
        slime = None,
    ),
    EwFish(
        id_fish = "paradoxcrocodile",
        str_name = "Paradox Crocodile",
        rarity = "promo",
        catch_time = None,
        catch_weather = None,
        str_desc = "He's a paradox! A contradiction! What a wild and crazy guy.",
        slime = "freshwater",
    ),
    EwFish(
        id_fish = "bathyphysaheadshark",
        str_name = "Bathyphysahead Shark",
        rarity = "promo",
        catch_time = None,
        catch_weather = "foggy",
        str_desc = "This one looks fucking terrifying. I'm serious.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "thebassedgod",
        str_name = "The Bassed God",
        rarity = "promo",
        catch_time = None,
        catch_weather = None,
        str_desc = "This is The Bassed God. He's gonna fuck your bitch.",
        slime = "saltwater",
    ),
    EwFish(
        id_fish = "negaslimesquid",
        str_name = "Negaslime Squid",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "It's just a black squid, but spooky.",
        slime = "void",
    ),
    EwFish(
        id_fish = "voidfish",
        str_name = "Void Fish",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "Translucent and quiet, it weighs less than nothing",
        slime = "void",
    ),
    EwFish(
        id_fish = "corpsefish",
        str_name = "Corpse Fish",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "It's just laying there.",
        slime = "void",
    ),
    EwFish(
        id_fish = "bonedoctopus",
        str_name = "Boned Octopus",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "Its tentacles crack while wriggling.",
        slime = "void",
    ),
    EwFish(
        id_fish = "artifish",
        str_name = "Artifish",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "It's chromatically abhorrent.",
        slime = "void",
    ),
    EwFish(
        id_fish = "stinggray",
        str_name = "Sting Gray",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "Its monochrome color remembers you of old-timey movies. Just as drab and antiquated.",
        slime = "void",
    ),
    EwFish(
        id_fish = "kaleidoscuttle",
        str_name = "Kaleidoscuttle",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "Whoa, dude.",
        slime = "void",
    ),
    EwFish(
        id_fish = "deathfish",
        str_name = "Death Fish",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "It is the beast it worships.",
        slime = "void",
    ),
    EwFish(
        id_fish = "ghostfish",
        str_name = "Ghost Fish",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "You remind yourself not to dip it in coleslaw.",
        slime = "void",
    ),
    EwFish(
        id_fish = "boxcrab",
        str_name = "Box Crab",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "Hiding in its own little fort. Not to be confused with the Cardboard Crab.",
        slime = "void",
    ),
    EwFish(
        id_fish = "bluejelly",
        str_name = "Blue Jelly",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "Its tentacles look like a mop head.",
        slime = "void",
    ),
    EwFish(
        id_fish = "lichfish",
        str_name = "Lich Fish",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "What you didn't reel is its phylactery.",
        slime = "void",
    ),
    EwFish(
        id_fish = "elderelver",
        str_name = "Elder Elver",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "Despite its seemingly young age, this eel has seen many eons pass. Treat it with respect.",
        slime = "void",
    ),
    EwFish(
        id_fish = "logfish",
        str_name = "Logfish",
        rarity = "promo",
        catch_time = None,
        catch_weather = None,
        str_desc = "WOODEN AND HORRIFYING.",
        slime = "void",
    ),
    EwFish(
        id_fish = "highmonkfish",
        str_name = "High Monkfish",
        rarity = "promo",
        catch_time = None,
        catch_weather = None,
        str_desc = "First of its creed.",
        slime = "void",
    ),
    EwFish(
        id_fish = "dahmerheadshark",
        str_name = "Dahmerhead Shark",
        rarity = "promo",
        catch_time = None,
        catch_weather = None,
        str_desc = "This dude just has a bad vibe.",
        slime = "void",
    ),
    # FISHINGEVENT - Event Fish
    # Common
    EwFish(
        id_fish = "deadplebefish",
        str_name = "Dead Plebefish",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "He overdosed ): .",
        slime = "event",
    ),
    EwFish(
        id_fish = "dabbutithasavape",
        str_name = "Dab But It Has A Vape",
        rarity = "common",
        catch_time = "night",
        catch_weather = None,
        str_desc = "Definitely hasn't developed an addiction to mango vape pens.",
        slime = "event",
    ),
    EwFish(
        id_fish = "thrashbutitsoncocaine",
        str_name = "Thrash But It's On Cocaine",
        rarity = "common",
        catch_time = "day",
        catch_weather = None,
        str_desc = "GETTT ROOOOOWWWWWWWWWWWWDDDDDDDDDDDYYYYYYYYYYYY MF'ERRRRRRRRRRRRRRRRRRR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
        slime = "event",
    ),
    EwFish(
        id_fish = "methamphetaminnow",
        str_name = "Methamphetaminnow",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "Its shiny quartz-like hide is quite delicious!",
        slime = "event",
    ),
    # Uncommon
    EwFish(
        id_fish = "needlefish",
        str_name = "Needlefish",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "Don't prick yourself!",
        slime = "event",
    ),
    EwFish(
        id_fish = "fangblenny",
        str_name = "Fang Blenny",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "One bite from this guy's chompers and you'll be OUT.",
        slime = "event",
    ),
    EwFish(
        id_fish = "salviamander",
        str_name = "Salviamander",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "Frequently bouncing on his boy's dick.",
        slime = "event",
    ),
    # Rare
    EwFish( # Gives BLUNT effects 
        id_fish = "weedurchin",
        str_name = "Weed Urchin",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "An urchin that's totallyyyyyyy chill, broh.",
        slime = "event",
    ),
    EwFish(
        id_fish = "blackgar",
        str_name = "Black Gar",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "It may have a snout, but there's no included spoon.",
        slime = "event",
    ),
    EwFish(
        id_fish = "salemaporgyznuts",
        str_name = "Salema Porgyznuts",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "Loves to roast people so hard. Just like ITS DICK OOOOOHHHHHHHHHHHHHHHHHHHHH.",
        slime = "event",
    ),
    # Promo
    EwFish(
        id_fish = "deepseaaddict",
        str_name = "Deep-Sea Addict",
        rarity = "promo",
        catch_time = None,
        catch_weather = None,
        str_desc = "The corpse of a slimeboi who tried to brave the Slime Sea's depths for some *exotic drugs*.",
        slime = "event",
    ),
    EwFish(
        id_fish = "prescriptionpilligator",
        str_name = "Prescription Pilligator",
        rarity = "promo",
        catch_time = None,
        catch_weather = None,
        str_desc = "Noooo babyyyy don't abuse your meds, your so sexy ahahaa :pleading:...,,.",
        slime = "event",
    ),
    EwFish(
        id_fish = "merhunk",
        str_name = "Merhunk",
        rarity = "promo",
        catch_time = None,
        catch_weather = None,
        str_desc = "Formerly a mertwink, it gained its big buff bara dom daddy hot hot hot hot steamy physique from... ***STEROIDS!!!***",
        slime = "event",
    ),
]

# A map of id_fish to EwFish objects.
fish_map = {}

common_fish = []
uncommon_fish = []
rare_fish = []
promo_fish = []
secret_fish = []

rainy_fish = []
sunny_fish = []
foggy_fish = []
snow_fish = []
night_fish = []
day_fish = []

salt_fish = []
fresh_fish = []
void_fish = []
event_fish = [] # FISHINGEVENT

size_to_reward = {
    "miniscule": 1,
    "small": 2,
    "average": 3,
    "big": 4,
    "huge": 5,
    "colossal": 6
}

rarity_to_reward = {
    "common": 1,
    "uncommon": 2,
    "rare": 3,
    "promo": 4,
    "secret": 8,
}

rarity_to_list = {
    "common": common_fish,
    "uncommon": uncommon_fish,
    "rare": rare_fish,
    "promo": promo_fish,
    "secret": secret_fish,
}

# A list of fish names.
fish_names = []

# Populate fish map, including all aliases.
for fish in fish_list:
    fish_map[fish.id_fish] = fish
    fish_names.append(fish.id_fish)
    # Categorize fish into their rarities
    rarity_to_list[fish.rarity].append(fish.id_fish)
    if fish.catch_weather == "rainy":
        rainy_fish.append(fish.id_fish)
    elif fish.catch_weather == "sunny":
        sunny_fish.append(fish.id_fish)
    elif fish.catch_weather == "foggy":
        foggy_fish.append(fish.id_fish)
    elif fish.catch_weather == "snow":
        snow_fish.append(fish.id_fish)
    if fish.catch_time == "night":
        night_fish.append(fish.id_fish)
    elif fish.catch_time == "day":
        day_fish.append(fish.id_fish)
    if fish.slime == "freshwater":
        fresh_fish.append(fish.id_fish)
    elif fish.slime == "saltwater":
        salt_fish.append(fish.id_fish)
    elif fish.slime == "void":
        void_fish.append(fish.id_fish)
    elif fish.slime == "event": # FISHINGEVENT
        event_fish.append(fish.id_fish)
    for alias in fish.alias:
        fish_map[alias] = fish
