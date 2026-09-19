"""Replay the checked-in exact proof checks in an isolated temporary copy."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]

def stable(value):
    if isinstance(value,dict):
        return {k:stable(v) for k,v in value.items() if k!='elapsed_seconds'}
    if isinstance(value,list):
        return [stable(v) for v in value]
    return value

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--independent',action='store_true')
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='pr26-check-') as temporary:
        work=Path(temporary)
        shutil.copytree(ROOT/'code',work/'code')
        (work/'logs').mkdir()
        subprocess.run([sys.executable,str(work/'code/run_final_checks.py')],check=True,cwd=work)
        for name in ['sparse_certificate.json','frame_exact_checks.json','negative_controls.json']:
            expected=json.loads((ROOT/'evidence'/name).read_text())
            actual=json.loads((work/'logs'/name).read_text())
            if stable(expected)!=stable(actual):
                raise AssertionError('Mathematical payload changed: '+name)
        if (ROOT/'PR26_FRAME_QI.json').read_bytes()!=(work/'PR26_FRAME_QI.json').read_bytes():
            raise AssertionError('Regenerated matrix does not match the supplied matrix')
        if args.independent:
            shutil.copytree(ROOT/'independent',work/'independent')
            subprocess.run([sys.executable,str(work/'independent/independent_sympy_check.py')],check=True,cwd=work)
            actual=json.loads((work/'independent/INDEPENDENT_SYMPY_RESULT.json').read_text())
            expected=json.loads((ROOT/'evidence/independent_sympy_result.json').read_text())
            for key in ['status','checks_count','checks','details']:
                if actual[key]!=expected[key]:
                    raise AssertionError('Independent check differs: '+key)
        print('PASS: exact input and mathematical payloads match the archived evidence.')

if __name__=='__main__':
    main()
