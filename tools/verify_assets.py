#!/usr/bin/env python3
"""Check copied source art, packed atlas and FantasyHex lookup coverage; never starts the game."""
from pathlib import Path
import json,re,hashlib,struct,sys
M=Path(__file__).resolve().parents[1];meta=json.loads((M/'design/原版美术映射.json').read_text());errors=[];checks=0

def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
load=lambda n:json.loads((M/'jsons'/f'{n}.json').read_text())
regions=set();pages=[]
raw=(M/'Atlases.json').read_text().strip()
try:atlases=json.loads(raw)
except json.JSONDecodeError:
 # LibGDX's own desktop packer emits minimal JSON such as [game].
 check(bool(re.fullmatch(r'\[\s*[A-Za-z0-9_.-]+(?:\s*,\s*[A-Za-z0-9_.-]+)*\s*\]',raw)),'Invalid atlas control file')
 atlases=[v.strip()for v in raw.strip('[]').split(',')] if not errors else []
for atlas in atlases:
 p=M/(atlas+'.atlas');check(p.is_file(),'Missing atlas '+atlas)
 if not p.is_file():continue
 # LibGDX treats every blank line as a page separator. A region name after
 # a separator is therefore a new texture-page filename, not another region.
 # Validate page boundaries before the flat name/coverage checks below.
 expect_page=True
 for line in p.read_text().splitlines():
  if not line.strip():
   expect_page=True
   continue
  if expect_page:
   check(line.endswith('.png') and (M/line).is_file(),
         'Invalid native atlas page after separator: '+line)
   expect_page=False
 current=None
 for line in p.read_text().splitlines():
  if line and not line[0].isspace() and ':'not in line:
   if line.endswith('.png'):
    page=M/line;pages.append(page);check(page.is_file(),'Missing texture page '+line)
    if page.is_file():
     raw=page.read_bytes();check(raw.startswith(b'\x89PNG\r\n\x1a\n'),'Invalid page PNG '+line);w,h=struct.unpack('>II',raw[16:24]);check(0<w<=4096 and 0<h<=4096,'Invalid page dimensions '+line)
   else:regions.add(line)
for v in meta['copied_images']:
 p=M/'Images'/v['target'];check(p.is_file(),'Missing source bitmap '+v['target'])
 if p.is_file():check(hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256'],'Source bitmap altered '+v['target'])
 check(v['target'][:-4] in regions,'Bitmap missing from atlas '+v['target'])
for n,prefix in [('Units','UnitIcons'),('Buildings','BuildingIcons'),('TileResources','ResourceIcons'),('UnitPromotions','UnitPromotionIcons')]:
 for o in load(n):
  if o['name']in ['R25','R26']:continue
  check(prefix+'/'+o['name']in regions,n+' portrait missing '+o['name'])
for c in load('CityStateTypes'):check('CityStateIcons/'+c['name']in regions,'City-state type icon missing '+c['name'])
for r in load('Religions'):check('ReligionIcons/'+r in regions,'Religion icon missing '+r)
for c in load('Techs'):
 for t in c['techs']:check('TechIcons/'+t['name']in regions,'Tech icon missing '+t['name'])
for b in load('Policies'):
 check('PolicyBranchIcons/'+b['name']in regions,'Policy branch icon missing '+b['name'])
 for p in b['policies']:check('PolicyIcons/'+p['name']in regions,'Policy icon missing '+p['name'])
for u in load('Units'):check('TileSets/FantasyHex/Units/'+u['name']in regions,'FantasyHex unit missing '+u['name'])
for r in load('TileResources'):
 if r['name']not in ['R25','R26']:check('TileSets/FantasyHex/Tiles/'+r['name']in regions,'FantasyHex resource missing '+r['name'])
for n in ['R22','R23','R24','R34','I25','I26','I27','I34']:
 check(not any(x.endswith('/'+n)for x in regions),'Retired object art remains '+n)
builtin=set(meta['builtin_fantasyhex_tiles'])
for key,vs in json.loads((M/'jsons/TileSets/FantasyHex.json').read_text())['ruleVariants'].items():
 for v in vs:check(v in builtin or 'TileSets/FantasyHex/Tiles/'+v in regions,'Unknown tile alias target '+key+': '+v)
options=load('ModOptions');check(options.get('tileset')==options.get('unitset')=='FantasyHex','Default FantasyHex sets')
report={'ok':not errors,'scope':'Static source bitmap hashes, atlas paths/pages and ruleset coverage; no UI or game rendering tested.','checks':checks,'atlas_regions':len(regions),'copied_images':len(meta['copied_images']),'texture_pages':[p.name for p in pages],'errors':errors}
print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
