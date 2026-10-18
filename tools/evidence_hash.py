"""Match legacy text digests without accepting content changes or binary variants."""
import hashlib
from pathlib import Path

TEXT_SUFFIXES = {'.json', '.jsonl', '.md', '.py', '.html', '.csv', '.kt', '.txt', '.log'}


def recorded_digest_matches(path, expected):
    path = Path(path)
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() == expected:
        return True
    if path.suffix not in TEXT_SUFFIXES or b'\0' in raw:
        return False
    try:
        raw.decode('utf-8')
    except UnicodeDecodeError:
        return False
    # The recorded Windows digest can be reconstructed only by changing LF to CRLF.
    # Whitespace, JSON formatting, Unicode and the trailing newline stay significant.
    crlf = raw.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
    return hashlib.sha256(crlf).hexdigest() == expected
