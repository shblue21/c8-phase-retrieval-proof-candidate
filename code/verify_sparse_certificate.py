"""Pure-Python rational sparse-polynomial verification, no CAS dependencies.
Checks the exact identities used in the proposed 26-measurement proof.
The formal proof of completeness of the cases is in the accompanying text.
"""
from fractions import Fraction as F
from pathlib import Path
import json, time, hashlib
ROOT=Path(__file__).resolve().parents[1]
# 28 independent real variables; sparse monomials avoid a polynomial-domain CAS.
NAMES=[f'{a}{j}' for a in ('x','y','r','a') for j in range(1,8)]
NV=len(NAMES); ZERO=(0,)*NV; IDX={a:i for i,a in enumerate(NAMES)}
class P:
 def __init__(self,data=0):
  if isinstance(data,P):self.d=data.d.copy()
  elif isinstance(data,dict):self.d={m:F(c) for m,c in data.items() if c}
  else:self.d={} if not data else {ZERO:F(data)}
 def __add__(self,other):
  z=self.d.copy()
  for m,c in P(other).d.items():
   z[m]=z.get(m,F(0))+c
   if not z[m]:del z[m]
  return P(z)
 __radd__=__add__
 def __neg__(self):return P({m:-c for m,c in self.d.items()})
 def __sub__(self,other):return self+-P(other)
 def __rsub__(self,other):return P(other)+-self
 def __mul__(self,other):
  z={}
  for m,c in self.d.items():
   for n,e in P(other).d.items():
    k=tuple(a+b for a,b in zip(m,n));z[k]=z.get(k,F(0))+c*e
  return P(z)
 __rmul__=__mul__
 def __truediv__(self,c):return self*F(1,F(c))
 def __pow__(self,n):
  assert n>=0;z=P(1)
  for _ in range(n):z=z*self
  return z
 def __eq__(self,other):return self.d==P(other).d
 def coefficient(self,name,power=1):
  j=IDX[name];z={}
  for m,c in self.d.items():
   if m[j]==power:
    n=list(m);n[j]=0;z[tuple(n)]=c
  return P(z)
 def subst(self,name,value):
  j=IDX[name];value=P(value);z=P();powers={0:P(1)}
  for m,c in self.d.items():
   k=m[j]
   if k not in powers:powers[k]=value**k
   n=list(m);n[j]=0;z+=P({tuple(n):c})*powers[k]
  return z
 def dump(self):
  return [[str(c),{NAMES[j]:e for j,e in enumerate(m) if e}] for m,c in sorted(self.d.items())]
def V(name):
 m=list(ZERO);m[IDX[name]]=1;return P({tuple(m):F(1)})
def cp(a=0,b=0):return (P(a),P(b))
def ca(z,w):return(z[0]+w[0],z[1]+w[1])
def cm(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def cj(z):return(z[0],-z[1])
# Coefficients P_j = t^(2j)(1+i s_j t)+..., exact Gaussian rationals.
RAW=[
 {0:(1,0),1:(0,1),3:(1,0),5:(0,4),12:(F(1,2),0),13:(0,F(-1,2))},
 {2:(1,0),3:(0,F(1,2)),5:(-1,0),10:(1,0),11:(0,F(-1,2)),13:(-1,0)},
 {4:(1,0),5:(0,1),8:(F(1,2),0),9:(0,F(-1,2)),11:(F(1,2),0),12:(-2,0)},
 {6:(1,0),7:(0,-2)},
 {8:(1,0),9:(0,1),11:(1,0),13:(0,4)},
 {10:(1,0),11:(0,F(1,2)),13:(-1,0)},
 {12:(1,0),13:(0,1)}, {14:(1,0)}]
BASIS=[[cp(*q.get(k,(0,0))) for k in range(15)] for q in RAW]
CHECKS=[];IDENTITIES={}
def check(name,condition):
 if not condition:raise AssertionError(name)
 CHECKS.append(name)
def combination(coeffs):
 out=[cp() for _ in range(15)]
 for j,c in coeffs.items():
  for k in range(15):out[k]=ca(out[k],cm(c,BASIS[j][k]))
 return out
def orthog(v,h):
 # h v# + h# v = 2 Re(h v#), real coefficients indexed in t.
 out=[]
 for k in range(29):
  z=P()
  for i in range(max(0,k-14),min(14,k)+1):
   z+=2*cm(h[i],cj(v[k-i]))[0]
  out.append(z)
 return out
def equations(i,hstart):
 v=combination({i:cp(1),**{j:cp(V(f'x{j}'),V(f'y{j}')) for j in range(i+1,8)}})
 h=combination({j:cp(V(f'r{j}'),V(f'a{j}')) for j in range(hstart,8)})
 return orthog(v,h)
def solve(eq,degree,name,tag,known):
 co=eq[degree].coefficient(name)
 assert all(m==ZERO for m in co.d), (name,'nonconstant pivot',co.dump())
 if co==0:return False
 p=co.d[ZERO]
 # Ensure the equation really is linear in the selected variable.
 rest=eq[degree].subst(name,0)
 check(f'{tag}: linear pivot {name}',eq[degree]==rest+p*V(name))
 val=-rest/p
 eq[:]=[a.subst(name,val) for a in eq]
 check(f'{tag}: solved coefficient {degree}',eq[degree]==0)
 known[name]=val.dump()
 return True

def eliminate(i,hstart,end,tag):
 eq=equations(i,hstart);known={}
 for j in range(hstart,end+1):
  d=2*i+2*j
  assert solve(eq,d,f'r{j}',tag,known)
  solve(eq,d+1,f'a{j}',tag,known)
 IDENTITIES[tag+'_substitutions']=known
 return eq

def main():
 tm=time.monotonic()
 # All norm products miss degrees 1,5,13. Off diagonal real/imag tested independently.
 for j in range(8):
  for k in range(j,8):
   for z in (cp(1),cp(0,1)):
    eq=orthog(BASIS[j],combination({k:z}))
    for d in (1,5,13):check(f'missing {d}: {j},{k},{"re" if z[0]==1 else "im"}',eq[d]==0)
 # Main stratum, first possible difference at j=2.
 eq=eliminate(0,1,4,'case0_first')
 G=F(5,6)*V('x1')**2+5*V('y1')**2-4*V('y1')+10
 check('case0 degree9 exact gate',eq[9]==V('a2')*G)
 check('case0 G positive decomposition',G==F(5,6)*V('x1')**2+5*(V('y1')-F(2,5))**2+F(46,5))
 IDENTITIES['case0_G']=G.dump()
 # After a2=0 the slope argument gives h1=h2=h3=0.
 eq=eliminate(0,4,7,'case0_remaining')
 x,y,z,w,u,v=[V(n) for n in ('x1','y1','x2','y2','x3','y3')]
 R=x*x+2*(y-2)**2+8
 T=-2*x*u-4*y*v-2*z
 S=-1-x*x-y*y-6*u*u-2*v*v-z*z-w*w
 h=V('a4');k=V('a6');r=k-h*z
 check('case0 degree17 exact gate',eq[17]==(R*r+2*h*T)/2)
 check('case0 degree21 exact gate',eq[21]==2*h*S+T*r)
 check('case0 combined negative identity',R*eq[21]-2*T*eq[17]==2*h*(R*S-T*T))
 IDENTITIES['case0_combined']={'R':R.dump(),'T':T.dump(),'S':S.dump(),'E17':eq[17].dump(),'E21':eq[21].dump()}
 # First nonzero signal at 1; only possible first difference at 5.
 eq=eliminate(1,5,7,'case1')
 g=-1-V('x2')**2-V('y2')**2-10*V('x3')**2-2*V('y3')**2
 check('case1 degree21 exact negative gate',eq[21]==2*V('a5')*g)
 IDENTITIES['case1_G']=g.dump()
 # First nonzero signal at 2; possible first difference 4 or 6.
 eq=eliminate(2,4,7,'case2_first')
 g=30*V('x3')**2+5*V('y3')**2-4*V('y3')+10
 check('case2 degree17 negative gate',eq[17]==-V('a4')*g)
 check('case2 positive decomposition',g==30*V('x3')**2+5*(V('y3')-F(2,5))**2+F(46,5))
 eq=eliminate(2,6,7,'case2_remaining')
 g=-1-6*V('x3')**2-2*V('y3')**2
 check('case2 degree21 negative gate',eq[21]==2*V('a6')*g)
 IDENTITIES['case2_G']=g.dump()
 # C4 tail: first nonzero signal at4, possible first difference6.
 eq=eliminate(4,6,7,'case4')
 # Direct determinant positivity gate; compare explicit computed coefficients.
 IDENTITIES['case4_orthogonality']={str(i):q.dump() for i,q in enumerate(eq) if q!=0}
 print('tail nonzero degrees',[i for i,q in enumerate(eq) if q!=0],flush=True)
 for i,q in enumerate(eq):
  if q!=0:print(i,q.dump(),flush=True)
 # Expected gate follows the same C4 calculation, here shifted by16 in t.
 # Obtain it explicitly rather than silently infer it.
 g=V('x5')**2+2*(V('y5')-2)**2+8
 check('case4 degree25 positive gate',eq[25]==V('a6')*g/2)
 slopes=[F(1),F(1,2),F(1),F(-2),F(1),F(1,2),F(1),F(0)]
 for j,row in enumerate(RAW):
  check(f'leading basis order {j}',min(row)==2*j and row[2*j]==(1,0))
  check(f'leading basis slope {j}',row.get(2*j+1,(0,0))==(0,slopes[j]))
  check(f'degree bound {j}',max(row)<=14)
 def restore(terms):
  data={}
  for c,mon in terms:
   m=list(ZERO)
   for name,power in mon.items():m[IDX[name]]=power
   data[tuple(m)]=F(c)
  return P(data)
 closure=[('case0_first',['a2'],['r1','a1','r2','r3','a3','r4']),
          ('case0_remaining',['a4','a6'],['r4','r5','a5','r6','r7','a7']),
          ('case1',['a5'],['r5','r6','a6','r7','a7']),
          ('case2_first',['a4'],['r4','r5','a5','r6']),
          ('case2_remaining',['a6'],['r6','r7','a7']),
          ('case4',['a6'],['r6','r7','a7'])]
 for tag,free,names in closure:
  sol=IDENTITIES[tag+'_substitutions']
  for name in names:
   z=restore(sol[name])
   for var in free:z=z.subst(var,0)
   check(f'{tag}: zero-difference closure {name}',z==0)
 matches={str(i):[j for j in range(i+1,8) if slopes[j]==slopes[i]] for i in range(8)}
 check('slope layer cover',matches=={'0':[2,4,6],'1':[5],'2':[4,6],'3':[],'4':[6],'5':[],'6':[],'7':[]})
 log={'status':'PASS','engine':'Python Fraction sparse polynomial convolution; no SymPy or other CAS imported',
      'checks':CHECKS,'count':len(CHECKS),'slope_matches':matches,'identities':IDENTITIES,
      'coefficient_table':[{str(k):[str(a),str(b)] for k,(a,b) in p.items()} for p in RAW],
      'elapsed_seconds':time.monotonic()-tm,
      'scope':'exact coefficient identities; completeness of normalization, cases, and evaluation inference must be justified in proof'}
 (ROOT/'logs/sparse_certificate.json').write_text(json.dumps(log,indent=2))
 print('PASS',len(CHECKS),'seconds',log['elapsed_seconds'],flush=True)
if __name__=='__main__':main()
