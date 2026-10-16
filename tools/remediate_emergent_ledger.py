"""Withdraw unsupported approvals and rebuild 500 learning entries from canonical sources."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = 'audit/maintenance/emergent-ledger-before-remediation-20261016.json'


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def dump(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def run():
    path = ROOT / 'data/emergent_lexicon_audit.json'
    old = json.loads(path.read_text(encoding='utf-8'))
    if old.get('schemaVersion') != '3.0.0':
        archive = ROOT / ARCHIVE
        if archive.exists() and archive.read_bytes() != path.read_bytes():
            raise ValueError('Existing audit snapshot differs; do not overwrite evidence')
        archive.write_bytes(path.read_bytes())
        report = json.loads((ROOT / 'audit/maintenance/emergent-ledger-independent-audit-20261016.json').read_text(encoding='utf-8'))
        if report['sourceSha256']['data/emergent_lexicon_audit.json'] != digest(ARCHIVE):
            raise ValueError('Independent audit does not describe this ledger')
        findings = {r['id']: r['flags'] for r in report['entries']}
        candidates = []
        for row in old['approvedLexicon']:
            original = dict(row)
            row = {k: v for k, v in row.items() if k not in ['gates', 'overall_score', 'gates_passed', 'gates_total', 'reused_by_partner']}
            row.update(approved=False, status='held', audit_status='REVIEW_REQUIRED',
                       human_audit_status='pending_review', previousAudit=original,
                       reviewIssues=findings[row['id']], bookEligible=False,
                       sourceSnapshot={'path': ARCHIVE, 'sha256': digest(ARCHIVE), 'id': row['id']})
            candidates.append(row)
        old.update(schemaVersion='3.0.0', auditPolicy='Evidence required; legacy six-gate scores do not grant approval',
                   legacySummary=old['summary'], approvedLexicon=[], candidates=candidates,
                   summary={'totalCandidates': len(candidates), 'totalApproved': 0,
                            'totalPendingReview': len(candidates), 'totalRejected': len(old['rejectedLog']),
                            'totalScenarios': len(old['scenarios']),
                            'totalRecorded': len(candidates) + len(old['rejectedLog'])},
                   remediation={'date': '2026-10-16', 'archive': ARCHIVE, 'archiveSha256': digest(ARCHIVE),
                                'reason': 'Unsupported semantic, syntax and consensus approvals withdrawn; no candidate promoted'})
        dump('data/emergent_lexicon_audit.json', old)

    canonical = json.loads((ROOT / 'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
    # Counts are editorial selection quotas, not frequency or independent linguistic approval.
    selection = [(16, 90), (12, 50), (13, 50), (11, 46), (15, 70), (14, 60), (4, 60), (6, 30), (9, 24), (10, 20)]
    entries = []
    for category, quota in selection:
        group = [r for r in canonical if r.get('category', '').startswith(str(category) + '.')]
        for row in group[:quota]:
            entries.append({k: row[k] for k in ['id', 'nrs', 'pos', 'meaningJa', 'meaningEn', 'category']})
    assert len(entries) == 500 and len({r['id'] for r in entries}) == 500
    dump('data/everyday_vocabulary_review.json', {
        'schemaVersion': 1, 'date': '2026-10-16', 'title': '暮らしの語彙500',
        'method': '既存正本の語義・品詞をそのまま再利用した分野別学習索引。新造語500件の承認ではない。',
        'source': 'data/lexicon.json', 'sourceSha256': digest('data/lexicon.json'),
        'reviewStatus': 'source-consistency-checked', 'newRoots': 0, 'entries': entries})
    dump('audit/maintenance/emergent-remediation-20261016.json', {
        'createdAt': datetime.now(timezone.utc).isoformat(), 'legacySnapshot': ARCHIVE,
        'legacySha256': digest(ARCHIVE), 'withdrawnApprovals': 1020, 'promotedRoots': 0,
        'regeneratedLearningEntries': len(entries), 'regeneratedNewRoots': 0,
        'ledgerSha256': digest('data/emergent_lexicon_audit.json'),
        'learningSha256': digest('data/everyday_vocabulary_review.json')})
    print('Withdrawn approvals: 1020; regenerated canonical learning entries: 500; promoted: 0')


if __name__ == '__main__':
    run()
