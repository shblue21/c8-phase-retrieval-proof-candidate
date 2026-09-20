"""Direct manuscript transcription; imports no provided verifier or basis data."""
from pathlib import Path
import json,time,hashlib
import sympy as S
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
t=S.symbols('t',real=True);b,c,s,m,g=S.symbols('b c s m g',real=True)
I=S.I;half=S.Rational(1,2)
x=S.symbols('x0:8',real=True);y=S.symbols('y0:8',real=True)
r=S.symbols('r0:8',real=True);a=S.symbols('a0:8',real=True)
p=[1+I*t+b*t**3+I*c*t**5+g*t**12/2-I*g*t**13/2,
 t**2+I*s*t**3-b*t**5+g*t**10/(2*s)-I*g*t**11/2-g*b*t**13/(2*s),
 t**4+I*t**5+g*t**8/2-I*g*t**9/2+g*b*t**11/2-g*c*t**12/2,
 t**6+I*m*t**7,t**8+I*t**9+b*t**11+I*c*t**13,
 t**10+I*s*t**11-b*t**13,t**12+I*t**13,t**14]
checks=[];start=time.time()
def equal(name,expr):
 z=S.cancel(S.expand(expr))
 if z!=0:raise AssertionError((name,str(z)))
 checks.append(name)
def truth(name,cond):
 if not cond:raise AssertionError(name)
 checks.append(name)
con=S.conjugate
slopes=[1,s,1,m,1,s,1,0]
for j,z in enumerate(p):
 P=S.Poly(z,t);truth(f'valuation_{j}',min(k[0] for k in P.monoms())==2*j)
 equal(f'leading_{j}',P.nth(2*j)-1);equal(f'slope_{j}',P.nth(2*j+1)-I*slopes[j])
for j in range(8):
 for k in range(8):
  P=S.Poly(S.expand(p[j]*con(p[k])),t)
  for d in [1,5,13]:equal(f'product_{j}_{k}_{d}',P.nth(d))
for i in range(8):
 v=p[i]+sum((x[k]+I*y[k])*p[k] for k in range(i+1,8))
 for j in range(i+1,8):
  hh=(r[j]+I*a[j])*p[j]
  F=S.Poly(S.expand(hh*con(v)+con(hh)*v),t)
  equal(f'first_{i}_{j}',F.nth(2*i+2*j)-2*r[j])
  equal(f'next_{i}_{j}',F.nth(2*i+2*j+1).subs(r[j],0)-2*(slopes[i]-slopes[j])*a[j])
R=lambda X,Y:c-2*b*Y+s*(1-s)*X**2+s*Y**2
D=c+g-b*b/(s-m)
RR=R(x[1],y[1]);TT=m*((1-s)*x[1]*x[3]+y[1]*y[3])-g*x[2]
SS=-g*(1+x[1]**2+y[1]**2+x[2]**2+y[2]**2)-m*(m-1)*x[3]**2+m*y[3]**2
rho=a[6]-a[4]*x[2]
expected={
 (4,6):{25:2*a[6]*R(x[5],y[5])},
 (1,5):{21:-2*a[5]*(g*(1+x[2]**2+y[2]**2)+m*(m-s)*x[3]**2/s-m*y[3]**2)},
 (2,4):{17:-2*a[4]*((1-m)*(s-m)*x[3]**2/(1-s)+(s-m)*(y[3]-b/(s-m))**2+D)},
 (2,6):{21:-2*a[6]*(g+m*(m-1)*x[3]**2-m*y[3]**2)},
 (0,2):{9:2*a[2]*((1-s)*(s-m)*x[1]**2/(1-m)+(s-m)*(y[1]-b/(s-m))**2+D)},
 (0,4):{17:2*(RR*rho+a[4]*TT),21:2*(a[4]*SS+TT*rho)}}
layers=[]
for i,j0,end in [(4,6,23),(1,5,17),(2,4,16),(2,6,19),(0,2,8),(0,4,15)]:
 v=p[i]+sum((x[k]+I*y[k])*p[k] for k in range(i+1,8))
 h=sum((r[k]+I*a[k])*p[k] for k in range(j0,8))
 F=S.Poly(S.expand(h*con(v)+con(h)*v),t);rules={};pivots=[]
 for j in range(j0,8):
  for d,var,want in [(2*i+2*j,r[j],S.Integer(2)),(2*i+2*j+1,a[j],2*(slopes[i]-slopes[j]))]:
   if d>end:continue
   e=S.cancel(F.nth(d).subs(rules));pivot=S.cancel(S.diff(e,var))
   equal(f'pivot_{i}_{j0}_{d}',pivot-want)
   if pivot==0:continue
   solution=S.factor(-e.subs(var,0)/pivot)
   truth(f'linear_{i}_{j0}_{d}',not solution.has(var))
   equal(f'substitution_{i}_{j0}_{d}',e.subs(var,solution))
   rules[var]=solution;pivots.append(str(pivot))
 if (i,j0)==(2,4):equal('appendix_r6',rules[r[6]]-a[4]*(-b+(s-m)*y[3]-(s-m)*x[3]*y[3]/(1-s)-y[4]))
 if (i,j0)==(0,2):equal('appendix_r4',rules[r[4]]-a[2]*(b+(m-s)*y[1]+(s-m)*x[1]*y[1]/(1-m)-y[2]))
 for d,target in expected[(i,j0)].items():equal(f'gate_{i}_{j0}_{d}',F.nth(d).subs(rules)-target)
 denoms=sorted({str(S.factor(S.denom(S.cancel(z)))) for z in rules.values()})
 for z in rules.values():truth('no_signal_denominator',not (S.denom(S.cancel(z)).free_symbols & set(x+y+r+a)))
 if (i,j0) in [(4,6),(1,5),(2,6),(0,4)]:
  zeros={a[4]:0,a[6]:0} if (i,j0)==(0,4) else {a[j0]:0}
  equal(f'terminal_h_{i}_{j0}',h.subs(rules).subs(zeros))
 else:
  for j in range(j0,(4 if i==0 else 6)):
   equal(f'restart_real_{i}_{j}',rules.get(r[j],r[j]).subs(a[j0],0))
   equal(f'restart_imag_{i}_{j}',rules.get(a[j],a[j]).subs(a[j0],0))
 layers.append({'i':i,'j_start':j0,'end_degree':end,'pivots':pivots,'denominators':denoms,'substitutions':{str(k):str(z) for k,z in rules.items()},'latex':{S.latex(k):S.latex(z) for k,z in rules.items()}})
equal('R_square',RR-(s*(1-s)*x[1]**2+s*(y[1]-b/s)**2+c-b*b/s))
equal('D_positive_decomposition',D-(c-b*b/s+g+(-m)*b*b/(s*(s-m))))
equal('schur',RR*expected[(0,4)][21]-TT*expected[(0,4)][17]-2*a[4]*(RR*SS-TT**2))
X,Y=S.symbols('X Y',real=True)
aa0=1+I*t+b*t**3+I*c*t**5;aa1=t*t+I*s*t**3-b*t**5;aa2=t**4+I*t**5
W=b+s*X*Y-s*Y;K=-b*X+(s-1)*W*X-W;Z=b*s*X*Y+c*(1-s)*X+W*Y
vv=aa0+(X+I*Y)*aa1+I*W*aa2+(Z+I*K)*t**6;hh=I*aa2+(-Y+I*(1-s)*X)*t**6
GG=(b*(2-s)+s*s*Y)*X+b-s*Y;HH=(s-1)*X-Y*Y
BB=R(X,Y)
equal('boundary_full_polynomial',hh*con(vv)+con(hh)*vv-2*BB*t**9-2*(HH*GG-(1-s)*X*Y*BB)*t**12)
curve=b*((2-s)*X+1)/(s*(1-s*X));rr=c-b*b/s+s*(1-s)*X*X+4*b*b*X*X/(s*(1-s*X)**2)
equal('curve_G',GG.subs(Y,curve));equal('curve_R',BB.subs(Y,curve)-rr)
equal('derivative_positive',S.diff(rr,X)-2*s*(1-s)*X-8*b*b*X/(s*(1-s*X)**3))
equal('quartic',rr*s*(1-s*X)**2-((s*s*(1-s)*X*X+s*c-b*b)*(1-s*X)**2+4*b*b*X*X))
equal('b_zero',BB.subs({b:0,Y:0})-(c+s*(1-s)*X*X))
base_v=1+I*t+I*b/s*t*t
equal('boundary_v',vv.subs({X:0,Y:b/s,c:b*b/s})-base_v)
equal('boundary_h',hh.subs({X:0,Y:b/s,c:b*b/s})-I*t**4*base_v)
old=[1+I*t+t**3+4*I*t**5+t**12/2-I*t**13/2,t*t+I*t**3/2-t**5+t**10-I*t**11/2-t**13,t**4+I*t**5+t**8/2-I*t**9/2+t**11/2-2*t**12,t**6-2*I*t**7,t**8+I*t**9+t**11+4*I*t**13,t**10+I*t**11/2-t**13,t**12+I*t**13,t**14]
sparse=[1+I*t+I*t**5-I*t**13,t*t+I*t**3/2-I*t**11,t**4+I*t**5-I*t**9,t**6-I*t**7,t**8+I*t**9+I*t**13,t**10+I*t**11/2,t**12+I*t**13,t**14]
oldparams={b:1,c:4,s:half,m:-2,g:1};newparams={b:0,c:1,s:half,m:-1,g:1}
base=[S.expand(z.subs(newparams)) for z in p];A=S.eye(8);A[0,6]=-half;A[1,5]=-1;A[2,4]=-half;A[2,6]=half
truth('basis_change_det',A.det()==1)
for j in range(8):
 equal(f'old_basis_{j}',p[j].subs(oldparams)-old[j]);equal(f'sparse_basis_{j}',sum(A[j,k]*base[k] for k in range(8))-sparse[j])
truth('20_terms',sum(len(S.Poly(z,t).terms()) for z in sparse)==20)
for label,basis,sourcefile in [('v1',old,ROOT/'data/v1_frame_gaussian_integer.json'),('sparse',sparse,ROOT/'sources/sparse8_frame_gaussian_integer.json')]:
 data=json.loads(sourcefile.read_text());cols=data.get('columns')
 if cols is None:cols=data['Q_columns']
 if cols and isinstance(cols[0],dict):cols=[list(map(list,zip(col['real'],col['imag']))) for col in cols]
 actual=[]
 for j in range(1,27):
  col=[]
  for k,z in enumerate(basis):
   z=S.expand(2*con(z).subs(t,j));re,im=z.as_real_imag();truth(f'integer_{label}_{j}_{k}',re.is_Integer and im.is_Integer)
   col.append([int(re),int(im)])
  actual.append(col)
 truth(f'frame_{label}',actual==cols)
 if label=='sparse':
  (ROOT/'data/v2_sparse_frame_gaussian_integer.json').write_text(json.dumps({'dimension':8,'measurement_count':26,'orientation':'columns[j-1][k] = [real, imag] of q_j[k]','rule':'q_j=2 conjugate(r(j)), j=1,...,26','parameters':[0,1,'1/2',-1,1],'columns':actual},indent=2)+'\n')
result={'status':'PASS','check_count':len(checks),'checks':checks,'layers':layers,'seconds':time.time()-start,'sympy':S.__version__,'provided_code_imported':False,'scope':'direct symbolic manuscript transcription and actual frames; analytic inequalities and quantified case coverage separately reviewed'}
(HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS',len(checks),'checks; seconds',time.time()-start)
