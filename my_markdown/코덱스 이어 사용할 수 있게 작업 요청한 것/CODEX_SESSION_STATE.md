# CODEX Session State

업데이트 시각: 2026-03-24

## 1) 프로젝트 목적
여러 출처의 기업 데이터를 수집·정리·통합하여, 최종적으로 기업 비교 / 밸류에이션 / 차트 / 추정치 분석에 활용할 수 있는 분석용 데이터베이스를 만든다.

## 2) 고정 원칙
- SQLite first, PostgreSQL portable
- raw / integrated 분리
- long-format 저장
- source_group(폴더 기준)으로 원천 식별
- 파일명 alone 사용 금지
- `is_estimate`로 추정치/확정치 구분
- 아직 integrated selection logic, metric 표준화, company matching은 시작하지 않음

## 3) canonical input
- `data/input/KDATA1/오파스넷.xls`
- `data/input/KDATA2/오파스넷.xls`
- `data/input/QDATA/오파스넷_종목현황_20260322_184846.csv`

## 4) 현재 완료 상태
### 완료
1. 프로젝트 규칙 문서화
2. base schema draft
3. source-group-aware inventory
4. SQLite runtime
5. inspection helper
6. KDATA1 parser
7. KDATA2 parser

### 검증 완료 사실
- inventory/runtime/inspection까지 완료되어 `source_file` 3건이 인식됨
- KDATA1은 row-wise quarterly table로 파싱되며 `raw_observation` 1086건 적재 성공
- KDATA1 metric 한글 깨짐(cp949/xlrd 경로) 해결 완료
- KDATA2는 row-wise yearly table로 파싱되며 `raw_observation` 247건 적재 성공
- KDATA2는 `period_type=YEAR`, `fiscal_quarter=NULL`, `is_estimate=0`로 정상 적재됨

## 5) 실제 파일 구조 메모
### KDATA1
- 실제 구조는 **row-wise quarterly table**
- 1행 = header
- 1열 = 날짜
- 2열 이후 = 지표
- `date_raw`에서 분기 계산
- `period_type = QUARTER`
- label 예: `25.4Q`

### KDATA2
- 실제 구조는 **row-wise yearly table**
- 1행 = header
- 1열 = 날짜
- 2열 이후 = 지표
- `date_raw`에서 연도 계산
- `period_type = YEAR`
- `fiscal_quarter = NULL`
- label 예: `2025`

## 6) 구현 파일(핵심)
### 이미 존재/완료
- `python/etl/db_runtime.py`
- `python/etl/run_inventory.py`
- `python/etl/inspect_inventory.py`
- `python/etl/parse_kdata1.py`
- `python/etl/run_kdata1_parser.py`
- `python/etl/inspect_kdata1_load.py`
- `python/etl/debug_kdata1_layout.py`
- `python/etl/parse_kdata2.py`
- `python/etl/run_kdata2_parser.py`
- `python/etl/inspect_kdata2_load.py`
- `python/etl/debug_kdata2_layout.py`

### 테스트
- `tests/test_inventory_sources.py`
- `tests/test_parse_kdata1.py`
- `tests/test_parse_kdata2.py`

## 7) 다음 milestone
### QDATA parser 구현
QDATA는 보고서형 CSV이며, 크게 세 영역으로 해석할 예정:
1. overview / snapshot
2. yearly
3. quarterly

### QDATA 목표
- QDATA 전용 debug helper 먼저 작성
- 실제 CSV 구조를 상단 dump로 확인
- overview / yearly / quarterly 섹션 경계를 먼저 파악
- raw_observation long-format으로 적재
- `(E)`가 붙은 항목은 `is_estimate=1`
- `연환산`은 별도 플래그 또는 raw 보존 대상으로 우선 유지
- 아직 company matching / metric standardization / integrated logic 금지

## 8) Codex 작업 시 금지 범위
- KDATA1 parser 변경 금지
- KDATA2 parser 변경 금지
- 종목코드 매칭 금지
- metric 표준화 금지
- integrated_observation 로직 금지
- Streamlit/UI 금지

## 9) 새 세션에서 먼저 해야 할 것
1. repo 트리 확인
2. `docs/db_design.md`, `docs/data_rules.md`, `docs/CODEX_SESSION_STATE.md` 읽기
3. KDATA1/KDATA2 관련 구현 파일이 실제로 있는지 확인
4. QDATA 파일 샘플 구조부터 debug helper로 출력
5. parser 구현은 실제 구조 확인 후 최소 범위로만 진행

## 10) 로컬 확인 명령(현재 완료 상태 검증용)
```powershell
py -3 -m python.etl.inspect_inventory
```

```powershell
py -3 -m python.etl.inspect_kdata1_load
```

```powershell
py -3 -m python.etl.inspect_kdata2_load
```

## 11) 참고
- PowerShell 명령은 앞으로 **항상 한 줄**로 제공
- 새 환경에서는 대화 URL보다 **repo 안의 상태 파일**이 더 중요함
- milestone 종료 때마다 이 문서를 업데이트하면 Codex 연속성이 가장 좋아짐
