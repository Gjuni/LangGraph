import json
import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

_SYSTEM = (
    "너는 보안 뉴스 사건사고 기사를 요약하는 에이전트다. 다음 규칙을 반드시 지켜라.\n"
    "1. 입력으로 주어진 각 기사의 본문 내용(content)을 근거로 summary를 총 5줄 내외로 작성한다.\n"
    "2. summary는 본문 내용에 없는 사실을 지어내지 않는다. 요약할 만한 내용이 없는 기사는 결과에서 제외한다.\n"
    "3. date, title, link는 입력값을 그대로 사용한다.\n"
    "4. 반드시 아래 형식의 JSON 배열로만 응답한다 (그 외 텍스트 금지).\n"
    '형식: [{{"date": "YYYY-MM-DD", "title": str, "link": str, "summary": str}}, ...]'
)
_PROMPT = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", "기사 목록:\n{articles}")])

_DATE_RE = re.compile(r"^\d{4}[.-]\d{2}[.-]\d{2}$")


def _has_verified_date(article: dict) -> bool:
    """스크랩 단계에서 실제로 확인된(서버 기준) 날짜인지 검사한다. 추정/생성된 날짜는 걸러낸다."""
    return bool(_DATE_RE.match((article.get("date") or "").strip()))


def organize_incidents(articles: list[dict]) -> dict:
    """확인된 날짜가 있는 기사만 골라 5줄 내외로 요약하고 날짜별(최신순)로 그룹화한다."""
    verified = [a for a in articles if _has_verified_date(a)]
    if not verified:
        return {}

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    payload = [
        {
            "date": a["date"].replace(".", "-"),
            "title": a["title"],
            "link": a["link"],
            "content": a.get("content", "")[:800],
        }
        for a in verified
    ]

    response = (_PROMPT | llm).invoke({"articles": json.dumps(payload, ensure_ascii=False)})
    text = response.content.strip().strip("`")
    if text.startswith("json"):
        text = text[4:].strip()

    organized: dict = {}
    for item in json.loads(text):
        if not (item.get("date") and item.get("title") and item.get("summary") and item.get("link")):
            continue
        organized.setdefault(item["date"], []).append(item)
    return organized
