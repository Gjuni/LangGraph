# state.py

## 설명
그래프 전체 노드가 공유하는 상태(`ReportState`)를 정의한다. `query`는 사용자가 CLI에서
입력한 검색어, `articles`는 여러 사이트에서 검색으로 수집한 결과, `organized`는 날짜별(최신순)
정리 결과, `report_path`는 최종 보고서 경로를 담는다.

## 코드
```python
from typing import TypedDict


class ReportState(TypedDict):
    """그래프 전체에서 공유되는 상태."""

    query: str  # 사용자가 CLI에서 입력한 검색어
    articles: list[dict]  # 스크랩 에이전트가 여러 사이트에서 검색으로 수집한 원본 기사 목록
    organized: dict  # 정리 에이전트가 날짜별(최신순)로 그룹화한 결과
    report_path: str  # 보고서 작성 에이전트가 저장한 파일 경로
```
