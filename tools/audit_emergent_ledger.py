"""Independent, offline evidence checks; never modifies or promotes the ledger."""
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from simulate_agent_dialogue import StrictArbiterEngine

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def audit():
    ledger = load('data/emergent_lexicon_audit.json')
    rows = ledger.get('candidates', ledger['approvedLexicon'])
    canon = load('data/lexicon.json')['vocabulary']
    extensions = load('data/translation_extensions.json')['entries']
    grammar = load('data/grammar_dictionary.json')['entries']
    base = canon + extensions + grammar
    by_root = defaultdict(list)
    for row in base:
        by_root[row['nrs'].lower()].append(row)
    root_groups = defaultdict(list)
    scenario_groups = defaultdict(list)
    for scenario in ledger.get('scenarios', []):
        scenario_groups[scenario['scenario_id']].append(scenario)
    glossary = defaultdict(list)
    for row in base:
        for gloss in re.split(r'[、／/]', row.get('meaningJa', '')):
            if gloss.strip():
                glossary[gloss.strip()].append(row['nrs'])
    details = []
    for row in rows:
        nrs = row['nrs'].lower()
        root_groups[nrs].append(row['id'])
        flags = []
        if not re.fullmatch(r'[aeiouylrmnszcjfvwhpbtdkg]{4,9}', nrs):
            flags.append('invalid_inventory_or_length')
        if not re.search(r'[aeiouy]', nrs) or re.search(r'[^aeiouy]{3,}|[aeiouy]{3,}', nrs):
            flags.append('vowel_or_cluster_failure')
        if nrs[-1] not in 'aeiouylrmns':
            flags.append('marked_coda_requires_review')
        if nrs in by_root:
            flags.append('exact_live_dictionary_collision')
        morphs = row.get('morphemes', [])
        if ''.join(morphs) != nrs:
            flags.append('nonconcatenative_formation_needs_rule')
        missing = [m for m in morphs if m not in by_root]
        if missing:
            flags.append('constituent_not_standalone_dictionary_entry')
        ja = row.get('meaningJa', '')
        if '身近な結びつき' in ja or 'の調和' in ja:
            flags.append('everyday_fallback_definition')
        if '統合作用' in ja or '固有現象' in ja:
            flags.append('specialized_fallback_definition')
        if 'の日常表現' in ja:
            flags.append('gloss_uniqueness_by_suffix')
        if re.search(r'[ぁ-んァ-ヶ一-龠]', row.get('meaningEn', '')):
            flags.append('japanese_in_english_gloss')
        if re.search(r'[a-z]{3}', row.get('example_ja', ''), re.I):
            flags.append('untranslated_term_in_japanese_example')
        if not row.get('example_ja'):
            flags.append('missing_japanese_example')
        overlap = {g.strip(): glossary[g.strip()] for g in re.split(r'[、／/]', ja) if g.strip() in glossary}
        if overlap:
            flags.append('exact_live_gloss_overlap_review')
        evidence = scenario_groups.get(row.get('scenario_id'), [])
        if not evidence:
            flags.append('missing_referenced_scenario')
        pattern = re.compile(r'\b' + re.escape(nrs) + r'(?:far|liv|ast|ar|cor|iin)?\b', re.I)
        turns = [t for s in evidence for t in s.get('turns', []) if pattern.search(t.get('nebulith', ''))]
        speakers = sorted({t.get('speaker', '') for t in turns})
        if len(speakers) < 2:
            flags.append('two_speaker_reuse_not_demonstrated_in_referenced_scenario')
        if row.get('pos') == '動' and re.search(r'\b(?:ia|uo)\s+\*?' + re.escape(nrs) + r'\b', row.get('example_sentence', ''), re.I):
            flags.append('verb_used_as_bare_case_complement_needs_rule')
        example = re.sub(r'\*?\b' + re.escape(nrs) + r'\b', '<TERM>', row.get('example_sentence', ''), flags=re.I)
        details.append({'id': row['id'], 'nrs': nrs, 'meaningJa': ja, 'pos': row.get('pos'),
                        'flags': flags, 'missingStandaloneConstituents': missing,
                        'exactGlossOverlaps': overlap, 'referencedScenarioSpeakers': speakers,
                        'exampleTemplate': example})
    counts = Counter(flag for row in details for flag in row['flags'])
    everyday = [r for r in rows if r.get('scenario_id', '').startswith('CONV-')]
    source_paths = ['data/emergent_lexicon_audit.json', 'data/lexicon.json',
                    'data/translation_extensions.json', 'data/grammar_dictionary.json',
                    'tools/simulate_agent_dialogue.py', 'tools/batch_colab_daily_conversation_expansion.py',
                    'tools/batch_colab_lexicon_expansion.py', 'tools/supplement_colab_lexicon.py',
                    'tools/studio_dictionary.py', 'tools/triage_feedback_queue.py',
                    'docs/Project Requirements And Design.md', 'tools/audit_emergent_ledger.py']
    engine = StrictArbiterEngine()
    probes = {
        'invalidSentenceAccepted': engine.gate5_syntactic_vso_frame('kelvas', ['nonsense el *kelvas']),
        'unverifiedReuseAccepted': engine.gate6_consensus_and_generational_reuse(True, 1),
        'sameConceptWithSuffixAccepted': engine.gate3_semantic_disjointness('水の日常表現')}
    return {'auditVersion': 1, 'createdAt': datetime.now(timezone.utc).isoformat(),
            'verdict': 'NOT_READY_FOR_PROMOTION',
            'scope': 'All rows mechanically checked; source-code inspection and semantic spot checks. No independent multilingual or human usability acceptance.',
            'sourceSha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in source_paths},
            'counts': {'rows': len(rows), 'uniqueRoots': len(root_groups), 'uniqueIds': len({r['id'] for r in rows}),
                       'canonical': len(canon), 'extensions': len(extensions), 'grammar': len(grammar),
                       'everyday': len(everyday), 'rejectedLog': len(ledger.get('rejectedLog', [])),
                       'scenarios': len(ledger.get('scenarios', []))},
            'declaredSummary': ledger.get('summary'), 'flagCounts': dict(sorted(counts.items())),
            'storedDistanceOneCount': sum(r.get('gates', {}).get('gate2_collision_distance', {}).get('min_distance') == 1 for r in rows),
            'arbiterDiagnosticProbes': probes,
            'duplicateRoots': {r: ids for r, ids in root_groups.items() if len(ids) > 1},
            'duplicateIds': {str(i): n for i, n in Counter(r['id'] for r in rows).items() if n > 1},
            'exampleTemplates': dict(Counter(r['exampleTemplate'] for r in details)),
            'everydayDomainCounts': dict(Counter(r.get('domain') for r in everyday)),
            'flagsAreNotAllRejections': 'Missing standalone constituents, overlapping glosses and nonconcatenative forms require explicit rules/review; these alone do not prove invalidity.',
            'entries': details}


if __name__ == '__main__':
    result = audit()
    target = ROOT / ('audit/maintenance/emergent-ledger-post-remediation-20261016.json' if load('data/emergent_lexicon_audit.json').get('schemaVersion') == '3.0.0' else 'audit/maintenance/emergent-ledger-independent-audit-20261016.json')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['verdict', 'counts', 'flagCounts', 'exampleTemplates']}, ensure_ascii=True, indent=2))
