#!/usr/bin/env python3
"""Verify hero promotion isolation and reachability without a game or map."""
from pathlib import Path
import json,re,sys
M=Path(__file__).resolve().parents[1];load=lambda n:json.loads((M/'jsons'/f'{n}.json').read_text());D=json.loads((M/'design/设计数据.json').read_text());P={p['name']:p for p in load('UnitPromotions')};U={u['name']:u for u in load('Units')};UT={t['name']:t for t in load('UnitTypes')};errors=[];checks=0
removed={f'P{i:02}'for i in [50,53,56,59,72,76,80,84,88,92,96,100]}
def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
check(not (removed&set(P)),'No no-effect personal initial promotions')
check(len({U[h]['unitType']for h in D['heroes']})==12,'Every hero has a separate promotion type')
for h,c in D['hero_promotion_rules'].items():
 u=U[h];candidates={k for k,p in P.items()if u['unitType']in p['unitTypes']};check(candidates==set(c['promotions']),h+' has exactly its intended ability tree')
 check(not u['promotions'],h+' no free player-facing identity promotions')
 check(D['hero_roles'][h]+' <hidden from users>'in u['uniques'],h+' keeps original tactical role')
 check(('P71 <hidden from users>'in u['uniques'])==(int(h[1:])>=5),h+' visitor identity only on visitors')
 check(UT[u['unitType']]['movementType']==('Water'if h=='H09'else'Land'),h+' original movement domain')
 check(not candidates&{f'P{i:02}'for i in range(1,41)},h+' no ordinary army promotion choices')
 reached=set();changed=True
 while changed:
  before=len(reached)
  for k in candidates:
   req=P[k]['prerequisites']
   if not req or any(r in reached for r in req):reached.add(k)
  changed=len(reached)!=before
 check(reached==candidates,h+' all abilities reachable without ordinary tactical purchases, ignoring technology timing and mutually exclusive choices')
 for k in candidates:
  check(P[k]['unitTypes'][0]==u['unitType'],h+':'+k+' listed in the hero encyclopedia promotion category')
  check(all(r in candidates or r in c.get('legacyPromotions',{}).values() for r in P[k]['prerequisites']),h+':'+k+' no invisible foreign-tree prerequisite')
  check(not removed&set(re.findall(r'P\d+',' '.join(P[k]['uniques']))),h+':'+k+' no removed identity condition')
check(all('Hero <hidden from users>'in U[h]['uniques']for h in D['heroes']),'All heroes keep exploration access')
check('for [Hero] units'in next(r for r in load('Ruins')if r['name']=='RU23')['uniques'][0]or any('for [Hero] units'in x for x in next(r for r in load('Ruins')if r['name']=='RU23')['uniques']),'Hero-only exploration eligibility updated')
for lang in ['English','Simplified_Chinese']:
 t=(M/'jsons/translations'/f'{lang}.properties').read_text();check('传奇'not in t,lang+' uses hero terminology');check('Legendary Creatures'not in t,lang+' no old type name')
print(json.dumps({'ok':not errors,'checks':checks,'scope':'Static promotion candidate and reachability contracts only; no gameplay or UI rendering test.','errors':errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
