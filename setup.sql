CREATE TABLE users (
	id_user bigint NOT NULL,
	id_server bigint NOT NULL,
	slimes bigint NOT NULL DEFAULT '0',
	time_lastkill int NOT NULL DEFAULT '0',
	time_lastrevive int NOT NULL DEFAULT '0',
	id_killer bigint NOT NULL DEFAULT -1,
	time_lastspar int NOT NULL DEFAULT '0',
	time_lasthaunt int NOT NULL DEFAULT '0',
	slimecoin bigint NOT NULL DEFAULT '0',
	time_lastinvest int NOT NULL DEFAULT '0',
	slimelevel int NOT NULL DEFAULT '1',
	hunger int NOT NULL DEFAULT '0',
	weapon int NOT NULL DEFAULT '-1',
	trauma varchar(64) NOT NULL DEFAULT '',
	totaldamage bigint NOT NULL DEFAULT '0',
	weaponskill int NOT NULL DEFAULT '0',
	bounty bigint NOT NULL DEFAULT '0',
	inebriation int NOT NULL DEFAULT '0',
	faction varchar(32) NOT NULL default '',
	poi varchar(64) NOT NULL default 'classroom',
	life_state int NOT NULL DEFAULT '1',
	time_last_action bigint NOT NULL DEFAULT '0',
	weaponmarried int NOT NULL DEFAULT '0',
	time_lastscavenge int NOT NULL DEFAULT '0',
	bleed_storage bigint NOT NULL DEFAULT '0',
	time_lastenter int NOT NULL DEFAULT '0',
	time_lastoffline int NOT NULL DEFAULT '0',
	time_joined int NOT NULL DEFAULT '0',
	poi_death varchar(64) NOT NULL default '',
	arrested int NOT NULL DEFAULT '0',
	visiting varchar(64) NOT NULL default 'empty',
	time_expirpvp int NOT NULL DEFAULT '0',
	time_lastenlist int NOT NULL DEFAULT '0',
	active_slimeoid int NOT NULL DEFAULT '-1',
	has_soul int NOT NULL DEFAULT '1',
	manuscript int NOT NULL DEFAULT '-1',
	time_lastdeath int NOT NULL DEFAULT '0',
	sidearm int NOT NULL DEFAULT '-1',
	id_inhabit_target bigint NOT NULL DEFAULT -1,
	race varchar(32) NOT NULL DEFAULT '',
	time_racialability int NOT NULL DEFAULT '0',
	time_lastpremiumpurchase int NOT NULL DEFAULT '0',
	spray varchar(400) NOT NULL DEFAULT 'https://img.booru.org/rfck//images/3/a69d72cf29cb750882de93b4640a175a88cdfd70.png',
	time_lasthit int NOT NULL DEFAULT '0',
	rand_seed bigint NOT NULL DEFAULT '0',
	verified boolean NOT NULL DEFAULT '0',	
	gender varchar(16) NOT NULL DEFAULT 'boi',
    hogtied smallint NOT NULL DEFAULT '0',
    crime bigint NOT NULL DEFAULT '0',
	event_points bigint NOT NULL DEFAULT '0',
	fashion_seed bigint NOT NULL DEFAULT '0'

	CONSTRAINT id_user_server PRIMARY KEY (id_user, id_server)
);

CREATE TABLE stats (
	id_user bigint NOT NULL,
	id_server bigint NOT NULL,
	stat_metric varchar(64) NOT NULL,
	stat_value bigint,

	PRIMARY KEY (id_user, id_server, stat_metric)
);

CREATE TABLE markets (
	id_server bigint NOT NULL,
	time_lasttick int NOT NULL DEFAULT '0',
	slimes_revivefee bigint NOT NULL DEFAULT '0',
	negaslime bigint NOT NULL DEFAULT '0',
	clock int NOT NULL DEFAULT '0',
	weather varchar(32) NOT NULL DEFAULT 'sunny',
	day int NOT NULL DEFAULT '726',
	decayed_slimes bigint NOT NULL DEFAULT '0',
	donated_slimes bigint NOT NULL DEFAULT '0',
	donated_poudrins bigint NOT NULL DEFAULT '0',
	caught_fish int NOT NULL DEFAULT '0',
	splattered_slimes bigint NOT NULL DEFAULT '0',
	global_swear_jar bigint NOT NULL DEFAULT '0',
	horseman_deaths int NOT NULL DEFAULT '0',
	horseman_timeofdeath int NOT NULL DEFAULT '0',
	winner varchar(32) NOT NULL DEFAULT '',

	PRIMARY KEY (id_server)
);

CREATE TABLE companies (
	id_server bigint NOT NULL,
	stock varchar(64) NOT NULL,
	recent_profits bigint NOT NULL DEFAULT '0',
	total_profits bigint NOT NULL DEFAULT '0',

	PRIMARY KEY (id_server, stock)
);

CREATE TABLE stocks (
	id_server bigint NOT NULL,
	stock varchar(64) NOT NULL,
	market_rate bigint NOT NULL DEFAULT '1000',
	exchange_rate bigint NOT NULL DEFAULT '1000000',
	boombust int NOT NULL DEFAULT '0',
	total_shares bigint NOT NULL DEFAULT '0',
	timestamp bigint NOT NULL DEFAULT '0'
);

CREATE TABLE shares (
	id_server bigint NOT NULL,
	id_user bigint NOT NULL,
	stock varchar(64) NOT NULL,
	shares bigint NOT NULL DEFAULT '0',


	PRIMARY KEY (id_server, id_user, stock)
);

CREATE TABLE weaponskills (
	id_user bigint NOT NULL,
	id_server bigint NOT NULL,
	weapon varchar(64) NOT NULL,
	weaponskill int NOT NULL DEFAULT '0',

	PRIMARY KEY (id_user, id_server, weapon)
);

CREATE TABLE players (
	id_user bigint NOT NULL,
	id_server bigint NOT NULL,

	avatar varchar(1024) NOT NULL DEFAULT '',
	display_name varchar(256) NOT NULL DEFAULT '',

	PRIMARY KEY (id_user)
);

CREATE TABLE servers (
	id_server bigint NOT NULL,

	name varchar(256) NOT NULL DEFAULT '',
	icon varchar(1024) NOT NULL DEFAULT '',

	PRIMARY KEY (id_server)
);

CREATE TABLE items (
	id_item int NOT NULL AUTO_INCREMENT,
	id_server bigint NOT NULL,
	id_user varchar(128) NOT NULL,
	item_type varchar(64) NOT NULL,
	time_expir int,
	stack_max int NOT NULL DEFAULT '-1',
	stack_size int NOT NULL DEFAULT '1',
	soulbound int NOT NULL DEFAULT '0',
	template varchar(64) NOT NULL DEFAULT '-2',

	PRIMARY KEY (id_item)
) ENGINE = INNODB;

CREATE TABLE items_prop (
	id_item int NOT NULL,

	name varchar(64) NOT NULL,
	value varchar(2048),

	FOREIGN KEY (id_item)
		REFERENCES items(id_item)
		ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE farms (
	id_server bigint NOT NULL,
	id_user bigint NOT NULL,
	farm varchar(32) NOT NULL,
	time_lastsow int NOT NULL DEFAULT '0',
	phase int NOT NULL DEFAULT '0',
	time_lastphase int NOT NULL DEFAULT '0',
	slimes_onreap int NOT NULL DEFAULT '0',
	action_required int NOT NULL DEFAULT '0',
	crop varchar(32) NOT NULL DEFAULT '',
	sow_life_state int NOT NULL DEFAULT '0',

	PRIMARY KEY (id_server, id_user, farm)
);

CREATE TABLE slimeoids (
	id_slimeoid int NOT NULL AUTO_INCREMENT,
	id_server bigint NOT NULL,
	id_user varchar(128) NOT NULL,
	life_state int NOT NULL DEFAULT '0',
	body varchar(32) NOT NULL DEFAULT '',
	head varchar(32) NOT NULL DEFAULT '',
	legs varchar(32) NOT NULL DEFAULT '',
	armor varchar(32) NOT NULL DEFAULT '',
	weapon varchar(32) NOT NULL DEFAULT '',
	special varchar(32) NOT NULL DEFAULT '',
	ai varchar(32) NOT NULL DEFAULT '',
	type varchar(32) NOT NULL DEFAULT 'Lab',
	name varchar(32) NOT NULL DEFAULT '',
	atk int NOT NULL DEFAULT '0',
	defense int NOT NULL DEFAULT '0',
	intel int NOT NULL DEFAULT '0',
	level int NOT NULL DEFAULT '0',
	time_defeated int NOT NULL DEFAULT '0',
	clout int NOT NULL DEFAULT '0',
	hue varchar(32) NOT NULL DEFAULT '',
	coating varchar(32) NOT NULL DEFAULT '',
	poi varchar(64) NOT NULL DEFAULT '',
	dogtag varchar(1024) NOT NULL DEFAULT '',
	
	PRIMARY KEY (id_slimeoid)
);

CREATE TABLE enemies (
	id_enemy int NOT NULL AUTO_INCREMENT,
	id_server bigint NOT NULL,
	slimes bigint NOT NULL DEFAULT '0',
	totaldamage bigint NOT NULL DEFAULT '0',
	ai varchar(32) NOT NULL DEFAULT '',
	enemytype varchar(32) NOT NULL DEFAULT '',
	attacktype varchar(32) NOT NULL DEFAULT '',
	display_name varchar(256) NOT NULL DEFAULT '',
	identifier varchar(32) NOT NULL DEFAULT '',
	level int NOT NULL DEFAULT '0',
	poi varchar(64) NOT NULL DEFAULT '',
	life_state int NOT NULL DEFAULT '0',
	bleed_storage bigint NOT NULL DEFAULT '0',
	time_lastenter int NOT NULL DEFAULT '0',
	initialslimes bigint NOT NULL DEFAULT '0',
	expiration_date bigint NOT NULL DEFAULT '0',
	id_target bigint NOT NULL DEFAULT '-1',
	raidtimer bigint NOT NULL DEFAULT '0',
	rare_status int NOT NULL DEFAULT '0',
	hardened_sap int NOT NULL DEFAULT '0',
	weathertype varchar(32) NOT NULL DEFAULT '',
	faction varchar(32) NOT NULL DEFAULT '',
	enemyclass varchar(32) NOT NULL DEFAULT '',
	owner bigint NOT NULL DEFAULT '0',

	PRIMARY KEY (id_enemy)
) ENGINE = INNODB;

CREATE TABLE enemies_prop (
    id_enemy int NOT NULL,

	name varchar(64) NOT NULL,
	value varchar(2048),

    FOREIGN KEY (id_enemy) 
        REFERENCES enemies(id_enemy)
    	ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE districts (
	id_server bigint NOT NULL,
	district varchar(64) NOT NULL,
	controlling_faction varchar(32) NOT NULL DEFAULT '',
	capturing_faction varchar(32) NOT NULL DEFAULT '',
	capture_points bigint NOT NULL DEFAULT '0',
	slimes bigint NOT NULL DEFAULT '0',
	time_unlock int NOT NULL DEFAULT '0',
	cap_side varchar(32) NOT NULL DEFAULT '',

	PRIMARY KEY (id_server, district)
);

CREATE TABLE roles (
	id_server bigint NOT NULL,
	name varchar(128) NOT NULL,

	id_role bigint NOT NULL DEFAULT -1,

	PRIMARY KEY (id_server, name)
);

CREATE TABLE mutations (
	mutation_counter int NOT NULL AUTO_INCREMENT,
	id_server bigint NOT NULL,
	id_user bigint NOT NULL,
	mutation varchar(32) NOT NULL,
	data varchar(64) NOT NULL DEFAULT '',
    artificial smallint NOT NULL DEFAULT '0',
    tier int NOT NULL DEFAULT '0',

	PRIMARY KEY (mutation_counter)
);

CREATE TABLE quadrants (
	id_server bigint NOT NULL,
	id_user bigint NOT NULL,
	quadrant varchar(32) NOT NULL,

	id_target bigint NOT NULL DEFAULT -1,
	id_target2 bigint NOT NULL DEFAULT -1,

	PRIMARY KEY (id_server, id_user, quadrant)
);

CREATE TABLE transports (
	id_server bigint NOT NULL,
	poi varchar(64) NOT NULL,

	transport_type varchar(64) NOT NULL DEFAULT '',
	current_line varchar(64) NOT NULL DEFAULT '',
	current_stop varchar(64) NOT NULL DEFAULT '',

	PRIMARY KEY(id_server, poi)
);

CREATE TABLE status_effects (
	id_server bigint NOT NULL,
	id_user bigint NOT NULL,
	id_status varchar(64) NOT NULL,
	
	time_expir int NOT NULL DEFAULT '-1',
	value varchar(255) NOT NULL DEFAULT 0,
	source varchar(128) NOT NULL DEFAULT '',
	id_target bigint NOT NULL DEFAULT -1,

	PRIMARY KEY (id_server, id_user, id_status)
);

CREATE TABLE enemy_status_effects (
	id_server bigint NOT NULL,
	id_enemy varchar(128) NOT NULL,
	id_status varchar(64) NOT NULL,
	
	time_expir int NOT NULL DEFAULT '-1',
	value varchar(255) NOT NULL DEFAULT 0,
	source varchar(128) NOT NULL DEFAULT '',
	id_target bigint NOT NULL DEFAULT -1,

	PRIMARY KEY (id_server, id_enemy, id_status)
);

CREATE TABLE bans (
	id_server bigint NOT NULL,
	id_user bigint NOT NULL,
	faction varchar(32) NOT NULL DEFAULT '',

	PRIMARY KEY (id_server, id_user, faction)
);

CREATE TABLE bazaar_wares (
	id_server bigint NOT NULL,
	name varchar(64) NOT NULL,
	value varchar(128) NOT NULL,
	
	PRIMARY KEY (id_server, name)
);

CREATE TABLE offers (
	id_server bigint NOT NULL,
	id_user bigint NOT NULL,
	offer_give int NOT NULL,
	offer_receive varchar(32) NOT NULL DEFAULT '',
	time_sinceoffer int NOT NULL DEFAULT '0',

	PRIMARY KEY (id_server, id_user, offer_give)
);

CREATE TABLE vouchers (
	id_server bigint NOT NULL,
	id_user bigint NOT NULL,
	faction varchar(32) NOT NULL DEFAULT '',

	PRIMARY KEY (id_server, id_user, faction)
);
	

CREATE TABLE apartment (
	apt_name varchar(64) NOT NULL DEFAULT '',
	apt_description varchar(5000) NOT NULL DEFAULT '',
	poi varchar(64) NOT NULL DEFAULT 'downtown',
	rent BIGINT NOT NULL DEFAULT 0,
	id_user bigint NOT NULL DEFAULT -1,
	id_server bigint NOT NULL DEFAULT -1,
	apt_class char NOT NULL DEFAULT 'c',
	num_keys int NOT NULL DEFAULT 0,
	key_1 int NOT NULL DEFAULT 0,
	key_2 int NOT NULL DEFAULT 0,

	PRIMARY KEY (id_server, id_user)
);

CREATE TABLE global_locks (
	id_server bigint NOT NULL,
	district varchar(32) NOT NULL,
	locked_status varchar(32) NOT NULL DEFAULT '',

	PRIMARY KEY (id_server, district)
);

CREATE TABLE world_events (
	id_event int NOT NULL AUTO_INCREMENT,
	id_server bigint NOT NULL,
	event_type varchar(64) NOT NULL,
	time_activate int NOT NULL DEFAULT '-1',
	time_expir int NOT NULL DEFAULT '-1',

	PRIMARY KEY (id_event)
) ENGINE = INNODB;

CREATE TABLE world_events_prop (
	id_event int NOT NULL,

	name varchar(64) NOT NULL,
	value varchar(2048),

	FOREIGN KEY (id_event)
		REFERENCES world_events(id_event)
		ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE ads (
	id_ad int NOT NULL AUTO_INCREMENT,
	id_server bigint NOT NULL,
	id_sponsor varchar(128) NOT NULL DEFAULT '',
	content varchar(500) NOT NULL DEFAULT '',
	time_expir int NOT NULL DEFAULT '0',

	PRIMARY KEY (id_ad)
);

CREATE TABLE books (
    id_book int NOT NULL AUTO_INCREMENT,
	id_server bigint NOT NULL,
	id_user bigint NOT NULL,
	title varchar(64) NOT NULL DEFAULT '',
	author varchar(32) NOT NULL DEFAULT '',
	book_state int NOT NULL DEFAULT '0',
	date_published int NOT NULL DEFAULT '0',
	genre int NOT NULL DEFAULT '-1',
	length int NOT NULL DEFAULT '0',
	sales int NOT NULL DEFAULT '0',
	rating varchar(4) NOT NULL DEFAULT '0',
	rates int NOT NULL DEFAULT '0',
	pages int NOT NULL DEFAULT '10',

	PRIMARY KEY (id_book, id_server, id_user)
) ENGINE = INNODB;

CREATE TABLE book_pages (
    id_book int NOT NULL,

	page int NOT NULL,
	contents varchar(2048),

	FOREIGN KEY (id_book)
		REFERENCES books(id_book)
		ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE book_sales (
    id_book int NOT NULL,
    id_server bigint NOT NULL,
    id_user bigint NOT NULL,
    bought int NOT NULL DEFAULT '0',
    rating int NOT NULL DEFAULT '0',

    PRIMARY KEY (id_book, id_server, id_user)
);

CREATE TABLE swilldermuk_prank_index (
    id_server bigint NOT NULL,
    id_user_pranker bigint NOT NULL,
    id_user_pranked bigint NOT NULL,
    prank_count int NOT NULL DEFAULT '0',
    
    PRIMARY KEY (id_user_pranker, id_user_pranked)
);

CREATE TABLE inhabitations (
    id_ghost bigint NOT NULL,
    id_fleshling bigint NOT NULL,
    id_server bigint NOT NULL,
    empowered varchar(32) NOT NULL default '',

	PRIMARY KEY (id_ghost, id_fleshling, id_server)
);

CREATE TABLE gamestates (
    id_server bigint NOT NULL,
    id_state varchar(32) NOT NULL,
    state_bit smallint NOT NULL DEFAULT '0',
    value varchar(255) NOT NULL DEFAULT '',
    number bigint NOT NULL DEFAULT '0',

    PRIMARY KEY (id_server, id_state)
);

create table records(
    id_server BIGINT NOT NULL DEFAULT -1,
    record_type VARCHAR(100) NOT NULL,
    record_amount DECIMAL(9, 2) NOT NULL DEFAULT 0.0,
    id_user BIGINT NOT NULL DEFAULT -1,
    id_post VARCHAR(500) NOT NULL DEFAULT '',
    legality SMALLINT NOT NULL DEFAULT 0,

    PRIMARY KEY(id_server, record_type)
);

CREATE TABLE blurbs(
    id_blurb BIGINT NOT NULL AUTO_INCREMENT,
    id_server BIGINT NOT NULL DEFAULT -1,
    blurb VARCHAR(2000) NOT NULL DEFAULT '',
    context VARCHAR(50) NOT NULL DEFAULT '',
    subcontext VARCHAR(50) NOT NULL DEFAULT '',
    subsubcontext VARCHAR(50) NOT NULL DEFAULT '',
    dateadded BIGINT NOT NULL DEFAULT (CURRENT_DATE),

    PRIMARY KEY(id_blurb, id_server)
);

CREATE TABLE votes(
    id_user BIGINT NOT NULL DEFAULT -1,
    id_server BIGINT NOT NULL DEFAULT -1,
    poi VARCHAR(50) NOT NULL DEFAULT '',
    target VARCHAR(50) NOT NULL DEFAULT '',
    PRIMARY KEY(id_user, id_server)
);

CREATE TABLE goonscape_stats (

	id_user BIGINT NOT NULL,
	id_server BIGINT NOT NULL,

	mining_level TINYINT UNSIGNED NOT NULL DEFAULT 1,
	mining_xp INT UNSIGNED NOT NULL DEFAULT 0,

	fishing_level TINYINT UNSIGNED NOT NULL DEFAULT 1,
	fishing_xp INT UNSIGNED NOT NULL DEFAULT 0,

	farming_level TINYINT UNSIGNED NOT NULL DEFAULT 1,
	farming_xp INT UNSIGNED NOT NULL DEFAULT 0,

	feasting_level TINYINT UNSIGNED NOT NULL DEFAULT 1,
	feasting_xp INT UNSIGNED NOT NULL DEFAULT 0,

	halloween_level TINYINT UNSIGNED NOT NULL DEFAULT 1,
	halloween_xp INT UNSIGNED NOT NULL DEFAULT 0,

	dslimernalia_level TINYINT UNSIGNED NOT NULL DEFAULT 1,
	dslimernalia_xp INT UNSIGNED NOT NULL DEFAULT 0,

	clout_level TINYINT UNSIGNED NOT NULL DEFAULT 1,
	clout_xp INT UNSIGNED NOT NULL DEFAULT 0,

	piss_level TINYINT UNSIGNED NOT NULL DEFAULT 1,
	piss_xp INT UNSIGNED NOT NULL DEFAULT 0,

	PRIMARY KEY (id_user, id_server)

);

CREATE TABLE quest_records (

	time_stamp int NOT NULL,

	id_user BIGINT NOT NULL,
	id_server BIGINT NOT NULL,

	record_type varchar(16) NOT NULL,
	record_data varchar(64) NOT NULL,

	PRIMARY KEY (time_stamp, id_user, id_server, record_type)

);


CREATE TABLE mut_rotations (
    month int NOT NULL DEFAULT 4,
    year int NOT NULL DEFAULT 2023,
    id_server BIGINT NOT NULL DEFAULT -1,
    mutation varchar(128) NOT NULL DEFAULT '',
    context_num decimal(9, 2) NOT NULL DEFAULT 1,

    PRIMARY KEY (month, year, id_server, mutation)
);
