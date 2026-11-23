# Estafet Emas

A data-driven scrollytelling story on Indonesian badminton, 1958–2026: how
the country passed the crown from one generation to the next, and whether the
"golden relay" is broken or just being handed over.

- Spec: [docs/spec.md](docs/spec.md)
- Timeline and task backlog: [docs/timeline.md](docs/timeline.md)
- Early source findings: [docs/recon-notes.md](docs/recon-notes.md)

## Layout

| Folder | What goes there |
|--------|-----------------|
| `config/` | Source lists for each scrape (e.g. `freeze_2026.yaml`) |
| `data/raw/` | Untouched pages as downloaded, plus a `manifest.csv` per folder (pages are git-ignored, manifests are committed) |
| `data/clean/` | Tidy tables built from the raw pages |
| `pipeline/` | Python scraping and cleaning code |
| `notebooks/` | Exploration and the methodology appendix |
| `web/` | The Next.js scrollytelling site (later) |
| `docs/` | Spec, timeline, notes |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Scripts

```bash
# s1: 2026 data freeze (run after the World Tour Finals, 13 Dec 2026)
python -m pipeline.freeze_2026 --dry-run   # list sources
python -m pipeline.freeze_2026             # save what's missing

# p1b: Taufik Hidayat test scrape (Wikipedia finals -> CSV)
python -m pipeline.recon.taufik_test_scrape
```

Every fetch waits 3 seconds between requests to the same site, identifies
itself with a project user agent, and never re-downloads a page that's
already saved.
