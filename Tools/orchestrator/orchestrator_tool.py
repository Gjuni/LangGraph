import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from Tools.web_scraper.web_scraper_tool import SECURITY_SITES

_SYSTEM = (
    "너는 보안 뉴스 스크랩 파이프라인의 오케스트레이션 에이전트다.\n"
    "사용자의 검색어를 받아 이후 단계(스크랩/정리/보고서 작성) 에이전트들이 참고할 실행 계획을 세운다.\n"
    "규칙:\n"
    "1. query를 분석해 검색에 더 적합한 refined_query(핵심 키워드)를 만든다.\n"
    "2. 아래 사이트 목록 중 이번 검색어와 관련성이 높은 사이트만 targets에 담는다. "
    "판단하기 어렵다면 전체 목록을 담는다. 이 targets는 이후 사이트별 병렬 스크랩에 사용된다.\n"
    "3. 사용자에게 보여줄 chat_response(1~2문장, 어떤 계획으로 수집할지 안내)를 작성한다.\n"
    "4. 반드시 아래 형식의 JSON으로만 응답한다 (그 외 텍스트 금지).\n"
    '형식: {{"refined_query": str, "targets": [str, ...], "chat_response": str}}\n'
    f"사이트 목록: {SECURITY_SITES}"
)
_PROMPT = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", "검색어: {query}")])


def run_orchestration(query: str) -> dict:
    """검색어를 분석해 정제된 검색어와 사이트별 병렬 스크랩 대상(targets)을 정하고, 사용자 안내 메시지를 만든다."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = (_PROMPT | llm).invoke({"query": query})
    text = response.content.strip().strip("`")
    if text.startswith("json"):
        text = text[4:].strip()

    try:
        plan = json.loads(text)
    except json.JSONDecodeError:
        plan = {}

    refined_query = plan.get("refined_query") or query
    targets = [t for t in plan.get("targets", []) if t in SECURITY_SITES] or list(SECURITY_SITES)
    chat_response = plan.get("chat_response") or f"'{refined_query}' 관련 보안 뉴스를 수집합니다."

    return {
        "plan": {"refined_query": refined_query, "targets": targets},
        "chat_response": chat_response,
    }
