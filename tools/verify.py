#!/usr/bin/env python3
"""Check cross-file invariants and the high-risk rules in the generated native mod."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];J=ROOT/'jsons'
D=json.loads((ROOT/'design/设计数据.json').read_text())
errors=[];checks=0
def check(ok,message):
 global checks
 checks+=1
 if not ok:errors.append(message)
def unique_keys(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('Duplicate JSON key: '+k)
  d[k]=v
 return d
def load(name):return json.loads((J/(name+'.json')).read_text(),object_pairs_hook=unique_keys)
def index(name):
 a=load(name);check(len({x['name'] for x in a})==len(a),name+' duplicate names');return {x['name']:x for x in a}
# The mod-manager date parser is stricter than the ruleset validator.
# Locally generated mods can omit lastUpdated; non-empty values must match the API format.
metadata=load('ModOptions')
updated=metadata.get('lastUpdated','')
valid_date=isinstance(updated,str) and (updated=='' or bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',updated)))
if valid_date and updated:
 try:__import__('datetime').datetime.strptime(updated,'%Y-%m-%dT%H:%M:%SZ')
 except ValueError:valid_date=False
check(valid_date,'ModOptions.lastUpdated must be empty or an ISO UTC timestamp for the mod-manager UI')
U=index('Units');B=index('Buildings');P=index('UnitPromotions');R=index('TileResources');I=index('TileImprovements');N=index('Nations');E=index('Events');V=index('VictoryTypes');C=index('CityStateTypes');ER=index('Eras')
T={t['name']:t for c in load('Techs') for t in c['techs']};PL={p['name']:p for b in load('Policies') for p in b['policies']}
check([c['columnNumber'] for c in load('Techs')]==sorted(c['columnNumber'] for c in load('Techs')),'technology columns are serialized in order')
check(len(T)==79,'79 technologies');check(len(ER)==6,'six eras');check(len(U)==127,'127 unit objects');check(len(B)==128,'128 building objects');check(len(P)==89,'89 promotion/status definitions');check(len(C)==24,'24 named city-state configurations');check(len(E)==15,'12 exploration encounters, 2 rituals and 1 internal medical resolver')
for group,target in [('techs',T),('units',U),('unique_units',U),('heroes',U),('parts',U),('buildings',B),('unique_buildings',B),('wonders',B),('religious_buildings',B),('resources',R),('promotions',P),('monsters',U),('civilians',U),('city_states',N)]:
 check(set(D[group])<=set(target),group+' ID coverage')
for k,t in T.items():
 for p in t['prerequisites']:check(p in T,k+' unknown tech prerequisite '+p)
seen=set();active=set()
def visit(k):
 check(k not in active,'technology cycle '+k)
 if k in active or k in seen:return
 active.add(k)
 for p in T[k]['prerequisites']:visit(p)
 active.remove(k);seen.add(k)
for k in T:visit(k)
for k,u in U.items():
 for field,table in [('requiredTech',T),('obsoleteTech',T),('upgradesTo',U),('replaces',U),('uniqueTo',N)]:
  if field in u:check(u[field] in table,k+' invalid '+field)
 for p in u.get('promotions',[]):check(p in P,k+' invalid promotion')
check([k for k,u in U.items() if 'Starting tech' in u.get('uniques',[])]==[],'no misplaced starting-tech unit')
check([k for k,t in T.items() if 'Starting tech' in t['uniques']]==[],'no universally granted starting technology')
for era in ER.values():
 check(era['startingSettlerUnit']=='C01' and era['startingMilitaryUnit']==D['era_start_rules'][era['name']]['military'],'starting unit mapping')
check(set(V)=={'Scientific','Cultural','Domination','Diplomatic','Time'},'five native victories')
check(V['Scientific']['requiredSpaceshipParts']==['S01','S01','S01','S02','S03','S04'],'scientific part quantities')
check(V['Cultural']['milestones']==['Complete [5] Policy branches','Build [J02]'],'cultural endgame closure')
check('in [Capital] cities' in ' '.join(B['J01']['uniques']),'scientific project in capital')
check('Completed Policy branches' in ' '.join(B['J02']['uniques']),'culture project branch gate')
check('Enables construction of Spaceship parts' in B['J01']['uniques'],'parts enabled by project')
for k in ['K13','K14']:
 check(k not in B and k in U,k+' is a repeatable unit, not a national wonder')
 check('Limited to [1] per Civilization' in U[k]['uniques'],k+' existing unit limit')
 check('Uncapturable' in U[k]['uniques'] and 'Cannot be purchased' in U[k]['uniques'],k+' acquisition restrictions')
for event,state,tech in [('E31','R25','D01-T102'),('E32','R26','D01-T24')]:
 check(E[event]['presentation']=='None',event+' has immediate non-popup execution')
 for speed,turns in [('Quick',7),('Standard',10),('Epic',15),('Marathon',30)]:
  choices=[c for c in E[event]['choices'] if f'on [{speed}] game speed' in ' '.join(c['uniques'])]
  check(len(choices)==1,event+' exactly one '+speed+' choice')
  c=choices[0];check(f'Provides [1] [{state}] <for [{turns}] turns>' in c['uniques'],event+' state duration')
  check(sum(f'<for [{turns}] turns>' in u for u in c['uniques'])==2,event+' matching state/effect durations')
  availability=c['uniques'][0];check(availability.startswith('Only available') and f'without [{state}]' in availability and tech in availability,event+' entry gates outside timed uniques')
for k in ['R25','R26']:
 check(not R[k]['terrainsCanBeFoundOn'] and not any('Stockpiled' in u for u in R[k]['uniques']),k+' is temporary supply, not stockpile')
for k in ['U36','U38','U40']:
 check(any('P104' in u and '[2] turn(s)' in u and 'for all movement' in u and 'for units without [P104]' in u for u in U[k]['uniques']),k+' crystal ward action')
for k in ['U77','U78']:
 check(any('[5] tile radius' in u and '[2] times' in u for u in U[k]['uniques']),k+' exploration charges')
for a,b in [('B76','B77'),('B77','B76')]:
 check(f'Only available <in cities without a [{b}]>' in B[a]['uniques'] and 'Unsellable' in B[a]['uniques'] and 'Destroyed when the city is captured' in B[a]['uniques'],a+' specialization mutual exclusion')
for a,b in [(21,70),(23,68),(48,69),(45,63),(52,65),(55,64),(58,66),(61,67),(74,75),(78,79),(82,83),(86,87),(90,91),(94,95),(98,99),(102,103)]:
 for x,y in [(a,b),(b,a)]:
  px=f'P{x:02}';py=f'P{y:02}';check(f'Only available <for units without [{py}]>' in P[px]['uniques'],px+' excludes '+py)
for k in ['P31','P33','P34','P36','P37','P38','P39','P40','P47','P71','P104']:
 check(P[k]['unitTypes']==[],k+' cannot be purchased as a normal promotion')
for k in ['P33','P43','P47']:
 for role in ['幽魂','英雄幽魂']:check(f'Can see invisible [{role}] units' in P[k]['uniques'],k+' detects '+role)
check('Unbuildable' not in I['Remove Forest']['uniques'],'workers can remove forests')
check(I['Railroad']['techRequired']=='D01-T36','runic road native connection gate')
check(not {'R22','R23','R24','R34'}&R.keys() and not {'I25','I26','I27','I34'}&I.keys(),'retired deposits and dedicated improvements absent')
for k in D['monsters']:check('Only available <for [Barbarians] Civilizations>' in U[k]['uniques'],k+' cannot be built by nations')
for k in list(D['units'])+list(D['unique_units']):check('Never appears as a Barbarian unit' in U[k]['uniques'],k+' excluded from hostile pool')
for k,r in D['city_states'].items():
 check(N[k]['cityStateType']==r[2]+'-'+k,k+' named pact mapping')
 check(len(C[r[2]+'-'+k]['allyBonusUniques'])>0,k+' ally effects')
for branch in load('Policies'):
 check(len(branch['policies'])==6,branch['name']+' has five members plus completion')
 check(branch['policies'][-1]['name']==branch['name']+' Complete',branch['name']+' native completion suffix')
check('requiredTech' not in U['C01'],'settler production is independent of research')
check({t['cost'] for t in T.values() if not t['prerequisites']}=={35},'opening roots share the same research price')
check('requiredTech' not in U['C02'] and 'requiredTech' not in U['U63'],'opening worker and scout remain available')
check(B['B83']['requiredTech']=='D01-T53' and I['I36']['techRequired']=='D01-T04','former introduction unlocks have live research homes')
check(R['R03']['revealedBy']=='D01-T04' and set(R['R03']['improvedBy'])=={'I30','Mine'},'crystals do not force the elemental school')
check(len(R)==30 and len(I)==35,'28 map resources plus 2 states, 31 designed improvements plus 4 system actions')
check(all(R[k]['uniques'] and R[k]['improvedBy'] for k in D['resource_rules']),'every map resource has generation and connection rules')
# Pricing follows actual research layers; arbitrary per-object premiums need explicit evidence.
for c in load('Techs'):
 check(len({t['cost'] for t in c['techs']})==1,'uniform cost within each research column')
 check(all(t['cost']==c['techCost'] for t in c['techs']),'native column default equals actual prices')
def cost_depth(k):
 ps=[p for p in T[k]['prerequisites'] if D['eras'][p]==D['eras'][k]]
 return 0 if not ps else 1+max(cost_depth(p) for p in ps)
def research_closure(k):return {k}|set().union(*(research_closure(p) for p in T[k]['prerequisites']))
for k,t in T.items():
 expected=D['research_cost_rules']['tiers'][str(D['eras'][k])][str(cost_depth(k))]
 check(t['cost']==expected,k+' follows documented era/role pricing')
 if D['eras'][k]>1:check(D['eras'][k]-1 in {D['eras'][p] for p in research_closure(k)},k+' does not bypass an entire research era')
for k in ['D01-T53','D01-T98','D01-T99','D01-T54']:
 check(T[k]['cost']==200,k+' equal school-entry price')
 check(sum(T[p]['cost'] for p in research_closure(k))==290,k+' school-entry path includes useful common knowledge')
check(R['R18']['revealedBy']=='D01-T64','mental research resource does not force elemental studies')
# Review regressions: opening access, optional branches, real city choices, and source sync.
check('requiredTech' not in B['B04'],'monuments are an opening production option')
check(T['D01-T15']['prerequisites']==['D01-T08'],'steel has no mounted or civic tax')
check('D01-T23' not in T['D01-T33']['prerequisites'],'infantry coordination does not require cavalry')
check('D01-T60' not in T['D01-T101']['prerequisites'],'mental survey does not require garrison doctrine')
check('D01-T60' not in T['D01-T71']['prerequisites'],'civil engineering is independent of garrisons')
for a in ['B76','B77','B81','B82']:
 for b in ['B76','B77','B81','B82']:
  if a!=b:check(f'Only available <in cities without a [{b}]>' in B[a]['uniques'],a+' specialization excludes '+b)
check(I['I28']['techRequired']=='D01-T112','forest stewardship is a midgame choice')
check(I['I29']['gold']==2 and 'Cannot be built on [Hill] tiles' in I['I29']['uniques'] and 'Cannot be built on [resource] tiles' in I['I29']['uniques'],'resource-free flatland commerce alternative')
check(sum('I29' in u for t in T.values() for u in t['uniques'])==0,'trade-post maturity is not double-counted')
check('[+1 Science] per [3] population [in all cities] <in cities with a [B03]>' in N['N11']['uniques'],'lich scholarship rewards population rather than a duplicated library bonus')
# Branch entry and meaningful hybrid gates are explicit regression requirements.
check('D01-T12' not in T,'standalone magic introduction is retired')
check({k for k,t in T.items() if not t['prerequisites']}=={'D01-T01','D01-T02','D01-T03','D01-T04','D01-T07'},'five shared opening foundations including independent navigation')
for k,parent in [('D01-T53','D01-T05'),('D01-T98','D01-T42'),('D01-T99','D01-T06'),('D01-T54','D01-T41')]:check(T[k]['prerequisites']==[parent],k+' grows from practical foundation')
check(T['D01-T13']['prerequisites']==['D01-T07','D01-T06'],'shipbuilding combines navigation and practical crafts')
check(T['D01-T20']['prerequisites']==['D01-T13','D01-T16'],'naval weapons combine ships and mechanisms')
check(T['D01-T24']['prerequisites']==['D01-T114'] and {'D01-T99','D01-T16'}<=research_closure('D01-T114'),'runecraft follows substantive elemental and mechanical application')
check(T['D01-T31']['prerequisites']==['D01-T27','D01-T83'],'life harmony retains medical knowledge')

check('[+1 Science] from all [B05] buildings' in T['D01-T62']['uniques'],'theology owns altar scholarship')
for k,r in D['techs'].items():check(T[k]['prerequisites']==re.findall(r'D01-T\d+',r[4]),k+' prerequisites match source')
for k,r in D['buildings'].items():check(B[k].get('requiredTech','开局')==r[2],k+' unlock matches source')
for k,r in D['natural_wonders'].items():check(next(x for x in load('Terrains') if x['name']==k)['turnsInto']==r[4],k+' base terrain matches source')
for lang in ['English','Simplified_Chinese']:

 lines=(J/'translations'/(lang+'.properties')).read_text().splitlines();table={}
 for line in lines:
  if line.startswith('#') or not line.strip():continue
  k,v=line.split(' = ',1);check(k not in table,lang+' duplicate translation '+k);check(bool(v.strip()),lang+' empty translation '+k);table[k]=v
 for group in [T,U,B,P,R,E]:
  for k in group:
   check(k in table,lang+' missing '+k)
   check(table.get(k)!=k,lang+' raw ID '+k)
 for k in set(T)|set(U)|set(B)|set(P)|set(R)|set(E):
  if lang=='English':check(not re.search('[\u4e00-\u9fff]',table.get(k,'')),'Chinese leaks into English '+k)
 for ev in E.values():
  for c in ev['choices']:check(c['text'] in table,lang+' missing event choice '+c['text'])
for n in ['Units','Buildings','UnitPromotions','TileImprovements','TileResources','Nations']:
 for o in load(n):check(len(o.get('uniques',[]))==len(set(o.get('uniques',[]))),n+' duplicate unique '+o['name'])
for p in J.glob('*.json'):

 raw=p.read_text();check(' OR ' not in raw,p.name+' unsupported OR filter');check('non-术士' not in raw,p.name+' invalid negation')
report=dict(ok=not errors,checks=checks,errors=errors,counts=dict(technologies=len(T),units=len(U),buildings=len(B),promotions=len(P),events=len(E),city_state_pacts=len(C)))
print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
