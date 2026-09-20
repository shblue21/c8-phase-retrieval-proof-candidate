"""Exact identities for the sharp C4/C8 family boundary, independently built."""
from pathlib import Path
import sympy as S,json,time
root=Path(__file__).resolve().parents[1];t,b,c,s,x,y=S.symbols('t b c s x y',real=True);I=S.I
con=S.conjugate;a0=1+I*t+b*t**3+I*c*t**5;a1=t**2+I*s*t**3-b*t**5;a2=t**4+I*t**5
w=b+s*x*y-s*y;k=-b*x+(s-1)*w*x-w;z=b*s*x*y+c*(1-s)*x+w*y
v=a0+(x+I*y)*a1+I*w*a2+(z+I*k)*t**6;h=I*a2+(-y+I*(1-s)*x)*t**6
R=c-2*b*y+s*(1-s)*x*x+s*y*y;G=(b*(2-s)+s*s*y)*x+b-s*y;H=(s-1)*x-y*y
checks=[]
def ck(name,expr):
 ok=S.cancel(S.expand(expr))==0
 checks.append({'name':name,'pass':ok})
 if not ok:raise AssertionError(name)
start=time.time()
ck('entire_F_identity',h*con(v)+con(h)*v-2*R*t**9-2*(H*G-(1-s)*x*y*R)*t**12)
ys=b*((2-s)*x+1)/(s*(1-s*x));rr=c-b*b/s+s*(1-s)*x*x+4*b*b*x*x/(s*(1-s*x)**2)
ck('G_zero_under_rational_curve',G.subs(y,ys));ck('R_curve',R.subs(y,ys)-rr)
quartic=(s*s*(1-s)*x*x+s*c-b*b)*(1-s*x)**2+4*b*b*x*x
ck('quartic_clearing',rr*s*(1-s*x)**2-quartic)
ck('completed_square',R-(c-b*b/s+s*(1-s)*x*x+s*(y-b/s)**2))
ck('bzero_G',G.subs({b:0,y:0}));ck('bzero_R',R.subs({b:0,y:0})-(c+s*(1-s)*x*x))
vv=1+I*t+I*b/s*t*t
ck('boundary_v',v.subs({x:0,y:b/s,c:b*b/s})-vv)
ck('boundary_h',h.subs({x:0,y:b/s,c:b*b/s})-I*t**4*vv)
vv=v.subs({b:0,c:-1,s:S.Rational(1,2),x:2,y:0});hh=h.subs({b:0,c:-1,s:S.Rational(1,2),x:2,y:0})
ck('strict_interior_collision',hh*con(vv)+con(hh)*vv)
# R'(x)>0 on 0<x<1/s for b!=0 and 0<s<1.
ck('positive_derivative_formula',S.diff(rr,x)-(2*s*(1-s)*x+8*b*b*x/(s*(1-s*x)**3)))
out={'status':'PASS','checks':checks,'count':len(checks),'elapsed_seconds':time.time()-start,
     'scope':'finite exact polynomial/rational identities for the displayed sharp boundary proof'}
(root/'data/sharp_boundary_checks.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
