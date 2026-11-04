#!/usr/bin/env python3
"""Read-only native RulesetValidator check with builtin UI assets; no GL, map or game.
Requires a Java 21 JDK for source-file execution. The original CLI log is not rewritten.
"""
from pathlib import Path
import argparse,json,subprocess,tempfile,zipfile,sys
M=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser(description=__doc__);p.add_argument('jar',type=Path);p.add_argument('--java',default='java');a=p.parse_args();jar=a.jar.resolve();version=subprocess.run([a.java,'-jar',str(jar),'--version'],capture_output=True,text=True,check=True).stdout.strip();assert version=='4.22.16',version
with tempfile.TemporaryDirectory(prefix='fantasy-native-ui-')as tmp:
 root=Path(tmp);wanted=set()
 def scan(v):
  if isinstance(v,dict):
   if v.get('extraImage'):wanted.add(v['extraImage'])
   for x in v.values():scan(x)
  elif isinstance(v,list):
   for x in v:scan(x)
 scan(json.loads((M/'jsons/Tutorials.json').read_text()));atlases=[];found=set()
 with zipfile.ZipFile(jar)as z:
  entries=set(z.namelist())
  for name in wanted:
   if any('ExtraImages/'+name+s in entries for s in ['', '.png','.jpg']):found.add(name)
  for n in entries:
   if not n.endswith('.atlas'):continue
   text=z.read(n).decode();hit=(wanted-found)&set(text.splitlines())
   if not hit:continue
   found|=hit;atlases.append(n[:-6]);(root/n).write_text(text)
   for l in text.splitlines():
    if l.endswith('.png')and not l[0].isspace()and l in entries:(root/l).write_bytes(z.read(l))
 assert found==wanted,'Missing builtin tutorial images: '+str(wanted-found)
 (root/'Atlases.json').write_text(json.dumps(atlases))
 r=subprocess.run([a.java,'-Djava.awt.headless=true','-cp',str(jar),str(M/'tools/NativeRulesetValidation.java'),str(M),str(root)],text=True,capture_output=True,timeout=60)
 out=r.stdout+r.stderr;reports=M/'build/validation';reports.mkdir(parents=True,exist_ok=True);(reports/'native-rules.txt').write_text(out);print(out);sys.exit(r.returncode)
