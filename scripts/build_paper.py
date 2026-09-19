"""Compile the committed LaTeX without overwriting the checked-in PDF."""
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'_build'
out.mkdir(exist_ok=True)
for _ in range(2):
    subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',
                    '-output-directory',str(out),'proof_candidate.tex'],
                   cwd=ROOT/'manuscript',check=True)
shutil.copy2(out/'proof_candidate.pdf',out/'PR26_Proof_Candidate.pdf')
print(out/'PR26_Proof_Candidate.pdf')
