# web_scraper_tool.py

## 설명
사건사고 스크랩 에이전트가 사용하는 Tool이다. 검색엔진(Bing/DuckDuckGo)에 헤드리스 브라우저로
질의했더니 봇으로 감지되어 캡차/anomaly 페이지만 반환되고 결과가 0건이었다 — 그래서 검색엔진을
거치지 않고, `SECURITY_SITES`에 등록된 여러 보안 뉴스 사이트의 홈페이지를 Playwright로 직접
방문해 링크를 수집한 뒤, 검색어 토큰이 제목에 포함된 기사만 후보로 남기는 방식으로 바꿨다.
후보 기사마다 상세 페이지에 접속해 날짜(한국어 숫자 형식 + 영문 월 이름 형식 모두 인식)와
본문 일부(800자)를 채운다.

## 코드
```python
import re
from datetime import datetime
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

# 검색 대상 보안 뉴스 사이트 allow-list(홈페이지 URL). 사이트를 늘리고 싶으면 URL만 추가하면 된다.
# 참고: 검색엔진(Bing/DuckDuckGo)은 헤드리스 브라우저를 봇으로 차단해 결과가 0건이 되므로,
# 각 사이트 홈페이지를 직접 방문해 링크를 수집하는 방식을 쓴다.
SECURITY_SITES = [
    "https://www.boannews.com/",
    "https://www.dailysecu.com/",
    "https://www.zdnet.co.kr/security/",
    "https://thehackernews.com/",
    "https://krebsonsecurity.com/",
]

_DATE_ISO_RE = re.compile(r"\d{4}[.-]\d{2}[.-]\d{2}")
_DATE_EN_RE = re.compile(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}")


def _extract_date(body: str) -> str:
    """기사 본문에서 날짜를 찾아 YYYY-MM-DD로 정규화한다. 못 찾으면 '날짜 미상'을 반환한다."""
    iso = _DATE_ISO_RE.search(body)
    if iso:
        return iso.group(0).replace(".", "-")
    en = _DATE_EN_RE.search(body)
    if en:
        cleaned = en.group(0).replace(",", "")
        for fmt in ("%b %d %Y", "%B %d %Y"):
            try:
                return datetime.strptime(cleaned, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
    return "날짜 미상"


def _matches_query(title: str, tokens: list[str]) -> bool:
    """제목에 검색어 토큰이 하나라도 포함되는지 확인한다(영문 토큰은 단어 경계로 오탐을 막는다)."""
    lowered = title.lower()
    for t in tokens:
        if t.isascii():
            if re.search(rf"\b{re.escape(t)}\b", lowered):
                return True
        elif t in lowered:
            return True
    return False


def search_security_news(query: str, limit: int = 15) -> list[dict]:
    """여러 보안 뉴스 사이트의 최신 기사 중 검색어와 관련된 기사를 찾아 제목/링크/날짜/본문을 수집한다."""
    tokens = [t.lower() for t in query.split() if len(t) > 1] or [query.strip().lower()]
    per_site_limit = max(2, limit // len(SECURITY_SITES))

    candidates: list[dict] = []
    seen: set[str] = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for site in SECURITY_SITES:
            domain = urlparse(site).netloc.replace("www.", "")
            found = 0
            try:
                page.goto(site, wait_until="domcontentloaded", timeout=20000)
                links = page.eval_on_selector_all(
                    "a[href]",
                    "els => els.map(e => ({href: e.href, text: e.innerText.trim()}))",
                )
            except Exception:
                continue

            for item in links:
                href, text = item["href"].split("&")[0], item["text"]
                if len(text) <= 15 or domain not in href or href in seen or found >= per_site_limit:
                    continue
                if not _matches_query(text, tokens):
                    continue
                seen.add(href)
                candidates.append({"title": text, "link": href})
                found += 1

        for art in candidates:
            try:
                page.goto(art["link"], wait_until="domcontentloaded", timeout=20000)
                body = page.inner_text("body")
                art["date"] = _extract_date(body)
                art["content"] = body[:800]
            except Exception:
                art["date"], art["content"] = "날짜 미상", ""

        browser.close()

    return candidates
```
