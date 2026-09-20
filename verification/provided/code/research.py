import sympy as S
from pathlib import Path
T=S.symbols('t',real=True)
I=S.I
p8=[1+I*T+T**3+4*I*T**5+S.Rational(1,2)*T**12-I*T**13/2,
 T**2+I*T**3/2-T**5+T**10-I*T**11/2-T**13,
 T**4+I*T**5+T**8/2-I*T**9/2+T**11/2-2*T**12,
 T**6-2*I*T**7,T**8+I*T**9+T**11+4*I*T**13,
 T**10+I*T**11/2-T**13,T**12+I*T**13,T**14]

def con(x):return S.conjugate(x).expand()
def real_coeff_tensor(p):
 n=len(p);D=max(S.degree(q,T) for q in p)
 B=[];labs=[]
 for a in range(n):
  for b in range(a,n):
   prod=S.expand(p[a]*con(p[b]))
   if a==b:
    B.append([prod.coeff(T,k) for k in range(2*D+1)]);labs.append((a,b,'diag'))
   else:
    re=S.expand(prod+con(prod));im=S.expand(I*prod-I*con(prod))
    B.extend([[re.coeff(T,k) for k in range(2*D+1)],[im.coeff(T,k) for k in range(2*D+1)]]);labs.extend([(a,b,'real'),(a,b,'imag')])
 return S.Matrix(B).T,labs

def triangular(p,i=0,jstart=1, verbose=False):
 n=len(p);D=max(S.degree(q,T) for q in p)
 xs=S.symbols(f'x0:{n}',real=True);ys=S.symbols(f'y0:{n}',real=True)
 rs=S.symbols(f'r0:{n}',real=True);aa=S.symbols(f'a0:{n}',real=True)
 v=p[i]+sum((xs[j]+I*ys[j])*p[j] for j in range(i+1,n))
 h=sum((rs[j]+I*aa[j])*p[j] for j in range(jstart,n))
 F=S.Poly(S.expand(h*con(v)+con(h)*v),T)
 eq=[F.nth(k) for k in range(2*D+1)]
 sols={};cons=[]
 for j in range(jstart,n):
  for k,var in [(2*i+2*j,rs[j]),(2*i+2*j+1,aa[j])]:
   e=S.expand(eq[k].subs(sols))
   c=e.coeff(var)
   if c!=0 and not c.free_symbols:
    sol=S.factor(-(e-c*var)/c);sols[var]=sol
    if verbose: print(k, var,'=',sol)
   elif e!=0:
    cons.append((k,S.factor(e)))
    if verbose: print('constraint',k,S.factor(e))
 return sols,[(k,S.factor(e.subs(sols))) for k,e in enumerate(eq) if e!=0],(xs,ys,rs,aa)

if __name__=='__main__':
 s=S.symbols('s',real=True)
 p=[1+I*T-I*T**5,T**2+I*s*T**3,T**4+I*T**5,T**6]
 sol,eq,vars=triangular(p,0,2,True)
 print('remaining:',[(k,e) for k,e in eq if e!=0])
