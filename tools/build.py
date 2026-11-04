#!/usr/bin/env python3
"""Build the native Unciv 4.22.16 ruleset from the checked-in wiki snapshot.
No third-party Python dependencies. Run from any directory.
"""
import json, re, copy, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'design/设计数据.json').read_text())
MAGIC=json.loads((ROOT/'design/魔法原生配置.json').read_text())
REEF=json.loads((ROOT/'design/造礁拓殖.json').read_text())
BASE=ROOT/'design/base-4.22.16'
OUT=ROOT/'jsons'
ZH={}; EN={}
PRESENTATION=json.loads((ROOT/'design/玩家体验文本.json').read_text())
def read(n): return json.loads((BASE/(n+'.json')).read_text())
from display_numbers import normalize_tree
DISPLAY=json.loads((ROOT/'design/数值显示规则.json').read_text())
def save(n,d): (OUT/(n+'.json')).write_text(json.dumps(normalize_tree(d,DISPLAY),ensure_ascii=False,indent=2)+'\n')
def label(k,z,e=None):
 ZH[k]=z
 if e: EN[k]=e
 return k
def ids(s,p=r'D01-T\d+'):return re.findall(p,s)
def optional(o,k,v):
 if v not in ('无','开局','—',''):o[k]=v
stats={'粮食':'Food','生产':'Production','金币':'Gold','科研':'Science','文化':'Culture','信仰':'Faith','本地幸福':'Happiness','全局幸福':'Happiness','幸福':'Happiness'}
def statstring(s):return ', '.join(f'{a} {stats[b]}' for a,b in re.findall(r'([+-]?\d+)(粮食|生产|金币|科研|文化|信仰|本地幸福|全局幸福|幸福)',s))
def fixed(s):return {stats[b].lower():int(a) for a,b in re.findall(r'([+-]\d+)(粮食|生产|金币|科研|文化|信仰|本地幸福|全局幸福|幸福)',s)}
def st(n,s,city='in this city'):return f'[{n:+d} {s}] [{city}]'
def pct(n,s,city='in this city'):return f'[{n:+d}]% [{s}] [{city}]'
def tiles(n,s,f,city='in this city'):return f'[{n:+d} {s}] from [{f}] tiles [{city}]'
def prod(n,f,city='in this city'):return f'[{n:+d}]% Production when constructing [{f}] units [{city}]'
def xp(n,f,city='in this city'):return f'New [{f}] units start with [{n}] XP [{city}]'
def train(f,p,city='in this city'):return f'All newly-trained [{f}] units [{city}] receive the [{p}] promotion <Civilopedia link [Promotion/{p}]>'
def strength(n,*conds):return f'[{n:+d}]% Strength'+''.join(f' <{c}>' for c in conds)
def vs(n,types,*conds):return [strength(n,*conds,f'vs [{t}] units') for t in types.split('/')]
def own(f):return f'for [{f}] units'
LAND='{Land} {Military}'; WATER='{Water} {Military}'
TYPES=sorted({r[3] for r in DATA['units'].values()}|{r[5] for r in DATA['unique_units'].values()}|{r[3] for r in DATA['heroes'].values()}|{r[3] for r in DATA['monsters'].values()}|set(DATA['hero_roles'].values()))
for t in TYPES:label(t,t)
for h,c in DATA['hero_promotion_rules'].items():label(c['type'],'英雄·'+DATA['heroes'][h][1])
unit_types=[{'name':t,'movementType':'Water' if t in ['海近战','海远程','英雄海军','Hero-09'] else 'Land'} for t in TYPES]+[{'name':'Civilian','movementType':'Land'},{'name':'Civilian Water','movementType':'Water'}]
for c in DATA['hero_promotion_rules'].values():
 next(t for t in unit_types if t['name']==c['type'])['civilopediaText']=[{'text':'FC Heroes','link':'Tutorial/FC Heroes'}]
# Register the conditional filter key without adding a visible unit/promotion.
unit_types.append({'name':REEF['rules']['near_city_tag'],'movementType':'Land'})
save('UnitTypes',unit_types)
# Base algorithms and data copied only from the pinned release.
remap={'Settler':'C01','Worker':'C02','Scout':'U63','Warrior':'U01','Pottery':'D01-T06','Animal Husbandry':'D01-T02','Mining':'D01-T03','The Wheel':'D01-T06'}
def replace_tree(v,m):
 if isinstance(v,dict):return {k:(x if k=='name' else replace_tree(x,m)) for k,x in v.items()}
 if isinstance(v,list):return [replace_tree(x,m) for x in v]
 if isinstance(v,str):
  if v in m:return m[v]
  for a,b in m.items():v=v.replace('['+a+']','['+b+']')
 return v
for f in ['Speeds','Personalities']:save(f,read(f))
save('Difficulties',replace_tree(read('Difficulties'),remap))
g=replace_tree(read('GlobalUniques'),remap);g['uniques'].append('[-35]% Culture cost of adopting new Policies');_med=DATA['unit_support_rules']['medic_end_turn'];g.setdefault('unitUniques',[]).append('Triggers a [E33] event <upon ending a turn in a [Land] tile> <when below [100] HP> <when adjacent to a [{医护} {non-[Embarked]}] unit> <hidden from users>');save('GlobalUniques',g)
save('ModOptions',{'isBaseRuleset':True,'tileset':'FantasyHex','unitset':'FantasyHex','author':'FantasyUnciv','uniques':[]})
era_names=['I','II','III','IV','V','VI']
eras=[]
for i,n in enumerate(era_names):
 label(n,['奠基','拓疆','交汇','专精','精炼','竞世'][i],['Foundations','Expansion','Confluence','Specialization','Refinement','World Age'][i])
 eras.append(dict(name=n,researchAgreementCost=[150,150,250,250,300,350][i],startingSettlerCount=1,startingWorkerCount=DATA['era_start_rules'][n]['workers'],startingMilitaryUnitCount=1,startingMilitaryUnit=DATA['era_start_rules'][n]['military'],settlerPopulation=DATA['era_start_rules'][n]['population'],startingGold=DATA['era_start_rules'][n]['gold'],startingCulture=0,baseUnitBuyCost=[200,200,300,400,500,600][i],embarkDefense=[3,5,8,12,18,24][i],startPercent=[0,12,28,45,65,82][i],iconRGB=read('Eras')[i]['iconRGB'],uniques=['Every major Civilization gains a spy once a civilization enters this era'] if i>=2 else []))
save('Eras',eras)
techs={};columns={}
for k,r in DATA['techs'].items():
 label(k,r[1]);col,row=map(int,r[7].split('/'));e=era_names[DATA['eras'][k]-1]
 t=dict(name=k,cost=int(r[3]),row=row,prerequisites=ids(r[4]),uniques=[]);techs[k]=t
 columns.setdefault(col,dict(columnNumber=col,era=e,techCost=int(r[3]),buildingCost=1,wonderCost=1,techs=[]))['techs'].append(t)
tech_add={'05':['Enables establishment of embassies'],'41':['[+1 Culture] from all [B04] buildings'],'81':[],'01':[],'11':['Enables Open Borders agreements'],'13':['Enables embarkation for land units'],'14':['Enables conversion of city production to [Gold]'],'19':['Enables [All] units to enter ocean tiles'],'26':['Enables conversion of city production to [Science]'],'58':['Enables Research agreements'],'71':['Roads connect tiles across rivers'],'85':['Enables Defensive Pacts'],'84':['When declaring friendship, both parties gain a [10]% boost to great person generation'],'36':[],'62':['[+1 Science] from all [B05] buildings'],'73':['[+1 Culture] from all [B03] buildings'],'79':[],'96':[pct(10,'Culture','in all cities')],'102':['Production to [Science] conversion in cities changed by [60]% <if [B52] is constructed> <with [R18]>'],'103':['[侦察] units gain the [P47] promotion',train('侦察','P47','in all cities'),xp(10,'侦察','in all cities')]}
for n,u in tech_add.items():techs['D01-T'+n]['uniques']+=u
save('Techs',[columns[k] for k in sorted(columns)])
# Base terrain keys remain native for map generation and road logic.
terrain_map={'Optics':'D01-T13','Astronomy':'D01-T19','Civil Service':'D01-T39','Fertilizer':'D01-T83','Scientific Theory':'D01-T86','Atomic Theory':'D01-T94','The Wheel':'D01-T11','Engineering':'D01-T71'}
terrains=replace_tree([t for t in read('Terrains') if t['type']!='NaturalWonder'],terrain_map)
# Remove old resource-specific regional guarantees; keep native fertility and movement.
old_res={r['name'] for r in read('TileResources')}
for t in terrains:t['uniques']=[u for u in t.get('uniques',[]) if not any('['+x+']' in u for x in old_res)]
for t in terrains:
 if t['name']=='Forest':t['uniques']=[u for u in t.get('uniques',[]) if 'when cut down' not in u]+['Provides a one-time bonus of [+20 Production] to the closest city when cut down']
terrains.append(copy.deepcopy(REEF['terrain']));label('Reef Island','岛礁','Reef Island')
# Units use IDs; improvements whose names drive engine behavior retain native keys.
IMP={k:r[2] for k,r in DATA['improvements'].items()}
RES={r[1]:k for k,r in DATA['resources'].items()}
def consume(o,s):
 for z,a in re.findall(r'([^、，\s]+?)(\d+)(?:、|$)',s):o.setdefault('uniques',[]).append(f'Consumes [{a}] [{RES[z]}]')
def keyword(t,ranged,ability):
 u=[]
 if ranged:u+=['No defensive terrain bonus']
 if t in ['轻骑','重骑','骑射']:u+=['No defensive terrain bonus','Can move after attacking']
 if t=='长柄':u+=vs(35,'轻骑/重骑/骑射/野兽')
 if t=='攻城':u+=['Must set up to ranged attack',strength(100,'when attacking','vs cities')]
 if t in ['海近战','英雄海军']:u+=['No defensive terrain bonus']
 if t in ['海近战','海远程','英雄海军']:u+=['Cannot enter ocean tiles <before discovering [D01-T19]>']
 if t=='术士':u+=vs(20,'重步兵/重骑/构装')+vs(25,'UX06/UX30/M05')+[strength(-35,'when attacking','vs cities')]
 if t=='医护':u+=['Comment [Field medicine]','FC medic near active patient <when adjacent to a [P109] unit> <hidden from users>']
 if t=='构装':u+=['No defensive terrain bonus',strength(10,'when defending')]
 if t=='野兽' and '战兽' in ability:u+=['No defensive terrain bonus',strength(-35,'when attacking','vs cities')]
 if t=='侦察':u+=['Ignores terrain cost','[1] Sight']
 if t=='幽魂':u+=['Ignores terrain cost','Invisible to non-adjacent units','No defensive terrain bonus',strength(-35,'when attacking','vs cities'),'[5] HP when healing']
 if '灵魂汲取' in ability:u+=['Heals [10] damage if it kills a unit']
 # Additional abilities belong to the object once, never re-expand the type keywords.
 if '视野+1' in ability and t!='侦察':u+=['[1] Sight']
 if '森林移动消耗减半' in ability:u+=['Double movement in [Forest]']
 if '森林交战战力+20%' in ability or '在森林交战战力+20%' in ability:
  u+=[strength(20,'when fighting in [Forest] tiles')]
 if '抗射' in ability or '防御远程单位攻击战力+15%' in ability:u+=vs(15,'Ranged','when defending')
 if '在友好领土防御' in ability:u+=[strength(15,'when defending','in [Friendly Land] tiles')]
 elif '防御时战力+15%' in ability:u+=[strength(15,'when defending')]
 if '对城市攻击战力+15%' in ability:u+=[strength(15,'when attacking','vs cities')]
 if '攻击城市战力-35%' in ability and t not in ['术士','野兽','幽魂']:u+=[strength(-35,'when attacking','vs cities')]
 if '自身正常休整额外恢复5HP' in ability:u+=['[5] HP when healing']
 if '不能主动攻击' in ability:u+=['Cannot attack']
 if '医疗' in ability and t!='医护':u+=['All adjacent units heal [5] HP when healing']
 if '侧翼协同' in ability:u+=['[50]% to Flank Attack bonuses']
 if '对构装单位战力+25%' in ability:u+=vs(25,'构装')
 if '能看见视野内幽魂类' in ability:u+=['Can see invisible [幽魂] units','Can see invisible [英雄幽魂] units']
 return list(dict.fromkeys(u))
units=[]
for group in ['units','unique_units']:
 for k,r in DATA[group].items():
  if group=='units':_,name,tech,t,melee,ran,rng,mov,cost,res,upgrade,ability,maintenance,obsolete=r
  else:_,nation,name,replaces,tech,t,melee,ran,rng,mov,cost,res,upgrade,ability,maintenance,obsolete=r
  label(k,name);o=dict(name=k,unitType=t,strength=int(melee),rangedStrength=int(ran),range=int(rng),movement=int(mov),cost=int(cost),uniques=keyword(t,int(ran),ability)+['Never appears as a Barbarian unit'])
  for field,val in [('requiredTech',tech),('upgradesTo',upgrade),('obsoleteTech',obsolete)]:optional(o,field,val)
  if group=='unique_units':
   o['uniqueTo']=nation;optional(o,'replaces',replaces)
  consume(o,res)
  if int(maintenance):o['uniques']+=[f'[{maintenance}]% maintenance costs']
  if k=='UX23':o['hurryCostModifier']=-20
  units.append(o)
for k,actions in MAGIC['actions_by_unit'].items():next(u for u in units if u['name']==k)['uniques']+=actions
for o in MAGIC['unit_definitions']:
 if o['name'] not in [u['name'] for u in units]:units.append(copy.deepcopy(o))
 else:
  existing=next(u for u in units if u['name']==o['name']);existing.clear();existing.update(copy.deepcopy(o))
# Nonmilitary native action carriers.
base_units={x['name']:x for x in read('Units')}
civ_base={'C01':'Settler','C02':'Worker','C03':'Work Boats','C04':'Missionary','C05':'Inquisitor','C06':'Great Prophet','C07':'Great Scientist','C08':'Great Engineer','C09':'Great Merchant','C10':'Great Artist','C11':'Great General'}
for k,b in civ_base.items():
 r=DATA['civilians'][k];label(k,r[1].split('（')[0]);o=copy.deepcopy(base_units[b]);o['name']=k;o.pop('requiredTech',None);o.pop('obsoleteTech',None);o.pop('upgradesTo',None);o['unitType']='Civilian Water' if k=='C03' else 'Civilian';o.pop('replaces',None)
 o['uniques']=[u for u in o.get('uniques',[]) if not any(s in u for s in ['gets a name from','May buy','Can hurry','Can speed up','Can undertake','Specialist','Great Person -','[Industrial era]'])]
 o['uniques']=replace_tree(o['uniques'],{'Optics':'D01-T13','Astronomy':'D01-T19','Theology':'D01-T62'})
 if k in ['C01','C02','C03']:
  o['cost']=int(r[4]);o['movement']=int(r[5].split('/')[-1]);optional(o,'requiredTech',r[2])
 if k=='C01':o['uniques']=['Founds a new city <by consuming this unit>','Requires at least [2] population','Excess Food converted to Production when under construction','Unbuildable <for [City-States] Civilizations>']
 if k=='C02':
  worker_targets=[v[2] for ik,v in DATA['improvements'].items() if ik not in ['I06','I15','I16','I17','I18','I19','I20','I21','I22']]
  worker_filter='non-['+' '.join('{non-['+v+']}' for v in worker_targets)+']'
  o['uniques']=[f'Can build [{worker_filter}] improvements on tiles <hidden from users>','Can build [Repair] improvements on tiles <hidden from users>','Comment [Build tile improvements]']
  label('Build tile improvements','修建地块改良','Build tile improvements')
 if k=='C03':o['uniques']=['May create improvements on water resources','Uncapturable','Cannot enter ocean tiles <before discovering [D01-T19]>']
 if k in ['C04','C05']:
  o['requiredTech']='D01-T62';o['uniques']=[u for u in o['uniques'] if 'Can be purchased' not in u]+[f'Can be purchased for [200] [Faith] [in all cities in which the majority religion is a {"major" if k=="C04" else "enhanced"} religion]']
 if k in ['C07','C08','C09','C10','C11']:
  o['uniques']=['Unbuildable','Uncapturable','Great Person - ['+b+']','Never appears as a Barbarian unit',f'Can instantly construct a [{["Academy","Manufactory","Customs house","Landmark","Citadel"][int(k[1:])-7]}] improvement <by consuming this unit>']
  if k!='C11':o['uniques']+=['Is part of Great Person group [Economic]']
  if k=='C10':o['uniques']+=['Empire enters a [8]-turn Golden Age <by consuming this unit>']
  if k=='C11':o['uniques']+=['Is part of Great Person group [General]','Can be earned through combat <for [Land] units>','[15]% Strength bonus for [{Land} {Military}] units within [2] tiles','Cannot be purchased']
 units.append(o)
for o in units:
 o['uniques']=list(dict.fromkeys(o['uniques']))
# Specialists point to the new economic units.
specialists=[]
for n,s,v,c,u in [('Scientist','science',3,[0,0,255],'C07'),('Merchant','gold',2,[255,215,0],'C09'),('Engineer','production',2,[255,120,0],'C08'),('Artist','culture',3,[160,32,240],'C10')]:specialists.append(dict(name=n,**{s:v},color=c,greatPersonPoints={u:3}))
save('Specialists',specialists)
# Buildings: scalar yields, specialists, prerequisites, training, and conditional yields.
buildings=[]
bextras={
'B01':[tiles(1,'Food','R05')], 'B06':[tiles(1,'Production','R02')],
'B07':[xp(15,'{Land} {Military} {non-[术士]} {non-[医护]} {non-[死灵]} {non-[幽魂]}')],
'B09':[tiles(1,'Production','R01'),tiles(1,'Food','R06')],
'B10':[tiles(1,'Production','Fishing Boats'),'Connects trade routes over water'],
'B11':[pct(15,'Gold')], 'B14':[xp(15,t) for t in ['术士','医护','死灵','幽魂']],
'B16':[prod(15,WATER)], 'B19':[xp(15,LAND)], 'B22':[pct(20,'Gold')], 'B23':[pct(25,'Science')],
'B24':[tiles(1,'Production','Forest')], 'B25':[tiles(1,'Production',t) for t in ['R02','R04']],
'B26':[pct(15,'Production')], 'B27':[pct(15,'Science')], 'B28':['[All] Units adjacent to this city heal [5] HP per turn when healing'],
'B29':[prod(15,WATER)],'B30':[xp(15,LAND)],'B31':[pct(15,'Science')],'B32':[pct(15,'Culture')],
'B33':[],'B36':[pct(10,'Science')],
'B44':['Removes extra unhappiness from annexed cities'], 'B45':[tiles(1,'Food','Coast')],
'B47':['[15]% Great Person generation [in this city]'],'B49':[],
'B51':[],
'B52':[train('侦察','P47')], 'B54':[pct(25,'Science')], 'B55':[train(WATER,'P36')],
'B59':['[15]% Production when constructing [All] buildings [in this city]'],
'B61':[tiles(1,'Science','Forest')],'B62':[pct(15,'Gold')], 'B63':[train(LAND,'P31')],
'B64':['[2] Unit Supply'], 'B66':[pct(10,'Culture')],'B67':[prod(25,t) for t in ['攻城','构装']],
'B76':[train(t,'P33') for t in ['术士','死灵']]+['Unsellable','Destroyed when the city is captured'],
'B77':[train('医护','P34'),'Unsellable','Destroyed when the city is captured'],
'B78':[tiles(1,'Culture','Forest')], 'B80':[train('构装','P47')],
'B83':[xp(5,t) for t in ['术士','医护','死灵','幽魂']],
'B13':[tiles(1,'Culture','R31')],
'B81':['[+1 Gold] from every [Artist]',xp(10,'死灵'),xp(10,'幽魂'),'Unsellable','Destroyed when the city is captured'],
'B82':['[+1 Science] from every specialist [in this city]','Unsellable','Destroyed when the city is captured'],
'XB01':[st(2,'Production')+' <in cities connected to the capital>'],
'XB02':[xp(15,LAND)]+[prod(15,t) for t in ['步兵','重步兵']],
'XB04':[pct(20,'Gold'),tiles(1,'Gold','Fishing Boats')], 'XB05':[tiles(1,'Production','Forest')],
'XB07':[tiles(1,'Production','Fishing Boats'),'Connects trade routes over water'],
'XB08':[prod(20,WATER),xp(15,WATER)], 'XB09':[tiles(1,'Production','R02')],
'XB11':[pct(15,'Production'),'[+1 Science] from every [Engineer]'], 'XB12':[pct(25,'Science')],
'XB13':[tiles(1,'Production',t) for t in ['R01','R06']], 'XB14':[xp(10,t) for t in ['轻骑','骑射']],
'XB15':[xp(15,'{Land} {Military} {non-[术士]} {non-[医护]} {non-[死灵]} {non-[幽魂]}')],
'XB16':['Removes extra unhappiness from annexed cities'],'XB17':[prod(15,'攻城')],
'XB18':[prod(15,'构装')], 'XB20':['[+1 Culture] from every [Scientist]'], 'XB22':[pct(15,'Science')], 'XB24':['[2] Unit Supply'],
}
# Native field names have different semantics: requiredBuilding is a single local requirement.
def conditions(o,s):
 u=o['uniques']
 for b in re.findall(r'B\d+',s):
  if '无'+b in s:u.append(f'Only available <in cities without a [{b}]>')
  else:u.append(f'Only available <in cities with a [{b}]>')
 if '沿海' in s:u.append('Must be next to [Coast]')
 if '邻河' in s:u.append('Must be next to [River]')
 if '邻山' in s:u.append('Must be next to [Mountain]')
 for n in re.findall(r'人口至少(\d+)',s):u.append(f'Requires at least [{n}] population')
 for z,v in [('矿井','Mine'),('森林','Forest'),('任意自然奇观','Natural Wonder'),('I28','I28')]:
  if '3格内有本方'+z in s:u.append(f'Must have an owned [{v}] within [3] tiles')
 if '已吞并' in s:u+=['Only available <in [Annexed] cities>']
 if '首都' in s:u+=['Only available <in [Capital] cities>']
 for v in ['Scientific','Cultural','Diplomatic']:
  if v+'胜利开启' in s:u.append(f'Only available <when [{v}] Victory is enabled>')
 if '宗教开启' in s:u+=['Only available <when religion is enabled>']
 if '已强化' in s:u+=['Only available <after enhancing a religion>']
 if '完成任意5政策分支' in s:u+=['Only available <when number of [Completed Policy branches] is more than [4]>']
 for z in ['铁','魔晶']:
  if '可用'+z in s or (z+'≥1' in s):u.append(f'Only available <with [{RES[z]}]>')
 if '访世英雄少于2' in s:u+=['Only available <when number of [[P71] Units] is less than [2]>']
 for h in re.findall(r'现存(H\d+)为0',s):u.append(f'Only available <when number of [[{h}] Units] is equal to [0]>')
def building_effect(o,e):
 # Only the leading scalar-yield clause, never harvest conditional tile/training yields as flat income.
 first=e.split('；')[0]
 if re.fullmatch(r'(?:[+\d、粮食生产金币科研文化信仰本地全局幸福]+)',first):o.update(fixed(first))
 o['specialistSlots']={}
 for z,n in re.findall(r'(科学家|工程师|商人|艺术家)槽(\d+)',e):o['specialistSlots'][{'科学家':'Scientist','工程师':'Engineer','商人':'Merchant','艺术家':'Artist'}[z]]=int(n)
 for n in re.findall(r'城市战力\+(\d+)',e):o['cityStrength']=int(n)
 for n in re.findall(r'最大生命\+(\d+)',e):o['cityHealth']=int(n)
for group in ['buildings','unique_buildings']:
 for k,r in DATA[group].items():
  if group=='buildings':_,name,tech,cost,maint,cond,res,e=r
  else:_,nation,name,replaces,tech,cost,maint,cond,e=r;res='无'
  label(k,name);o=dict(name=k,cost=int(cost),maintenance=int(maint),requiredTech=tech,uniques=copy.deepcopy(bextras.get(k,[])))
  if tech=='开局':o.pop('requiredTech',None)
  building_effect(o,e);conditions(o,cond);consume(o,res)
  if k in ['B76','B77','B81','B82']:
   o['uniques']+=['Unsellable','Destroyed when the city is captured']
  o['uniques']=list(dict.fromkeys(o['uniques']))
  if group=='unique_buildings':o.update(uniqueTo=nation,replaces=replaces)
  buildings.append(o)
label('B00','宫殿','Palace')
buildings.append(dict(name='B00',cost=0,gold=3,science=3,production=3,culture=1,cityStrength=2,uniques=['Unbuildable','Cannot be purchased','Indicates the capital city','Moves to new capital when capital changes','[+3 Happiness]','Unsellable']))
# All 35 world/national/endgame structures.
wextra={
'W03':['[1] Sight <for [{Water} {Military}] units>','[1] Movement <for [{Water} {Military}] units>'],
'W04':[xp(15,LAND),prod(15,LAND)], 'W05':[], 'W06':[pct(15,'Science')],
'W07':['Gifts of Gold to City-States generate [15]% more Influence',tiles(1,'Gold','Water')],
'W08':['Free [H03] appears <when number of [[H03] Units] is equal to [0]>'],
'W09':['Free [H01] appears <when number of [[H01] Units] is equal to [0]>'],
'W10':['Free [H02] appears <when number of [[H02] Units] is equal to [0]>'],
'W11':['[-10]% Culture cost of adopting new Policies','[+2 Happiness]'],
'W12':[prod(20,'构装','in all cities')],'W13':['Free Social Policy'],
'W14':['[-15]% Gold cost of upgrading'],'W15':['[10]% growth [in all cities]'],
'W16':[pct(10,'Science','in all cities')],
'W17':['Free [H04] appears <when number of [[H04] Units] is equal to [0]>'],
'W18':['Triggers voting for the Diplomatic Victory','[+2 Happiness]'],
'W19':['Gain a free [Enhancer] belief'],
'W20':['Reveals the entire map','Free Social Policy'],
'W21':[prod(50,t,'in all cities') for t in DATA['parts']],
'K01':[pct(25,'Science')], 'K02':[prod(10,LAND)],'K03':[pct(25,'Gold')],
'K04':['[20]% Great Person generation [in this city]'],'K05':['[15]% Great Person generation [in this city]'],
'K06':['[1] Movement <for [{Water} {Military}] units>'],
'K07':['[-5]% Unhappiness from [Population] [in all cities]'],
'K09':['Gifts of Gold to City-States generate [10]% more Influence'],
'K10':[tiles(1,'Culture','I28','in all cities')],
'K11':['Free [H09] appears <when number of [[P71] Units] is less than [2]> <when number of [[H09] Units] is equal to [0]>'],
'K12':['Free [H11] appears <when number of [[P71] Units] is less than [2]> <when number of [[H11] Units] is equal to [0]> <with [R02]> <with [R03]>'],
'J01':['Enables construction of Spaceship parts'],'J02':[]}
for k,r in DATA['wonders'].items():
 _,name,tech,cost,cond,e=r;label(k,name)
 o=dict(name=k,requiredTech=tech,cost=int(cost),maintenance=0,uniques=['Cannot be purchased <hidden from users>','Unsellable <hidden from users>','Cannot be hurried <hidden from users>']+copy.deepcopy(wextra.get(k,[])))
 o['isWonder' if k.startswith('W') else 'isNationalWonder']=True
 if not k.startswith('W'):o['uniques']+=['Destroyed when the city is captured']
 building_effect(o,e);conditions(o,cond)
 # Global happiness must not also be a local field.
 if k in ['W11','W18']:o.pop('happiness',None)
 if k in ['W05','W06','W12','W13']:o['greatPersonPoints']={'W01':{'C08':1},'W02':{'C08':1},'W05':{'C08':2},'W06':{'C07':2},'W12':{'C08':1},'W13':{'C10':2}}[k]
 if k in ['W19','W20','W21','J02']:o['uniques']+=['Triggers a global alert upon build start','Triggers a global alert upon completion']
 if k=='W18':o['uniques']+=['Only available <when [Diplomatic] Victory is enabled>']
 if k=='J01':o['uniques']+=['Triggers a global alert upon completion']
 buildings.append(o)
for k,r in DATA['religious_buildings'].items():
 _,name,cost,e,belief=r;label(k,name);o=dict(name=k,cost=int(cost),uniques=['Unbuildable','Only available <when religion is enabled>']);building_effect(o,e);buildings.append(o)
save('Buildings',buildings)
# Military legends are not Great People. Their shared marker constrains the eight visitors.
for k,r in DATA['heroes'].items():
 _,name,source,t,melee,ran,rng,mov,cost,res,maint,e=r;label(k,name)
 i=int(k[1:]);u=['Unbuildable','Cannot be purchased','Never appears as a Barbarian unit',f'[{maint}]% maintenance costs']
 if int(ran):u+=['No defensive terrain bonus']
 if i!=4:u += [strength(25,'starting from the [V]'),strength(25,'starting from the [VI]')]
 if i in [1,2,4,8,9]:u+=['[1] Sight']
 if i==1:u+=['[10]% Strength bonus for [{Land} {Military}] units within [2] tiles']
 if i==2:u+=vs(15,'重步兵/重骑/构装')+['Earn [50]% of killed [Military] unit\'s [Strength] as [Science]']
 if i==3:u+=['Double movement in [Forest]',strength(20,'when fighting in [Forest] tiles'),'[5] HP when healing','All adjacent units heal [5] HP when healing']
 if i==3:
  for old,new in [('P41','P110'),('P42','P111')]:
   u.append(f'[This Unit] gains the [{new}] promotion <upon turn start> <for units with [{old}]> <for units without [{new}]> <hidden from users>')
   u.append(f'[This Unit] loses the [{old}] promotion <upon turn start> <for units with [{old}]> <for units with [{new}]> <hidden from users>')
 if i==4:u+=['Ignores terrain cost','May travel on Water tiles without embarking','No defensive terrain bonus']
 if i==5:u+=['All adjacent units heal [10] HP when healing']
 if i==6:u+=['Invisible to non-adjacent units','No defensive terrain bonus',"Earn [25]% of killed [Military] unit's [Strength] as [Culture]"]
 if i==7:u+=['Must set up to ranged attack']+vs(25,'构装/元素')
 if i==8:u+=['Can see invisible [幽魂] units','Can see invisible [英雄幽魂] units','Ignores Zone of Control',strength(15,'when adjacent to a [长柄] unit')]
 if i==9:u+=['May heal outside of friendly territory','[5] HP when healing','No defensive terrain bonus','Cannot enter ocean tiles <before discovering [D01-T19]>']
 if i==10:u+=vs(25,'死灵/幽魂/英雄幽魂')+["Earn [35]% of killed [Military] unit's [Strength] as [Faith]"]
 if i==11:u+=['Can build [Fort] improvements on tiles','Can build [Repair] improvements on tiles','[10] HP when healing','No defensive terrain bonus']
 if i==12:u+=[strength(15,'when defending','in [Friendly Land] tiles'),"Earn [50]% of killed [Military] unit's [Strength] as [Gold]"]
 if i in [2,4,6,10,11]:u+=[strength(-25,'when attacking','vs cities')]
 if i in [5,7,8,12]:u+=[strength(-50,'when attacking','vs cities')]
 u.append(DATA['hero_roles'][k]+' <hidden from users>')
 u.append('Hero <hidden from users>')
 if i>=5:u.append('P71 <hidden from users>')
 o=dict(name=k,unitType=t,strength=int(melee),rangedStrength=int(ran),range=int(rng),movement=int(mov),cost=0,uniques=u,promotions=[])
 o['civilopediaText']=[{'text':'FC Heroes','link':'Tutorial/FC Heroes'}]
 consume(o,res);units.append(o)
# Ocean Elf reef colonist is an additional settler, not a C01 replacement.
r=DATA['civilians']['C12'];label('C12',r[1],'Reef Settler')
o=copy.deepcopy(next(u for u in units if u['name']=='C01'))
o.update(name='C12',uniqueTo='N04',requiredTech=REEF['rules']['tech'],cost=int(r[4]),movement=int(r[5].split('/')[-1]))
o['uniques']+=['Uncapturable','May travel on Water tiles without embarking','Only available <in [Coastal] cities>','FC Reef near city <within [3] tiles of a [City center]> <hidden from users>',REEF['rules']['action'],'Comment [FC Reef foundation]']
o['civilopediaText']=[{'text':'FC Reef workflow'},{'text':'D01-T19','link':'Technology/D01-T19'},{'text':'Reef Island','link':'Terrain/Reef Island'}]
units.append(o)
for k,r in DATA['parts'].items():
 _,name,tech,cost,count=r;label(k,name);units.append(dict(name=k,unitType='Civilian',strength=0,movement=2,cost=int(cost),requiredTech=tech,uniques=['Spaceship part','Can be added to [Origin Apparatus] in the Capital','Cannot be purchased','Never appears as a Barbarian unit','Only available <if [J01] is constructed> <when [Scientific] Victory is enabled>']))
# Hostile ecology: only the Barbarian nation can construct these; normal armies cannot spawn.
for k,r in DATA['monsters'].items():
 _,name,tech,t,melee,ran,rng,mov,cost,res,obsolete,e=r;label(k,name)
 o=dict(name=k,unitType=t,strength=int(melee),rangedStrength=int(ran),range=int(rng),movement=int(mov),cost=int(cost),uniques=keyword(t,int(ran),e)+['Only available <for [Barbarians] Civilizations>'])
 optional(o,'requiredTech',tech);optional(o,'obsoleteTech',obsolete)
 if '无防御地形' in e:o['uniques']+=['No defensive terrain bonus']
 if '攻击城市战力-25%' in e:o['uniques']+=[strength(-25,'when attacking','vs cities')]
 if k=='M07':o['uniques']+=[strength(15,'when attacking')]
 o['uniques']=list(dict.fromkeys(o['uniques']));units.append(o)
save('Units',units)
# Promotions: OR prerequisites plus independent AND identity, technology, exclusions.
sees=['Can see invisible [幽魂] units','Can see invisible [英雄幽魂] units']
move=['[1] Movement'];sight=['[1] Sight'];heal=['[5] HP when healing'];mobile=['Can move after attacking'];zoc=['Ignores Zone of Control'];march=['Unit will heal every turn, even if it performs an action'];weight=['[25]% maintenance costs']
pe={}
def pset(ns,u):
 for n in ns.split():pe['P'+str(int(n)).zfill(2)]=u.copy()
pset('1 2',[strength(10,'when fighting in [Open terrain] tiles')]);pset('3 4',[strength(10,'when fighting in [Rough terrain] tiles')])
pset('5 25',vs(15,'Ranged','when defending'));pset('6 15 21 58',move);pset('7 8',[strength(10,'when attacking')]);pset('9 12',[strength(15,'when defending')]);pset('10 11',[strength(15,'vs cities')]);pset('13 14',[strength(10)])
pset('16 22 26 38 73 93',heal);pset('17 77',[strength(10,'when defending')]);pset('18',vs(15,'重步兵/重骑/构装/UX06/UX30/M05'));pset('20 30 40 101',sight)
pset('23',vs(20,'死灵/幽魂/英雄幽魂'));pset('27',vs(15,'元素/构装'));pset('29',vs(15,'射手/攻城'))
pset('31',['[1] Movement point cost to embark','[1] Movement point cost to disembark']);pset('33 43',sight+sees);pset('34 42 67',march+weight);pset('36',['May heal outside of friendly territory']+heal)
pset('37 51 54 81 85 89 97',vs(10,'Ranged','when defending'));pset('39 57 61',zoc)
pset('41',['[15]% Strength bonus for [{Land} {Military}] units within [1] tiles']);pset('44',['[1] Range']);pset('45',vs(20,'构装/元素'));pset('46',['Before engaging in combat performs an extra ranged attack with [30]% of melee combat strength']);pset('47',sees)
pset('48 78',["Earn [25]% of killed [Military] unit's [Strength] as [Culture]"]);pset('52 95 98',['All adjacent units heal [5] HP when healing']);pset('55',mobile);pset('60',['Heals [10] damage if it kills a unit']);pset('62 64',['No damage penalty for wounded units']+weight);pset('63',['Ignores terrain cost']+sight)
pset('65',['[15]% Strength bonus for [{Land} {Military}] units within [2] tiles']);pset('66',[strength(15,'when fighting in [Forest] tiles')]);pset('68 74',['All adjacent units heal [5] HP when healing']+weight);pset('69 79',mobile+zoc+weight);pset('70',sight+['Can build [Repair] improvements on tiles'])
pset('75 103',move+march+weight);pset('82',vs(20,'构装'));pset('83',vs(20,'Ranged','when defending'));pset('86',move+['Ignores terrain cost']);pset('87',vs(25,'Ranged','when defending'));pset('90',['[10]% Strength bonus for [{Water} {Military}] units within [2] tiles']);pset('91',move+mobile);pset('94',sight+sees);pset('99',[strength(15,'when adjacent to a [构装] unit')]);pset('102',["Earn [50]% of killed [Military] unit's [Strength] as [Gold]"]);pset('104',[strength(15,'when defending')])
pe['P109']=['Will not be displayed in Civilopedia','FC medic near active patient']
pe['P110']=copy.deepcopy(pe['P41'])
pe['P42']=['Unit will heal every turn, even if it performs an action <hidden from users>','Comment [FC Bridge healing H01]']+weight
pe['P111']=['Unit will heal every turn, even if it performs an action <hidden from users>','Comment [FC Bridge healing H03]']+weight
promotions=[]
for k,r in DATA['promotions'].items():
 _,name,types,req,e=r;label(k,name);parts=req.split('；');prereq=ids(parts[0],r'P\d+')
 u=copy.deepcopy(pe.get(k,[]))
 for tech in ids(req):u.append(f'Only available <after discovering [{tech}]>')
 for part in parts[1:]:
  ps=ids(part,r'P\d+')
  if not ps:continue
  if '无' in part:
   for p in ps:u.append(f'Only available <for units without [{p}]>')
  elif '或' in part and ('初印' in part or k in ['P41','P42']):
   u.append('Only available <for [non-[{non-['+ps[0]+']} {non-['+ps[1]+']}]] units>')
  else:
   for p in ps:u.append(f'Only available <for units with [{p}]>')
 if k in ['P110','P111']:u=[x+' <hidden from users>'if x.startswith('Only available')else x for x in u]
 # Some AND clauses are comma-delimited after the first identity.
 promotions.append(dict(name=k,unitTypes=[] if '专用' in types else types.split('/'),prerequisites=prereq,uniques=u))
save('UnitPromotions',promotions)
# Native improvement names are needed by roads, ruins and existing worker actions.
base_imps={x['name']:x for x in read('TileImprovements')}
improvements=[]
for k,r in DATA['improvements'].items():
 _,name,native,tech,turns,e,cond=r;label(native,name)
 if native in base_imps:o=copy.deepcopy(base_imps[native])
 else:o=dict(name=native,terrainsCanBeBuiltOn=[],uniques=[])
 o.pop('techRequired',None);o['uniques']=[]
 for a in ['food','production','gold','science','culture','faith']:o.pop(a,None)
 optional(o,'techRequired',tech if tech.startswith('D01-') else '无')
 o['turnsToBuild']=int(turns) if turns.isdigit() else -1
 o.update(fixed(e.split('；')[0]));u=o['uniques']
 if k=='I01':o['terrainsCanBeBuiltOn']=['Grassland','Plains','Flood plains'];u+=['Cannot be built on [Hill] tiles', '[+1 Food] <in [Fresh water] tiles> <after discovering [D01-T39]>']
 if k in ['I02','I03','I05','I06','I08']:o['terrainsCanBeBuiltOn']=[];u+=['Can only be built to improve a resource']
 if k=='I03':u+=['Does not need removal of [Forest]']
 if k=='I04':o['terrainsCanBeBuiltOn']=['Hill'];u+=['[+1 Production] <after discovering [D01-T28]>']
 if k=='I09':o['terrainsCanBeBuiltOn']=['Forest']
 if k in ['I07','I14']:o['terrainsCanBeBuiltOn']=['Land'];u += [f'Costs [{1 if k=="I07" else 2}] [Gold] per turn when in your territory']
 if k=='I10':o['terrainsCanBeBuiltOn']=['Land'];u+=['Gives a defensive bonus of [25]%']
 if k=='I11':pass  # Production reward belongs to Forest, not the removal order.
 if k in ['I15','I16','I17','I18','I19','I20']:o['terrainsCanBeBuiltOn']=['Land'];u+=['Great Improvement','Can only be built on [Land] tiles','Will not be replaced by automated units','Removes removable features when built']
 if k=='I20':u+=['Gives a defensive bonus of [50]%','Adjacent enemy units ending their turn take [10] damage','Can be built just outside your borders','Gain control over [All] tiles in a [1]-tile radius']
 if k=='I21':u+=['Unbuildable','Unpillagable','Provides a random bonus when entered','Excluded from map editor']
 if k=='I22':u+=['Unbuildable','Unpillagable','Marks a barbarian camp']
 if k=='I28':o['terrainsCanBeBuiltOn']=['Forest'];u+=['Cannot be built on [resource] tiles']
 if k=='I29':o['terrainsCanBeBuiltOn']=['Grassland','Plains'];u+=['Cannot be built on [Hill] tiles','Cannot be built on [resource] tiles','[+1 Gold] <after discovering [D01-T81]>']
 if k in ['I30','I31','I32','I33']:
  o['terrainsCanBeBuiltOn']=[];u+=['Can only be built to improve a resource']
  if k in ['I30','I31','I33']:u+=['Does not need removal of [Forest]']
 if k=='I32':u+=['[+1 Gold] <after discovering [D01-T08]>']
 if k=='I33':u+=['[+1 Faith] <after discovering [D01-T98]>']
 if k=='I35':
  o['terrainsCanBeBuiltOn']=['Hill'];u+=['Can only be built on [{Hill} {non-[Desert]} {non-[Tundra]} {non-[Snow]}] tiles','Cannot be built on [resource] tiles','[+1 Food] <in [Fresh water] tiles>']
 if k=='I36':
  o['terrainsCanBeBuiltOn']=['Land'];u+=['Cannot be built on [resource] tiles','Must be next to [R03]','Does not need removal of [Forest] <hidden from users>','Does not need removal of [Jungle] <hidden from users>','[+1 Science] <after discovering [D01-T17]>']
 if k=='I37':
  o['terrainsCanBeBuiltOn']=['Grassland','Plains'];u+=['Cannot be built on [Hill] tiles','Cannot be built on [resource] tiles']
  u+=['Must be next to [River]']
 improvements.append(o)
for n in ['City center','City ruins','Repair','Cancel improvement order']:improvements.append(base_imps[n])
save('TileImprovements',improvements)
# Map resources use the same ruleset IDs as the consuming units.
resources=[]
for k,r in DATA['resources'].items():
 if k not in DATA['resource_rules']:
  label(k,r[1]);continue
 _,name,typ,reveal,connect,imp,terr,deposit,e,desc=r;label(k,name);rule=DATA['resource_rules'][k]
 o=dict(name=k,resourceType={'战略':'Strategic','奖励':'Bonus','奢侈':'Luxury'}[typ],terrainsCanBeFoundOn=rule['terrains'],uniques=list(rule['uniques']),**fixed(e.split('；')[0]))
 optional(o,'revealedBy',reveal)
 o['improvedBy']=rule.get('improvedBy') or [next(v[2] for v in DATA['improvements'].values() if v[1]==imp)]
 if typ=='战略':
  a,b=map(int,deposit.split('/'))
  o['majorDepositAmount']={'sparse':max(1,b-1),'default':b,'abundant':b+2 if k in ['R01','R02'] else b+1}
  o['minorDepositAmount']={'sparse':max(1,a-1),'default':a,'abundant':a+1}
 if '；正确改良再' in e:o['improvementStats']=fixed(e.split('；')[1])
 resources.append(o)
resources+=copy.deepcopy(MAGIC['resource_definitions']);save('TileResources',resources)
# Natural wonders replace the base pool entirely, while preserving native terrain generation.
for k,r in DATA['natural_wonders'].items():
 _,name,kind,occurs,becomes,impassable,e,extra=r;label(k,name)
 o=dict(name=k,type='NaturalWonder',occursOn=occurs.split('/'),turnsInto=becomes,weight=10,uniques=[],**fixed(e))
 if impassable=='是':o['impassable']=True
 if extra=='FreshWater':o['uniques']+=['Fresh water']
 if extra=='Sight(+1)':o['uniques']+=['[1] Sight']
 contracts={'NW01':('P37',LAND),'NW02':('P40',LAND),'NW04':('P38',LAND),'NW05':('P39',WATER)}
 if k in contracts:
  p,f=contracts[k];filters={'NW01':['术士','死灵','英雄施法'],'NW04':['医护','英雄近战']}.get(k,[f]);o['uniques']+=[f'Grants [{p}] ([{k}]) to adjacent [{filt}] units for the rest of the game' for filt in filters]
 terrains.append(o)
for _t in terrains:
 if _t['name']=='Fallout':_t['uniques']+=['Will not be displayed in Civilopedia','Excluded from map editor']
save('Terrains',terrains)
# Policies and automatic completion effects.
A='in all cities'
def frombuilding(n,s,b):return f'[{n:+d} {s}] from all [{b}] buildings'
# Authoritative reviewed policy rules; IDs, prerequisites and layout stay native.
policies=copy.deepcopy(DATA['policy_rules'])
for branch in policies:
 k=branch['name'];label(k,DATA['policies'][k][1]);label(k+' Complete',DATA['policies'][k][1]+'·收束')
 for node in branch['policies']:
  if not node['name'].endswith(' Complete'):label(node['name'],DATA['policies'][node['name']][1])
save('Policies',policies)
# Religion effects use actual native belief categories and no second mana currency.
beliefs={}
def belief(n,u):beliefs[f'RB{n:02}']=u
for n,stat,tile in [(1,'Faith','Camp'),(3,'Culture','Pasture'),(4,'Faith','Fishing Boats'),(7,'Culture','Forest'),(8,'Faith','Jungle'),(9,'Faith','Desert'),(57,'Food','Camp'),(61,'Production','Quarry')]:belief(n,[f'[+1 {stat}] from every [{tile}]'])
for n,stat,b in [(2,'Science','B03'),(11,'Culture','B41'),(12,'Faith','B04'),(33,'Food','B01'),(34,'Production','B02'),(35,'Science','B12'),(37,'Happiness','B41')]:belief(n,[frombuilding(1,stat,b)])
belief(5,['[+1 Faith] from every [R02]','[+1 Faith] from every [R04]']);belief(6,['[+1 Faith, +1 Culture] from every [Quarry]']);belief(10,['[+1 Faith] from [Tundra] tiles without [Forest] [in this city]']);belief(13,['[+3 Faith] from every [Natural Wonder]']);belief(14,[st(1,'Happiness')+' <in cities with at least [6] [Population]>']);belief(15,['[10]% growth [in this city]']);belief(16,["Earn [50]% of [Military] unit's [Strength] as [Faith] when killed within 4 tiles of a city following this religion"])
belief(55,['[+1 Food, +1 Faith] in cities on [River] tiles']);belief(56,[prod(15,WATER)]);belief(58,['[+1 Gold, +1 Faith] [in all cities connected to capital]']);belief(59,[frombuilding(1,'Faith','B03'),frombuilding(1,'Culture','B54')]);belief(60,[train('侦察','P20')]);belief(62,['[15]% growth [in this city] <when not at war>'])
for n,s,a in [(17,'Gold',2),(18,'Science',1),(19,'Faith',1),(20,'Culture',1)]:belief(n,[f'[+{a} {s}] for each global city following this religion'])
for n,s,a,c in [(21,'Gold',4,A),(22,'Science',6,A),(23,'Culture',8,'in foreign cities')]:belief(n,[f'[+1 {s}] from every [{a}] global followers [{c}]'])
belief(24,['[+30 Gold] when a city adopts this religion for the first time']);belief(25,['Resting point for Influence with City-States following this religion [10]']);belief(26,['[+2 Culture, +2 Faith] [in capital]'])
for n,r in enumerate(DATA['religious_buildings'].values(),27):belief(n,[f'May buy [{r[0]}] buildings for [{r[2]}] [Faith] [in this city]'])
belief(36,[frombuilding(2,'Culture','B15')]);belief(38,['[10]% growth [in this city]']);belief(39,[frombuilding(2,'Gold','B11')]);belief(40,['[+2 Faith, +1 Happiness] from all [B24] buildings']);belief(41,['[+2 Faith, +1 Culture] from all [B14] buildings']);belief(42,[pct(10,'Science')]);belief(43,[xp(10,'医护')]);belief(44,['[All] Units adjacent to this city heal [5] HP per turn when healing']);belief(63,[train('侦察','P47')]);belief(64,[train('构装','P34')]);belief(45,['[25]% Natural religion spread [in all cities]']);belief(46,['Religion naturally spreads to cities [13] tiles away']);belief(47,['[-15]% Faith cost of generating Great Prophet equivalents']);belief(48,['[Faith] cost of purchasing [C04] units [-15]%']);belief(49,[frombuilding(2,'Faith','B28')]);belief(50,[frombuilding(2,'Faith','B49')])
# Last four enhancer rows are explicit to keep purchase authorization distinct from discounts.
belief(51,[frombuilding(2,'Culture','B45')]);belief(52,['[+2 Faith, +1 Culture] from all [B32] buildings']);belief(53,[frombuilding(1,'Faith','B41')]);belief(54,['[+2 Gold] from every [Holy site]'])
bl=[]
for k,r in DATA['beliefs'].items():
 label(k,r[1]);n=int(k[2:]);typ='Pantheon' if n<=16 or 55<=n<=62 else 'Founder' if n<=26 else 'Follower' if n<=44 or n>=63 else 'Enhancer'
 bl.append(dict(name=k,type=typ,uniques=beliefs[k]))
save('Beliefs',bl)
META=json.loads((ROOT/'design/metadata.json').read_text())
religion_roster=json.loads((ROOT/'design/宗教候选.json').read_text())
religions=[r['zh']for r in religion_roster];religion_en=[r['name']for r in religion_roster]
for z,e in zip(religions,religion_en):label(e,z,e)
religion_map=dict(zip(religions,religion_en));save('Religions',religion_en)
# Nations and their fully expanded, scoped effects.
nextra={
'N01':['[15]% Production towards any buildings that already exist in the Capital <in [non-[Capital]] cities>'],
'N02':['[15]% [Gold] from Trade Routes','[-10]% Gold cost of upgrading'],
'N03':[tiles(1,'Faith','{Forest} {'+x+'}',A) for x in ['Camp','Lumber mill','I28']],
'N04':[tiles(1,'Gold','Fishing Boats',A)]+[f'[1] Movement <for [{t}] units>' for t in ['海近战','海远程']]+['Comment [FC Reef colonization]'],
'N05':[tiles(1,'Gold','Mine',A),'[15]% Strength for cities'],
'N06':[frombuilding(1,'Science','B02'),'[+1 Science] from every [Engineer]'],
'N07':[tiles(1,'Gold','Pasture',A)]+[f'[1] Movement <for [{t}] units>' for t in ['轻骑','骑射']],
'N08':[prod(15,t,A) for t in ['步兵','重步兵','长柄']]+['[-10]% XP required for promotions'],
'N09':[frombuilding(1,'Production','B02')]+[prod(15,t,A) for t in ['攻城','构装']],
'N10':['[1] Sight <for [侦察] units>',frombuilding(1,'Culture','B49'),prod(20,'侦察',A)],
'N11':['[+1 Science] per [3] population [in all cities] <in cities with a [B03]>']+[f'[-15]% maintenance costs <for [{t}] units>' for t in ['死灵','幽魂']],
'N12':[f'[-15]% maintenance costs <for [{t}] units>' for t in ['步兵','重步兵','长柄']]+[xp(10,'长柄',A)]}
diplomacy={
'introduction':('May our roads bring knowledge and peace.','愿我们的道路带来知识与安宁。'),
'declaringWar':('Words can no longer sustain our oath.','我们的誓约已无法以言语维系。'),
'attacked':('Our cities and people will defend their roads.','我们的城市与人民将守住自己的道路。'),
'defeated':('Our nation falls, but its memory endures.','国家虽败，记忆仍将传承。'),
'neutralHello':('State your proposal.','说出你的提议。'),
'hateHello':('Trust must be rebuilt through action.','信任必须由行动重建。'),
'declaringFriendship':('May this agreement benefit us both.','愿这份约定使双方受益。'),
'neutralDenouncing':('Your deeds have broken our trust.','你的行为辜负了我们的信任。'),
'hateDenouncing':('The nations shall hear of your broken oaths.','诸国将知晓你的背约之举。'),
'denounced':('Let deeds judge these accusations.','让行动来评判这些指责。'),
'acceptingDemand':('We accept these terms.','我们接受这些条件。'),
'neutralRejectingDemand':('We cannot accept this demand.','我们无法接受这项要求。'),
'hateRejectingDemand':('Your demands have no place here.','这里不接受你的勒索。'),
'tradeRequest':('Let us exchange fairly.','让我们公平交换。')}
for e,z in diplomacy.values():label(e,z,e)
nations=[]
for k,r in DATA['nations'].items():
 label(k,r[1]);m=META['nations'][k]
 o=dict(name=k,leaderName=k+' Leader',outerColor=[int(m['color'][i:i+2],16) for i in [0,2,4]],innerColor=[255,255,255] if k=='N08' else [35,35,40],startBias=[m['bias']],preferredVictoryType=m['victory'],cities=[k+f' City {i+1}' for i in range(8)],favoredReligion=religion_map[m['religion']],uniqueName=k+' Ability',uniques=nextra[k])
 label(o['leaderName'],m['leader']);label(o['uniqueName'],r[2])
 for i,c in enumerate(m['cities']):label(o['cities'][i],c)
 o['spyNames']=[k+f' Agent {j+1}' for j in range(8)]
 for j in range(8):label(o['spyNames'][j],m['cities'][j]+'密探','Agent '+str(j+1))
 o.update({key:val[0] for key,val in diplomacy.items()});nations.append(o)
# Diplomacy bonuses are carried by named CityStateTypes, not by the CS nation.
cscolors={'Scientific':[70,150,245],'Cultured':[160,95,235],'Maritime':[70,200,90],'Industrial':[220,145,60],'Mercantile':[245,205,40],'Happiness':[245,145,180],'Militaristic':[220,65,65],'Religious':[220,225,230]}
# Every city-state combines a readable base payoff with its own allied pact.
csbonus={k:r['uniques'] for k,r in DATA['city_state_pacts'].items()}
def cs_base(typ,ally):
 if typ in ['Scientific','Cultured','Religious','Mercantile']:
  stat={'Scientific':'Science','Cultured':'Culture','Religious':'Faith','Mercantile':'Gold'}[typ]
  values={'Scientific':[2,4,6],'Cultured':[3,6,9],'Religious':[3,6,9],'Mercantile':[4,6,8]}[typ]
  conditions=['<before the [III]>','<starting from the [III]> <before the [V]>','<starting from the [V]>']
  return [f'[+{v*(2 if ally else 1)} {stat}] '+c for v,c in zip(values,conditions)]
 if typ=='Maritime':return ['[+2 Food] [in capital]']+(['[+1 Food] [in all cities]']if ally else [])
 if typ=='Industrial':
  result=[]
  for j,cond in enumerate(['<before the [III]>','<starting from the [III]> <before the [V]>','<starting from the [V]>']):
   result.append(f'[+{[2,3,4][j]} Production] [in capital] '+cond)
   if ally:result.append(f'[+{[1,1,2][j]} Production] [in all cities] '+cond)
  return result
 if typ=='Happiness':return [f'[+{3 if ally else 2} Happiness] <before the [V]>',f'[+{4 if ally else 3} Happiness] <starting from the [V]>']
 return [f'Provides military units every ≈[{17 if ally else 20}] turns']
label('City-state pact','独有盟约','Unique pact')
label('Industrial capital total','首都同时享受每城收益：盟友时，I—II时代首都基础产能合计+3，III—IV时代合计+4，V—VI时代合计+6；其他城市分别+1、+1、+2。','The capital also receives the per-city yield. Allied capital base Production totals +3 in eras I–II, +4 in III–IV and +6 in V–VI; other cities receive +1, +1 and +2 respectively.')
cstypes=[]
for k,r in DATA['city_states'].items():
 _,name,typ,display,personality=r;ck=typ+'-'+k;label(k,name);label(ck,display+'·'+name)
 extra=csbonus[k]
 pactkey=k+' Pact';pact=DATA['city_state_pacts'][k];label(pactkey,'特色盟约：'+pact['zh'],'Unique pact: '+pact['en'])
  # The type page shows both the base tiers and the named city's distinct pact.
 cstypes.append(dict(name=ck,color=cscolors[typ],friendBonusUniques=cs_base(typ,False),allyBonusUniques=cs_base(typ,True)+['Comment [City-state pact]']+extra,uniques=['Start bias [Coast]'] if typ=='Maritime' else [],civilopediaText=[]))
 pedia=[]
 if typ=='Industrial':pedia.append({'text':'Industrial capital total'})
 nations.append(dict(name=k,cityStateType=ck,personality=personality,cities=[k],outerColor=cscolors[typ],innerColor=[35,35,40],startBias=['Coast'] if typ=='Maritime' else [],civilopediaText=pedia))
nations += [dict(name='Barbarians',outerColor=[146,76,76],innerColor=[5,5,5]),dict(name='Spectator',outerColor=[255,255,255])]
save('Nations',nations);save('CityStateTypes',cstypes)
base_quests={q['name']:q for q in read('Quests')}
quests=[]
weights={1:{'Mercantile':2,'Maritime':2},2:{'Militaristic':3},3:{'Mercantile':3,'Maritime':2},4:{'Cultured':3},5:{'Cultured':3},6:{'Maritime':3,'Mercantile':2},7:{'Cultured':2},8:{'Mercantile':3},9:{'Religious':2},10:{'Cultured':3},11:{'Religious':3},12:{'Cultured':3},13:{'Religious':3}}
for k,r in DATA['quests'].items():
 _,name,display,typ,influence,duration,desc,w=r;n=int(k[1:]);o=copy.deepcopy(base_quests[name]);o.update(type=typ,influence=int(influence),duration=int(duration),minimumCivs=1 if n==2 else 2,weightForCityStateType={x:1 for x in ['Friendly','Neutral','Hostile','Irrational']})
 for cs,cr in DATA['city_states'].items():
  pref=META['city_preferences'][cs];v=4 if k==pref[0] else 3 if k==pref[1] else weights[n].get(cr[2],1);o['weightForCityStateType'][cr[2]+'-'+cs]=v
 quests.append(o)
save('Quests',quests)
victories=read('VictoryTypes')
for v in victories:
 if v['name']=='Scientific':
  v.update(milestones=['Build [J01]','Add all [Origin Apparatus parts] in capital'],requiredSpaceshipParts=['S01']*3+['S02','S03','S04'],victoryString='Magic victory won',civilopediaText=[{'text':'Magic victory overview'},{'text':'Magic victory assembly'},{'text':'Magic victory access'}])
 if v['name']=='Cultural':v['milestones']=['Complete [5] Policy branches','Build [J02]']
 if v['name']=='Diplomatic':v['milestones']=['Anyone should build [W18]','Win diplomatic vote']
 v['victoryScreenHeader']='AOD '+v['name']+' Objective';label(v['victoryScreenHeader'],{'Scientific':'建成本源观测工程，将六件本源装置部件运至首都并组装，达成魔法胜利。','Cultural':'完成五个政策分支，并建成文明大典。','Diplomatic':'任一文明建成万邦议席后，通过外交投票获胜。','Domination':'控制所有主要文明的原始首都。','Time':'达到最大回合时取得最高分。'}[v['name']])
save('VictoryTypes',victories)
# Events use explicit non-timed availability and native triggerable results.
def gain(n,s):return f'Gain [{n}] [{s}]'
def damage(n):return f'[This Unit] takes [{n}] damage'
def healnow(n):return f'[This Unit] heals [{n}] HP'
def givep(p):return f'[This Unit] gains the [{p}] promotion'
def timed(u,n):return f'{u} <for [{n}] turns>'
results={
'E16':[[gain(200,'Culture')],[damage(20),givep('P47')],[gain(90,'Culture')]],
'E17':[[damage(25),givep('P33')],[gain(180,'Science')],[gain(100,'Gold')]],
'E18':[[damage(20),gain(180,'Science')],[damage(20),givep('P38')],[gain(90,'Culture')]],
'E19':[[damage(20),givep('P31')],['Reveal up to [All] [Water] within a [10] tile radius',gain(60,'Culture')],[gain(100,'Gold')]],
'E20':[['Reveal up to [All] [Ancient ruins] within a [12] tile radius',gain(30,'Culture')],['Reveal up to [All] [Barbarian encampment] within a [8] tile radius',healnow(20)],[gain(100,'Culture')]],
'E24':[['[This Unit] gains [20] XP'],[gain(200,'Culture')],[healnow(30)]],
'E25':[[damage(20),'Free [H05] appears'],[healnow(25)],[gain(80,'Culture')]],
'E26':[['Free [H06] appears'],[gain(140,'Culture')]],
'E27':[['Free [H07] appears'],[gain(220,'Science')]],
'E28':[[damage(25),'Free [H08] appears'],[gain(160,'Science')]],
'E29':[['Free [H10] appears'],[gain(160,'Culture')]],
'E30':[['Free [H12] appears'],[gain(220,'Culture')]]}
# Conditions are constructed explicitly, never inferred from localized prose at runtime.
def eventconds(text):
 c=[]
 if '有城市' in text:c+=['when number of [Cities] is more than [0]']
 if '有沿海城市' in text:c+=['when number of [[Coastal] Cities] is more than [0]']
 for n in re.findall(r'HP>(\d+)',text):c.append(f'when above [{n}] HP')
 if '受伤' in text:c+=['when below [100] HP']
 if '不是U77/H08' in text:c+=['for [{non-[U77]} {non-[H08]}] units']
 if '术士或英雄施法' in text:c+=['for [non-[{non-[术士]} {non-[英雄施法]}]] units']
 if '有P16' in text:c+=['for units with [P16]']
 if '无P' in text:
  after=text.split('无P',1)[1].split('；')[0]
  for p in re.findall(r'P?\d+', 'P'+after):c.append('for units without [P'+p.lstrip('P')+']')
 if 'P71单位<2' in text:c+=['when number of [[P71] Units] is less than [2]']
 for h in re.findall(r'现存(H\d+)=0',text):c.append(f'when number of [[{h}] Units] is equal to [0]')
 if '可用魔晶' in text:c+=['with [R03]']
 if '宗教开启' in text:c+=['when religion is enabled']
 return c
events=[]
for k,r in DATA['events'].items():
 if k=='E33':continue
 if k in ['E31','E32']:continue
 source,choices=r;label(k,META['events'].get(k,k));o=dict(name=k,text=k,presentation='Alert',civilopediaText=[],choices=[])
 for n,paragraph in enumerate(PRESENTATION['events'][k]['paragraphs']):
  key=k+f' Paragraph {n+1}';label(key,paragraph['zh'],paragraph['en']);o['civilopediaText'].append({'text':key})
 for j,(name,cond,cost,e,weight) in enumerate(choices):
  ck=k+'-'+chr(65+j);label(ck,name)
  c=eventconds(cond)
  if cost:c+=[f'when above [{int(cost)-1}] [Gold]']
  effects=copy.deepcopy(results[k][j])
  if cost:effects.insert(0,gain(-int(cost),'Gold')+' <hidden from users>')
  if not effects:
   label('No immediate effect','无直接效果。','No immediate effect.')
   effects=['Comment [No immediate effect]']
  if weight:effects.append(f'[{weight}]% weight to this choice for AI decisions')
  req=PRESENTATION['events'][k]['requirements'][j];reqkey=ck+' Requirements'
  if req['zh']:label(reqkey,req['zh'],req['en'])
  # All game speeds offer the same decisions. Variants only scale timed duration.
  variants=[('Quick',.67),('Standard',1),('Epic',1.5),('Marathon',3)] if any('<for [' in x for x in effects) else [('Any',1)]
  for speed,mult in variants:
   gates=c+([f'on [{speed}] game speed'] if speed!='Any' else [])
   availability=['Only available'+''.join(f' <{x}>' for x in gates)+' <hidden from users>'] if gates else []
   choice=dict(name=ck+'-'+speed,text=ck,civilopediaText=[{'text':reqkey}] if req['zh'] else [],uniques=availability+[re.sub(r'<for \[(\d+)\] turns>',lambda m:f'<for [{max(1,int(int(m[1])*mult+.5))}] turns>',x) for x in effects])
   o['choices'].append(choice)
 events.append(o)
 assert not source.startswith('D01-'), 'Research must not trigger encounters: '+k
events+=copy.deepcopy(MAGIC['event_definitions'])
for o in events:
 if o['name'] in ['E31','E32']:
  label(o['name'],'群星共研' if o['name']=='E31' else '国土结界')
  for c in o['choices']:c['text']='Perform the ritual'
label('Perform the ritual','施行仪式','Perform the ritual')
events.append(dict(name='E33',text='E33',presentation='None',choices=[dict(name='E33-Resolve',text='E33-Resolve',uniques=['[This Unit] gains the [P109] status for [1] turn(s)','[This Unit] heals [5] HP <for every [[{医护} {FC medic near active patient} {non-[P109]} {non-[Embarked]}] Units]>','[This Unit] loses the [P109] status'])]))
label('E33','医疗结算','Medical resolution');label('E33-Resolve','结算相邻医护并清除临时状态','Resolve adjacent medics and clear the temporary status')
save('Events',events);save('Techs',[columns[k] for k in sorted(columns)])
ruins=[]
for k,r in DATA['ruins'].items():
 _,name,weight,cond,e,desc=r;label(k,name);u=[];cs=[]
 for t in ids(cond):cs.append(f'after discovering [{t}]' if '未知'+t not in cond else f'before discovering [{t}]')
 if '至少1城' in cond:cs+=['when number of [Cities] is more than [0]']
 if '宗教开启' in cond:cs+=['when religion is enabled']
 if 'Land Military' in cond:cs+=[own(LAND)]
 elif 'Military' in cond or '探索者为军事单位' in cond:cs+=[own('Military')]
 if '受伤' in cond:cs+=['when below [100] HP']
 if k=='RU13':cs += [own('术士'),'for units without [P37]']
 if k=='RU14':cs += ['for units with [P16]','for units without [P38]']
 if k=='RU23':cs += ['for [Hero] units']
 if 'Hill' in cond:cs+=['within [2] tiles of a [Hill]']
 if 'Forest' in cond:cs+=['within [2] tiles of a [Forest]']
 if 'Water' in cond:cs+=['within [3] tiles of a [Water]']
 if 'Road' in cond:cs+=['within [2] tiles of a [Road]']
 if cs:u+=['Only available'+''.join(' <'+c+'>' for c in cs)]
 u.append(e)
 msg=PRESENTATION['ruins'][k];key=msg['en'];label(key,msg['zh'],msg['en'])
 ruins.append(dict(name=k,weight=int(weight),notification=key,uniques=u))
save('Ruins',ruins)
# Final native compatibility adjustments. These are kept separate from source data.
# Chinese type names are legal internal IDs and receive English display translations too.
for era in eras:era.update(startingSettlerUnit='C01',startingWorkerUnit='C02')
save('Eras',eras)
for o in units:
 if o['unitType'] in ['Civilian','Civilian Water']:o.setdefault('rangedStrength',0);o.setdefault('range',0)
 if o['name'] in ['K13','K14']:label(o['name'],DATA['civilians'][o['name']][1])
 if o['name']=='C06':o['uniques']+=['Great Person - [Faith]']
 if o['name'] in ['C07','C08','C09','C10','C11']:
  typ={'C07':'Science','C08':'Production','C09':'Gold','C10':'Culture','C11':'War'}[o['name']]
  o['uniques']=[u for u in o['uniques'] if not u.startswith('Great Person -')]+[f'Great Person - [{typ}]']
 if o['name']=='C05':o['uniques']=[u.replace('a enhanced religion','an enhanced religion') for u in o['uniques']]
 # Noncombat civilian actions must never enter the wild unit pool.
 if o['unitType'] in ['Civilian','Civilian Water']:o['uniques']+=['Never appears as a Barbarian unit']
 o['uniques']=list(dict.fromkeys(o['uniques']))
for _k,_r in DATA['city_state_units'].items():
 _base=next(u for u in units if u['name']==_r['base']);_u=copy.deepcopy(_base);_u.update(name=_k,uniqueTo=_r['cityState'],replaces=_r['base']);_u['uniques']=[_v for _v in _u['uniques']if _v not in _r.get('removeUniques',[])]+_r['extraUniques'];units.append(_u);label(_k,_r['zh'],_r['en'])
save('Units',units)
for n in nations:
 if n['name'].startswith('CS'):
  n['cities']=[n['name']+' Capital'];label(n['cities'][0],ZH[n['name']])
save('Nations',nations)
# Actual grant rechecks the shared visitor cap even after a choice was queued.
for event in events:
 for choice in event['choices']:
  for i,u in enumerate(choice['uniques']):
   m=re.fullmatch(r'Free \[(H\d+)\] appears',u)
   if m:choice['uniques'][i]=u+f' <when number of [[{m[1]}] Units] is equal to [0]> <when number of [[P71] Units] is less than [2]>'
save('Events',events)
# One native Civilopedia-only article collects all twelve heroes across domains.
label('FC Heroes','英雄','Heroes')
label('Unciv Tutorials','原版教程','Unciv Tutorials')
label('FC Mod introduction','模组介绍','Introduction')
label('FC Heroes overview','查看全部十二位英雄。点击名称可打开各英雄的百科条目。','Browse all twelve heroes. Select a name to open that hero’s Civilopedia entry.')
label('FC Introduction setting','FantasyUnciv 是独立的奇幻文明规则集。十二个文明在六个时代中发展城邦、探索荒野，并争夺世界的未来。','FantasyUnciv is a standalone fantasy civilization ruleset. Twelve civilizations develop their realms, explore the wilderness and compete across six eras.')
label('FC Introduction choices','选择适合地形与文明的科技和政策路线，发展农业、工业、航海、文化、宗教与四学派魔法；招募英雄支持军队。','Choose technologies and policies suited to your civilization and terrain. Develop agriculture, industry, navigation, culture, religion and four schools of magic, and recruit heroes to support your armies.')
label('FC Introduction victories','可以争取魔法、文化、征服、外交或时间胜利。推荐从第一时代、标准速度开始。','Pursue Magic, Cultural, Domination, Diplomatic or Time Victory. Era I and Standard speed are recommended for a first game.')
# Move unchanged native tutorial contents into a named base chapter, allowing
# FantasyUnciv to sort before it without invisible characters or client changes.
native_tutorials=copy.deepcopy(read('Tutorials'))
for t in native_tutorials:t['category']='Unciv Tutorials'
mod_tutorials=[{'name':'FC Mod introduction','category':'FantasyUnciv','civilopediaText':[{'text':'FC Introduction setting'},{'text':'FC Introduction choices'},{'text':'FC Introduction victories'},{'text':'FC Heroes','link':'Tutorial/FC Heroes'}]},{'name':'FC Heroes','category':'FantasyUnciv','civilopediaText':[{'text':'FC Heroes overview'}]+[{'text':h,'link':'Unit/'+h}for h in DATA['heroes']]}]
# Player-facing acquisition and exploration articles; no gameplay effects.
pedia=json.loads((ROOT/'design/百科补充.json').read_text())
for key,text in pedia['labels'].items():label(key,text['zh'],text['en'])
next(x for x in mod_tutorials if x['name']=='FC Heroes')['civilopediaText']=pedia['hero_rows']
mod_tutorials.append({'name':'FC Ruins encounters','category':'FantasyUnciv','civilopediaText':pedia['ruin_rows']})
mod_tutorials[0]['civilopediaText'].append({'text':'FC Ruins encounters','link':'Tutorial/FC Ruins encounters'})
save('Tutorials',mod_tutorials+native_tutorials)
# Language-independent defaults are English; the base client supplies native UI/Unique translations.
from english_names import NAMES
EN.update(NAMES)
for h,c in DATA['hero_promotion_rules'].items():EN[c['type']]='Hero: '+EN[h]
for k in ZH:
 if k.endswith(' Capital') and k.startswith('CS'):EN[k]=EN[k[:4]]
 if k not in EN and not re.search('[\u4e00-\u9fff]',k):EN[k]=k
for r in DATA['city_states'].values():
 k,_,typ,_,_=r;EN[typ+'-'+k]={'Cultured':'Cultural City-State','Maritime':'Agrarian City-State','Mercantile':'Commercial City-State','Militaristic':'Military City-State','Religious':'Religious City-State','Scientific':'Scientific City-State','Industrial':'Industrial City-State','Happiness':'Happiness City-State'}[typ]+' - '+EN[k]
for k in list(ZH):
 if k.startswith('PB') and k.endswith(' Complete'):EN[k]=EN[k.split()[0]]+' Complete'
missing=[k for k in ZH if k not in EN]
if missing:raise ValueError('Missing English translations: '+str(missing))
label('Enable Nuclear Weapons','启用核武器（本模组无此内容）','Enable Nuclear Weapons (not used by this mod)')
# Normal healing is conditional; do not invent a fixed heal amount.
label('Unit will heal every turn, even if it performs an action','即使移动或攻击，回合结束仍正常恢复：城市中心基础25、友好陆地20、其他陆地10生命；友好水域符合恢复资格时基础20、其他水域基础0。已有恢复加成另计，登船时不恢复，最多至100生命。','Heals at turn end even after moving or attacking. Base healing: 25 HP in a city center, 20 on friendly land, 10 on other land; 20 in eligible friendly water and 0 on other water. Existing healing bonuses apply. Embarked units cannot heal; maximum health is 100 HP.')
label('FC Bridge healing H01','即使移动或攻击，回合结束仍恢复：城市中心25、友好陆地20、其他陆地10生命。已有恢复加成另计，最多至100生命；登船时不恢复。','Heals at turn end even after moving or attacking: 25 HP in a city center, 20 on friendly land, or 10 on other land. Existing healing bonuses apply, up to 100 HP. Cannot heal while embarked.')
label('FC Bridge healing H03','即使移动或攻击，回合结束仍恢复：城市中心30、友好陆地25、其他陆地15生命（已计入本体+5）。其他恢复加成另计，最多至100生命；登船时不恢复。','Heals at turn end even after moving or attacking: 30 HP in a city center, 25 on friendly land, or 15 on other land, including this hero’s innate +5 HP. Other healing bonuses apply, up to 100 HP. Cannot heal while embarked.')
label('FC Reef colonization','远洋航行后可在沿海城市训练造礁开拓者，建立岛礁殖民地。','After Ocean Navigation, coastal cities can train Reef Settlers to establish reef colonies.')
label('FC Reef foundation','每队可造礁1次，造礁不消耗移动力，可在同回合继续建城。选址须为无主、无资源、未改良、无地貌的浅海；可邻接陆地，3格内无城市。之后按正常规则建城。','Can raise one reef without spending movement, then found a city in the same turn. Requires an unowned, resource-free, unimproved, featureless Coast tile, more than 3 tiles from any city. Found a city afterward using the normal rules.')
label('FC Reef workflow','抵达合适浅海并保留移动力时，执行“改造地形：岛礁”；造礁不消耗移动力，随后可在同一回合建城并消耗本单位。建城前岛礁仍是无主地块。','Reach a suitable Coast tile with movement remaining and choose “Transform terrain: Reef Island”. Reef construction spends no movement. You may immediately found a city on the reef in the same turn, consuming this unit. The reef remains unowned until settled.')
label('Turn this tile into a [terrainName] tile','改造地形：[terrainName]','Transform terrain: [terrainName]')
label('Field medicine','每名医护使相邻本方陆地单位在回合结束时额外恢复5生命；移动或攻击后仍生效，多名医护可叠加。','Each medic restores 5 extra HP to adjacent friendly land units at turn end, even after moving or attacking. Multiple medics stack.')
label('Must be next to [tileFilter]','所在地块须与[tileFilter]相邻','Must be next to [tileFilter]')
label('Gifts of Gold to City-States generate [relativeAmount]% more Influence','赠予城邦金币获得的影响力[relativeAmount]%','Gifts of Gold to City-States generate [relativeAmount]% more Influence')
label('[amount]% Food is carried over after population increases [cityFilter]','[cityFilter]每次增加1人口后，返还本次增长所需粮食的[amount]%到粮仓','[cityFilter] retains [amount]% of the Food required for each population increase')
label('Enables construction of Spaceship parts','允许制造本源装置部件','Enables construction of Origin Apparatus parts')
label('Spaceship parts','本源装置部件','Origin Apparatus parts')
label('Spaceship part','本源装置部件','Origin Apparatus part')
label('The Spaceship','本源装置','The Origin Apparatus')
label('spaceship parts','本源装置部件','Origin Apparatus parts')
label('Complete all the spaceship parts to win!','组装全部本源装置部件以获胜！','Assemble all Origin Apparatus parts to win!')
label('Influence of all other civilizations with all city-states degrades [relativeAmount]% faster','其他文明对城邦的影响力衰减速度[relativeAmount]%','Influence of all other civilizations with all city-states degrades [relativeAmount]% faster')
label('Scientific','魔法','Magic')
label('Scientific Victory','魔法胜利','Magic Victory')
label('Science Victory','魔法胜利','Magic Victory')
label('Magic victory won','你已掌握四源知识，并在首都完成本源装置。魔法胜利属于你的文明。','Your civilization has mastered the four sources and completed the Origin Apparatus in its capital. You have achieved a Magic Victory.')
label('Magic victory overview','魔法胜利以四源知识和本源装置为目标。研究相关科技，建成本源观测工程，随后生产并组装所需部件。','A Magic Victory requires knowledge of the four sources and completion of the Origin Apparatus. Research the relevant technologies, build the Origin Observation Project, then produce and assemble its components.')
label('Magic victory assembly','需要三件共鸣锚，以及星位矩阵、稳定核心、物质校准仪各一件，共六件。可以在不同城市生产，最后运到当前首都，逐件执行组装。','Build three Resonance Anchors and one Stellar Matrix, Stabilization Core and Material Calibrator: six components in total. Different cities may produce them; bring them to the current capital and assemble them individually.')
label('Magic victory access','所有文明都可争取魔法胜利，不要求创立宗教或训练特定施法单位。未组装部件可被拦截；相关胜利开关仍需启用。','Every civilization may pursue a Magic Victory. Founding a religion or training particular spellcasters is not required. Unassembled components can be intercepted, and this victory must be enabled.')
label('There are four ways to win in Unciv. They are:\\n - Cultural Victory: Complete 5 Social Policy Trees and build the Utopia Project\\n - Domination Victory: Conquer the original capital of all other Major civs\\n - Science Victory: Be the first to construct a Spaceship\\n - Diplomatic Victory: Build the United Nations and win the vote','本模组有五种胜利方式：\\n - 魔法胜利：建成本源观测工程，将六件本源装置部件运到首都并组装。\\n - 文化胜利：完成五个政策分支，并建成文明大典。\\n - 征服胜利：控制所有主要文明的原始首都。\\n - 外交胜利：万邦议席开启投票后，赢得外交投票。\\n - 时间胜利：到达回合上限时取得最高原生总分。',"This mod has five victory types:\\n - Magic Victory: Build the Origin Observation Project and assemble all six Origin Apparatus components in the capital.\\n - Cultural Victory: Complete five policy branches and build the Great Chronicle of Civilizations.\\n - Domination Victory: Control every major civilization's original capital.\\n - Diplomatic Victory: Win the vote after the Assembly of Nations enables diplomatic voting.\\n - Time Victory: Have the highest native score at the turn limit.")
label('Once you have completed the Apollo Program, you can start constructing spaceship parts in your cities (with the relevant technologies) to win a Scientific Victory!','建成本源观测工程后，可以在符合科技条件的城市生产本源装置部件。将全部六件运到当前首都并组装，即达成魔法胜利。','After completing the Origin Observation Project, cities with the relevant technologies can produce Origin Apparatus components. Bring all six to the current capital and assemble them to achieve a Magic Victory.')
# The built-in templates translate all nested arguments, including custom role names.
for lang,table in [('Simplified_Chinese',ZH),('English',EN)]:
 path=OUT/'translations'/(lang+'.properties')
 path.write_text('# FantasyUnciv\n# Generated by tools/build.py; edit tools/english_names.py or design data.\n\n'+'\n'.join(f'{k} = {v}' for k,v in sorted(table.items()))+'\n')
print(f'Generated {len(techs)} technologies, {len(units)} units, {len(buildings)} buildings, {len(promotions)} promotions, {len(events)} events; {len(ZH)} bilingual display keys.')
