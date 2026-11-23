"""Timeline task p1b (early run): Taufik Hidayat test scrape.

Saves Taufik's Wikipedia page (EN) raw, parses every finals table into
data/clean/recon/taufik_wikipedia_finals.csv, and prints a short coverage
summary. Optionally also saves his BWF Tournament Software profile so the
two sources can be compared side by side.

Usage (from the repo root):
    python -m pipeline.recon.taufik_test_scrape
    python -m pipeline.recon.taufik_test_scrape --tsoft-url "https://bwf.tournamentsoftware.com/player-profile/<GUID>"
"""

from __future__ import annotations

import argparse
import sys

from pipeline.estafet.browser import save_with_browser
from pipeline.estafet.fetch import REPO_ROOT, Fetcher
from pipeline.estafet.wiki_finals import parse_finals

OUT_DIR = REPO_ROOT / "data" / "clean" / "recon"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Taufik Hidayat test scrape")
    ap.add_argument("--tsoft-url", help="Taufik's BWF Tournament Software player page (optional)")
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args(argv)

    f = Fetcher("recon")
    res = f.wikipedia("taufik-hidayat-wiki-en", "Taufik Hidayat", refresh=args.refresh)
    if res.error:
        print(f"Wikipedia fetch failed: {res.error}")
        return 1

    df = parse_finals(res.path.read_text(encoding="utf-8"), source_url=res.url)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "taufik_wikipedia_finals.csv"
    df.to_csv(out, index=False)

    print(f"Parsed {len(df)} rows -> {out.relative_to(REPO_ROOT)}\n")
    if not df.empty:
        print("Rows per section:")
        print(df.groupby(["section", "subsection"], dropna=False).size().to_string(), "\n")
        print("Scoring systems seen:")
        print(df["scoring_system"].value_counts().to_string(), "\n")
        print(f"Years covered: {int(df['year'].min())}-{int(df['year'].max())}")
        missing = df[df["n_games"] == 0]
        print(f"Rows with no game scores (walkovers, gaps): {len(missing)}")

    if args.tsoft_url:
        t = save_with_browser(f, "taufik-hidayat-tsoft", args.tsoft_url, refresh=args.refresh)
        print(f"\nTournament Software: {'saved ' + str(t.path) if t.path else 'FAILED: ' + str(t.error)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
