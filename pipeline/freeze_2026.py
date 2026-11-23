"""Timeline task s1: save a raw copy of every 2026-season source.

Usage (from the repo root):
    python -m pipeline.freeze_2026             # fetch whatever is missing
    python -m pipeline.freeze_2026 --refresh   # re-download everything
    python -m pipeline.freeze_2026 --dry-run   # just list the sources

Pages land in data/raw/2026/ with a manifest.csv recording the URL, time,
checksum and (for Wikipedia) the revision id of every page.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from pipeline.estafet.browser import save_with_browser
from pipeline.estafet.fetch import REPO_ROOT, Fetcher, wikipedia_suggest

CONFIG = REPO_ROOT / "config" / "freeze_2026.yaml"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--config", type=Path, default=CONFIG)
    ap.add_argument("--refresh", action="store_true", help="re-download pages already saved")
    ap.add_argument("--dry-run", action="store_true", help="list sources without fetching")
    args = ap.parse_args(argv)

    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    wiki = cfg.get("wikipedia") or []
    urls = cfg.get("urls") or []
    print(f"{len(wiki)} Wikipedia pages, {len(urls)} other URLs")
    if args.dry_run:
        for s in wiki:
            print(f"  wiki/{s.get('lang', 'en')}  {s['id']:<26} {s['title']}")
        for s in urls:
            print(f"  url{' (browser)' if s.get('browser') else '':<10} {s['id']:<26} {s['url']}")
        return 0

    f = Fetcher("2026")
    failed: list[str] = []

    for s in wiki:
        lang = s.get("lang", "en")
        res = f.wikipedia(s["id"], s["title"], lang=lang, refresh=args.refresh)
        if res.error:
            hint = wikipedia_suggest(f.session, s["title"], lang=lang)
            failed.append(f"{s['id']}: {res.error}. Closest titles: {hint or 'none found'}")
            print(f"  FAIL  {s['id']}")
        else:
            print(f"  {'cache' if res.from_cache else 'saved'} {s['id']}")

    for s in urls:
        if s.get("browser"):
            res = save_with_browser(f, s["id"], s["url"], refresh=args.refresh)
        else:
            res = f.get(s["id"], s["url"], refresh=args.refresh)
        if res.error:
            failed.append(f"{s['id']}: {res.error}")
            print(f"  FAIL  {s['id']}")
        else:
            print(f"  {'cache' if res.from_cache else 'saved'} {s['id']}")

    print(f"\nManifest: {f.manifest.relative_to(REPO_ROOT)}")
    if failed:
        print(f"\n{len(failed)} source(s) need attention:")
        for line in failed:
            print(f"  - {line}")
        return 1
    print("All sources saved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
