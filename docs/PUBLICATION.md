# First public release preparation

This is the unnumbered Proof Candidate. No release or DOI is claimed by the
presence of these files. The publication record must describe it as a preprint
or proof candidate, with the exact validation scope in `PROVENANCE.md`.

Before the first public release:

1. Confirm the author list, affiliation/contact details, and file-specific
   licenses. Reflect the same attribution in the PDF, `CITATION.cff`, and
   `.zenodo.json`.
2. Run `python scripts/verify.py --independent` from a clean checkout and check
   the PDF/source pair. Exclude private exploratory files and local paths.
3. Publish the repository under the confirmed GitHub owner and name.
4. Connect that public repository in the author's Zenodo GitHub settings.
5. Create the first public GitHub release only after the connection and
   metadata are correct. The first release needs a Git tag; no pre-release
   version number is assigned by this draft.
6. Wait for Zenodo to archive that release, then verify the actual files,
   authors, resource type and DOI on the resulting record. Add the real DOI
   to the repository citation and links. Do not invent a DOI in advance.

Zenodo uses `.zenodo.json` in preference to `CITATION.cff` when both are present.
The candidate paper and its reproduction material are to be archived together
as a preprint package, using `upload_type: publication` and
`publication_type: preprint` in `.zenodo.json`.

Official guides:

- https://help.zenodo.org/docs/github/enable-repository/
- https://help.zenodo.org/docs/github/describe-software/zenodo-json/
- https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content

DOI registration is an archival and citation step, not mathematical peer review.
