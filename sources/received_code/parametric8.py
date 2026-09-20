from research import *
import time,json
b,c,s,m,g=S.symbols('b c s m g',real=True,nonzero=True)
a=S.Matrix([1+I*T+b*T**3+I*c*T**5,T**2+I*s*T**3-b*T**5,T**4+I*T**5])
J=S.Matrix([[2*c,0,2],[0,2*s,0],[2,0,0]])
p=[S.expand(z) for z in a+g*T**8*J.inv()*a.applyfunc(con)]+[T**6+I*m*T**7]+[S.expand(T**8*z) for z in a]+[T**14]

def get_eq(i,jstart,end,params=None):
 pp=p if params is None else [S.cancel(z.subs(params)) for z in p]
 n=8;xs=S.symbols('x0:8',real=True);ys=S.symbols('y0:8',real=True);rs=S.symbols('r0:8',real=True);aa=S.symbols('a0:8',real=True)
 v=pp[i]+sum((xs[j]+I*ys[j])*pp[j] for j in range(i+1,n))
 h=sum((rs[j]+I*aa[j])*pp[j] for j in range(jstart,n))
 F=S.Poly(S.expand(h*con(v)+con(h)*v),T)
 sols={};cons=[]
 for j in range(jstart,8):
  for k,var in [(2*i+2*j,rs[j]),(2*i+2*j+1,aa[j])]:
   if k>end:break
   e=S.cancel(F.nth(k).subs(sols));coef=S.expand(e).coeff(var)
   if coef!=0:
    sol=S.factor(-(e-coef*var)/coef);sols[var]=sol
   elif e!=0:cons.append((k,S.factor(e)))
  if 2*i+2*j+1>=end:break
 return F,sols,cons,(xs,ys,rs,aa)

if __name__=='__main__':
 for i,j,end,targets in [(4,6,23,[25]),(1,5,17,[21]),(2,4,16,[17]),(2,6,19,[21]),(0,2,8,[9]),(0,4,15,[17,21])]:
  print('LAYER',i,j,'start',flush=True);tm=time.time()
  F,sol,cons,vs=get_eq(i,j,end)
  print('sols',sol,flush=True)
  for k in targets:print('E',k,S.factor(F.nth(k).subs(sol)),flush=True)
  print('secs',time.time()-tm,flush=True)
