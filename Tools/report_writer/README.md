report_writer Tool의 역할을 정의한다.

역할: 보고서 작성 에이전트(report_node)가 사용하는 Tool이다.
    - incident_organizer가 만든 날짜별 정리 결과를 Markdown 문서로 변환한다.
    - `reports/` 폴더에 타임스탬프가 포함된 파일명으로 저장한다.
    - incident_organizer가 이미 "제목+요약 필수" 규칙을 검증했으므로, 여기서는 organized 결과를 그대로 렌더링한다.
    - organized가 빈 dict인 경우(서버 기준 날짜가 확인된 기사가 없는 경우)에도 빈 보고서 대신 안내 문구를 남긴다.

입력/출력:
    - 함수: `write_report(organized: dict, out_dir: str = "reports") -> str`
    - 반환값: 저장된 보고서 파일의 경로(str)

수정 시 주의:
    - 보고서 포맷(제목, 정렬 순서 등)만 이 파일에서 수정하면 된다.
    - 이 Tool은 정리 로직을 직접 수행하지 않고 organized 결과를 그대로 신뢰한다.
