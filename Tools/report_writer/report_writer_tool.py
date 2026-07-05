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
