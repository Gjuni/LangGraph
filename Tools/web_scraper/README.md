web_scraper Tool의 역할을 정의한다.

역할: 사건사고 스크랩 에이전트(scrape_node)가 사용하는 Tool이다.
    - Playwright(Chromium)로 `SECURITY_SITES`에 등록된 여러 보안 뉴스 사이트의 홈페이지를 직접 방문해
      링크 목록을 수집하고, 사용자 검색어(단어 단위)가 제목에 포함된 기사만 후보로 남긴다.
    - 후보로 남은 기사 링크에 각각 접속하여 날짜와 본문 일부를 수집한다.
    - 검색엔진(Bing/DuckDuckGo)은 헤드리스 브라우저를 봇으로 감지해 결과를 차단(캡차/anomaly 페이지)하는
      것을 확인했다. 그래서 검색엔진을 거치지 않고 각 사이트를 직접 스크랩하는 방식을 쓴다.

입력/출력:
    - 함수: `search_security_news(query: str, limit: int = 15) -> list[dict]`
    - 반환 항목: `{title, link, date, content}`
    - 사이트별로 최대 `limit // 사이트 수`개까지만 후보로 남겨, 특정 사이트 하나가 결과를 독식하지 않게 한다.

사이트 추가 방법:
    - `SECURITY_SITES` 리스트에 홈페이지 URL 하나만 추가하면 검색 대상 사이트가 늘어난다.

수정 시 주의:
    - `_matches_query`는 영문 토큰은 단어 경계(`\b`)로 매칭해 "campaign" 안의 "ai" 같은 오탐을 막는다.
      한글 토큰은 단순 부분 문자열 매칭이다.
    - `_extract_date`는 `YYYY-MM-DD`/`YYYY.MM.DD`와 영문 월 이름(`Jul 5, 2026` 등) 두 형식을 모두 인식해
      `YYYY-MM-DD`로 정규화한다. 새 사이트의 날짜 형식이 다르면 여기만 수정하면 된다.
    - 이 Tool은 정리(organize)나 보고서 작성 로직을 포함하지 않는다.
