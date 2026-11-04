#!/usr/bin/env python3
"""Count native JSON definitions in supplied ruleset directories, without running a game.
Usage: python3 tools/count_reference_rulesets.py /path/to/mod/jsons [...]
These are object counts, including replacements; they are NOT tactical roles or all selectable units.
"""
import json,re,sys
from pathlib import Path

def count(root):
 def load(name):
  raw=(root/(name+'.json')).read_text()
  # Preserve strings before removing JSON comments and trailing commas.
  raw=re.sub(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*[\s\S]*?\*/',lambda m:'' if m[0].startswith('/') else m[0],raw)
  return json.loads(re.sub(r',\s*([}\]])',r'\1',raw))
 t=load('Techs');u=load('Units');b=load('Buildings');n=load('Nations')
 return {'directory':str(root),'technology_definitions':sum(len(c['techs']) for c in t),'unit_definitions':len(u),'strength_above_zero':sum(x.get('strength',0)>0 for x in u),'building_definitions':len(b),'non_wonder_buildings_including_replacements':sum(not x.get('isWonder') and not x.get('isNationalWonder') for x in b),'major_nation_definitions':sum(not x.get('cityStateType') and x['name'] not in ['Barbarians','Spectator'] for x in n)}
if __name__=='__main__':print(json.dumps([count(Path(p)) for p in sys.argv[1:]],ensure_ascii=False,indent=2))
