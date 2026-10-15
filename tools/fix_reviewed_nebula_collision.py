"""Resolve reviewed nebula/nebulis similarity; preserve different-meaning roots."""
import json
from nebulith_data import ROOT,dump,export_lexicon,entry_hash


def main():
    p=ROOT/'data/lexicon.json';data=json.loads(p.read_text(encoding='utf-8'))
    row=next(r for r in data['vocabulary'] if r['id']==37)
    if row['nrs']=='kyrven':return
    if row['nrs'] not in ['nebulis','nyvel'] or any(r['nrs']=='kyrven' for r in data['vocabulary']):raise ValueError('Unexpected source or duplicate target')
    previous=ROOT/'data/audit/nebula_root_migration.json'
    before=json.loads(previous.read_text(encoding='utf-8'))['before'] if previous.exists() else dict(row)
    row['nrs']='kyrven';row['ipa']='[kyr.ven]'
    derivative=next(r for r in data['vocabulary'] if r['id']==38)
    old_note=derivative['notes'];derivative['notes']='kyrven ＋ 微小環（旧語幹 nebu- を保持）'
    data['version']='23.4';export_lexicon(data)
    dump(ROOT/'data/audit/nebula_root_migration.json',{'before':before,'after':row,
      'reason':'星雲のnebulisとIAU OAEのNebula/Nebulosaは意味が一致し編集距離2。語形も近いためkyrvenへ変更。',
      'rejectedTrial':{'nrs':'nyvel','reason':'German Nebel remains at distance 2; rejected after recheck.'},
      'source':'https://astro4edu.org/resources/glossary/term-detail/211/','reviewer':'Codex',
      'noteUpdate':{'lexiconId':38,'before':old_note,'after':derivative['notes']},
      'preserved':['neburil: protoplanetary disk, different meaning','nebulin: purple, adjective','Nebulith: project name']})


if __name__=='__main__':main()
