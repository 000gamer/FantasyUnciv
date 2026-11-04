#!/usr/bin/env python3
"""Static checks for 0.9 rules and encyclopedia. Does not execute gameplay."""
from pathlib import Path
import json,re,hashlib,sys
M=Path(__file__).resolve().parents[1];D=json.loads((M/'design/设计数据.json').read_text());load=lambda n:json.loads((M/'jsons'/f'{n}.json').read_text());ix=lambda n:{x['name']:x for x in load(n)};U=ix('Units');B=ix('Buildings');P=ix('UnitPromotions');E=ix('Eras');I=ix('TileImprovements');T={x['name']:x for c in load('Techs')for x in c['techs']};N=ix('Nations');errors=[];checks=0

def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
for k,r in D['city_state_units'].items():
 o=U[k];b=U[r['base']];check(o['uniqueTo']==r['cityState']and o['replaces']==r['base'],k+' static CS ownership')
 check(r['cityState']in N and 'cityStateType'in N[r['cityState']],k+' actual city-state owner')
 for key in ['strength','rangedStrength','range','movement','cost','requiredTech','upgradesTo','obsoleteTech']:check(o.get(key)==b.get(key),k+' base '+key)
 check(all(x in o['uniques']for x in r['extraUniques']),k+' role distinction')
check(I['I36']['terrainsCanBeBuiltOn']==['Land'],'Circle passable land scope')
check('Must be next to [R03]'in I['I36']['uniques']and not any('Hill'in x for x in I['I36']['uniques']),'Circle adjacency on its tile, no hill ban')
for f in ['Forest','Jungle']:check('Does not need removal of ['+f+'] <hidden from users>'in I['I36']['uniques'],'Circle preserves '+f)
check(I['I36']['faith']==1 and '[+1 Science] <after discovering [D01-T17]>'in I['I36']['uniques'],'Circle yields kept')
check(sum('Triggers a [E33] event' in x for x in load('GlobalUniques').get('unitUniques',[]))==1,'Exactly one medical resolver trigger per recipient')
for k in ['U41','U43','U45']:
 check('Comment [Field medicine]'in U[k]['uniques'],'Medic concise support description '+k)
 check(not any(x.startswith('All adjacent units heal')for x in U[k]['uniques']),'No duplicate rest aura on ordinary medic '+k)
fall=ix('Terrains')['Fallout'];check(all(x in fall['uniques']for x in ["Doesn't generate naturally",'Will not be displayed in Civilopedia','Excluded from map editor']),'Fallout hidden compatibility only')
check('Can only start games from the starting era'not in load('ModOptions')['uniques'],'Era selector unlocked')
for era,o in E.items():
 r=D['era_start_rules'][era];check(o['startingMilitaryUnit']==r['military']and o['startingWorkerCount']==r['workers']and o['startingGold']==r['gold']and o['settlerPopulation']==r['population'],era+' configured start')
 u=U[r['military']];tech=u.get('requiredTech');check(not tech or D['eras'][tech]<E[era].get('eraNumber',list(E).index(era)+1),era+' start unit uses earlier tech')
for k,v in [('B51',3),('B33',5)]:check(B[k]['food']==v and not any('Food is carried over'in u for u in B[k]['uniques']),k+' direct Food yield, no carry-over rule')
for k in ['B52','B76','B77','B80']:
 for u in B[k]['uniques']:
  if u.startswith('All newly-trained'):
   p=re.search(r'receive the \[(P\d+)\]',u)[1];check(p in P and '<Civilopedia link [Promotion/'+p+']>'in u,k+' actual promotion link '+p)
for k in ['W05','W06','W12']:check(bool(B[k].get('greatPersonPoints')),k+' great person points')
for k in ['W01','W02','W03']:check(not B[k].get('greatPersonPoints'),k+' no great person points')
check(B['W01'].get('faith')==5 and B['W02'].get('food')==6,'Early wonder base yields comparable to native')
check('[+1] Movement <for [{Water} {Military}] units>'in B['W03']['uniques'],'Lighthouse naval movement')
check('[+15]% [Science] [in this city]'in B['W06']['uniques'],'Academy wonder city specialization')
check('[+1 Gold] from [Water] tiles [in this city]'in B['W07']['uniques'],'Harbor wonder local worked water economy')
for lang in ['English','Simplified_Chinese']:
 tr=dict(l.split(' = ',1)for l in(M/'jsons/translations'/f'{lang}.properties').read_text().splitlines()if ' = 'in l)
 check('+[relativeAmount]'not in tr['Gifts of Gold to City-States generate [relativeAmount]% more Influence'],lang+' influence avoids duplicate signs')
 check('Spaceship'not in tr['Enables construction of Spaceship parts']and '飞船'not in tr['Enables construction of Spaceship parts'],lang+' fantasy victory wording')
 if lang=='Simplified_Chinese':
  check('城市'not in tr['Must be next to [tileFilter]'],'Adjacency translation applies to both city and improvement')
  check('返还本次增长所需粮食'in tr['[amount]% Food is carried over after population increases [cityFilter]'],'Accurate food refund wording')
# User approved the second policy draft and removal of city-state-owned units.
from display_numbers import normalize_tree
check(load('Policies')==normalize_tree(D['policy_rules'],json.loads((M/'design/数值显示规则.json').read_text())),'Installed policies match authoritative reviewed rules')
check(not D['city_state_units'] and not any(k.startswith('CU') for k in U),'City-state unique units removed')
check(next(b for b in load('Policies') if b['name']=='PB03')['uniques']==['[+20]% Strength <for [{Land} {Military}] units> <vs [Barbarians] units>'],'Military opener retains +20% vs Barbarians')
print(json.dumps({'ok':not errors,'scope':'Static/source-derived assertions only. No game, map generation or AI test.','checks':checks,'errors':errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
