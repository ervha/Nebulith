"""Current freshness of historical screening; changed entries never inherit coverage."""
from nebulith_data import entry_hash
from compare_all_roots import english_senses


def screening_state(vocabulary, historical):
    previous = {r['lexiconId']: r for r in historical['entries']}
    current = {r['id']: r for r in vocabulary}
    entries = []
    for ident, entry in current.items():
        old = previous.get(ident)
        fresh = bool(old and old['entryHash'] == entry_hash(entry))
        entries.append({'lexiconId': ident, 'entryHash': entry_hash(entry),
                        'historicalEntryHash': old['entryHash'] if old else None,
                        'status': 'historical-screening-current' if fresh else 'needs-source-and-semantic-review',
                        'uncoveredSenses': [] if fresh else english_senses(entry),
                        'semanticCertification': False})
    pending = [r['lexiconId'] for r in entries if r['status'] != 'historical-screening-current']
    return {'entries': entries, 'pendingIds': pending,
            'removedIds': sorted(previous.keys() - current.keys()),
            'historicalScreenedCount': len(entries) - len(pending),
            'currentInventoryComplete': True, 'screeningFresh': not pending,
            'semanticCertification': False}
