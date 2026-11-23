"""Save pages that need a real browser (cookie walls, JavaScript tables).

Optional: needs `pip install playwright` and `playwright install chromium`.
"""

from __future__ import annotations

import re

from .fetch import Fetcher, FetchResult, slugify

# Buttons that dismiss cookie walls on BWF Tournament Software and similar sites.
ACCEPT_PATTERN = re.compile(r"^(accept|agree|i agree|allow all|accept all)", re.I)


def save_with_browser(fetcher: Fetcher, source_id: str, url: str,
                      refresh: bool = False) -> FetchResult:
    path = fetcher.dir / f"{slugify(source_id)}.html"
    if path.exists() and not refresh:
        return FetchResult(url, path, None, from_cache=True)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return FetchResult(url, None, None, False,
                           error="playwright not installed (pip install playwright && playwright install chromium)")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        fetcher._wait_for_host(url)
        resp = page.goto(url, wait_until="networkidle")
        btn = page.get_by_role("button", name=ACCEPT_PATTERN)
        if btn.count():
            btn.first.click()
            page.wait_for_load_state("networkidle")
        html = page.content().encode("utf-8")
        status = resp.status if resp else 0
        browser.close()
    saved = fetcher._save(source_id, "browser", url, html, ".html", status)
    return FetchResult(url, saved, status, from_cache=False)
