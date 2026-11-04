from pathlib import Path
import json,re,itertools
M=Path(__file__).resolve().parents[1];D=json.loads((M/'design/设计数据.json').read_text())
# Static mirror of native gift-pool criteria; this is not map generation or a game test.
U=json.loads((M/'jsons/Units.json').read_text());N=json.loads((M/'jsons/Nations.json').read_text());types={x['name']:x for x in json.loads((M/'jsons/UnitTypes.json').read_text())};majors={x['name']for x in N if not x.get('cityStateType')and x['name']not in ['Barbarians','Spectator']}
def techs(u):
 out=[u['requiredTech']]if u.get('requiredTech')else[]
 for x in u['uniques']:
  if x.startswith(('Only available','Can only be built')):out+=re.findall(r'after discovering \[(D01-T\d+)\]',x)
 return list(dict.fromkeys(out))
def pool(era,selected):return [u for u in U if u.get('uniqueTo')in majors-selected and types[u['unitType']]['movementType']=='Land'and max(u.get('strength',0),u.get('rangedStrength',0))>0 and techs(u)and max(D['eras'][t]for t in techs(u))>era]
summary={}
for era in range(1,7):
 sizes=[len(pool(era,set(ss)))for ss in itertools.combinations(sorted(majors),8)]
 summary[str(era)]={'eight_major_selections':len(sizes),'minimum_pool':min(sizes),'maximum_pool':max(sizes),'empty_selections':sum(x==0 for x in sizes),'all_twelve_pool':len(pool(era,majors))}
report={'scope':'Static transcription of 4.22.16 initializer conditions; not a game or randomized map test.','criteria':'Unselected major civilization, land military, available only after the starting era. All required-tech clauses are considered.','per_starting_era':summary,'eligible_by_nation_in_era_I':{n:[u['name']for u in pool(1,majors-{n})]for n in sorted(majors)}}
print(json.dumps(report,ensure_ascii=False,indent=2))
