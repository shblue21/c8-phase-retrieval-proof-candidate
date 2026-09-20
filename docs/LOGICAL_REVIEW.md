# Scope of the local logical review

This checklist records a local AI-assisted reading of the v2 proof. It is not
external expert review or proof-assistant verification. The reproducibility
scripts check algebraic identities and exact inputs; the arguments below are
read in the manuscript.

| Step | Claim and scope checked |
|---|---|
| Defined family | b,c are arbitrary real numbers, 0<s<1, m<0, gamma>0. det J=-8s, so the family is defined on both sides of the boundary. |
| Sampling | Degree at most 28, three missing coefficients, hence at most 26 nonzero terms. Rolle induction uses the actual term count and separates the single-term case. Nodes are distinct and positive. |
| Normalization | Zero polynomials are separated. Equal squared moduli give equal initial index and initial-coefficient modulus. Independent phase rotations and common nonzero scaling preserve the equality. |
| Case coverage | The possible equal-slope pairs are (0,2),(0,4),(0,6),(1,5),(2,4),(2,6),(4,6). Initial indices 3,5,6,7 end immediately. No generic-signal assumption is used. |
| Divisors and signs | Divisors are fixed nonzero parameter expressions. All scalar brackets have positive constant margins in the stated domain. R>=Delta>0, S<=-gamma<0 imply RS-T^2<0. |
| Restarts | For initial index 2, alpha4=0 kills the lower difference coefficients before restarting at 6. For index 0, alpha2=0 kills the coefficients before index 4. Higher free variables are retained until justified. |
| Necessity | The full polynomial identity yields collisions for b=0 and b!=0, at equality and strictly below c=b^2/s. In the strict b!=0 branch, monotonicity and endpoint signs give the unique root in (0,1/s); clearing denominators adds no root there. |
| Nonproportionality | Both candidate polynomials have constant coefficient 1 and their difference begins with a nonzero multiple of it^4. The t^8 tail inclusion transfers the ambiguity to the C8 family for all allowed m,gamma. |
| Actual frames | q_j=2 conjugate(p(t_j)), so |q_j*x|^2=4|f_x(t_j)|^2. The original specialization, sparse basis transformation, and both 208-entry matrices agree with the displayed definitions. |
| Kernel formulation | Both implications between phase retrieval and absence of nonzero rank-at-most-two Hermitian kernel elements are stated. Semidefinite elements are excluded using spanning. |

The revised executable copy of `parametric8.py` declares b,c merely real,
matching the theorem; s,m,g remain nonzero on its domain. The received code
is preserved in `sources/received_code/`. The family checker explicitly
rejects denominators involving b or c and denominators involving signal
coordinates. These assertions strengthen the same existing denominator checks
without changing the recorded 224 check-group count. The boundary and separate
transcription use real parameters and include zero-parameter branches.

The 224 and 11 result files record named assertions and pass/fail values;
they are not full symbolic proof objects. The separately transcribed 847-check
result also records substitutions and denominators. All implementations use
SymPy 1.14.0. Historical replay logs document the runs that produced them.
Fresh runs are identified by interpreter/version and source/output hashes in
`verification/REVIEW_FIX_RUN.json`.

`ARTIFACT_INTEGRITY.json` links the reviewed manuscript, checked-in PDF,
checker code and frame data by hashes. The CI configuration builds the LaTeX
and compares extracted text against the checked-in PDF. This detects stale
artifacts, not a mathematical error shared by the manuscript and code.
