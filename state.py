from typing import TypedDict


class ReportState(TypedDict):
    """그래프 전체에서 공유되는 상태."""

    query: str  # 사용자가 CLI에서 입력한 검색어
    plan: dict  # 오케스트레이션 에이전트가 세운 실행 계획(정제된 검색어, 병렬 스크랩 대상 사이트 목록)
    chat_response: str  # 오케스트레이션 에이전트가 사용자에게 보여주는 안내 메시지
    articles: list[dict]  # 스크랩 에이전트가 여러 사이트에서 검색으로 수집한 원본 기사 목록
    organized: dict  # 정리 에이전트가 날짜별(최신순)로 그룹화한 결과
    report_path: str  # 보고서 작성 에이전트가 저장한 파일 경로
