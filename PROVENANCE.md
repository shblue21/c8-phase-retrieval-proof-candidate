# Mathematical and computational status

The proof candidate was supplied on 19 September 2026 with an explicit
Gaussian-integer frame, a self-contained English argument, standard-library
verification code, and an additional Wolfram log.

The original matrix JSON has SHA256:

```text
354fedefbbb0323ca506b65518fe1b09465aedf42d90fc26e32162b30ab09107
```

The original proof source has SHA256:

```text
a4db968909ef34069e94afe9d4ffe60ea4647ba9f259453bc568656da6d9ab81
```

The public manuscript is an expository revision: it explains the construction,
the fixed-average real-linear map, and the final two-by-two determinant before
and alongside the full coefficient calculations. Original equations (1)-(15)
and their mathematical content are retained. The source proof and private
research history are preserved separately; they are not required to run this
package.

## Checks already performed

- The supplied standard-library verifier was rerun in an isolated directory:
  336 polynomial checks, seven matrix checks, and two negative controls passed.
  Its stable mathematical payloads agreed with the supplied logs.
- An independently transcribed SymPy implementation, importing no supplied
  verifier code, recomputed the basis products, all first-index pairs, the
  coefficient eliminations, strict-sign identities, and 208 matrix entries.
  Its 633 finite checks passed.
- Local logical review covered positive sampling, phase normalization, all
  first-index cases, zero signals, zero measurements, repeated roots, common
  factors, constant denominators, and the connection to the physical frame.
- The stored Wolfram output was supplied with the research. It was not rerun
  in the local review. The `.wl` input is included for further examination.

These are arithmetic reproductions and local review, not completed external
independent specialist review or a formal proof. A numerical search is not
part of the final acceptance criterion.

The original archive contained 97 files including its manifest; the accompanying
message referred to 201 files. The received manifest's 96 entries all matched.
The discrepancy was recorded; the core proof, matrix and verification scripts
were present. This repository contains a deliberately selected public package,
not the full exploration archive.

The manuscript, discovery and exact-check implementation were developed with
substantial AI assistance. Attribution and licensing are specified separately
in the finalized citation and license files.
