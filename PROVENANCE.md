# Mathematical and computational provenance — Version 2

The first release supplied an explicit C8/26 frame and a candidate proof.
Version 2 extends that construction to a five-parameter family, proves its
boundary within the stated parameter domain, and gives a twenty-term
representative. It does not include the higher-dimensional follow-up
candidates or the incomplete all-dimensions conjecture as theorems.

The original frame is retained byte-for-byte in `PR26_FRAME_QI.json` and
`data/v1_frame_gaussian_integer.json`. Its SHA256 is
`354fedefbbb0323ca506b65518fe1b09465aedf42d90fc26e32162b30ab09107`.
The new frame is `data/v2_sparse_frame_gaussian_integer.json`.

## Checks and their scope

The original family and boundary checkers were replayed in an isolated copy:
224 and 11 checks passed and their mathematical payloads agreed with the
source results. A new script transcribed the expanded family directly without
importing those checkers or their basis data. Its 847 assertions cover all
64 products at the three missing degrees, all 28 initial-index pairs, fixed
triangular pivots and substitutions, strict-sign identities, the full boundary
identity, both specializations, the invertible basis change, and all 416
Gaussian-integer entries across the two frames.

Both implementations use SymPy 1.14.0. Separate transcription is not a second
computer-algebra system or external expert review. The local logical review
covered the positive-root argument, signal normalization, every initial-index
case, nonzero divisors, justified restarts, the boundary and strict-interior
collision constructions, and the passage from polynomial bases to measurement
vectors. In the final copyedit, the Rolle induction was stated using the
actual number of monomials to treat the single-term case explicitly.

The files in `verification/` record v2 code and execution evidence. The
`verification/provided/data/` and `verification/independent/RESULT.json` files
are expected payloads used by the replay wrapper. `sources/` retains the
originally supplied sparse frame for comparison.
The original v1 code and evidence remain in `code/`, `independent/`, and
`evidence/`; their checks apply to the first fixed input. The stored v1 Wolfram
log was supplied with that research and was not rerun in the local review.

No numerical tolerance, random search, or failure to find a collision serves
as the proof criterion. External independent expert review and proof-assistant
verification have not been completed. The work used substantial AI assistance.
