# Recon notes

Early findings from reading the sources, ahead of the January recon phase
(timeline tasks s1 and p1b). Checked 23 Nov 2026 by reading the pages in a
browser-like fetch; the scripts in `pipeline/` have not yet been run against
the live sites.

## 2026 season (data freeze, s1)

- The **2026 BWF World Tour** Wikipedia page runs 6 Jan – 13 Dec 2026. On
  23 Nov its results stopped around mid-September (Vietnam Open). Later
  events (Japan Masters, Hong Kong Open, Syed Modi, Kaohsiung, Guwahati,
  Odisha Masters) had no champions listed yet. Abu Dhabi Masters is marked
  cancelled.
- The **2026 BWF World Tour Finals** article did not exist yet (red link).
  So the freeze run should wait until after 13 Dec, and probably a few days
  more for Wikipedia editors to fill in results.
- Because Wikipedia lags, BWF Tournament Software should be the primary
  source for the late-season events. Add those result pages to
  `config/freeze_2026.yaml` under `urls:` with `browser: true`.

## Taufik Hidayat on Wikipedia (p1b)

- Finals tables are clean and consistent: `Year | Venue | Opponent | Score |
  Result` for majors (Olympics, World Champs, World Cup, Asian Games, Asian
  Champs, SEA Games, Asian Juniors) and `Year | Tournament | Opponent | Score
  | Result` for tour events (Superseries, Grand Prix). About 50 finals or
  medal matches, 1997–2011.
- Olympic tables are round by round (2000, 2004, 2008, 2012), so the
  Olympics give a full match log even before Tournament Software coverage.
- **New scoring system to model:** the 2001 Singapore Open final reads
  `7–5 0–7 7–1 1–7 7–4`, the IBF's 2001–02 trial of five games to 7 points.
  The spec's `scoring_system` field needs a value for it; the parser uses
  `side_out_7x5`.
- Retirements and walkovers appear inline in the score text
  (`15–11 5–15 7–1 retired`, `Walkover`). The parser flags both.
- "Grand Prix" on Wikipedia covers the old IBF World Grand Prix (pre-2007)
  and the BWF Grand Prix / Grand Prix Gold (2007+). Tier mapping will need
  the year as well as the label.
- The head-to-head section ("Record against Superseries finalists, World
  Championships semifinalists and Olympic quarterfinalists") is a plain list
  such as `Lin Dan 4–13`, with no header saying which number is wins. Treat
  it as a cross-check only, and confirm the order against a known record
  (Taufik vs Lin Dan is widely reported) before using it.

## BWF Tournament Software

- The home page answered normally to a plain fetch, showing ranking tables.
  Whether a cookie wall appears in a real browser is still unconfirmed; the
  Playwright saver in `pipeline/estafet/browser.py` clicks an "Accept"
  button if one shows up.
- Player and tournament pages are addressed by GUIDs, so the Taufik profile
  URL needs looking up by hand once and passing with `--tsoft-url`.
