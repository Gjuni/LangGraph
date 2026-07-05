Tools 폴더의 역할과 규칙을 정의한다.

역할: 각 에이전트(노드)가 사용하는 Tool을 모아두는 컨테이너 폴더다.
    - Tool 하나당 하위 폴더 하나(Tools/{tool_name}/)를 가진다.
    - 각 하위 폴더는 `{tool_name}_tool.py`(실제 구현)와 `README.md`(역할 정의)를 가진다.
    - graph.py의 노드 함수는 이 폴더의 함수를 import 하여 호출하는 방식으로만 Tool을 사용한다.

규칙:
    - 새 에이전트가 필요로 하는 기능은 반드시 이 폴더 하위에 새 폴더를 만들어 추가한다.
    - 노드(graph.py)에는 Tool의 세부 구현(스크래핑, LLM 호출, 파일 저장 등)을 직접 작성하지 않는다.

현재 구성:
    - web_scraper: 사용자 검색어를 기반으로 여러 보안 뉴스 사이트에서 기사 검색/수집
    - incident_organizer: 스크랩 결과 정리/요약
    - report_writer: 최종 보고서 파일 작성
