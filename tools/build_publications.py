"""One command refreshes stable literary references, print editions and Web excerpts."""
from build_reviewed_codex import build_codex
from build_web_studio import build_web_studio

if __name__=='__main__':
    build_codex()
    build_web_studio()
