"""Parse the finals/achievements tables on a Wikipedia player page.

Wikipedia badminton player pages list finals in small tables with columns
like ``Year | Venue | Opponent | Score | Result`` (majors) or
``Year | Tournament | Opponent | Score | Result`` (tour events), each under a
heading such as "World Championships" or "BWF Grand Prix". This module turns
all of them into one tidy table, one row per final or medal match.
"""

from __future__ import annotations

import re
from io import StringIO

import pandas as pd
from bs4 import BeautifulSoup

DASH = re.compile(r"[–—−-]")
GAME = re.compile(r"(\d+)\s*[–—−-]\s*(\d+)")
FOOTNOTE = re.compile(r"\[[^\]]*\]")

OUT_COLUMNS = [
    "section", "subsection", "year", "event", "venue_or_level", "partner",
    "opponent", "score_raw", "games", "n_games", "scoring_system",
    "walkover", "retired", "result", "source_url",
]


def _clean(text) -> str:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    return FOOTNOTE.sub("", str(text)).replace("\xa0", " ").strip()


def parse_score(raw: str) -> dict:
    """Split a score like '15–11 5–15 7–1 retired' into games and flags."""
    raw = _clean(raw)
    low = raw.lower()
    games = [(int(a), int(b)) for a, b in GAME.findall(raw)]
    return {
        "games": games,
        "n_games": len(games),
        "walkover": "walkover" in low or low in {"w/o", "wo"},
        "retired": "retired" in low or "ret." in low,
    }


def infer_scoring_system(games: list[tuple[int, int]], retired: bool = False) -> str:
    """Guess the scoring system from game scores.

    Uses the highest winning score among completed games:
      <=8 -> 5 games to 7 (IBF trial, 2001-02), 9-13 -> side-out to 11
      (women's singles before 2006), 14-18 -> side-out to 15,
      19+ -> rally point to 21 (from 2006).
    Returns 'unknown' when there is nothing to go on.
    """
    done = games[:-1] if retired else games
    winners = [max(a, b) for a, b in done]
    if not winners:
        return "unknown"
    top = max(winners)
    if top <= 8:
        return "side_out_7x5"
    if top <= 13:
        return "side_out_11"
    if top <= 18:
        return "side_out_15"
    return "rally_21"


def _section_for(table) -> tuple[str, str]:
    """Nearest headings above a table: (section, subsection)."""
    h3 = table.find_previous(["h3"])
    h4 = table.find_previous(["h4"])
    sec = _clean(h3.get_text(" ")) if h3 else ""
    sub = ""
    # Only use the h4 if it sits after the h3 (i.e. belongs to it).
    if h4 is not None and (h3 is None or h4.find_previous(["h3"]) is h3):
        sub = _clean(h4.get_text(" "))
    return sec, sub


def _flatten_cols(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[-1] for c in df.columns]
    df.columns = [_clean(c).lower() for c in df.columns]
    return df


def parse_finals(html: str, source_url: str = "") -> pd.DataFrame:
    soup = BeautifulSoup(html, "lxml")
    rows: list[dict] = []
    for table in soup.select("table.wikitable"):
        try:
            df = pd.read_html(StringIO(str(table)))[0]
        except ValueError:
            continue
        df = _flatten_cols(df)
        cols = set(df.columns)
        if not {"opponent", "score", "result"} <= cols:
            # Not a finals table (e.g. performance timeline or H2H list).
            continue
        if "year" not in cols and "round" not in cols:
            continue
        section, subsection = _section_for(table)
        for rec in df.to_dict("records"):
            score = parse_score(rec.get("score", ""))
            year_txt = _clean(rec.get("year", ""))
            year_m = re.search(r"\d{4}", year_txt)
            rows.append({
                "section": section,
                "subsection": subsection,
                "year": int(year_m.group()) if year_m else None,
                "event": _clean(rec.get("tournament", "")) or section,
                "venue_or_level": _clean(rec.get("venue", "")) or _clean(rec.get("level", "")),
                "partner": _clean(rec.get("partner", "")),
                "opponent": _clean(rec.get("opponent", "")) or _clean(rec.get("opponents", "")),
                "score_raw": _clean(rec.get("score", "")),
                "games": " ".join(f"{a}-{b}" for a, b in score["games"]),
                "n_games": score["n_games"],
                "scoring_system": infer_scoring_system(score["games"], score["retired"]),
                "walkover": score["walkover"],
                "retired": score["retired"],
                "result": _clean(rec.get("result", "")),
                "source_url": source_url,
            })
    return pd.DataFrame(rows, columns=OUT_COLUMNS)
