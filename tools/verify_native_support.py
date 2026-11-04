#!/usr/bin/env python3
"""Native support contracts only; no game, map or turn simulation."""
from pathlib import Path
import json,re,sys,subprocess
M=Path(__file__).resolve().parents[1];D=json.loads((M/'design/设计数据.json').read_text());load=lambda n:json.loads((M/'jsons'/f'{n}.json').read_text());ix=lambda n:{x['name']:x for x in load(n)};errors=[];checks=0

def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
G=load('GlobalUniques');E=ix('Events');P=ix('UnitPromotions');U=ix('Units');V=ix('VictoryTypes');tag=D['unit_support_rules']['medic_end_turn']['tag']
check(len(G.get('unitUniques',[]))==1 and 'Triggers a [E33] event'in G['unitUniques'][0],'Single receiver-driven medical event trigger')
for s in ['upon ending a turn in a [Land] tile','when below [100] HP','when adjacent to a [{医护} {non-[Embarked]}] unit']:check(s in G['unitUniques'][0],'Trigger guard: '+s)
check(E['E33']['presentation']=='None'and len(E['E33']['choices'])==1,'No dialog and no AI choice divergence')
us=E['E33']['choices'][0]['uniques'];expected=['[This Unit] gains the [P109] status for [1] turn(s)','[This Unit] heals [5] HP <for every [[{医护} {FC medic near active patient} {non-[P109]} {non-[Embarked]}] Units]>','[This Unit] loses the [P109] status']
check(us==expected,'Ordered marker, local-count healing, immediate cleanup')
check(P['P109']['unitTypes']==[] and not P['P109']['prerequisites'],'Internal status is not an XP promotion')
check(tag in P['P109']['uniques']and 'Will not be displayed in Civilopedia'in P['P109']['uniques'],'Filter registry marker hidden in encyclopedia')
for k in ['U41','U43','U45']:
 check(tag+' <when adjacent to a [P109] unit> <hidden from users>'in U[k]['uniques'],k+' provider tag evaluated relative to active patient')
 check(not any(x.startswith('All adjacent units heal')for x in U[k]['uniques']),k+' no second ordinary rest aura')
check({o['name']for o in U.values()if any(u.startswith(tag)for u in o['uniques'])}=={'U41','U43','U45'},'Only ordinary medics provide this tag')
check(not any('for every [[医护] Units]'in x for x in us),'Not a global empire medic-count multiplier')
check(V['Scientific']['requiredSpaceshipParts']==['S01','S01','S01','S02','S03','S04'],'Internal scientific victory and six components preserved')
check(V['Scientific']['milestones']==['Build [J01]','Add all [Origin Apparatus parts] in capital'],'Victory milestone semantics unchanged')
check(len(V['Scientific'].get('civilopediaText',[]))==3,'Victory encyclopedia has explanations')
check(V['Scientific']['victoryString']=='Magic victory won','Fantasy victory conclusion')
for lang in ['English','Simplified_Chinese']:
 tr=dict(l.split(' = ',1)for l in(M/'jsons/translations'/f'{lang}.properties').read_text().splitlines()if ' = 'in l)
 check(tr['Scientific']==('魔法'if lang=='Simplified_Chinese'else'Magic'),lang+' victory name')
 check('本源升华'not in '\n'.join(tr.values()),lang+' no requested subtitle')
 check('not stack'not in tr['Field medicine']and '不叠加'not in tr['Field medicine'],lang+' medic stacking description')
 for k in ['Magic victory overview','Magic victory assembly','Magic victory access','Magic victory won']:check(k in tr and len(tr[k])>20,lang+' explanation '+k)
 key=next(k for k in tr if k.startswith('There are four ways to win'))
 check(('五种'in tr[key]if lang=='Simplified_Chinese'else'five victory types'in tr[key]),lang+' generic victory tutorial updated')
 print_name=tr['Magic victory assembly'];check((all(x in print_name for x in ['星位矩阵','稳定核心','物质校准仪'])if lang=='Simplified_Chinese'else all(x in print_name for x in ['Stellar Matrix','Stabilization Core','Material Calibrator'])),lang+' actual component names')
report=json.loads(subprocess.run([sys.executable,str(M/'tools/audit_gift_pool.py')],capture_output=True,text=True,check=True).stdout);r=report['per_starting_era']['1'];check(r['eight_major_selections']==495 and r['empty_selections']==0 and r['minimum_pool']==3 and r['maximum_pool']==14,'Default era-I eight-major pool statically nonempty for every roster')
check(r['all_twelve_pool']==0,'Full twelve-major roster has no unused major pool')
check(len(ix('Nations'))==38,'No dummy major civilizations added')
print(json.dumps({'ok':not errors,'scope':'Static structure and native source contracts only. Clinical timing and games untested.','checks':checks,'errors':errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
