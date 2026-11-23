"""Polite, cached fetching of raw source pages.

Every page is saved untouched under data/raw/<bucket>/ and logged in that
bucket's manifest.csv (url, file, time, status, checksum), so any number in
the final story can be traced back to the exact page it came from.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw"

USER_AGENT = (
    "EstafetEmas/0.1 (badminton history research; "
    "+https://github.com/artcreatech/Estafet-Emas)"
)

MANIFEST_FIELDS = [
    "source_id",
    "kind",
    "url",
    "file",
    "fetched_at_utc",
    "http_status",
    "bytes",
    "sha256",
    "note",
]


def slugify(text: str, max_len: int = 80) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return text[:max_len] or "page"


@dataclass
class FetchResult:
    url: str
    path: Path | None
    status: int | None
    from_cache: bool
    error: str | None = None


class Fetcher:
    """Fetch pages with a per-host delay and a disk cache.

    A page that is already on disk is never downloaded again unless
    ``refresh=True``, so re-running a script is free and safe.
    """

    def __init__(self, bucket: str, delay_s: float = 3.0, timeout_s: float = 30.0):
        self.dir = RAW_DIR / bucket
        self.dir.mkdir(parents=True, exist_ok=True)
        self.manifest = self.dir / "manifest.csv"
        self.delay_s = delay_s
        self.timeout_s = timeout_s
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        self._last_hit: dict[str, float] = {}

    # -- internals -------------------------------------------------------
    def _wait_for_host(self, url: str) -> None:
        host = urlparse(url).netloc
        last = self._last_hit.get(host)
        if last is not None:
            wait = self.delay_s - (time.monotonic() - last)
            if wait > 0:
                time.sleep(wait)
        self._last_hit[host] = time.monotonic()

    def _log(self, row: dict) -> None:
        new = not self.manifest.exists()
        with self.manifest.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=MANIFEST_FIELDS)
            if new:
                w.writeheader()
            w.writerow({k: row.get(k, "") for k in MANIFEST_FIELDS})

    def _save(self, source_id: str, kind: str, url: str, body: bytes,
              suffix: str, status: int, note: str = "") -> Path:
        path = self.dir / f"{slugify(source_id)}{suffix}"
        path.write_bytes(body)
        self._log({
            "source_id": source_id,
            "kind": kind,
            "url": url,
            "file": path.relative_to(REPO_ROOT).as_posix(),
            "fetched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "http_status": status,
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "note": note,
        })
        return path

    # -- public API ------------------------------------------------------
    def get(self, source_id: str, url: str, kind: str = "url",
            suffix: str = ".html", refresh: bool = False) -> FetchResult:
        path = self.dir / f"{slugify(source_id)}{suffix}"
        if path.exists() and not refresh:
            return FetchResult(url, path, None, from_cache=True)
        self._wait_for_host(url)
        try:
            r = self.session.get(url, timeout=self.timeout_s)
        except requests.RequestException as e:
            return FetchResult(url, None, None, False, error=str(e))
        if r.status_code != 200:
            return FetchResult(url, None, r.status_code, False,
                               error=f"HTTP {r.status_code}")
        saved = self._save(source_id, kind, url, r.content, suffix, r.status_code)
        return FetchResult(url, saved, r.status_code, from_cache=False)

    def wikipedia(self, source_id: str, title: str, lang: str = "en",
                  refresh: bool = False) -> FetchResult:
        """Save a Wikipedia article's rendered HTML plus its revision id.

        Uses the MediaWiki parse API, which is the officially supported way
        to read article content by script. The revision id is stored in the
        manifest note so the exact version can be cited later.
        """
        path = self.dir / f"{slugify(source_id)}.html"
        if path.exists() and not refresh:
            return FetchResult(title, path, None, from_cache=True)
        api = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            "action": "parse",
            "page": title,
            "prop": "text|revid|displaytitle",
            "redirects": 1,
            "format": "json",
            "formatversion": 2,
        }
        self._wait_for_host(api)
        try:
            r = self.session.get(api, params=params, timeout=self.timeout_s)
            data = r.json()
        except (requests.RequestException, json.JSONDecodeError) as e:
            return FetchResult(title, None, None, False, error=str(e))
        if "error" in data:
            return FetchResult(title, None, r.status_code, False,
                               error=data["error"].get("info", "unknown error"))
        parse = data["parse"]
        page_url = f"https://{lang}.wikipedia.org/wiki/{parse['title'].replace(' ', '_')}"
        saved = self._save(
            source_id, f"wikipedia-{lang}", page_url,
            parse["text"].encode("utf-8"), ".html", r.status_code,
            note=f"revid={parse['revid']}",
        )
        return FetchResult(page_url, saved, r.status_code, from_cache=False)


def wikipedia_suggest(session: requests.Session, query: str, lang: str = "en",
                      limit: int = 5) -> list[str]:
    """Return article titles that best match ``query`` (for fixing wrong titles)."""
    try:
        r = session.get(
            f"https://{lang}.wikipedia.org/w/api.php",
            params={"action": "query", "list": "search", "srsearch": query,
                    "srlimit": limit, "format": "json", "formatversion": 2},
            timeout=30,
        )
        return [hit["title"] for hit in r.json()["query"]["search"]]
    except (requests.RequestException, KeyError, json.JSONDecodeError):
        return []
