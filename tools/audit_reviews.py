"""Evidence completeness checks; missing reviews never count as approvals."""
import hashlib
from fontTools.pens.svgPathPen import SVGPathPen
from nebulith_data import ROOT, entry_hash


def coda_review(vocab, records):
    marked = {r['id']: r for r in vocab if r['nrs'][-1] not in 'aeiouylrnms'}
    rows = records.get('entries', [])
    errors, approved, rejected, pending = [], [], [], []
    seen = set()
    for row in rows:
        id_ = row.get('lexiconId')
        if id_ in seen or id_ not in marked:
            errors.append({'id': id_, 'error': 'duplicate or unexpected entry'})
            continue
        seen.add(id_)
        source = marked[id_]
        if row.get('nrs') != source['nrs'] or row.get('finalConsonant') != source['nrs'][-1] or row.get('reviewedAgainstEntryHash') != entry_hash(source):
            errors.append({'id': id_, 'error': 'stale entry review'})
            continue
        decision = row.get('decision')
        if decision in ['approved', 'rejected']:
            allowed = ['SOP.CHK08.hard', 'SOP.CHK08.impulsive'] if decision == 'approved' else ['SOP.CHK08.neither']
            if not row.get('reason') or not row.get('reviewer') or row.get('ruleId') not in allowed:
                errors.append({'id': id_, 'error': 'missing semantic evidence or unsupported rule'})
                continue
            (approved if decision == 'approved' else rejected).append(id_)
        elif decision == 'pending':
            pending.append(id_)
        else:
            errors.append({'id': id_, 'error': 'unknown decision'})
    missing = sorted(marked.keys()-seen)
    lower_bound = (len(vocab)-len(marked)+len(approved))/len(vocab)
    complete = not errors and not missing and not pending
    return {'approved': approved, 'rejected': rejected, 'pending': pending,
            'missing': missing, 'errors': errors, 'complete': complete,
            'verifiedLowerBound': lower_bound, 'complianceRate': lower_bound if complete else None}


def glyph_review(font, font_sha, records):
    names = font.getGlyphOrder()
    rows = records.get('entries', [])
    errors = []
    if records.get('comparisonScope') != 'corresponding-codepoint':
        errors.append('comparison scope must match the user policy: corresponding codepoint only')
    if records.get('fontSha256') != font_sha:
        errors.append('font hash changed')
    criteria_sha = records.get('criteriaSha256')
    if criteria_sha and criteria_sha != hashlib.sha256((ROOT / 'audit/docs/Nebulith Standard Audit Report.md').read_bytes()).hexdigest():
        errors.append('glyph review criteria changed')
    if len(rows) != len(names) or set(r.get('glyph') for r in rows) != set(names):
        errors.append('glyph inventory mismatch')
    approved, rejected, pending, functional = [], [], [], []
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    for row in rows:
        if row.get('codepoints') != [c for c, g in cmap.items() if g == row.get('glyph')]:
            errors.append('cmap mismatch: '+str(row.get('glyph')))
        decision = row.get('decision')
        if decision in ['approved', 'rejected']:
            name = row.get('glyph')
            if decision == 'approved':
                evidence = row.get('approvalEvidence', {})
                if (evidence.get('scope') != 'corresponding-codepoint' or evidence.get('sameCharacterCompared') is not True
                        or evidence.get('styleCompared') is not True or evidence.get('fontSha256') != font_sha):
                    errors.append('missing corresponding-character/style approval evidence: '+str(name))
                    continue
            if name not in glyph_set:
                errors.append('unknown glyph: '+str(name))
                continue
            pen = SVGPathPen(glyph_set)
            glyph_set[name].draw(pen)
            outline_sha = hashlib.sha256(pen.getCommands().encode()).hexdigest()
            reference = row.get('comparisonReference', '')
            reference_path = (ROOT / reference.split('#')[0]).resolve()
            if (row.get('outlineSha256') != outline_sha or ROOT / 'audit/comparisons' not in reference_path.parents
                    or not reference_path.is_file() or reference.split('#')[-1] != 'glyph-'+name):
                errors.append('stale or missing comparison: '+str(name))
                continue
            if not all(row.get(k) for k in ['reason', 'reviewer', 'comparisonReference']) or not records.get('criteriaVersion'):
                errors.append('missing comparison evidence: '+str(row.get('glyph')))
                continue
            (approved if decision == 'approved' else rejected).append(row['glyph'])
        elif decision == 'functional':
            name = row.get('glyph')
            evidence = row.get('functionalEvidence', {})
            valid = name in ['space', '.notdef'] and evidence.get('fontSha256') == font_sha
            if valid:
                valid = font['hmtx'][name][0] > 0 and row.get('reviewer') and row.get('reason')
                valid = valid and ((name=='space' and font['glyf'][name].numberOfContours==0)
                                   or (name=='.notdef' and font['glyf'][name].numberOfContours>0))
            if not valid:
                errors.append('invalid functional glyph exemption: '+str(name))
            else:
                functional.append(name)
        elif decision == 'pending':
            pending.append(row['glyph'])
        else:
            errors.append('unknown decision')
    return {'errors': errors, 'approved': approved, 'functional': functional, 'rejected': rejected,
            'pending': pending, 'complete': not errors and not pending}
