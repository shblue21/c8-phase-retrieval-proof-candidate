"""Replay final proof arithmetic with Python's standard library only.
Run from any directory: python3 path/to/code/run_final_checks.py
The optional Wolfram verification is stored separately, not invoked here.
"""
from pathlib import Path
import subprocess,sys,json,hashlib,time,platform
ROOT=Path(__file__).resolve().parents[1]

def stable_payload(obj):
 if isinstance(obj,dict):return {k:stable_payload(v) for k,v in obj.items() if k not in ('elapsed_seconds',)}
 if isinstance(obj,list):return [stable_payload(x) for x in obj]
 return obj

def main():
 result=[];started=time.monotonic()
 for name in ['verify_sparse_certificate.py','export_verify_frame.py','negative_controls.py']:
  cp=subprocess.run([sys.executable,str(ROOT/'code'/name)],cwd=ROOT,capture_output=True,text=True,check=False)
  (ROOT/'logs'/(name.removesuffix('.py')+'_final_stdout.txt')).write_text(cp.stdout+cp.stderr)
  result.append({'script':name,'return_code':cp.returncode})
  if cp.returncode:raise RuntimeError(f'{name} failed:\n{cp.stdout}\n{cp.stderr}')
 verified={}
 for name in ['sparse_certificate.json','frame_exact_checks.json','negative_controls.json']:
  data=json.loads((ROOT/'logs'/name).read_text());assert data['status']=='PASS'
  raw=json.dumps(stable_payload(data),sort_keys=True,separators=(',',':')).encode()
  verified[name]={'status':data['status'],'count':data.get('count',len(data['checks'])),'mathematical_payload_sha256':hashlib.sha256(raw).hexdigest()}
 output={'status':'PASS','python':platform.python_version(),'scripts':result,'verified':verified,
         'elapsed_seconds':time.monotonic()-started,'external_wolfram_rerun':False,
         'note':'A rerun of the same code is a reproducibility check, not a new independent mathematical verification.'}
 (ROOT/'logs/final_replay.json').write_text(json.dumps(output,indent=2));print(json.dumps(output,indent=2))
if __name__=='__main__':main()
