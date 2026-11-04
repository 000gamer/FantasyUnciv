#!/usr/bin/env python3
"""Static safeguards for resource rule-list construction; does not generate maps."""
from pathlib import Path
import json,re,sys
M=Path(__file__).resolve().parents[1];D=json.loads((M/'design/设计数据.json').read_text());load=lambda n:json.loads((M/'jsons'/f'{n}.json').read_text());ix=lambda n:{x['name']:x for x in load(n)};R=ix('TileResources');E=ix('Events');N=ix('Nations');RU=ix('Ruins');errors=[];checks=0

def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
for k,r in D['resource_rules'].items():
 for u in R[k]['uniques']:
  if u.startswith(('Generated on every','Generated with weight','Minor deposits generated'))and R[k]['resourceType']!='Luxury':check(' <in ['in u,k+' no unconditional bonus/strategic weighting')
check('Generated on every [12] tiles <in [{Featureless} {Coast}] tiles>'in R['R07']['uniques'],'Fish count uses coastal list at frequency12')
base={x['name']:x for x in json.loads((M/'design/base-4.22.16/TileResources.json').read_text())}
check('Generated on every [10] tiles <in [{Featureless} {Coast}] tiles>'in base['Fish']['uniques'],'Pinned native coastal fish denominator10')
check(R['R33']['terrainsCanBeFoundOn']==base['Whales']['terrainsCanBeFoundOn']==['Coast'],'Whales use native coastal eligibility')
for k in ['R15','R33']:check(not any(u.startswith('Generated on every')for u in R[k]['uniques']),k+' luxury regional generation is not a bonus frequency')
for k in ['R02','R03','R04']:check(any(re.fullmatch(r'Generated with weight \[\d+\] <in \[Hill\] tiles>',u)for u in R[k]['uniques']),k+' matches native hill major-deposit rule text')
check('Generated with weight [32] <in [Hill] tiles>'in R['R03']['uniques'],'Crystal large hill weighting')
check('Minor deposits generated with weight [30] <in [Hill] tiles> <in tiles without [Jungle]>'in R['R03']['uniques'],'Crystal small hill weighting excludes jungle')
check(R['R03']['terrainsCanBeFoundOn']==['Hill','Tundra','Grassland'],'Crystal eligible land')
check(not any('Forest'in u and "Doesn't generate"in u for u in R['R03']['uniques']),'Crystal forested hills allowed')
check(R['R03']['minorDepositAmount']['default']==2 and R['R03']['majorDepositAmount']['default']==3,'Deposit supply unchanged')
check('Guaranteed with Strategic Balance resource option'in R['R03']['uniques'],'Crystal strategic balance participation')
check('RU07'not in RU and 'E13'not in E,'Travel workers and worker-choice event removed')
check('Gain [100] [Gold]'in RU['RU17']['uniques']and not any('event'in u for u in RU['RU17']['uniques']),'Inheritance chest directly grants gold')
check(not any('[C02]'in u for o in RU.values()for u in o['uniques']),'No ordinary worker spawned from ruins')
check(not any('[C02]'in u for o in E.values()for c in o['choices']for u in c['uniques']),'No ordinary worker spawned from event choices')
for k,r in D['city_state_rules'].items():
 if r['base']=='Militaristic':check(not N[k].get('civilopediaText'),k+' no long gift explanation')
check(len(E)==15 and sum(x.get('presentation')=='Alert'for x in E.values())==12 and len(RU)==27,'Current encounter counts')
for lang in ['English','Simplified_Chinese']:
 text=(M/'jsons/translations'/f'{lang}.properties').read_text();check('Military gift pool = 'not in text and 'Military gift conditions = 'not in text,lang+' removed gift explanation keys')
print(json.dumps({'ok':not errors,'scope':'Static JSON/source-derived constraints only; no map generation, gameplay or AI test.','checks':checks,'errors':errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
