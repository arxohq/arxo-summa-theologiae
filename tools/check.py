#!/usr/bin/env python3
"""Addressed consumer checks for the 28 explicitly listed Summa models only."""
import argparse,hashlib,json,os,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(law,*args):
 p=subprocess.run([law,*map(str,args)],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stdout+'\n'+p.stderr)
 return json.loads(p.stdout)
def verify_bytes(row):
 b=(ROOT/row['path']).read_bytes();assert len(b)==row['size'] and 'sha256:'+hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--law',default=os.environ.get('LAW_BIN','law'));p.add_argument('--examples-only',action='store_true');a=p.parse_args();version=run(a.law,'version','--json');assert version['tool']==json.loads((ROOT/'toolchain.lock.json').read_text())['tool'],'CLI version differs from tested pin'
 for row in json.loads((ROOT/'source-pin.json').read_text())['files']:verify_bytes(row)
 for row in json.loads((ROOT/'CANON-MANIFEST.json').read_text())['files']:verify_bytes(row)
 models=json.loads((ROOT/'models.json').read_text());bySlug={m['slug']:m for m in models};total=0
 for m in models:
  raw=(ROOT/m['world']).read_bytes();assert 'sha256:'+hashlib.sha256(raw).hexdigest()==m['worldSha256'];d=json.loads(raw);assert d['package']['name']+'@'+d['package']['version']==m['spec'];assert not d.get('imports')
  if not a.examples_only:
   files=sorted((ROOT/'packages'/m['slug']/'tests').rglob('*.lawtest'))
   with tempfile.TemporaryDirectory(prefix='summa-tests-') as tmp:
    f=Path(tmp)/'tests.json';f.write_text(json.dumps([str(x) for x in files]));d=run(a.law,'engine','test',f,'--lawtest-list','--program',ROOT/m['world'],'--json');assert d['failed']==0 and d['total']>0;total+=d['total'];print('PACKAGE PASS',m['spec'],d['passed'])
 for row in json.loads((ROOT/'examples/index.json').read_text()):
  folder=ROOT/'examples'/row['name'];req=json.loads((folder/'request.json').read_text());assert req['ir']==json.loads((ROOT/bySlug[row['slug']]['world']).read_text()),row['name']+' world differs';assert req['case']==json.loads((folder/'case.json').read_text());assert req['query']==json.loads((folder/'query.json').read_text());expected=json.loads((folder/'result.json').read_text());assert run(a.law,'eval',folder)==expected,row['name'];assert run(a.law,'eval',folder)==expected,row['name']+' repeat';print('REPLAY PASS',row['name'],expected['resultHash'])
 cases={name:json.loads((ROOT/'examples'/name/'case.json').read_text()) for name in ['traveller-defense','defense-awaits-judgment','excessive-defense']}
 def moderation(case):return [x for x in case['assertions'] if x['literal']['predicate'].endswith('#vis_moderata')]
 assert moderation(cases['traveller-defense'])[0]['origin']=='adjudicated';assert not moderation(cases['defense-awaits-judgment']);assert moderation(cases['excessive-defense'])[0]['origin']=='adjudicated' and moderation(cases['excessive-defense'])[0]['literal']['polarity']=='negative'
 with tempfile.TemporaryDirectory(prefix='summa-native-ask-') as tmp:
  actual=run(a.law,'ask',ROOT/'cases/moral-cases','--case','ViatorContraLatronem','--query-json',ROOT/'cases/moral-cases/queries/viator-defensio-licita.json','--out',tmp);assert actual['results'][0]['truthStatus']=='TRUE_ONLY' and actual['results'][0]['evaluationStatus']=='COMPUTED';assert run(a.law,'eval',tmp)==actual;print('NATIVE ASK / REPLAY PASS')
 inspect=run(a.law,'inspect',ROOT/'examples/traveller-defense/result.json','summary');assert inspect['ok'];print('INSPECT PASS; models',len(models),'scenarios',total,'(0 when examples-only)')
if __name__=='__main__':main()
