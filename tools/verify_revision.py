#!/usr/bin/env python3
"""Static regressions for the 0.7 player reports. Never starts a game."""
from pathlib import Path
import json,sys,re
from display_numbers import signed
M=Path(__file__).resolve().parents[1];D=json.loads((M/'design/设计数据.json').read_text());P=json.loads((M/'design/玩家体验文本.json').read_text());load=lambda n:json.loads((M/'jsons'/f'{n}.json').read_text());ix=lambda n:{x['name']:x for x in load(n)};I=ix('TileImprovements');U=ix('Units');B=ix('Buildings');C=ix('CityStateTypes');N=ix('Nations');T={t['name']:t for c in load('Techs')for t in c['techs']};E=ix('Events');cfg=json.loads((M/'design/数值显示规则.json').read_text());errors=[];checks=0

def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
nav={'D01-T07','D01-T13','D01-T19','D01-T20','D01-T32','D01-T95'}
for k,r in D['techs'].items():check((int(r[7].split('/')[1])<=2)==(k in nav),k+' naval top rows')
check(len(E)==15 and sum(x.get('presentation')=='Alert'for x in E.values())==12,'12 visible encounters and 2 rituals')
check(len(load('Ruins'))==27,'27 ruin rewards')
for k,r in D['events'].items():
 if k in ['E31','E32','E33']:continue
 check(r[0].startswith('RU'),k+' random ruin source')
 check(len(P['events'][k]['paragraphs'])==4 and len(E[k]['civilopediaText'])==4,k+' four separate paragraphs')
 for idx,label in enumerate(['地点：','人物：','起因：']):check(P['events'][k]['paragraphs'][idx]['zh'].startswith(label),k+' context '+label)
for k,o in T.items():check(not any(' event'in u for u in o.get('uniques',[])),k+' no research narrative event')
for k,p in D['city_state_pacts'].items():
 typ=D['city_state_rules'][k]['base']+'-'+k
 check(all(signed(u,cfg)in C[typ]['allyBonusUniques']for u in p['uniques']),k+' native ally pact')
 if D['city_state_rules'][k]['base']=='Militaristic':
  check(any('[20]'in u and 'Provides military units'in u for u in C[typ]['friendBonusUniques']),k+' military friend interval')
  check(any('[17]'in u and 'Provides military units'in u for u in C[typ]['allyBonusUniques']),k+' military ally interval')
  check(not N[k]['civilopediaText'],k+' no verbose military gift explanation')
 if D['city_state_rules'][k]['base']=='Industrial':
  for n in [2,3,4]:check(any(f'[+{n} Production] [in capital]'in u for u in C[typ]['friendBonusUniques']),k+' era production tier '+str(n))
check(all('<hidden from users>'in u for u in U['C02']['uniques']if u.startswith('Can build')),'Worker permission rules hidden')
check('Comment [Build tile improvements]'in U['C02']['uniques'],'Worker concise action label')
for k in D['wonders']:
 for rule in ['Cannot be purchased','Unsellable','Cannot be hurried']:
  check(any(u==rule+' <hidden from users>'for u in B[k]['uniques']),k+' hidden '+rule)
check('[+15]% Great Person generation [in this city]'in B['B47']['uniques'],'Garden positive sign')
for s in ['[1] Sight','[1] Movement','[1] Range']:check(signed(s,cfg).startswith('[+1]'),'Signed '+s)
for s in ['Reveal up to [All] [Water] within a [10] tile radius','Gain [140] [Culture]','[This Unit] takes [20] damage']:
 check(signed(s,cfg)==s,'Non-modifier counts preserved: '+s)
for k in ['I21','I22']:check('Unpillagable'in I[D['improvements'][k][2]]['uniques'],k+' native pillage protection')
check('Must be next to [R03]'in I['I36']['uniques'],'Circle adjacent crystal')
check(I['I36'].get('faith')==1 and '[+1 Science] <after discovering [D01-T17]>'in I['I36']['uniques'],'Circle keeps faith and Education science')
for n in ['Difficulties','Speeds']:
 base={x['name']:x for x in json.loads((M/'design/base-4.22.16'/f'{n}.json').read_text())}
 for o in load(n):
  for key,value in base[o['name']].items():
   if 'barbarian'in key.lower()or key=='clearBarbarianCampReward':check(o.get(key)==value,n+' '+o['name']+' native '+key)
check(not load('ModOptions').get('constants'),'No ModOptions constants overridden')
print(json.dumps({'ok':not errors,'scope':'Static invariants only; no game or AI behavior test.','checks':checks,'errors':errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
