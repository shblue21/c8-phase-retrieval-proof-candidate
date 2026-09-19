"""Independent transcription of manuscript formulas; imports no supplied code.

Exact SymPy rational symbolic checks. The analytic case cover and positive-root
lemma require the separate written review, not an inference from check counts.
"""
from pathlib import Path
import json
import time
import sympy as S

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent
t = S.Symbol('t', real=True)
I = S.I
half = S.Rational(1, 2)
polys = [
    1+I*t+t**3+4*I*t**5+half*t**12-I*half*t**13,
    t**2+I*half*t**3-t**5+t**10-I*half*t**11-t**13,
    t**4+I*t**5+half*t**8-I*half*t**9+half*t**11-2*t**12,
    t**6-2*I*t**7,
    t**8+I*t**9+t**11+4*I*t**13,
    t**10+I*half*t**11-t**13,
    t**12+I*t**13,
    t**14,
]
X = {j: S.Symbol('x'+str(j), real=True) for j in range(1, 8)}
Y = {j: S.Symbol('y'+str(j), real=True) for j in range(1, 8)}
R = {j: S.Symbol('r'+str(j), real=True) for j in range(1, 8)}
A = {j: S.Symbol('a'+str(j), real=True) for j in range(1, 8)}
slopes = [1, half, 1, -2, 1, half, 1, 0]
checks = []
details = {}

def require(label, predicate):
    passed = bool(predicate)
    checks.append({'name': label, 'pass': passed})
    if not passed:
        raise AssertionError(label)

def identity(label, lhs, rhs=0):
    require(label, S.expand(lhs-rhs) == 0)

def coefficients(v, h):
    # Expand the actual manuscript's h*v# + h#*v, without supplied formulas.
    f = S.Poly(S.expand(h*S.conjugate(v)+S.conjugate(h)*v), t)
    return [f.nth(k) for k in range(29)]

def eliminate(i, start, end, label):
    v = polys[i]+sum((X[j]+I*Y[j])*polys[j] for j in range(i+1, 8))
    h = sum((R[j]+I*A[j])*polys[j] for j in range(start, 8))
    eq = coefficients(v, h)
    solved = {}
    for j in range(start, end+1):
        for degree, variable, expected in [
            (2*i+2*j, R[j], S.Integer(2)),
            (2*i+2*j+1, A[j], 2*(slopes[i]-slopes[j])),
        ]:
            expression = S.expand(eq[degree])
            pivot = S.diff(expression, variable)
            identity(label+': numeric pivot '+str(variable), pivot, expected)
            if expected == 0:
                continue
            require(label+': constant nonzero pivot '+str(variable), not pivot.free_symbols and pivot != 0)
            remainder = expression.subs(variable, 0)
            value = S.expand(-remainder/pivot)
            solved[variable] = value
            eq = [S.expand(e.subs(variable, value)) for e in eq]
            identity(label+': coefficient eliminated '+str(degree), eq[degree])
    details[label] = {'substitutions': {str(k):str(v) for k,v in solved.items()}}
    return eq, solved

def closure(label, solved, zeros, names):
    for variable in names:
        identity(label+': zero difference '+str(variable), solved[variable].subs(zeros))

def main():
    started = time.monotonic()
    for j, p in enumerate(polys):
        f=S.Poly(p,t)
        require('basis valuation '+str(j), min(k[0] for k,c in f.terms())==2*j)
        identity('basis leading coefficient '+str(j), f.nth(2*j), 1)
        identity('basis slope '+str(j), f.nth(2*j+1), I*slopes[j])
    products = [[S.Poly(S.expand(p*S.conjugate(q)),t) for q in polys] for p in polys]
    missing = [k for k in range(29) if all(products[i][j].nth(k)==0 for i in range(8) for j in range(8))]
    require('all 64 complex products miss exactly 1,5,13',missing==[1,5,13])
    matrix=S.Matrix([[products[i][j].nth(k) for i in range(8) for j in range(8)] for k in range(29)])
    rank=matrix.rank()
    require('full product dimension over Q(i)',rank==26)
    details['product_dimension']=rank

    # Check the universal slope lemma for every potential first pair, not only matches.
    for i in range(8):
        for j in range(i+1,8):
            v=polys[i]+sum((X[k]+I*Y[k])*polys[k] for k in range(i+1,8))
            h=sum((R[k]+I*A[k])*polys[k] for k in range(j,8))
            e=coefficients(v,h)
            identity(f'slope leading {i},{j}',e[2*i+2*j],2*R[j])
            identity(f'slope next {i},{j}',e[2*i+2*j+1].subs(R[j],0),2*(slopes[i]-slopes[j])*A[j])
    cover={str(i):[j for j in range(i+1,8) if slopes[j]==slopes[i]] for i in range(8)}
    require('all eight index strata',cover=={'0':[2,4,6],'1':[5],'2':[4,6],'3':[],'4':[6],'5':[],'6':[],'7':[]})
    details['case_cover']=cover

    e,sol=eliminate(0,1,4,'index0_early')
    g=S.Rational(5,6)*X[1]**2+5*(Y[1]-S.Rational(2,5))**2+S.Rational(46,5)
    identity('manuscript eq11 E9',e[9],A[2]*g)
    closure('index0_early',sol,{A[2]:0},[R[1],A[1],R[2],R[3],A[3],R[4]])

    e,sol=eliminate(0,4,7,'index0_mixed')
    rr=X[1]**2+2*(Y[1]-2)**2+8
    tt=-2*X[1]*X[3]-4*Y[1]*Y[3]-2*X[2]
    ss=-1-X[1]**2-Y[1]**2-6*X[3]**2-2*Y[3]**2-X[2]**2-Y[2]**2
    rho=A[6]-A[4]*X[2]
    identity('manuscript eq14 E17',e[17],(rr*rho+2*A[4]*tt)/2)
    identity('manuscript eq14 E21',e[21],2*A[4]*ss+tt*rho)
    identity('manuscript eq15 strict mixed determinant',rr*e[21]-2*tt*e[17],2*A[4]*(rr*ss-tt**2))
    # Explicit nonnegative decomposition of -RS+T^2-8.
    u=X[1]**2+2*(Y[1]-2)**2
    v=X[1]**2+Y[1]**2+6*X[3]**2+2*Y[3]**2+X[2]**2+Y[2]**2
    identity('mixed strict bound decomposition',-rr*ss+tt**2-8,u+8*v+u*v+tt**2)
    closure('index0_mixed',sol,{A[4]:0,A[6]:0},[R[4],R[5],A[5],R[6],R[7],A[7]])

    e,sol=eliminate(1,5,7,'index1')
    identity('manuscript eq8',e[21],-2*A[5]*(1+X[2]**2+Y[2]**2+10*X[3]**2+2*Y[3]**2))
    closure('index1',sol,{A[5]:0},[R[5],R[6],A[6],R[7],A[7]])
    e,sol=eliminate(2,4,7,'index2_early')
    identity('manuscript eq9',e[17],-A[4]*(30*X[3]**2+5*(Y[3]-S.Rational(2,5))**2+S.Rational(46,5)))
    closure('index2_early',sol,{A[4]:0},[R[4],R[5],A[5],R[6]])
    e,sol=eliminate(2,6,7,'index2_remaining')
    identity('manuscript eq10',e[21],-2*A[6]*(1+6*X[3]**2+2*Y[3]**2))
    closure('index2_remaining',sol,{A[6]:0},[R[6],R[7],A[7]])
    e,sol=eliminate(4,6,7,'index4')
    identity('manuscript eq7',e[25],A[6]*(X[5]**2+2*(Y[5]-2)**2+8)/2)
    closure('index4',sol,{A[6]:0},[R[6],R[7],A[7]])

    data=json.loads((SOURCE/'PR26_FRAME_QI.json').read_text())
    require('artifact dimension',data['dimension']==8 and data['measurements']==26 and len(data['columns'])==26)
    require('artifact nodes',data['nodes']==list(range(1,27)))
    for node,column in zip(data['nodes'],data['columns']):
        for j,p in enumerate(polys):
            exact=S.expand(2*S.conjugate(p.subs(t,node)))
            identity(f'physical column {node} coordinate {j}',exact,S.Integer(column['real'][j])+I*S.Integer(column['imag'][j]))
            require(f'Gaussian integer {node},{j}',S.re(exact).is_Integer and S.im(exact).is_Integer)
    details['physical_entries_verified']=208
    return {'status':'PASS','checks_count':len(checks),'checks':checks,'details':details,
            'sympy':S.__version__,'elapsed_seconds':time.monotonic()-started,
            'scope':'Independent exact transcription of basis, all slope cases, necessary elimination equations, gates and actual frame. Analytic proof obligations reviewed separately. No supplied code imported.'}

if __name__=='__main__':
    try:
        result=main()
    except Exception as exc:
        result={'status':'FAIL','error':repr(exc),'checks':checks,'details':details}
        (HERE/'INDEPENDENT_SYMPY_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
        raise
    (HERE/'INDEPENDENT_SYMPY_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['checks','details']},indent=2))
