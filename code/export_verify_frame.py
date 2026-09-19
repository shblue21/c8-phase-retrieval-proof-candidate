"""Actual Gaussian-integer 8 x 26 frame and independent exact checks.
Only Python standard-library arithmetic is used.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time,hashlib
from verify_sparse_certificate import RAW
ROOT=Path(__file__).resolve().parents[1]
PRIME=65537

def q_formula(t):
 return [
  (2+2*t**3+t**12, t**13-8*t**5-2*t),
  (2*t**2-2*t**5+2*t**10-2*t**13,t**11-t**3),
  (2*t**4+t**8+t**11-4*t**12,t**9-2*t**5),
  (2*t**6,4*t**7),
  (2*t**8+2*t**11,-2*t**9-8*t**13),
  (2*t**10-2*t**13,-t**11),
  (2*t**12,-2*t**13),(2*t**14,0)]

def gauss_mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def product_coeff(p,q):
 out=[(F(0),F(0)) for _ in range(29)]
 for i,a in p.items():
  for j,b in q.items():
   z=gauss_mul(a,(b[0],-b[1]));old=out[i+j];out[i+j]=(old[0]+z[0],old[1]+z[1])
 return out

def rank_mod(A,p=PRIME):
 B=[[int(x)%p for x in row] for row in A];nr=len(B);nc=len(B[0]);rank=0;ids=list(range(nr));rows=[];cols=[];piv=[]
 for j in range(nc):
  k=next((k for k in range(rank,nr) if B[k][j]),None)
  if k is None:continue
  B[rank],B[k]=B[k],B[rank];ids[rank],ids[k]=ids[k],ids[rank]
  val=B[rank][j];piv.append(val);rows.append(ids[rank]);cols.append(j);iv=pow(val,-1,p)
  B[rank]=[(x*iv)%p for x in B[rank]]
  for k in range(rank+1,nr):
   c=B[k][j]
   if c:
    for l in range(j,nc):B[k][l]=(B[k][l]-c*B[rank][l])%p
  rank+=1
  if rank==nr:break
 return {'rank':rank,'pivot_rows':rows,'pivot_columns':cols,'elimination_pivots':piv,'prime':p}

def main():
 tm=time.monotonic();nodes=list(range(1,27));cols=[q_formula(t) for t in nodes];checks=[]
 for t,col in zip(nodes,cols):
  for j,(r,im) in enumerate(col):
   pr=sum(a*t**k for k,(a,b) in RAW[j].items());pi=sum(b*t**k for k,(a,b) in RAW[j].items())
   assert r==2*pr and im==-2*pi
 checks.append('All 208 Gaussian-integer entries match 2*conjugate(p_j(t))')
 # Hermitian coefficient basis: diag, real off diagonal, imaginary off diagonal.
 polys=[];labels=[]
 for j in range(8):
  z=product_coeff(RAW[j],RAW[j]);assert all(b==0 for a,b in z)
  polys.append([a for a,b in z]);labels.append(['diag',j,j])
 for j in range(8):
  for k in range(j+1,8):
   z=product_coeff(RAW[j],RAW[k]);polys.append([2*a for a,b in z]);labels.append(['real',j,k]);polys.append([-2*b for a,b in z]);labels.append(['imag',j,k])
 M=[[polys[j][k] for j in range(64)] for k in range(29)]
 assert [k for k in range(29) if all(a==0 for a in M[k])]==[1,5,13]
 checks.append('The exact product coefficient rows vanish exactly at 1,5,13')
 # Clear denominators before reducing modulo p. This is an exact lower rank certificate.
 scaled=[]
 for row in M:
  line=[4*a for a in row];assert all(a.denominator==1 for a in line);scaled.append([int(a) for a in line])
 productrank=rank_mod(scaled);assert productrank['rank']==26
 checks.append('Product rank 26: exact upper bound and nonzero minor modulo 65537')
 # Actual q q* rows, not arbitrary Hermitian observables.
 lifted=[]
 for t,col in zip(nodes,cols):
  row=[a*a+b*b for a,b in col]
  for j in range(8):
   for k in range(j+1,8):
    a,b=gauss_mul(col[j],(col[k][0],-col[k][1]));row.extend([2*a,2*b])
  assert row==[4*sum(polys[j][k]*t**k for k in range(29)) for j in range(64)]
  lifted.append(row)
 checks.append('Every physical lifted row equals 4 times the evaluated polynomial coefficient row, including conjugation signs')
 liftrank=rank_mod(lifted);assert liftrank['rank']==26
 qmod=[[(cols[j][i][0]+256*cols[j][i][1])%PRIME for j in range(26)] for i in range(8)]
 assert 256**2%PRIME==PRIME-1
 signalrank=rank_mod(qmod);assert signalrank['rank']==8
 checks.extend(['Actual lifted measurement rank 26 modulo 65537','Actual signal rank 8 under i->256 modulo 65537'])
 data={'name':'PR26_confluent_jet_frame','status':'EXPLICIT_PR26_FRAME_WITH_SELF_CONTAINED_PROOF_MANUSCRIPT; external review pending',
  'dimension':8,'measurements':26,'orientation':'8 signal rows, 26 measurement columns; intensity is |q_j^* x|^2',
  'nodes':nodes,'formula':'q_j=2 conjugate((p_0(j),...,p_7(j))^T), p in proofs/PR26_EXPLICIT_FRAME_EN.md',
  'columns':[{'real':[r for r,i in col],'imag':[i for r,i in col]} for col in cols],
  'signal_rank':8,'lifted_measurement_rank':26,'field':'Gaussian integers','minimality_claim':False}
 out=ROOT/'PR26_FRAME_QI.json';out.write_text(json.dumps(data,indent=2))
 lines=['# q_j columns; each row below is coordinate k=0,...,7. All entries are exact Gaussian integers.']
 for i in range(8):lines.append(' ; '.join(f'{col[i][0]}{col[i][1]:+d}*I' for col in cols))
 (ROOT/'PR26_FRAME_QI.txt').write_text('\n'.join(lines)+'\n')
 # Reload the written artifact and check it against the separate integer formula.
 again=json.loads(out.read_text());assert all(list(zip(c['real'],c['imag']))==q_formula(t) for t,c in zip(again['nodes'],again['columns']))
 checks.append('Exported JSON reloaded and all entries independently regenerated')
 log={'status':'PASS','checks':checks,'count':len(checks),'product_rank_certificate':productrank,
 'lifted_rank_certificate':liftrank,'signal_rank_certificate':signalrank,
 'frame_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'elapsed_seconds':time.monotonic()-tm,
 'scope':'Frame arithmetic and ranks; the separate polynomial proof establishes phase retrieval.'}
 (ROOT/'logs/frame_exact_checks.json').write_text(json.dumps(log,indent=2))
 print(json.dumps(log,indent=2))
if __name__=='__main__':main()
