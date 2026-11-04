#!/usr/bin/env python3
"""Regressions for the reported player-facing rules. Static checks only."""
from pathlib import Path
import json,re,sys
M=Path(__file__).resolve().parents[1];D=json.loads((M/'design/设计数据.json').read_text());load=lambda n:json.loads((M/'jsons'/f'{n}.json').read_text());ix=lambda n:{o['name']:o for o in load(n)};U=ix('Units');I=ix('TileImprovements');R=ix('TileResources');E=ix('Events');C=ix('CityStateTypes');T={t['name']:t for c in load('Techs')for t in c['techs']};errors=[];checks=0

def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
check(not T['D01-T07']['prerequisites']and T['D01-T07']['cost']==35,'Independent coastal navigation opening')
worker=next(u for u in U['C02']['uniques'] if u.startswith('Can build [non-['))
allowed=set(re.findall(r'\{non-\[([^\]]+)\]\}',worker))
expected={v[2] for k,v in D['improvements'].items() if k not in ['I06','I15','I16','I17','I18','I19','I20','I21','I22']}
check(allowed==expected and not {D['improvements'][k][2] for k in ['I15','I16','I17','I18','I19','I20']} & allowed,'Worker explicit ordinary-improvement scope excludes great improvements and fishing boats, even for old queued orders')
for k in ['I15','I16','I17','I18','I19','I20']:
 o=I[D['improvements'][k][2]];check(o['turnsToBuild']==-1,k+' instant creation must not be worker buildable');check('Will not be replaced by automated units'in o['uniques'],k+' automatic replacement blocked');check(len(D['improvements'][k][1])==2,k+' two-character Chinese name')
check(not {'树人','战兽'}&ix('UnitTypes').keys(),'Species-only tree and duplicate beast categories removed')
for k in ['UX06','UX30','M05']:check(U[k]['unitType']=='步兵' and '[+20]% Strength <when fighting in [Forest] tiles>'in U[k]['uniques'],k+' preserves its own forest trait')
for k in ['U58','U60','UX19']:check(U[k]['unitType']=='野兽',k+' Beast type')
check(len(D['resource_rules'])==28 and len(R)==30 and len(I)==35,'Resource/improvement counts after retirement')
for k in ['R22','R23','R24','R34','I25','I26','I27','I34']:check(k not in R and k not in I,'Retired content remains '+k)
for f in (M/'jsons').rglob('*.json'):
 if f.name=='FantasyHex.json':continue
 check(not re.search(r'(?<![A-Z0-9])(?:R22|R23|R24|R34|I25|I26|I27|I34)(?!\d)',f.read_text()),f.name+' retains a deleted object reference')
check(not any('Nuclear weapon of Strength'in u or 'Enables nuclear weapon'in u or 'when nuclear weapons are'in u for n in ['Units','Buildings','Terrains','GlobalUniques']for o in (load(n) if isinstance(load(n),list) else [load(n)])for u in o.get('uniques',[])),'No nuclear weapons, unlocks or option-dependent content')
spy='Every major Civilization gains a spy once a civilization enters this era'
for era in load('Eras'):check((spy in era['uniques'])==(era['name']in ['III','IV','V','VI']),era['name']+' spy era policy')
check(len({r['base']for r in D['city_state_rules'].values()})==8,'Eight city-state types')
check(len(D['city_state_pacts'])==24,'Every city-state has its own pact')
for typ in ['Scientific','Cultured','Maritime','Industrial','Mercantile','Happiness','Religious','Militaristic']:
 check(sum(r['base']==typ for r in D['city_state_rules'].values())>=2,'At least two city-states of '+typ)
for k,r in D['city_state_rules'].items():
 native=C[r['base']+'-'+k]
 text='\n'.join(native['friendBonusUniques']);stats=set(re.findall(r'(?:Science|Culture|Food|Production|Gold|Happiness|Faith)',text));expected={'Scientific':{'Science'},'Cultured':{'Culture'},'Maritime':{'Food'},'Industrial':{'Production'},'Mercantile':{'Gold'},'Happiness':{'Happiness'},'Religious':{'Faith'},'Militaristic':set()}[r['base']];check(stats==expected,k+' friendship gives only its base yield')
# Each speed gets the same decisions; internal availability is invisible in RenderEvent.
for k,o in E.items():
 if k in ['E31','E32','E33']:continue
 check(bool(o.get('civilopediaText')),k+' missing event body');expected=[k+'-'+chr(65+j)for j in range(len(D['events'][k][1]))]
 for speed in ['Quick','Standard','Epic','Marathon']:
  matching=[c for c in o['choices']if c['name'].endswith('-Any')or c['name'].endswith('-'+speed)];check([c['text']for c in matching]==expected,k+' different choices at '+speed)
 for c in o['choices']:
  for u in c['uniques']:
   if re.match(r'Gain \[-\d+\] \[Gold\]',u):check('<hidden from users>'in u,k+' raw negative gold should be explained as a payment')
   if u.startswith('Only available'):check('<hidden from users>'in u,k+' exposes internal availability')
for lang in ['English','Simplified_Chinese']:
 text=dict(l.split(' = ',1)for l in(M/'jsons/translations'/f'{lang}.properties').read_text().splitlines()if ' = 'in l)
 if lang=='Simplified_Chinese':check(text['R01']=='马','Chinese horse name')
 else:check(text['野兽']=='Beast','English Beast name')
 for o in E.values():
  for p in o.get('civilopediaText',[]):check(len(text.get(p['text'],''))>2 and text.get(p['text'])!=p['text'],'Missing readable event prose '+p['text'])
 for r in load('Ruins'):
  check(r['notification']in text and len(text[r['notification']])>10,r['name']+' missing discovery explanation')
  if re.search(r'^Gain \[',D['ruins'][r['name']][4]):check('[]'in r['notification'],r['name']+' must show actual numeric reward')
print(json.dumps({'ok':not errors,'scope':'Static invariants tied to reported problems; no game executed.','checks':checks,'errors':errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
