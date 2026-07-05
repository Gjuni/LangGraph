from langgraph.graph import StateGraph, START, END

from state import ReportState
from Tools.web_scraper.web_scraper_tool import search_security_news
from Tools.incident_organizer.incident_organizer_tool import organize_incidents
from Tools.report_writer.report_writer_tool import write_report


def scrape_node(state: ReportState) -> dict:
    """사건사고 스크랩 에이전트: 검색어와 관련된 보안 뉴스를 여러 사이트에서 수집한다."""
    return {"articles": search_security_news(state["query"])}


def organize_node(state: ReportState) -> dict:
    """사건사고 정리 에이전트: 수집된 기사를 날짜별로 정리/요약한다."""
    return {"organized": organize_incidents(state["articles"])}


def report_node(state: ReportState) -> dict:
    """보고서 작성 에이전트: 정리된 내용을 Markdown 보고서로 저장한다."""
    return {"report_path": write_report(state["organized"])}


def build_graph():
    graph = StateGraph(ReportState)
    graph.add_node("scrape", scrape_node)
    graph.add_node("organize", organize_node)
    graph.add_node("report", report_node)

    graph.add_edge(START, "scrape")
    graph.add_edge("scrape", "organize")
    graph.add_edge("organize", "report")
    graph.add_edge("report", END)

    return graph.compile()
