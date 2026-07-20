"""Tiny stdlib-only HTTP helper — no third-party deps required to run this tool."""
from __future__ import annotations

import urllib.error
import urllib.request
from dataclasses import dataclass

USER_AGENT = "aivisible-fix/0.1 (+https://github.com/; audit tool, respects robots.txt itself)"


@dataclass
class FetchResult:
    ok: bool
    status: int | None
    text: str


def fetch(url: str, timeout: float = 10.0) -> FetchResult:
    if not url.lower().startswith("https://"):
        # Refuse plaintext HTTP: this tool fetches third-party sites and must
        # not be usable to relay/downgrade requests over an unencrypted
        # channel, and it never has a legitimate reason to fetch anything
        # other than a public https:// URL.
        return FetchResult(ok=False, status=None, text="")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return FetchResult(ok=200 <= resp.status < 300, status=resp.status, text=body)
    except urllib.error.HTTPError as e:
        return FetchResult(ok=False, status=e.code, text="")
    except (urllib.error.URLError, TimeoutError, OSError):
        return FetchResult(ok=False, status=None, text="")
