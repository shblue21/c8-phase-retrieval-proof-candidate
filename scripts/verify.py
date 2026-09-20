"""Replay the v2 C8 family, boundary and separately transcribed exact checks."""
from pathlib import Path
import argparse,subprocess,sys,json,tempfile,shutil
ROOT=Path(__file__).resolve().parents[1]
def stable(value):
 if isinstance(value,dict):return {k:stable(v) for k,v in value.items() if k not in {'seconds','elapsed_seconds'}}
 if isinstance(value,list):return [stable(v) for v in value]
 return value

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--v1',action='store_true',help='also replay the retained v1 checks')
 parser.add_argument('--independent',action='store_true',help='compatibility option: v2 always runs both transcriptions')
 args=parser.parse_args()
 with tempfile.TemporaryDirectory(prefix='pr26-v2-') as td:
  work=Path(td)
  for rel in ['data','sources','verification/provided/code','verification/provided/data','verification/independent']:
   shutil.copytree(ROOT/rel,work/rel,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
  for script in ['verification/provided/code/verify_parametric8.py','verification/provided/code/verify_sharp_boundary.py','verification/independent/check_c8_family.py']:
   subprocess.run([sys.executable,str(work/script)],cwd=work,check=True)
  for rel in ['verification/provided/data/parametric8_checks.json','verification/provided/data/sharp_boundary_checks.json','verification/independent/RESULT.json']:
   if stable(json.loads((work/rel).read_text()))!=stable(json.loads((ROOT/rel).read_text())):raise AssertionError('Mathematical payload mismatch: '+rel)
  for rel in ['data/v2_sparse_frame_gaussian_integer.json','verification/provided/data/sparse8_frame_gaussian_integer.json']:
   if (work/rel).read_bytes()!=(ROOT/rel).read_bytes():raise AssertionError('Frame bytes mismatch: '+rel)
  if (ROOT/'data/v1_frame_gaussian_integer.json').read_bytes()!=(ROOT/'PR26_FRAME_QI.json').read_bytes():raise AssertionError('Original frame copy differs')
 if args.v1:subprocess.run([sys.executable,str(ROOT/'scripts/verify_v1.py'),'--independent'],check=True,cwd=ROOT)
 print('PASS: v2 family 224, boundary 11, separate transcription 847; payloads and exact frames agree.')
if __name__=='__main__':main()
