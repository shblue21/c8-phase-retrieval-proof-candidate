# Publication and reproducibility

Version 2 is a C8-focused revision of the first proof-candidate release.
The v2 release is archived at DOI 10.5281/zenodo.22860179 in the existing
record family. Its source archive matches the release commit byte for byte. Each archived version has a distinct DOI;
the concept DOI 10.5281/zenodo.22847199 identifies all versions.

The manuscript is a preprint/proof candidate, not a completed external peer
review or formal verification. `.zenodo.json` supplies the preprint metadata;
`CITATION.cff` records how to cite the manuscript and its research package.
The first version DOI is 10.5281/zenodo.22847200.

Author: Jihun Kim, Independent Researcher.
Paper, prose and data: CC BY 4.0. Build and verification code: MIT.

Reproduce current exact checks with `python scripts/verify.py`; optionally
include the preserved first-release checks with `--v1`. Rebuild the PDF with
`python scripts/build_paper.py` after installing TeX Live.

Official versioning guidance:
https://help.zenodo.org/docs/deposit/manage-versions/
