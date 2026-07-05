from asyncio import graph

from langgraph.graph import StateGraph, START, END

from state import ReportState
from Tools.orchestrator.orchestrator_tool import run_orchestration
from Tools.web_scraper.web_scraper_tool import search_security_news
from Tools.incident_organizer.incident_organizer_tool import organize_incidents
from Tools.report_writer.report_writer_tool import write_report


def orchestrate_node(state: ReportState) -> dict:
    """오케스트레이션(Chat) 에이전트: 검색어를 분석해 정제된 검색어와 스크랩 대상 사이트(병렬 처리 단위)를 정한다."""
    return run_orchestration(state["query"])
def scrape_node(state: ReportState) -> dict:
    """사건사고 스크랩 에이전트: 오케스트레이션 계획에 따라 대상 사이트에서 관련 보안 뉴스를 수집한다."""
    plan = state.get("plan") or {}
    query = plan.get("refined_query", state["query"])
    sites = plan.get("targets")
    return {"articles": search_security_news(query, sites=sites)}


def organize_node(state: ReportState) -> dict:
    """사건사고 정리 에이전트: 수집된 기사를 날짜별로 정리/요약한다."""
    return {"organized": organize_incidents(state["articles"])}
def report_node(state: ReportState) -> dict:
    """보고서 작성 에이전트: 정리된 내용을 Markdown 보고서로 저장한다."""
    return {"report_path": write_report(state["organized"])}


def build_graph():
    graph = StateGraph(ReportState)
    graph.add_node("orchestrate", orchestrate_node)  # Add node for orchestrate
    graph.add_node("scrape", scrape_node)
    graph.add_node("organize", organize_node)  # Add node for organize
    graph.add_node("report", report_node)

    graph.add_edge(START, "orchestrate")
    graph.add_edge("orchestrate", "scrape")
    graph.add_edge("scrape", "organize")
    graph.add_edge("organize", "report")
    graph.add_edge("report", END)

    return graph.compile()
