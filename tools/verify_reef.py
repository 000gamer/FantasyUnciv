#!/usr/bin/env python3
"""Static reef-colonization contracts. Does not execute terrain changes or create a map."""
from pathlib import Path
import json,re,sys
M=Path(__file__).resolve().parents[1];load=lambda n:json.loads((M/'jsons'/f'{n}.json').read_text());ix=lambda n:{x['name']:x for x in load(n)};U=ix('Units');T=ix('Terrains');N=ix('Nations');types=ix('UnitTypes');tech={x['name']:x for col in load('Techs')for x in col['techs']};D=json.loads((M/'design/设计数据.json').read_text());cfg=json.loads((M/'design/造礁拓殖.json').read_text());errors=[];checks=0

def ck(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
u=U['C12'];a=[x for x in u['uniques']if x.startswith('Turn this tile into')];ck(len(a)==1,'Exactly one terrain action on reef settler');a=a[0]
ck(u['uniqueTo']=='N04'and not u.get('replaces'),'N04 additional unit, does not replace early settler')
ck(u['requiredTech']=='D01-T19'and not U['C01'].get('requiredTech'),'Era III unlock; normal settler available at start')
ck(u['cost']==180 and u['movement']==3,'Production and movement match advertised unit')
ck(u['unitType']=='Civilian'and types[u['unitType']]['movementType']=='Land','Land civilian remains valid on newly raised land')
for s in ['Founds a new city <by consuming this unit>','May travel on Water tiles without embarking','Uncapturable','Requires at least [2] population','Only available <in [Coastal] cities>']:ck(s in u['uniques'],'Native capability: '+s)
ck(u.get('upgradesTo')is None and not any('Can transform to'in x for x in u['uniques']),'No upgrade/transform route to refresh the once-per-unit charge')
for s in ['{Coast}','{Featureless}','{Unowned}','{unimproved}','{non-[pillaged]}','{non-[resource]}','{non-[Natural Wonder]}','<for [N04] Civilizations>','<[1] times>','<for [0] movement>','<for [non-[FC Reef near city]] units>']:ck(s in a,'Terrain action guard or cost: '+s)
ck('for all movement'not in a and 'by consuming this unit'not in a,'Reef action leaves unit and movement for same-turn founding')
ck('not adjacent to [Land]'not in a and not any('neighboring [Land]'in x for x in u['uniques']),'Adjoining land is allowed')
ck('FC Reef near city <within [3] tiles of a [City center]> <hidden from users>'in u['uniques'],'Dynamic three-tile city buffer')
ck('FC Reef near city'in types and not any(x['unitType']=='FC Reef near city'for x in U.values()),'Native filter key registered without a playable marker type')
ck(T['Reef Island']['type']=='Land'and "Doesn't generate naturally"in T['Reef Island']['uniques'],'Permanent Land terrain, not natural map generation')
ck(T['Reef Island']['food']==T['Reef Island']['production']==1,'Reef base yields')
ck(not any(x.startswith('Turn this tile into')for x in U['C01']['uniques']),'Ordinary settlers cannot raise reefs')
ck(all(not x.get('revealedBy')for x in load('TileResources')if'Coast'in x.get('terrainsCanBeFoundOn',[])),'Every native Coast resource is visible and protected by the resource filter')
ck(D['reef_colonization']['action']==cfg['rules']['action']==a,'Canonical reef action and generated unit agree')
ck(any('FC Reef colonization'in x for x in N['N04']['uniques']),'Nation encyclopedia advertises the feature')
for lang in ['English','Simplified_Chinese']:
 tr=dict(l.split(' = ',1)for l in(M/'jsons/translations'/f'{lang}.properties').read_text().splitlines()if' = 'in l)
 ck(tr['C12']==('Reef Settler'if lang=='English'else'造礁开拓者'),lang+' unit display name')
 ck('same turn'in tr['FC Reef workflow']if lang=='English'else'同一回合'in tr['FC Reef workflow'],lang+' same-turn workflow explained')
 ck('Ocean Voyaging'not in tr['FC Reef colonization'],lang+' research label matches actual name')
for p in [M/'README.md',M/'README.zh-CN.md']:
 s=p.read_text();ck('1.0'in s,p.name+' current version')
 ck('Unciv'in s and'FantasyHex'in s and('Contributions'in s or'欢迎大家贡献'in s),p.name+' source credit and contributions')
 ck('Original artwork is still to be developed'in s or'原创贴图还待开发'in s,p.name+' native placeholder art disclosed')
for p in [M/'README.md',M/'README.zh-CN.md']:
 for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',p.read_text()):
  if target.startswith(('http:','https:','#','mailto:')):continue
  ck((p.parent/target.split('#')[0]).exists(),str(p.relative_to(M))+' link '+target)
print(json.dumps({'ok':not errors,'checks':checks,'scope':'Rule structure, native source contracts, translation and documentation links; no gameplay or map created.','errors':errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
