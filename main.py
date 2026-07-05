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
