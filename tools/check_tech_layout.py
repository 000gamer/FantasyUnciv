from pathlib import Path
import json,re
M=Path(__file__).resolve().parents[1]
D=json.loads((M/'design/设计数据.json').read_text());T=D['techs']
def segments(a,b):
 x1,y1=map(int,T[a][7].split('/'));x2,y2=map(int,T[b][7].split('/'));x1=x1*260+210;x2*=260;y1=y1*87+31;y2=y2*87+31;m=(x1+x2)/2
 return [(x1,y1,m,y1),(m,y1,m,y2),(m,y2,x2,y2)]
collisions=[]
for b,r in T.items():
 for a in re.findall(r'D01-T\d+',r[4]):
  segs=segments(a,b)
  for k,v in T.items():
   if k in [a,b]:continue
   c,row=map(int,v[7].split('/'));xl=c*260;xr=xl+210;yt=row*87;yb=yt+62
   if any((y1==y2 and yt<y1<yb and max(x1,x2)>xl and min(x1,x2)<xr) or (x1==x2 and xl<x1<xr and max(y1,y2)>yt and min(y1,y2)<yb) for x1,y1,x2,y2 in segs):collisions.append((a,b,k))
edges=[(a,b) for b,r in T.items() for a in re.findall(r'D01-T\d+',r[4])]
def hit(s,t):
 x1,y1,x2,y2=s;u1,v1,u2,v2=t
 if x1==x2 and v1==v2:return min(u1,u2)<=x1<=max(u1,u2) and min(y1,y2)<=v1<=max(y1,y2)
 if y1==y2 and u1==u2:return min(x1,x2)<=u1<=max(x1,x2) and min(v1,v2)<=y1<=max(v1,v2)
 if y1==y2==v1==v2:return max(min(x1,x2),min(u1,u2))<min(max(x1,x2),max(u1,u2))
 if x1==x2==u1==u2:return max(min(y1,y2),min(v1,v2))<min(max(y1,y2),max(v1,v2))
 return False
crossings=sum(any(hit(s,t) for s in segments(a,b) for t in segments(c,d)) for i,(a,b) in enumerate(edges) for c,d in edges[:i] if len({a,b,c,d})==4)
spans=[int(T[b][7].split('/')[0])-int(T[a][7].split('/')[0]) for a,b in edges]
vertical=[abs(int(T[b][7].split('/')[1])-int(T[a][7].split('/')[1])) for a,b in edges]
report={'scope':'Idealized uniform-grid midpoint routing only. Not an actual UI or font/layout test.',
'node_obstructions':len(collisions),'edge_count':len(edges),'long_edges_span_at_least_4':sum(v>=4 for v in spans),
'summed_horizontal_column_span':sum(spans),'summed_vertical_row_span':sum(vertical),'unrelated_crossing_or_overlapping_edge_pairs':crossings,
'items':[[T[a][1],T[b][1],T[k][1],a,b,k] for a,b,k in collisions]}
print(json.dumps(report,ensure_ascii=False,indent=2))
if collisions:raise SystemExit(1)
