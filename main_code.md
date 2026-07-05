# main.py

## 설명
그래프 실행 진입점이다. `.env`를 로드하고, CLI에서 `input()`으로 검색어를 입력받는다.
입력값은 터미널 인코딩 문제로 생길 수 있는 손상된 서로게이트 문자를 제거하도록
`encode("utf-8", errors="ignore").decode("utf-8")`로 한 번 정제한다.
이후 `build_graph()`로 컴파일된 LangGraph 앱을 `stream(..., stream_mode="updates")`로 실행하고,
노드(에이전트)가 끝날 때마다 실행 로그를 출력한다. 마지막에 `report_node`가 반환한
`report_path`를 최종 안내 메시지로 출력한다.

## 코드
```python
from dotenv import load_dotenv

from graph import build_graph

load_dotenv()

NODE_LABEL = {"scrape": "스크랩 에이전트", "organize": "정리 에이전트", "report": "보고서 작성 에이전트"}

if __name__ == "__main__":
    query = input("검색할 보안 뉴스 키워드를 입력하세요: ").strip()
    query = query.encode("utf-8", errors="ignore").decode("utf-8")  # 터미널 인코딩 오류로 생긴 손상 문자 제거

    app = build_graph()
    report_path = None

    for update in app.stream({"query": query}, stream_mode="updates"):
        for node, output in update.items():
            summary = {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in output.items()}
            print(f"[{NODE_LABEL.get(node, node)}] 완료: {summary}")
            report_path = output.get("report_path", report_path)

    print(f"\n보고서 생성 완료: {report_path}")
```
