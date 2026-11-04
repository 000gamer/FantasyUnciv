"""English display names; IDs and all rule references remain language-independent."""
NAMES={}
def group(prefix, pairs):
 for row in pairs.strip().splitlines():
  num, name=row.split(' ',1);NAMES[prefix+num]=name

group('D01-T','''
01 Agriculture and Storage
02 Hunting and Husbandry
03 Mining
04 Rituals
05 Writing
06 Basic Crafts
07 Coastal Navigation
08 Smelting
09 Riding
10 Composite Bows
11 City-State Organization
13 Shipbuilding
14 Currency and Exchange
15 Steel Forging
16 Mechanical Engineering
17 Public Education
19 Ocean Navigation
20 Naval Armaments
21 Guilds
22 Military Formations
23 Mobile Warfare
24 Runic Crafts
25 Administration and Finance
26 Higher Learning
27 Covenants of Life
28 Mithril Metallurgy
29 Precision Manufacturing
30 Elemental Shaping
31 Harmony of Life
32 Deep-Sea Shipbuilding
33 War Coordination
35 Governance of Nations
36 Grand Crafts
37 Source Synergy
38 World Strategy
39 Irrigation
41 Oral Tradition
42 Herbalism
44 Laws of War
48 Saddlery
50 Codes of Law
53 Symbolic Arts
54 Repose and Memory
57 Cartography
58 Diplomatic Envoys
60 Garrison Systems
62 Theology
63 Literature
64 Mirror Arts
66 Citizenship
67 Star Charts
71 Structural Engineering
73 Soul Recognition
79 Soul Covenants
80 Ecological Accords
81 Trade Charters
83 Medicine
84 Cultural Exchange
85 Mutual Defense
86 Celestial Surveying
87 Universal History
89 Mithril Composites
90 Integrated City Governance
91 Elemental Boundaries
92 Charter of Shared Rule
93 Enduring Memory
94 Resonance of Heaven and Earth
95 Ocean Supremacy
96 Heritage of Nations
98 Attunement of Life
99 Elemental Guidance
101 Mental Coordination
102 Collaborative Research
103 Mental Resonance
''')
group('U','''
01 Militia
02 Shield Infantry
03 Regular Infantry
04 Formation Infantry
05 Heavy Infantry
06 Legion Guards
07 Spearmen
08 Pikemen
09 Halberdiers
10 Phalanx Guards
11 Massed Pike Guards
12 Archers
13 Composite Bowmen
14 Crossbowmen
16 Windlass Crossbowmen
17 Sharpshooters
19 Rangers
21 Windriders
22 Heavy Cavalry
24 Royal Cavalry
25 Catapults
26 Heavy Catapults
27 Heavy Ballistae
28 Great Siege Arbalest
29 Oared Galleys
30 Ocean Escorts
31 Deep-Sea Warships
32 Armored Warships
33 Naval Ballistae
35 Armored Ballista Ships
36 Evokers
38 Shaping Mages
40 Boundary Mages
41 Field Physicians
43 Life Physicians
45 Harmony Physicians
54 Construct Guards
55 Heavy Construct Guards
58 Trained Warbeasts
60 Armored Warbeasts
63 Scouts
64 Woodland Scouts
65 Expedition Scouts
66 Necromancers
70 Horse Archers
71 Windstring Horse Archers
72 Skyline Horse Archers
74 Soulbinders
75 Final Cantors
76 Ocean Supply Ship
77 Mirror Detection Team
78 Spirit Survey Team
''')
group('UX','''
01 Imperial Legion
02 Oathshield Guards
03 Contract Guards
04 Convoy Escort
05 Woodland Bowmen
06 Ancient Grove Guardians
07 Moonbranch Archers
08 Tidepattern Galley
09 Sail Ballista Ship
10 Pass Pikemen
11 Mountain Gate Guards
13 Precision Construct Guards
14 Wolf Riders
15 Steppe Horse Archers
16 Ancestral Banner Riders
17 Legion Assault Infantry
19 Ironback Warbeasts
20 Gear Ballista
21 War Golems
22 Ruin Surveyors
23 Mercenary Crossbowmen
24 Lich Apprentices
25 Spectral Knights
26 Court Liches
27 Bone Legion
28 Bone Halberdiers
29 Undead Guards
30 Elder Tree Guards
32 Nether Oath Rangers
''')
group('B','''
00 Palace
01 Granary
02 Workshop
03 Library
04 Monument
05 Altar
06 Foundry
07 Barracks
08 Walls
09 Beast Pens
10 Harbor
11 Market
12 School
13 Theater
14 Academy of Magic
15 Temple
16 Shipyard
17 Guildhall
19 Armory
21 Administration Hall
22 Bank
23 University
24 Life Research Hall
25 Advanced Forge
26 Precision Workshop
27 Sourceflow Institute
28 Infirmary
29 Ocean Drydock
30 Military Academy
31 Grand Library
32 Museum
33 Urban Granary
35 Great Factory
36 Source Observatory
41 Council Hall
44 Courthouse
45 Lighthouse
47 Garden
49 Survey Hall
51 Aqueduct
52 Mirror Tower
53 Civic Hall
54 Star Observatory
55 Supply Harbor
57 Fortress
59 Waterworks Factory
60 Soul Archive
61 Ecological Garden
62 Exchange
63 Expedition Camp
64 Defense Depot
66 Museum of Civilizations
67 Siege Assembly Plant
68 Public Square
69 Sanctuary of Memory
70 Dawnoath Chapel
71 Monastery of Life
72 Greenring Shrine
73 Hearth Sanctuary
74 Tideway Meeting Hall
75 Hall of Quiet Memory
76 Runeweaving Institute
77 Oathguard Hospice
78 Root Council
80 Sealing Node
''')
group('XB','''
01 Provincial Office
02 Legion Camp
03 Trading Hall
04 Maritime Bank
05 Canopy Sanctuary
06 Treespeech School
07 Tidal Harbor
08 Startide Drydock
09 Mountain Foundry
10 Rock Bastion
11 Inscription Workshop
12 Artificer University
13 Waterside Pasture
14 Clan Assembly
15 Service Hall
16 Conquest Court
17 Engineering Workshop
19 Surveyors Guild
20 Expedition Archive
21 Sleepless Library
22 Meditation Institute
23 Muster Monument Walls
24 Permanent Supply Depot
''')
group('W','''
01 Circle of the Ancestors
02 Terraces of Plenty
03 Lights of the Encircling Sea
04 Bronze Oath Memorial
05 Festival of Crafts
06 Mirror Lake Academy
07 League of a Hundred Ports
08 Ancient Grove Covenant
09 Throne of Military Oaths
10 Gallery of Star Charts
11 Dome of Deliberation
12 Great Rune Forge
13 Centennial Exposition
14 Vault of All Roads
15 Great Garden of Life
16 Hall of the Heavens
17 Covenant of Dragons
19 Council of the Gods
20 Atlas of the World
21 Resonance Calibration Array
''')
group('K','''
01 Capital Archive
02 Legion Banner
03 Ledger of All Markets
04 College of Arts
05 Source Study Society
06 Maritime and Land Governorate
07 Grand Civic Assembly
08 Comprehensive Geography
09 Heritage Council
10 Rootwatch
11 Sea Road Oathhall
12 Artificers Council
13 Starlight Research Ritualists
14 National Ward Ritualists
''')
group('J','''
01 Origin Observation Project
02 Great Chronicle of Civilizations
''')
group('S','''
01 Resonance Anchor
02 Stellar Matrix
03 Stabilization Core
04 Material Calibrator
''')
group('H','''
01 Oathsworn Commander
02 Star-Mirror Sage
03 Guardian of the Wilds
04 Ancient Oath Dragon
05 Springroad Physician
06 Monument Oathwalker
07 Molten Seal Envoy
08 Silent Mirror Keeper
09 Sea Road Navigator
10 Lantern Oathguard
11 Hundredforge Artificer
12 Caravan Arbiter
''')
group('N','''
01 Human Empire
02 Mercantile Republic
03 Forest Elves
04 Sea Elves
05 Mountain Dwarves
06 Artificer Dwarves
07 Nomadic Orcs
08 Orc Empire
09 Industrial Goblins
10 Explorers Guild
11 Lich Dynasty
12 Bone Empire
''')
group('R','''
01 Horses
02 Iron
03 Mana Crystals
04 Mithril
05 Wheat
06 Livestock
07 Fish
08 Stone
09 Deer
10 Silver
11 Gems
12 Silk
13 Spices
14 Incense
15 Pearls
16 Herbs
17 Amber
19 Grapes
20 Rock Salt
21 Wild Berries
22 Star Calendar Remains
23 Oathstone Remains
24 Rootcourt Remains
25 Research Ritual Active
26 National Ward Active
''')
group('M','''
01 Wild Wolf Pack
02 Outlaw Raiders
03 Bone Hunters
04 Stone-Eating Giant
05 Feral Tree Guards
06 Rogue Construct
07 Raging Elemental
08 Bay Serpent
09 Deep-Tide Serpent
10 Forsworn Specter
11 Echo Wraithlord
12 Wandering Spiritfire
13 Tidal Jellyfish Swarm
''')
group('NW','''
01 Crystalsleep Mountains
02 Dragonbone Plateau
03 Star-Mirror Lake
04 Evergreen Sacred Grove
05 Singing Tide Pillars
06 Ember Furnace Peak
07 Amber Sunken Forest
08 Mirror Salt Basin
09 Iceblue Springs
10 Thunderstone Plains
11 Giant Fern Rain Valley
12 Migrating Whale Bay
13 Silent Sand Sea
14 Skycleft Gorge
''')
group('CS','''
01 Inkbell
02 Sevenstrings
03 Ancient Scroll
04 Whitepage
05 Starbridge
06 Tidemarket
07 Twin Oars
08 Coral Bay
09 Wheatsail
10 Southlight
11 Amber Haven
12 Twin Scales Station
13 Salt Ring
14 Spice Road
15 Silver Market
16 Brokenbridge Fort
17 Redshield
19 Beaconstone
20 Blade Trial City
21 Spring Altar
22 Dusk Prayer
23 Green Candle
24 Court of Echoes
''')
group('PB','''
01 City-State Tradition
02 Hunting and Expansion
03 Legion Discipline
04 Path of Faith
05 Guilds and Sea Trade
06 Diplomacy of Nations
07 Scholarship and Runes
08 Citizens and Crafts
''')
group('PL','''
01 Public Granaries
02 Inscribed Law
03 City Guard
04 Hereditary Duties
05 Local Autonomy
06 Public Labor
07 Reclamation
08 Camp Exchange
09 Woodland Knowledge
10 Land Survey
11 Regular Training
12 Military Logistics
13 Siege Preparation
14 Drills
15 Hold the Line
16 Morning Prayer
17 Public Teachings
19 Congregations
20 Public Rites
21 Road Maintenance
22 Contract Procurement
23 Port Crafts
24 Commercial Studies
25 Exchange of Goods
26 Reciprocal Gifts
27 Resident Envoys
28 Academic Accords
29 Cultural Accords
30 Common Measures
31 Experimental Methods
32 University League
33 Spellcraft Curriculum
35 Academic Succession
36 Public Accounts
37 Craft Standards
38 Specialist Support
39 Civil Rights
40 Territorial Security
''')
group('RB','''
01 God of the Forest
02 God of Knowledge
03 Song of the Herds
04 God of the Sea
05 God of the Forge
06 Words on Stone Altars
07 Prayers Beneath the Trees
08 Rainforest Echoes
09 Desert Sanctuaries
10 Keepers of the Winter Flame
11 God of Order
12 God of Death
13 Manifest Earth
14 Family Blessings
15 God of Life
16 God of War
17 Neighborly Donations
19 Communal Ritual
20 Archived Canons
21 Tithe Ledgers
22 Fellowship of Practice
23 Songs from Abroad
24 Initiation Donations
25 Sacred Diplomacy
26 Public Oaths
27 Dawnoath Worship
28 Order of the Living Spring
29 Greenring Ministry
30 Hearth Worship
31 Tideway Congregation
32 Quiet Remembrance
33 Sharing Bread
35 Schools of Teaching
36 Choral Rites
37 Public Rest
38 Peaceful Cultivation
39 Festival Markets
40 Shelter of Life
41 Sourceflow Rituals
42 Inquiring Faithful
43 Clerical Military Training
44 Battlefield Care
45 Itinerant Preaching
47 Spiritual Revelation
48 Simple Vestments
49 Physicians Oath
50 Way of the Wise
51 Teaching by Lamplight
52 Preservation of the Ancestors
53 Exchange of Covenants
54 Shared Sanctuary
55 God of Rivers
56 God of Storms
57 God of the Hunt
58 God of Commerce
59 God of the Stars
60 God of Travel
61 God of the Earth
62 God of Peace
63 Watchful Witnesses
64 Care of Bound Spirits
''')
group('RU','''
01 Ancient Coins
02 Fragments of Old Songs
03 Lost Calculations
04 Exiled Farmers
05 Sketch of the Old Roads
06 Ritual Inscriptions
07 Traveling Workers
08 Ancestral Training
09 Ruin Medicine
10 Records of Repose
11 Frontline Clues
13 Spell Calibration Platform
14 Monument of Renewal
15 Refugee Guides
16 Old Road Coordinates
17 Sealed Heritage Chest
19 Blind Calendar Mirror
20 Sealed Root Garden
21 Chart of the Sunken Bell
22 Lost Courier Register
23 Unclaimed Sealed Casket
24 The Last Load on Springroad
25 Silent Mirror Watch
''')
group('E','''
01 The Stonemasons Sealed Accounts
03 The Lost Sailors of Southlight
06 Two Lakeshore Inscriptions
09 Irrigation Boundaries
13 The Sealed Inheritance
16 Watchers Beneath the Oathstone
17 The Blind Star Mirror
19 The Sunken Bell Chart
20 The Lost Courier Register
21 Expedition Records
22 A Window for Mutual Aid
23 Joint Boundary Calibration
24 The Sealed Relic Casket
25 The Last Load on Springroad
26 A Voluntary Soul Covenant
27 The Molten Seal Envoy
28 The Silent Mirror Watch
29 Public Hearing of Oaths
30 Caravan Protection Terms
31 Starlight Research
32 National Ward
''')
NAMES.update(dict(zip(['C%02d'%i for i in range(1,12)],['Settler','Worker','Work Boat','Missionary','Inquisitor','Great Prophet','Great Scholar','Great Artificer','Great Trade Envoy','Great Artist','Great Commander'])))
NAMES.update(dict(zip(['步兵','重步兵','长柄','射手','轻骑','重骑','骑射','攻城','海近战','海远程','术士','医护','构装','树人','战兽','侦察','死灵','幽魂','野兽','元素','英雄近战','英雄施法','英雄幽魂','英雄海军','英雄生物'],['Infantry','Heavy Infantry','Polearms','Archers','Light Cavalry','Heavy Cavalry','Horse Archers','Siege','Naval Melee','Naval Ranged','Elemental Mages','Physicians','Constructs','Treants','Warbeasts','Recon','Necromancers','Specters','Beasts','Elementals','Melee Heroes','Spellcasting Heroes','Spectral Heroes','Naval Heroes','Heroic Creatures'])))
# IDs for promotions are sparse; names are stable even when a design row is retired.
group('P','''
01 Open-Field Tactics I
02 Open-Field Tactics II
03 Rough-Terrain Tactics I
04 Rough-Terrain Tactics II
05 Armored Protection
06 Flexible Deployment
07 Sighting I
08 Sighting II
09 Skirmisher Protection
10 Breaching I
11 Breaching II
12 Protect the Engines
13 Crew Drills I
14 Crew Drills II
15 Ocean Sail Handling
16 Breath of Life
17 Mental Ward
20 Far Sight
21 Pathfinder
22 Field Repairs
23 Unbinding
25 Mind Mirror
26 Returning Tide
27 Spirit Binding
29 Mounted Raid
30 Starlight Watch
31 Amphibious Transport
33 Mirror-Eye Training
36 Ocean Supply
37 Crystal Ward Covenant
38 Springwood Covenant
39 Tidal Navigation
40 Witness of the Ancestors
41 Command
42 Oath of the Bridge
43 Insight
44 Starlight Extension
45 Oath of the Magehunter
47 Seal Detection
48 Memories of the Soul
50 Military Oath Seal: Broken
51 Military Oath Seal: Reforged
52 Military Oath Seal: Alliance
53 Calendar Mirror: Broken
54 Calendar Mirror: Restored
55 Calendar Mirror: Afterimage
56 Rootbranch Charm: Broken
57 Rootbranch Charm: Renewed
58 Rootbranch Charm: Farwatch
59 Dragonspine Stone: Dormant
60 Dragonspine Stone: Echoing
61 Dragonspine Stone: Far Oath
62 Unbroken Thought
63 Oath of the Traveler
64 Calendar Mirror: Steadfast
65 Military Oath Seal: Discipline
66 Rootbranch Charm: Grovekeeper
67 Dragonspine Stone: Nestguard
68 Healing Relay
69 Returning Soul Covenant
70 Archaeological Survey
71 Visitor Covenant Seal
72 Spring Ring: First Seal
73 Spring Ring: Restored
74 Spring Ring: Many Springs
75 Spring Ring: Urgent Care
76 Name Tag: First Seal
77 Name Tag: Restored
78 Name Tag: Archive
79 Name Tag: Unbound
80 Molten Rule: First Seal
81 Molten Rule: Restored
82 Molten Rule: Breaker
83 Molten Rule: Solid Phase
84 Still Mirror Needle: First Seal
85 Still Mirror Needle: Restored
86 Still Mirror Needle: Displacement
87 Still Mirror Needle: Resolve
88 Tideway Needle: First Seal
89 Tideway Needle: Restored
90 Tideway Needle: Escort
91 Tideway Needle: Racing Tide
92 Lantern Seal: First Seal
93 Lantern Seal: Restored
94 Lantern Seal: Reveal Specters
95 Lantern Seal: Aid All
96 Hundredforge Ruler: First Seal
97 Hundredforge Ruler: Restored
98 Hundredforge Ruler: Field Repair
99 Hundredforge Ruler: Resonance
100 Twin Scales Badge: First Seal
101 Twin Scales Badge: Restored
102 Twin Scales Badge: Reimbursement
103 Twin Scales Badge: Roadguard
104 Crystal Ward
''')
for k,vals in zip(['N%02d'%i for i in range(1,13)],[
['Ilena the Balanced Crown','Written Order','Balance Crown|Rivergate|Whitefield|Dawnwall|Harvestbridge|Northbeacon|Long Canal|Sun Court'],
['Speaker Vess Goldpact','Contract Government','Goldpact Harbor|Twin Scales|Silver Bay|Council City|Four Bridges|Far Sail|Copper Spring|Freeport'],
['Elanshi Greenbranch','Woodland Symbiosis','Greenbranch|Moonroot|Deerbrook|Longsong Grove|Mistleaf|Forest Court|Greenring|Starbud'],
['Seriel Tidesong','Tidal Routes','Tidesong|Pearl Bay|Whitesail|Returning Tide|Cape Light|Azure Harbor|Saltwind|Starreef'],
['Brand Rockoath','Mountain Hearths','Rockoath|Redforge|Stonegate|Deepvale|Copper Ridge|Snow Bastion|Broken Ridge|Iron Spring'],
['Helga Silverrule','Runic Artifice','Silverrule|Inscription City|Thousand Gears|Assay Terrace|Runebridge|Fineforge|Balance Hammer|Crystal Rule'],
['Aruk Windchaser','Steppe Clans','Windchaser|Three Springs|Wolffang Camp|Fargrass|Riverbend|Goldsaddle|Ancestral Banner|Longsky'],
['Talga Redbanner','Legion Law','Redbanner|Military Law City|Gatebreaker Fort|Colony Plain|Coppertusk|Great Camp|Stonehorn|Common Oath'],
['Chief Artificer Grik','Precision Mobilization','Assembly City|Gearport|Sparkwell|Test Grounds|Screwthread|Rivetbridge|Copper Smoke|Wheel City'],
['Guildmaster Mia Farroad','Survey Contracts','Farroad|New Chart|Old Monument Station|Faraway Haven|Boundary Marker|Lantern Register|Openbook|Worldsend'],
['Sevian Duskstar','Sleepless Scholarship','Duskstar|Sleepless Tower|Quiet Reading|Silverbone Court|Mirror Abyss|Soulpact|Longnight Academy|Memory River'],
['Oser the Standard Bearer','Enduring Muster','Eternal Banner|Muster City|Whitebone Pass|Monument Plain|Quiet Bastion|Hundred Oaths|Watchfort|Echo City'],
]):
 NAMES[k+' Leader']=vals[0];NAMES[k+' Ability']=vals[1]
 for i,n in enumerate(vals[2].split('|')):NAMES[k+f' City {i+1}']=n
for k in list(NAMES):
 if k.startswith('PB'):NAMES[k+' Complete']=NAMES[k]+' Complete'
for k,v in {'I25':'Archaeological Camp','I26':'Sealing Circle','I27':'Memorial Sanctuary','I28':'Spiritroot Reserve'}.items():NAMES[k]=v
# Localized choice names; all costs/results are also shown using native translated Unique descriptions.
CHOICES={
'E01':['Fund a second survey','Publish the accident records','Defer action'],
'E03':['Organize naval training','Publish the charts','Defer action'],
'E06':['Standardize the calculations','Preserve alternative accounts','Maintain both records'],
'E09':['Coordinate irrigation','Survey the boundaries first','Defer action'],
'E13':['Take the supplies','Recruit the workers'],
'E16':['Build a public memorial','Listen to the echoes','Archive the names'],
'E17':['Calibrate the spellwork','Study the scale markings','Recover the lenses'],
'E18':['Study the old tree covenant','Renew the care agreement','Record the shared covenant'],
'E19':['Train amphibious transport','Compile the sea charts','Recover the equipment'],
'E20':['Search for old sites','Repair and resupply','Publish the history'],
'E21':['Reinforce the survey team','Fund expedition supplies','Open the records'],
'E22':['Organize mutual funding','Publish the translations','Defer action'],
'E23':['Pay for joint calibration','Support city recovery','Publish the observations'],
'E24':['Study the relic','Publish the records','Repair on site'],
'E25':['Invite the physician','Use the medical supplies','Publish the rescue routes'],
'E26':['Fund resettlement and renew the covenant','Publish the voluntary testimony'],
'E27':['Hire the Molten Seal Envoy','Publish the calibration records'],
'E28':['Sponsor the Mirror Keeper','Preserve the public markers'],
'E29':['Support the Lantern Oathguard','Hold a public hearing'],
'E30':['Appoint the Caravan Arbiter','Publish the escort terms']}
for k,arr in CHOICES.items():
 for i,v in enumerate(arr):NAMES[k+'-'+chr(65+i)]=v
NAMES.update({
'AOD Scientific Objective':'Build the Origin Observation Project and assemble all six parts in your capital.',
'AOD Cultural Objective':'Complete five policy branches and build the Great Chronicle of Civilizations.',
'AOD Domination Objective':'Control the original capitals of all major civilizations.',
'AOD Diplomatic Objective':'After any nation builds the Assembly of Nations, win the diplomatic vote.',
'AOD Time Objective':'Have the highest score when the turn limit is reached.'})

NAMES.update({'B81':'Soul Covenant Archive','B82':'Mental Colloquium','I29':'Trade Post'})

# Opening/economy revision 0.4.0.
NAMES.update({'D01-T110':'Mathematics and Measurement','B83':'Arcane Lodge','B84':'School of Numbers',
'R27':'Copper','R28':'Clay','R29':'Sheep','R30':'Honey','R31':'Dyes','R32':'Spirit Spring','R33':'Whales','R34':'Dragonbone Beds',
'I30':'Ley Extractor','I31':'Spring Garden','I32':'Kiln','I33':'Apiary','I34':'Bone Excavation','I35':'Terrace Farm','I36':'Practice Circle','I37':'Waterwheel Yard'})

NAMES['D01-T111']='Natural Philosophy'

NAMES.update({'D01-T41':'Oral Tradition','D01-T17':'Education','D01-T87':'History and Classical Studies'})

NAMES.update({"D01-T112":"Spiritual Symbiosis","D01-T113":"Spirit Communion","D01-T114":"Rune Weaving"})

NAMES.update({'U18': 'Light Cavalry', 'U34': 'Heavy Ballista Ships', 'UX18': 'Gatebreaker Catapult', 'XB18': 'Final Assembly Plant', 'W18': 'Assembly of Nations', 'R18': 'Night Jade', 'CS18': 'Halberd Pass', 'PL18': 'Revelation', 'PL34': 'Community of Inquiry', 'RB18': 'Offerings of Learning', 'RB34': 'Ritual of Crafts', 'RB46': 'Traveling Order', 'RU18': 'Watchers Beneath the Oathstone', 'E18': 'The Old Root Covenant', 'P18': 'Elemental Penetration', 'P34': 'Marching Prayer', 'P46': 'Dragon Breath'})

NAMES.update({'野兽':'Beast','D01-T07':'Coastal Navigation','R21':'Berries','P70':'Far Sight'})

for retired in ['R22','R23','R24','R34','I25','I26','I27','I34','树人','战兽']:
 NAMES.pop(retired,None)

NAMES.update({'E13-A': 'A Take the old coins', 'E13-B': 'B Recruit workers', 'E16-A': 'A Fund the watcher', 'E16-B': 'B Listen to the echoes', 'E16-C': 'C Take a copy of the names', 'E17-A': 'A Let a caster try it', 'E17-B': 'B Study the notes', 'E17-C': 'C Sell the fragments', 'E18-A': 'A Examine the roots', 'E18-B': 'B Care for the roots', 'E18-C': 'C Copy the inscriptions', 'E19-A': 'A Test the crossing', 'E19-B': 'B Copy the chart', 'E19-C': 'C Sell the equipment', 'E20-A': 'A Find the marked ruins', 'E20-B': 'B Resupply along the markers', 'E20-C': 'C Preserve the register', 'E24-A': 'A Study the equipment', 'E24-B': 'B Copy the records', 'E24-C': 'C Use the medicine', 'E25-A': 'A Invite the physician', 'E25-B': 'B Use the medicine', 'E25-C': 'C Record the shelters', 'E26-A': 'A Invite the Oathstone Walker', 'E26-B': 'B Preserve the names', 'E27-A': 'A Invite the Molten Sigil Envoy', 'E27-B': 'B Copy the forge notes', 'E28-A': 'A Repair the frame and invite its keeper', 'E28-B': 'B Preserve the measurements', 'E29-A': 'A Invite the Lantern Oathguard', 'E29-B': 'B Record the healing methods', 'E30-A': 'A Invite him to join', 'E30-B': 'B Copy the road map', 'RU26': 'Watcher at the Broken Stone', 'RU27': 'Visitor at the Old Forge', 'RU28': 'Lanterns in the Grove', 'RU29': 'Guards by the Old Road', 'E29': 'Lanterns in the Grove', 'E30': 'Guards by the Old Road'})
for k in list(NAMES):
 if any(k==e or k.startswith(e+'-')for e in ['E01','E03','E06','E09','E21','E22','E23']):NAMES.pop(k,None)

for _key in ["RU07", "E13", "E13-A", "E13-B"]: NAMES.pop(_key, None)

NAMES['P109']='Medical resolution marker'

# Policy identities approved in revision 0.11.0.
NAMES.update({'PB01': 'Civic Tradition', 'PB02': 'Frontier and Autonomy', 'PB03': 'Legions and Expeditions', 'PB04': 'Temples and Oaths', 'PB05': 'Guilds and Sea Routes', 'PB06': 'Diplomacy of Nations', 'PB07': 'Academies and Runes', 'PB08': 'Citizens and Crafts', 'PL02': 'Public Learning', 'PL04': 'City Charters', 'PL05': 'Court Construction', 'PL06': 'Organized Labor', 'PL08': 'Rural Exchange', 'PL10': 'Frontier Connections', 'PL15': 'Homeland Defense', 'PL18': 'Missionary Learning', 'PL23': 'Trade Workshops'})

NAMES.update({'PL29':'Joint Instructors','PL32':'Academic Alliance','PL34':'Research Community','PL36':'Public Works','PL40':'Municipal Coordination'})

NAMES.update({"P45":"Dragonspine Oathstone: Monster Hunter","P63":"Dragonspine Oathstone: Sky Patrol"})

NAMES.update({'P110':'Command','P111':'Oath of the Bridge'})
