"""Check the reviewed source/PDF/data snapshot; this is not a proof verifier."""
from pathlib import Path
import hashlib,json,argparse,re,subprocess,unicodedata
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pdf_text(p):
 text=subprocess.check_output(['pdftotext',str(p),'-'],text=True)
 return re.sub(r'\s+','',unicodedata.normalize('NFKC',text))
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--rebuilt-pdf',type=Path);a=parser.parse_args()
 manifest=json.loads((ROOT/'ARTIFACT_INTEGRITY.json').read_text())
 for f in manifest['files']:
  p=ROOT/f['path']
  if not p.is_file() or digest(p)!=f['sha256']:raise AssertionError('Reviewed artifact changed: '+f['path'])
 source=(ROOT/manifest['main_tex']).read_text()
 for rel in manifest['included_tex']:source+='\n'+(ROOT/rel).read_text()
 if 'KimV1' in source:raise AssertionError('Earlier version must be a version note, not a bibliography entry')
 defs=set(re.findall(r'\\label\{([^}]+)\}',source));refs=set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',source))
 if refs-defs:raise AssertionError('Undefined LaTeX references: '+str(refs-defs))
 bibs=set(re.findall(r'\\bibitem\{([^}]+)\}',source));cites={k for group in re.findall(r'\\cite\{([^}]+)\}',source) for k in group.split(',')}
 if cites-bibs:raise AssertionError('Undefined citations: '+str(cites-bibs))
 if a.rebuilt_pdf:
  if pdf_text(ROOT/manifest['pdf'])!=pdf_text(a.rebuilt_pdf.resolve()):raise AssertionError('Rebuilt PDF text differs from checked-in PDF')
 print('PASS: reviewed source/PDF/data hashes and references'+('; rebuilt PDF text agrees' if a.rebuilt_pdf else ''))
if __name__=='__main__':main()
