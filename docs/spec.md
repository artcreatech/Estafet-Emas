# Estafet Emas: Indonesian Badminton Legends, 1958–2026
### A data-driven scrollytelling project: spec, story, scope and timeline

**Author:** artcreatech
**Status:** Draft v0.1 (24 Nov 2026)
**Inspiration:** SRF Data, *"20 Years, 20 Titles | Roger Federer"* (2018), a match-by-match analysis of a whole career
**Working title options:** *Estafet Emas* ("The Golden Relay") · *Dari Rudy ke Alwi* · *Smash Generations*

---

## 1. One-line pitch

The story of how Indonesia passed the badminton crown from one generation to the next, from the 1958 Thomas Cup to Rudy Hartono, Susi Susanti, Taufik Hidayat and the doubles empire, and why 2026 became a crossroads: the country's first-ever Thomas Cup group-stage exit, followed months later by its first Asian Games men's team gold in 28 years.

## 2. Why this project

- **Portfolio fit:** It shows the whole data and visual storytelling pipeline (scraping, cleaning, modeling, spatial analysis, design, front-end) in one piece, which matches the target "data & visual storytelling" role.
- **Novelty:** Tennis has clean open match datasets, and that's why pieces like SRF's Federer story are possible. Badminton has no equivalent. **Building the dataset is itself part of the contribution.**
- **Local relevance:** Badminton is Indonesia's most successful Olympic sport, and the 2026 season gives the story a natural cliffhanger.

## 3. The core story question

> **"Is Indonesia's golden relay broken, or is the baton just being passed?"**

Every chapter answers part of that question with data: who carried the baton, how dominant they were, who they beat, where they won, and what the handovers between generations looked like.

---

## 4. Storytelling structure (scrollytelling chapters)

| # | Chapter | Era | Key data moment | Main visual |
|---|---------|-----|-----------------|-------------|
| 0 | **Cold open: Horsens, April 2026** | 2026 | Indonesia, 14-time Thomas Cup champions, lose 1–4 to France and exit at the group stage for the first time | A single scoreboard, then zoom out to a 68-year timeline of every Thomas Cup |
| 1 | **The Pioneers** | 1958–1979 | Thomas Cup dynasty begins; Rudy Hartono's 8 All England titles | "Trophy shelf" of All England titles by country per decade |
| 2 | **Barcelona Gold** | 1989–1998 | Susi Susanti and Alan Budikusuma win Indonesia's first Olympic golds (1992); Susi holds the Olympic, World and All England titles at the same time | Susi's career as a dot grid (every recorded final) plus a "simultaneous titles" ribbon |
| 3 | **The Backhand Genius** | 1996–2013 | Taufik Hidayat: Olympic gold 2004, World Champion 2005, 6× Indonesia Open; rivalry with Lin Dan | Federer-style match grid plus a head-to-head "tug of war" vs. Lin Dan, Lee Chong Wei and others |
| 4 | **Rules Change the Game** | 2006 | Switch from 15/11-point side-out scoring to 21-point rally scoring | Before/after comparison of match length and score margins (an explainer interlude) |
| 5 | **The Doubles Empire** | 2000–2021 | Olympic golds in doubles (2000, 2008, 2016, 2021); Kevin/Marcus as World No. 1; Thomas Cup 2020 | Small multiples: one career strip per pair; an Olympic "gold relay" chain across Games |
| 6 | **Where Indonesia Won** | 1958–2026 | Geography of titles: Istora Senayan vs. the world | Map of every title won, with clustered cities and animated by decade (GIS chapter) |
| 7 | **The Crossroads** | 2022–2026 | Paris 2024 bronze (Gregoria); Putri KW's 2025 World bronze ends a 10-year drought in women's singles; 2026 Thomas Cup exit; Fajar/Fikri win Japan and China Open; Alwi Farhan's rise; Asian Games men's team gold | "Baton chart": Indonesia's share of major titles by year, with the 2026 dip and rebound annotated |
| 8 | **Who's Next?** | 2026→ | Juniors and new pairs (Alwi Farhan, Amri/Nita, junior team results) | Interactive player explorer with search, filters and a match log for any player |

**Narrative devices**
- **The baton:** A recurring visual motif. One gold line passes from player to player across chapters.
- **"Tonight in 1992…" moments:** Short vignettes at each era's defining match, with the score typed out game by game.
- **Honest data notes:** Each chapter shows a small "how complete is this?" badge (see §6.4). Being transparent about older-era gaps becomes part of the craft.

---

## 5. Player roster and coverage

Tiers set how deep each player's treatment goes. Facts in this table must be verified during Phase 1.

| Era | Players / pairs | Category | Depth |
|-----|-----------------|----------|-------|
| Pioneers (1958–1979) | Rudy Hartono, Liem Swie King, Tjun Tjun / Johan Wahjudi, Christian Hadinata | MS, MD | Titles and finals only |
| Olympic Gold (1989–1998) | **Susi Susanti**, **Alan Budikusuma**, Ardy Wiranata, Hariyanto Arbi, Joko Suprianto, Ricky Subagja / Rexy Mainaky | WS, MS, MD | Finals plus partial match log |
| Taufik era (1996–2013) | **Taufik Hidayat**, Tony Gunawan / Candra Wijaya, Markis Kido / Hendra Setiawan, Nova Widianto / Liliyana Natsir | MS, MD, XD | Near-full match log (gaps before 2007) |
| Doubles Empire (2013–2021) | **Tontowi Ahmad / Liliyana Natsir**, **Kevin Sanjaya / Marcus Gideon**, Hendra Setiawan / Mohammad Ahsan, Greysia Polii / Apriyani Rahayu, Jonatan Christie, Anthony Ginting | XD, MD, WD, MS | Full match log |
| Crossroads (2022–2026) | Fajar Alfian / M. Shohibul Fikri (and Fajar/Rian), Gregoria Mariska Tunjung, Putri Kusuma Wardani, **Alwi Farhan**, Amri Syahnawi / Nita Violina Marwah, Leo Rolly Carnando / Daniel Marthin | All | Full match log, updated through Dec 2026 |

**Bold** = "hero" profiles that get a full Federer-style deep-dive (about 6 profiles: Susi, Alan, Taufik, Tontowi/Liliyana, Kevin/Marcus, plus one current hero, either Alwi or Fajar/Fikri).

---

## 6. Data specification

### 6.1 Two-layer data strategy

The data is complete in some places and patchy in others, so it's split into two layers:

1. **Spine dataset (complete, all countries):** The champions and medalists of major events across their whole history. Because it covers *all* countries, you can calculate Indonesia's *share* of world badminton over time.
   - Olympics (1992–2024), World Championships (1977–2026), All England (complete history), Thomas Cup (1949–2026), Uber Cup (1957–2026), Sudirman Cup (1989–2025), Asian Games (1962–2026), World Tour / Superseries Finals
2. **Deep dataset (Indonesian players, match level):** Every recorded match for each player on the roster, mostly from 1989 onward.

### 6.2 Sources

| Source | Use | Coverage | Access | Notes |
|--------|-----|----------|--------|-------|
| BWF Tournament Software (`bwf.tournamentsoftware.com`) | Deep dataset: match results, draws, scores | ~1989→2026 | Scrape (cookie wall, paging) | Official record. Many pre-2007 events missing (e.g., 2002 All England, team cups); IDs are inconsistent in early years |
| badmintonstatistics.net | Cross-check H2H and win counts; fill gaps | 1989→ | Manual / light scrape | Fan-built from Tournament Software crawls; no export found |
| Wikipedia (EN + ID) player pages | Finals tables (year, event, opponent, score) for older eras; "record against selected opponents" | 1960s→ | Scrape via API (`action=parse`) | Main source for Pioneers and finals; cite each row |
| Wikipedia event pages | Spine dataset (champions lists) | Full history | Scrape | Cross-check with BWF history pages |
| Olympedia | Olympic results, round by round | 1992→2024 | Scrape | Clean and reliable |
| BWF rankings (historical) and Kaggle scrapes | Rank timelines | ~2009→ (sparse earlier) | Download / scrape | Ranking-history charts only for modern players |
| News archives (Antara, Kompas, Jakarta Post, RRI, BWF news) | Vignettes, quotes, 2026 events, missing scores | All | Manual | For narrative color and gap-filling |
| PBSI / national archives, books | Pioneer-era stats | 1950s–80s | Manual (stretch) | Possibly offline |

**Out of reach (state this explicitly):** rally- and shot-level stats for historical matches. These were never collected consistently. Stroke-level datasets like ShuttleSet only cover a few dozen matches from 2018–2021.

### 6.3 Data model (tidy tables)

```text
players
  player_id, name, name_alt[], country, gender, birth_date, handedness,
  birthplace, birthplace_lat, birthplace_lon, career_start, career_end, era

pairs
  pair_id, player_id_1, player_id_2, category (MD/WD/XD), first_match, last_match

tournaments
  tournament_id, name, edition_year, start_date, end_date, tier
  (Olympics | WorldChamps | AllEngland | SuperSeries/WorldTour level | GrandPrix | Team | Continental | Other),
  city, country, venue, lat, lon

matches
  match_id, tournament_id, date, category, round,
  side_a (player_id or pair_id), side_b, winner_side,
  score_raw ("15-10 11-15 15-11"), games[] (a,b points), n_games,
  scoring_system (side_out_15 | side_out_11 | side_out_7x5 | rally_21 | other),
  walkover (bool), retired (bool), duration_min (nullable),
  source, source_url, confidence (A/B/C)

team_ties
  tie_id, event (Thomas/Uber/Sudirman/AsianGames/...), year, stage,
  team_a, team_b, score, winner, rubbers[] -> match_id

titles (derived view)
  player_or_pair_id, tournament_id, category, result (W/F/SF/Bronze)

rankings
  player_or_pair_id, date, category, rank, points
```

### 6.4 Data quality rules
- **Confidence grade per row:** A = official source with full score; B = secondary source or score partly missing; C = result only (who won), no score.
- **Coverage badge per chapter:** % of the player's known events that have match-level rows.
- **Name resolution:** Keep a manual alias table (e.g., *Susi / Susy Susanti*; romanizations of Chinese and Korean names).
- **Scoring system flag** for every match, so pre-2006 and post-2006 scores are never compared naively.
- **Freeze date:** Final data pull after the **2026 BWF World Tour Finals** (mid-December 2026); later updates go into a changelog.

### 6.5 Derived metrics
- Win rate by year, by tournament tier, by opponent country
- Titles and finals per season; "peak window" (best rolling 24-month win rate)
- Head-to-head records vs. top rivals (Lin Dan, Lee Chong Wei, Bang Soo-hyun, Chinese pairs, etc.)
- Indonesia's **share of major titles** per year and per decade (spine dataset)
- Average game margin, deciding-game win % ("clutch"), modern era only where scores are complete
- Titles by city/country; home (Istora) vs. away win rate

---

## 7. Visualization spec

| Viz | Purpose | Notes |
|-----|---------|-------|
| **Career match grid** (Federer-style) | Every match as one square: color = W/L, row = year, ordered by date | Hero profiles; hover shows opponent, score, event |
| **Baton line** | Indonesia's share of major titles by year, with the "carrier" annotated | The main through-line chart; appears in Ch. 1, 7 and 8 |
| **Trophy shelf** | Stacked icons of All England / WC / Olympic titles by country per decade | Ch. 1 |
| **H2H tug of war** | Diverging bars per rival (wins left, losses right) | Taufik vs. Lin Dan as the showcase |
| **Olympic gold chain** | Linked medallions 1992 → 2024 showing the sector of each gold | Shows the gap years (2012, 2024) |
| **Scoring-system explainer** | Animated rally vs. side-out scoring; match length before/after 2006 | Ch. 4 |
| **Title map** | Points per title city, animated by decade; Istora Senayan highlighted | MapLibre GL; clustered; ties into GIS skills |
| **Pair career strips** | Small multiples of doubles careers on a shared time axis | Ch. 5 |
| **Player explorer** | Search any roster player → match log, filters, mini-grid | Ch. 8; also a useful reference tool |

**Design direction:** Red and white palette accents on a neutral base, plus one "gold" accent reserved for the baton. Typography in the editorial style of SRF/NYT. Mobile-first scroll steps. Optionally bilingual (Bahasa Indonesia / English).

---

## 8. Tech stack

| Layer | Choice | Why |
|-------|--------|-----|
| Scraping | Python (`requests`/`httpx`, `BeautifulSoup`, Playwright for JS pages), polite rate limits and caching | Tournament Software uses a cookie wall and dynamic pages |
| Cleaning / modeling | Python (`pandas`/`polars`), DuckDB as the local warehouse | Fast joins, reproducible |
| Spatial | GeoPandas (geocode tournament cities), export GeoJSON | Title map |
| Notebooks | Jupyter / Quarto for EDA and the methodology appendix | Doubles as a portfolio case study |
| Front-end | Next.js (fits the artcreatech site) + Scrollama + D3 / Observable Plot + MapLibre GL | Scrollytelling standard |
| Data delivery | Pre-aggregated JSON/Parquet per chapter (static) | No backend needed |
| Hosting | Vercel / Cloudflare Pages | Static, free tier |
| Repo | GitHub, with `/data/raw`, `/data/clean`, `/pipeline`, `/web`, `/docs` | Open methodology; optional dataset release on Kaggle |

---

## 9. Scope

### In scope (v1.0)
- Spine dataset of major events, all countries, full history through 2026
- Deep match logs for the roster in §5, 1989→Dec 2026 (titles/finals only for the Pioneers)
- 6 hero deep-dives and 8 scrollytelling chapters
- Title map, H2H module, player explorer
- Methodology page plus a downloadable cleaned dataset (with a source licensing note)

### Stretch (v1.1+)
- Full Bahasa Indonesia version
- Pre-1989 match logs from print archives and PBSI
- Ranking timelines for all modern players
- Video embeds of iconic matches (official BWF YouTube only)
- Rally-level analysis using a few modern matches from public datasets

### Out of scope
- Shot- or rally-level stats for historical matches (the data doesn't exist)
- Live auto-updating after the 2026 freeze (manual yearly refresh instead)
- Players from other countries beyond their role as opponents and in the spine dataset
- Betting or prediction models

---

## 10. Timeline (part-time, ~10–12 hours/week)

| Phase | Weeks | Dates (target) | Deliverables |
|-------|-------|----------------|--------------|
| **0. Setup and recon** | 1 | 1–7 Dec 2026 | Repo; test scrape of Taufik's Tournament Software history vs. Wikipedia; coverage report; final roster |
| **1. Spine dataset** | 2 | 8–21 Dec 2026 | Champions of all majors, all countries, 1949–2026; **data freeze after the World Tour Finals** |
| **2. Deep dataset** | 3 | 22 Dec 2026 – 11 Jan 2027 | Match logs for the roster; alias table; confidence grades; geocoded tournaments |
| **3. Analysis and story lock** | 2 | 12–25 Jan 2027 | EDA notebook; derived metrics; chapter outline with the key numbers locked; static chart drafts |
| **4. Design** | 2 | 26 Jan – 8 Feb 2027 | Figma: mobile and desktop scroll steps, chart styles, map style |
| **5. Build** | 4 | 9 Feb – 8 Mar 2027 | Next.js scrollytelling; all chapters; explorer; map |
| **6. QA and fact-check** | 1 | 9–15 Mar 2027 | Every number traced to a source; a11y check; performance; mobile testing |
| **7. Launch and distribution** | 1 | 16–22 Mar 2027 | Publish; methodology post; LinkedIn/Threads launch thread; portfolio case study; dataset release |

**Total:** ~16 weeks. **MVP checkpoint (week 8):** Chapters 0, 3 and 7 live as a teaser (cold open + Taufik deep-dive + crossroads chart), so there's something to show recruiters early.

---

## 11. Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Tournament Software blocks scraping or changes its markup | High | Cache raw HTML; slow rate; Playwright fallback; manual entry for hero players |
| Gaps before 2007 (missing events, team cups) | Medium | Wikipedia + Olympedia + news to fill; confidence grades; show the gaps on purpose |
| Pioneer-era data too thin for match grids | Medium | Use titles-only visuals for that era; make it a design choice, not a weakness |
| Name/ID mismatches | Medium | Alias table; manual review of hero players |
| Scope creep (too many players) | High | Keep the hero list to 6; everyone else gets an explorer entry only |
| Licensing of photos/video | Medium | Use no player photos (illustrated or typographic portraits); link to official video |
| 2026 story still moving (World Tour Finals in December) | Low | Freeze date; editor's note with a "last updated" stamp |

---

## 12. Open questions (decide in Phase 0)

1. Language: English first, Bahasa Indonesia first, or both at launch?
2. Hero for the current era: Alwi Farhan (individual rising star) or Fajar/Fikri (2026's most successful pair)?
3. Should the Pioneers chapter go deeper (archive research) or stay a short prologue?
4. Publish on the artcreatech site or as a standalone domain?
5. Release the dataset publicly (check Tournament Software terms first)?

---

## 13. Key facts to anchor the story (verify in Phase 1)

- 1992: Susi Susanti and Alan Budikusuma win Indonesia's first Olympic golds (Barcelona).
- Susi: 4× All England (1990, 1991, 1993, 1994), 1993 World Champion; the only woman to hold the Olympic, World and All England singles titles at the same time.
- Taufik Hidayat: 2004 Olympic gold, 2005 World Champion, 6× Indonesia Open; now Indonesia's Deputy Minister for Youth and Sport.
- Indonesia has won 23 World Championship golds; the most recent was Hendra/Ahsan in 2019. Women's doubles has never won one.
- 2025 World Championships: Putri KW's bronze ends a 10-year women's singles medal drought (last: Lindaweni Fanetri, 2015).
- 2026 Thomas Cup (Horsens): Indonesia, 14-time champions, exit at the group stage for the first time after losing 1–4 to France. The Uber Cup team wins bronze.
- 2026: Fajar/Fikri win the Japan Open (Super 750) and defend the China Open (Super 1000); Alwi Farhan wins the Indonesia Masters and the Australian Open; Amri/Nita win World Championships bronze in New Delhi.
- Sept 2026 Asian Games (Aichi-Nagoya): the men's team beat China 3–2 for Indonesia's first men's team gold in 28 years.

---

## 14. References (starting points)

- SRF Data, "20 Years, 20 Titles | Roger Federer": https://www.srf.ch/static/srf-data/data/2018/federer/en.html
- Scroll.in on badmintonstatistics.net and BWF data quality: https://scroll.in/field/967108
- badmintonstatistics.net: https://www.badmintonstatistics.net
- BWF Tournament Software: https://bwf.tournamentsoftware.com
- Wikipedia, Susi Susanti: https://en.wikipedia.org/wiki/Susi_Susanti
- Wikipedia, Taufik Hidayat: https://en.wikipedia.org/wiki/Taufik_Hidayat
- Olympedia, Taufik Hidayat: https://www.olympedia.org/athletes/82734
- ShuttleSet (stroke-level dataset, 2018–2021): https://arxiv.org/abs/2306.04948
- RRI, Indonesia crash out of Thomas Cup group stage for first time (Apr 2026): https://rri.co.id/voice-of-indonesia/sport/2376587
- RRI, Asian Games 2026 men's team gold: https://rri.co.id/en/sport/2758099
- RRI, Fajar/Fikri Japan Open 2026: https://rri.co.id/en/sport/2581401
- RRI, Alwi Farhan Australian Open 2026: https://rri.co.id/en/sport/2492008
- RRI, Amri/Nita 2026 World Championships bronze: https://rri.co.id/voice-of-indonesia/sport/2672069
- VOI, Putri KW 2025 World Championships: https://voi.id/en/sports/510186
