#!/usr/bin/env python3
"""Run official Unciv validation and an optional isolated game-creation smoke test.
Usage: python3 tools/check_engine.py /path/to/Unciv.jar --java /path/to/java --smoke
The engine's auto-updater runs only on a temporary copy, never on source JSON.
"""
import argparse,json,re,shutil,subprocess,tempfile,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('jar',type=Path);p.add_argument('--java',default='java');p.add_argument('--smoke',action='store_true');a=p.parse_args();jar=a.jar.resolve()
version=subprocess.run([a.java,'-jar',str(jar),'--version'],capture_output=True,text=True,check=True).stdout.strip()
if version!='4.22.16':sys.exit('Expected Unciv 4.22.16, got '+version)
reports=ROOT/'build/validation';reports.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(prefix='fantasyunciv-') as d:
 temp=Path(d);shutil.copytree(ROOT/'jsons',temp/'jsons')
 for asset in [*ROOT.glob('*.atlas'),*ROOT.glob('*.png'),ROOT/'Atlases.json']:
  if asset.is_file():shutil.copyfile(asset,temp/asset.name)
 r=subprocess.run([a.java,'-jar',str(jar),'mod-ci'],cwd=temp,text=True,capture_output=True)
 output=r.stdout+r.stderr;(reports/'engine.txt').write_text(output);print(output)
 # 4.22.16 mod-ci leaves Ruleset.name empty; AtlasPreview then scans an empty
 # combined-mod list instead of this rule set's existing atlas (see upstream source).
 # Preserve the raw warning and accept only this exact diagnostic after independent
 # source-hash, atlas and texture lookup coverage checks. No unknown warnings pass.
 diagnostics=re.findall(r'(?m)^(?:Error\w*|Warning\w*)\s*:.*$',output)
 known='Warning: Mod has no graphics for configured tilesets: FantasyHex'
 if known in diagnostics:
  asset=subprocess.run([sys.executable,str(ROOT/'tools/verify_assets.py')],text=True,capture_output=True)
  (reports/'assets.json').write_text(asset.stdout)
  if asset.returncode:print(asset.stdout,asset.stderr);sys.exit(1)
  diagnostics.remove(known)
  print('Known upstream anonymous-atlas CLI warning retained; independent asset checks passed. Actual rendering is untested.')
 if r.returncode or diagnostics:sys.exit(r.returncode or 1)
 if a.smoke:
  shutil.copytree(ROOT/'jsons',temp/'mods/FantasyUnciv/jsons')
  shutil.copyfile(ROOT/'tools/standard-game.json',temp/'setup.json')
  r=subprocess.run([a.java,'-jar',str(jar),'--creategame=setup.json'],cwd=temp,text=True,capture_output=True)
  output=r.stdout+r.stderr;(reports/'game-creation.txt').write_text(output);print(output)
  if r.returncode or 'Game started successfully' not in output:sys.exit(r.returncode or 1)
print('Official rule validation completed'+('; isolated game creation passed.' if a.smoke else '.'))
