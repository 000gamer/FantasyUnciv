#!/usr/bin/env python3
"""Static checks for tutorial organization, concise descriptions and native placeholders."""
from pathlib import Path
import json,sys,re
M=Path(__file__).resolve().parents[1];L=lambda n:json.loads((M/'jsons'/f'{n}.json').read_text());ix=lambda n:{x['name']:x for x in L(n)};T=ix('Tutorials');P=ix('UnitPromotions');U=ix('Units');B=ix('Buildings');I=ix('TileImprovements');errors=[];checks=0

def ck(v,msg):
 global checks
 checks+=1
 if not v:errors.append(msg)
base=json.loads((M/'design/base-4.22.16/Tutorials.json').read_text())
for x in base:ck({k:v for k,v in T[x['name']].items()if k!='category'}=={k:v for k,v in x.items()if k!='category'},x['name']+' native tutorial contents preserved')
ck(T['FC Heroes']['category']==T['FC Mod introduction']['category']=='FantasyUnciv','Mod chapter contains intro and heroes')
ck(all(T[x['name']]['category']=='Unciv Tutorials'for x in base),'Native tutorials grouped after mod chapter')
for lang in ['Simplified_Chinese','English']:
 tr=dict(l.split(' = ',1)for l in(M/'jsons/translations'/f'{lang}.properties').read_text().splitlines()if' = 'in l)
 group=lambda s:((ord(s.lower()[0])<<16)+ord(s.lower()[1]))
 ck(group('FantasyUnciv')<group(tr['Unciv Tutorials']),lang+' native tutorial category formula puts FantasyUnciv first')
 ck(tr['FC Heroes']==('英雄'if lang=='Simplified_Chinese'else'Heroes'),lang+' short hero article title')
 text='\n'.join(tr.values());ck('不会免费完成整项科技'not in text and 'no technology is completed for free'not in text,lang+' lost calculations notification concise')
 if lang=='Simplified_Chinese':ck(tr['Remove Marsh']=='清除沼泽','Consistent marsh removal display')
ck(P['P111']['prerequisites']==['P110'],'Bridge promotion lists command exactly once')
for k in ['P110','P111']:ck(all('<hidden from users>'in s for s in P[k]['uniques']if s.startswith('Only available')),k+' internal compatibility restrictions hidden')
for old,new in [('P41','P110'),('P42','P111')]:
 ck(any(s.startswith('[This Unit] gains the ['+new+'] promotion')and'upon turn start'in s and f'with [{old}]'in s for s in U['H03']['uniques']),old+' -> '+new+' legacy free grant')
 ck(any(s.startswith('[This Unit] loses the ['+old+'] promotion')and f'with [{new}]'in s for s in U['H03']['uniques']),old+' removed only after replacement exists')
for k,food in [('B51',3),('B33',5)]:ck(B[k]['food']==food and not any('carried over'in x for x in B[k]['uniques']),k+' simple Food yield')
for k in ['W01','W02','W03']:ck(not B[k].get('greatPersonPoints')and not any('Great Person'in x for x in B[k]['uniques']),k+' no GP bonus')
for k,stat in [('Academy','science'),('Manufactory','production'),('Customs house','gold'),('Landmark','culture'),('Holy site','faith')]:ck(I[k][stat]==6,k+' baseline 6')
for f in ['Forest','Jungle']:ck('Does not need removal of ['+f+'] <hidden from users>'in I['I36']['uniques'],'Stone circle keeps '+f+' silently')
ck(len(L('Religions'))==8 and len(json.loads((M/'design/原版美术映射.json').read_text())['religion_sources'])==8 and len(set(json.loads((M/'design/原版美术映射.json').read_text())['religion_sources'].values()))==8,'All 8 religions have distinct attributed native placeholder sources')
print(json.dumps({'ok':not errors,'checks':checks,'scope':'Static structure, tutorial sort formula and native-source contracts only; no gameplay or UI test.','errors':errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
