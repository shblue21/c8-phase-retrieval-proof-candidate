"""Exact checks for the NEW parametric theorem; not a formal proof assistant."""
from parametric8 import *
import json,sys,time
from pathlib import Path
checks=[]
def check(name,z):
 val=S.cancel(S.expand(z));ok=(val==0)
 checks.append({'name':name,'pass':ok})
 if not ok:print('FAIL',name,val);raise AssertionError(name)

t0=time.time()
for i in range(8):
 for j in range(8):
  prod=S.Poly(S.expand(p[i]*con(p[j])),T)
  for k in [1,5,13]:check(f'product_{i}_{j}_missing_{k}',prod.nth(k))

def R(x,y):return c-2*b*y+s*(1-s)*x*x+s*y*y
for i,j,end,targets in [(4,6,23,[25]),(1,5,17,[21]),(2,4,16,[17]),(2,6,19,[21]),(0,2,8,[9]),(0,4,15,[17,21])]:
 F,sol,cons,vs=get_eq(i,j,end);xs,ys,rs,aa=vs
 xx=lambda k:xs[k];yy=lambda k:ys[k]
 if (i,j)==(4,6):expected={25:2*aa[6]*R(xs[5],ys[5])}
 elif (i,j)==(1,5):expected={21:-2*aa[5]*(g*(1+xs[2]**2+ys[2]**2)+m*(m-s)/s*xs[3]**2-m*ys[3]**2)}
 elif (i,j)==(2,4):expected={17:-2*aa[4]*((1-m)*(s-m)/(1-s)*xs[3]**2+(s-m)*(ys[3]-b/(s-m))**2+c+g-b*b/(s-m))}
 elif (i,j)==(2,6):expected={21:-2*aa[6]*(g+m*(m-1)*xs[3]**2-m*ys[3]**2)}
 elif (i,j)==(0,2):expected={9:2*aa[2]*((1-s)*(s-m)/(1-m)*xs[1]**2+(s-m)*(ys[1]-b/(s-m))**2+c+g-b*b/(s-m))}
 else:
  rr=R(xs[1],ys[1]);tt=m*((1-s)*xs[1]*xs[3]+ys[1]*ys[3])-g*xs[2]
  ss=-g*(1+xs[1]**2+ys[1]**2+xs[2]**2+ys[2]**2)-m*(m-1)*xs[3]**2+m*ys[3]**2
  rho=aa[6]-aa[4]*xs[2]
  expected={17:2*(rr*rho+aa[4]*tt),21:2*(aa[4]*ss+tt*rho)}
  check('schur_elimination_identity',rr*expected[21]-tt*expected[17]-2*aa[4]*(rr*ss-tt**2))
 for k,expr in expected.items():check(f'layer_{i}_{j}_E{k}',F.nth(k).subs(sol)-expr)
 # all divisions arise from these fixed slope gaps; solved variable is reinserted exactly.
 for var,value in sol.items():
  d=S.denom(S.cancel(value))
  if d.free_symbols & set(xs+ys+rs+aa):raise AssertionError(('signal dependent denominator',var,d))
 checks.append({'name':f'layer_{i}_{j}_no_signal_denominators','pass':True})

source_params={b:1,c:4,s:S.Rational(1,2),m:-2,g:1}
for i in range(8):check(f'inherited_basis_specialization_{i}',p[i].subs(source_params)-p8[i])
small_params={b:0,c:1,s:S.Rational(1,2),m:-1,g:1}
base=[S.expand(z.subs(small_params)) for z in p]
small=[1+I*T+I*T**5-I*T**13,T**2+I*T**3/2-I*T**11,T**4+I*T**5-I*T**9,T**6-I*T**7,T**8+I*T**9+I*T**13,T**10+I*T**11/2,T**12+I*T**13,T**14]
transform=S.eye(8);transform[0,6]=-S.Rational(1,2);transform[1,5]=-1;transform[2,4]=-S.Rational(1,2);transform[2,6]=S.Rational(1,2)
for i in range(8):check(f'sparse_basis_transform_{i}',sum(transform[i,k]*base[k] for k in range(8))-small[i])
assert transform.det()==1
checks.append({'name':'sparse_basis_transform_invertible','pass':True})
B,labels=real_coeff_tensor(small);rk=B.rank();assert rk==26
checks.append({'name':'sparse_product_dimension_exact_26','pass':True})
frame=[]
for j in range(1,27):
 col=[]
 for q in small:
  v=S.expand(2*con(q).subs(T,j));r,im=S.re(v),S.im(v)
  assert r.is_Integer and im.is_Integer
  col.append([int(r),int(im)])
 frame.append(col)
out={'status':'PASS','checks':checks,'check_count':len(checks),'elapsed_seconds':time.time()-t0,'exact_product_rank':rk,'scope':'finite rational-function identities and exact rank; proof inequalities/case coverage in accompanying manuscript'}
root=Path(__file__).resolve().parents[1]
(root/'data'/'parametric8_checks.json').write_text(json.dumps(out,indent=2))
(root/'data'/'sparse8_frame_gaussian_integer.json').write_text(json.dumps({'orientation':'26 measurement columns, each has 8 [real,imag] pairs','q_j':'2 conjugate(r(j)), j=1,...,26','columns':frame},indent=2))
print('PASS',len(checks),'exact checks; product rank',rk,'; elapsed',time.time()-t0)
