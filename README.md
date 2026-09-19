# An explicit 26-measurement frame in complex dimension eight

**Proof candidate.** This repository contains an explicit Gaussian-integer
8-by-26 frame and a self-contained proposed proof of its global phase-retrieval
property. The claim is **m_C(8) <= 26**, not that 26 is minimal. External
independent expert review and formal verification have not been completed.

## Read the argument

- [Proof candidate PDF](manuscript/PR26_Proof_Candidate.pdf)
- [Readable mathematical source](manuscript/proof_body.md)
- [Exact measurement matrix](PR26_FRAME_QI.json)
- [Verification status and provenance](PROVENANCE.md)

The construction represents a signal by a polynomial in a specified
eight-dimensional space. Three squared-modulus coefficients vanish, so
26 distinct positive evaluations determine the entire squared modulus.
After aligning the first coefficients of two possible signals, their average
and half-difference must be pointwise perpendicular in the real plane C.
Successive coefficient equations, ending with an invertible real symmetric
two-by-two matrix, force the difference to vanish.

The matrix supplied here evaluates the eight polynomials at t = 1,...,26.
Its orientation is eight signal coordinates by 26 measurement columns;
the measurement is |q_j^* x|^2. JSON integers must be read without converting
them to floating point.

## Reproduce the exact checks

Use Python 3.9 or newer. The original verifier needs only the standard library:

```sh
python3 scripts/verify.py
```

Expected: 336 polynomial checks, seven frame checks, and two negative controls
pass, with the mathematical payloads matching `evidence/`. The wrapper runs
in a temporary directory and does not overwrite the archived input or logs.

The separate symbolic implementation requires SymPy:

```sh
python3 -m pip install -r requirements-verification.txt
python3 scripts/verify.py --independent
```

Expected: the same checks plus 633 separately transcribed finite symbolic
checks. A check count is not a count of independently proved theorems.
The analytic sampling and case-coverage arguments are in the manuscript.

To rebuild the PDF from the included LaTeX sources:

```sh
python3 scripts/build_paper.py
```

This requires `pdflatex` and standard AMS/LaTeX packages. The rebuilt file is
written to `_build/PR26_Proof_Candidate.pdf`; the checked-in PDF is preserved.

## Scope

The proposed theorem applies to the displayed family at any 26 distinct
positive real sample points. It does not assert that all or generic sets of
26 vectors work, that 25 measurements are impossible, or that this integer
matrix is well conditioned for computation. No numerical tolerance or failure
to find a collision is used as the acceptance criterion of the proof.

The final proof does not rely on earlier unpublished curve-classification
or obstruction claims. Only the explicit polynomials, coefficient identities,
real inequalities and Rolle's theorem enter the argument.

## Citation and DOI

The manuscript is by Jihun Kim (Independent Researcher). Manuscript,
documentation and data are licensed CC BY 4.0; code is licensed MIT.
See [LICENSE.md](LICENSE.md) and [CITATION.cff](CITATION.cff).

The repository is prepared for a Zenodo archive of its first public release.
A DOI will be linked after the archived record has been verified.

See [publication preparation](docs/PUBLICATION.md) for the release checklist.

## Contributions

The mathematical exploration, manuscript preparation and verification used
substantial AI assistance. Local logical review and independent arithmetic
implementations are documented in `PROVENANCE.md`. They are not represented
as completed external peer review or proof-assistant certification.
