#!/usr/bin/env python3
"""Pack the included, unmodified source bitmaps. Does not start Unciv or create a game."""
from pathlib import Path
import argparse,subprocess,sys
M=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('jar',type=Path);p.add_argument('--java',default='java');a=p.parse_args()
r=subprocess.run([a.java,'-Djava.awt.headless=true','-cp',str(a.jar.resolve()),'com.badlogic.gdx.tools.texturepacker.TexturePacker',str(M/'Images'),str(M),'game'],capture_output=True,text=True)
if r.returncode:print(r.stdout,r.stderr);sys.exit(r.returncode)
(M/'Atlases.json').write_text('["game"]\n')
print('Packed source bitmaps into game.atlas/game.png. No game was started.')
