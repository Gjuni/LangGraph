# report_writer_tool.py

## 설명
보고서 작성 에이전트가 사용하는 Tool이다. 정리 에이전트가 만든 `{날짜: [기사, ...]}` 결과를
Markdown으로 렌더링한다. 기사마다 제목/5줄 요약/원문 링크를 섹션으로 나눠 적고, 날짜 키를
내림차순 정렬해 최신 날짜가 상단에 오도록 한다. 확인된 날짜를 가진 기사가 하나도 없으면
빈 목록 대신 안내 문구를 남긴다. 파일은 `reports/report_YYYYMMDD_HHMMSS.md`로 저장되고
그 경로를 반환한다.

## 코드
```python
from datetime import datetime
from pathlib import Path


def write_report(organized: dict, out_dir: str = "reports") -> str:
    """날짜별로 정리된 사건사고를 Markdown 보고서로 저장하고 경로를 반환한다."""
    Path(out_dir).mkdir(exist_ok=True)

    lines = [f"# 보안 사건사고 보고서 ({datetime.now():%Y-%m-%d})\n"]
    if not organized:
        lines.append("\n서버 기준으로 확인된 날짜를 가진 보안 사건사고가 없습니다.\n")
    for date in sorted(organized.keys(), reverse=True):
        lines.append(f"\n## {date}\n")
        for item in organized[date]:
            lines.append(f"\n### {item['title']}\n\n{item['summary']}\n\n[원문 보기]({item['link']})\n")

    path = Path(out_dir) / f"report_{datetime.now():%Y%m%d_%H%M%S}.md"
    path.write_text("\n".join(lines), encoding="utf-8")

    return str(path)
```
