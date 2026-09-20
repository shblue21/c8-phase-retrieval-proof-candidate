# Explicit phase retrieval in complex dimension eight — Version 2

**Proof candidate; not peer reviewed.** Version 2 gives a five-parameter family
of explicit 26-measurement frames, its exact success/failure boundary, and a
representative defined by twenty polynomial terms. The result is
**m_C(8) <= 26**. Minimality and numerical stability are not established.

## Manuscript and inputs

- [Version 2 PDF](manuscript/PR26_Proof_Candidate.pdf)
- [LaTeX source](manuscript/proof_candidate.tex)
- [Exact coefficient substitutions](manuscript/coefficient_substitutions.tex)
- [Twenty-term representative: 8-by-26 Gaussian-integer frame](data/v2_sparse_frame_gaussian_integer.json)
- [Original frame, retained without changes](data/v1_frame_gaussian_integer.json)
- [Changes from the first release](CHANGELOG.md)
- [Verification and provenance](PROVENANCE.md)

For real b,c and 0<s<1, m<0, gamma>0, the family in the manuscript gives
phase retrieval precisely when c>b²/s. Any 26 distinct positive real sampling
points work in that region. Outside it, the manuscript constructs pairs with
identical squared moduli on the entire real line.

The first release is the specialization (1,4,1/2,-2,1). The twenty-term example
uses (0,1,1/2,-1,1) followed by the displayed invertible basis transformation.
Both frames use q_j = 2 conjugate(p(j)), with the appropriate displayed basis.
They are different inputs and have separate data files. Read the integer JSON
entries without conversion to floating point.

## Reproduce the checks

Use Python 3.9 or newer and SymPy 1.14.0:

```sh
python3 -m pip install -r requirements-verification.txt
python3 scripts/verify.py
```

The command uses a temporary copy and checks:

- 224 family identities/checks;
- 11 boundary identities;
- 847 assertions in a separately transcribed implementation;
- agreement with the archived mathematical payloads and both frame inputs.

Both transcriptions use SymPy. These are finite exact arithmetic checks, not
external expert review or proof-assistant certification. The inequalities,
coverage of all cases, restart arguments, and nonproportionality are proved
in the manuscript. Counts are documented execution units, not separate theorems.

The original v1 code and evidence remain in `code/`, `independent/`, and
`evidence/`. They concern the original fixed frame. To replay them as well:

```sh
python3 scripts/verify.py --v1
```

To build the manuscript with `pdflatex`:

```sh
python3 scripts/build_paper.py
```

The output is `_build/PR26_Proof_Candidate.pdf`; the checked-in PDF is preserved.
To check the reviewed source/PDF/data snapshot and compare PDF text:

```sh
python3 scripts/check_artifact_integrity.py --rebuilt-pdf _build/PR26_Proof_Candidate.pdf
```

This requires Poppler's `pdftotext`. The check detects stale files and unresolved
references; it is not a formal proof or a semantic parser of all formulas.
See the [logical-review checklist](docs/LOGICAL_REVIEW.md).

## Citation and versions

Author: Jihun Kim, Independent Researcher.

- Version 2 release and version-specific DOI: not yet created.
- [All versions on Zenodo](https://doi.org/10.5281/zenodo.22847199)
- [First release DOI](https://doi.org/10.5281/zenodo.22847200)

The concept DOI links the archived version history; it is not a version-specific
DOI for this v2 draft. Cite the repository/commit until v2 is archived.
Version 2 is prepared for release; the version-specific DOI will be linked
once the archival record is confirmed.
DOI registration preserves an identifiable research artifact; it does not
constitute mathematical peer review.

The research, exposition and computational checks used substantial AI
assistance. External expert review and formal verification remain incomplete.
Paper, prose and data: CC BY 4.0. Code: MIT. See [LICENSE.md](LICENSE.md)
and [CITATION.cff](CITATION.cff).
