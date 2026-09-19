"""Exact negative controls for the polynomial arithmetic/certificate checker."""
import copy,json,contextlib,io
from pathlib import Path
import verify_sparse_certificate as v
ROOT=Path(__file__).resolve().parents[1]
original=copy.deepcopy(v.RAW)
# A real coefficient perturbation creates a missing-norm-coefficient violation.
v.RAW[0][5]=(1,4)
v.BASIS=[[v.cp(*q.get(k,(0,0))) for k in range(15)] for q in v.RAW]
mut=v.orthog(v.BASIS[0],v.BASIS[0])[5]
assert mut!=0
# The real t^5 perturbation produces norm coefficient 2, hence orthog coefficient 4.
assert mut==4
# Switching off all high mixing corrections gives a known exact failed family.
raw=copy.deepcopy(original)
for k in (12,13):del raw[0][k]
for k in (10,11,13):del raw[1][k]
for k in (8,9,11,12):del raw[2][k]
v.RAW=raw;v.BASIS=[[v.cp(*q.get(k,(0,0))) for k in range(15)] for q in raw]
vv=v.combination({0:v.cp(1)});hh=v.combination({4:v.cp(0,1)})
assert all(p==0 for p in v.orthog(vv,hh))
# Indeed p4=t8*p0, so p0+i*p4 and p0-i*p4 have equal norms but are not proportional.
assert all(v.BASIS[4][k]==(v.BASIS[0][k-8] if 8<=k<=14 else v.cp()) for k in range(15))
log={'status':'PASS','checks':['A real t5 perturbation is detected: orthogonality coefficient changes to 4',
 'Zero-mixing comparison family has exact nonproportional collision p0+i p4 versus p0-i p4'],
 'scope':'These are arithmetic/certificate negative controls, not additional PR examples.'}
(ROOT/'logs/negative_controls.json').write_text(json.dumps(log,indent=2));print(json.dumps(log,indent=2))
