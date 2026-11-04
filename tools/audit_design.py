#!/usr/bin/env python3
"""Compare canonical wiki data with actual native files. No engine or game execution.
Run after build.py. Reports exact fields checked; does not infer gameplay verification.
"""
from pathlib import Path
import json,re,sys
M=Path(__file__).resolve().parents[1];W=M.parents[2]/'wiki';D=json.loads((M/'design/设计数据.json').read_text());J=M/'jsons'
load=lambda n:json.loads((J/(n+'.json')).read_text())
index=lambda n:{o['name']:o for o in load(n)}
U=index('Units');B=index('Buildings');N=index('Nations');I=index('TileImprovements');R=index('TileResources');T={t['name']:t for c in load('Techs') for t in c['techs']}
errors=[];checks=0

def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
def same(o,field,v,k):check(o.get(field)==v,f'{k}.{field}: {o.get(field)!r} != {v!r}')
def nullable(o,field,v,k):same(o,field,None if v in ['无','开局'] else v,k)
check((M/'design/设计数据.json').read_bytes()==(W/'06-规则规格/设计数据.json').read_bytes(),'Wiki snapshot drift')
resources={v[1]:k for k,v in D['resources'].items()}
def supply(v):return {resources[z]:int(a) for z,a in re.findall(r'([^、，\s]+?)(\d+)(?:、|$)',v)}
def checksupply(o,s,k):
 expected=supply(s);found={m[2]:int(m[1]) for u in o.get('uniques',[]) if (m:=re.fullmatch(r'Consumes \[(\d+)\] \[(.+)\]',u))}
 if o.get('requiredResource'):found[o['requiredResource']]=found.get(o['requiredResource'],0)+1
 check(found==expected,k+' resource supply mismatch')
for group in ['units','unique_units']:
 for k,r in D[group].items():
  if group=='units':_,_,tech,role,melee,ranged,rng,mov,cost,res,up,_,fee,ob=r
  else:_,nation,_,replaces,tech,role,melee,ranged,rng,mov,cost,res,up,_,fee,ob=r
  o=U[k]
  for f,v in [('unitType',role),('strength',int(melee)),('rangedStrength',int(ranged)),('range',int(rng)),('movement',int(mov)),('cost',int(cost))]:same(o,f,v,k)
  for f,v in [('requiredTech',tech),('obsoleteTech',ob),('upgradesTo',up)]:nullable(o,f,v,k)
  checksupply(o,res,k)
  if group=='unique_units':same(o,'uniqueTo',nation,k);nullable(o,'replaces',replaces,k)
  if int(fee):check(f'[{int(fee):+d}]% maintenance costs' in o['uniques'],k+' maintenance weighting')
for k,r in D['heroes'].items():
 o=U[k]
 for f,v in [('unitType',r[3]),('strength',int(r[4])),('rangedStrength',int(r[5])),('range',int(r[6])),('movement',int(r[7]))]:same(o,f,v,k)
 checksupply(o,r[9],k);check('Unbuildable' in o['uniques'] and 'Cannot be purchased' in o['uniques'],k+' hero acquisition')
for group in ['buildings','unique_buildings','wonders']:
 for k,r in D[group].items():
  if group=='buildings':tech,cost,maint,cond,res=r[2:7]
  elif group=='unique_buildings':tech,cost,maint,cond=r[4:8];res='无'
  else:tech,cost,cond=r[2:5];maint='0';res='无'
  o=B[k];same(o,'cost',int(cost),k);same(o,'maintenance',int(maint),k);nullable(o,'requiredTech',tech,k);checksupply(o,res,k)
  if group=='unique_buildings':same(o,'uniqueTo',r[1],k);same(o,'replaces',r[3],k)
  for token in cond.split('；'):
   if m:=re.match(r'^(B\d+)',token):check(f'Only available <in cities with a [{m[1]}]>' in o['uniques'] or o.get('requiredBuilding')==m[1],k+' missing local prerequisite '+token)
   if m:=re.fullmatch(r'本城无(B\d+)',token):check(f'Only available <in cities without a [{m[1]}]>' in o['uniques'],k+' missing exclusion '+token)
for k,r in D['improvements'].items():
 o=I[r[2]]
 if r[3].startswith('D01-'):same(o,'techRequired',r[3],k)
 if r[4].isdigit():same(o,'turnsToBuild',int(r[4]),k)
for k,r in D['techs'].items():
 same(T[k],'cost',int(r[3]),k);same(T[k],'prerequisites',re.findall(r'D01-T\d+',r[4]),k)
 c,row=map(int,r[7].split('/'));column=next(c for c in load('Techs') if any(t['name']==k for t in c['techs']))
 same(T[k],'row',row,k);check(column['columnNumber']==c,k+' column drift');check(column['era']==['I','II','III','IV','V','VI'][D['eras'][k]-1],k+' era drift')
zh=dict(l.split(' = ',1) for l in (J/'translations/Simplified_Chinese.properties').read_text().splitlines() if ' = ' in l)
for group,target,nameidx in [('techs',T,1),('units',U,1),('unique_units',U,2),('buildings',B,1),('unique_buildings',B,2),('promotions',index('UnitPromotions'),1),('heroes',U,1),('resources',R,1),('nations',N,1),('natural_wonders',index('Terrains'),1)]:
 for k,r in D[group].items():check(k in target and zh.get(k)==r[nameidx],k+' canonical ID/name mismatch')
meta=json.loads((M/'design/metadata.json').read_text())
for k,v in meta['nations'].items():
 check(zh.get(N[k]['leaderName'])==v['leader'],k+' leader name drift')
 check([zh.get(x) for x in N[k]['cities']]==v['cities'],k+' city name drift')
# Resource generation/connection and actual baseline yields are checked against source.
stat_keys={'粮食':'food','生产':'production','金币':'gold','科研':'science','文化':'culture','信仰':'faith'}
def yields(v):return {stat_keys[b]:int(a) for a,b in re.findall(r'([+-]\d+)(粮食|生产|金币|科研|文化|信仰)',v)}
for k,rule in D['resource_rules'].items():
 r=D['resources'][k];o=R[k]
 same(o,'resourceType',{'战略':'Strategic','奖励':'Bonus','奢侈':'Luxury'}[r[2]],k)
 same(o,'terrainsCanBeFoundOn',rule['terrains'],k);same(o,'uniques',rule['uniques'],k)
 nullable(o,'revealedBy',r[3],k)
 expected=rule.get('improvedBy') or [next(v[2] for v in D['improvements'].values() if v[1]==r[5])]
 same(o,'improvedBy',expected,k)
 for f in stat_keys.values():check(o.get(f,0)==yields(r[8].split('；')[0]).get(f,0),k+' base yield '+f)
 expected=yields(r[8].split('；')[1]) if '；正确改良再' in r[8] else {}
 check(o.get('improvementStats',{})==expected,k+' improved yield mismatch')
for k,r in D['improvements'].items():
 for f in stat_keys.values():check(I[r[2]].get(f,0)==yields(r[5].split('；')[0]).get(f,0),k+' improvement base yield '+f)
check('requiredTech' not in U['C01'],'settler must be research-independent')
check(not any('Starting tech' in t['uniques'] for t in T.values()),'no global starting technology')
# Each ordinary endgame remains independent of the four-source gate.
def ancestors(k):return {k}|set().union(*(ancestors(p) for p in T[k]['prerequisites']))
closure_targets=[[94,86,91,89],[96],[92],[38],[95]]
closures=[]
for row,targets in zip(D['closure_summary'],closure_targets):
 acc=set().union(*(ancestors(f'D01-T{n:02}') for n in targets));result=[row[0],len(acc),sum(T[t]['cost'] for t in acc),'是' if acc&{'D01-T53','D01-T98','D01-T99','D01-T54'} else '否'];check(result==row,'closure summary mismatch '+row[0]);closures.append(result)
# Also follow mandatory city building chains. Technology-only closure can hide research costs.
def construction_techs(k,visited=None):
 visited=set() if visited is None else visited
 if k in visited:return set()
 visited.add(k);o=B.get(k,U.get(k,{}));acc=set()
 if o.get('requiredTech'):acc|=ancestors(o['requiredTech'])
 reqs=set(re.findall(r'Only available <in cities with a \[(B\d+)\]>', '\n'.join(o.get('uniques',[]))))
 if o.get('requiredBuilding'):reqs.add(o['requiredBuilding'])
 for q in reqs:acc|=construction_techs(q,visited)
 return acc
for target,own in [('D01-T31','D01-T98'),('D01-T93','D01-T54'),('D01-T91','D01-T99'),('D01-T103','D01-T53')]:
 check(ancestors(target)&{'D01-T53','D01-T98','D01-T99','D01-T54'}=={own},target+' forces another magic school')
construction_closures=[]
for label,targets in [('求真建设链',['J01','S01','S02','S03','S04']),('文化建设链',['J02']),('外交建设链',['W18'])]:
 acc=set().union(*(construction_techs(k) for k in targets))
 construction_closures.append([label,len(acc),sum(T[t]['cost'] for t in acc),sorted(acc)])
report={'ok':not errors,'scope':'Static field comparison only: IDs, translated names, technology/era/coordinates, unit values/resources/upgrades, building costs/prerequisites, improvements, leaders/cities, victory research closures. No game executed.','checks':checks,'errors':errors,'technology_edges':sum(len(t['prerequisites']) for t in T.values()),'max_layout_row':max(t['row'] for t in T.values()),'closure_summary':closures,'mandatory_construction_closures':construction_closures}
print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
