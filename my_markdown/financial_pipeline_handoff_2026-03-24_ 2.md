# Financial Pipeline Handoff — 2026-03-24

## 1) 프로젝트 목적
장기 재무/시계열 데이터를 원천별로 수집해 DB에 적재하고, 이후 통합/표준화 레이어로 확장하는 파이프라인을 구축한다.

핵심 방향:
- `raw_observation`와 향후 `integrated_observation`를 분리
- 원천 파일은 `source_file`로 관리
- 적재는 long-format 중심
- 추정치/확정치는 `is_estimate`로 구분
- 현재는 **원천 적재 안정화 단계**이며, 표준화/통합 로직은 아직 시작하지 않음

---

## 2) 현재까지 완료된 단계

### 공통 기반
- inventory / runtime / inspection 완료
- SQLite DB 기반으로 진행 중
- `source_file` 등록 및 원천 파일 추적 가능

### KDATA1 완료
실제 파일 구조를 확인한 뒤, **row-wise 시계열 테이블**로 파싱하도록 수정 완료.

최종 구조 해석:
- 1행 = 헤더
- 1열 = 날짜
- 2열 이후 = 지표 컬럼

적재 결과:
- `raw_observation` 1086건 적재 성공
- 한글 metric 복원 완료
- `date_raw`, `fiscal_year`, `fiscal_quarter`, `period_label_std` 정상
- anomaly summary 전부 0

주의:
- 처음에는 quarter-by-column 구조로 잘못 가정했으나, 디버그 헬퍼로 실제 구조를 확인한 뒤 row-wise로 보정함
- `.xls` 인코딩 이슈는 `xlrd.open_workbook(..., encoding_override="cp949")` 방식으로 해결

### KDATA2 완료
KDATA2도 실제 파일 구조 확인 후 파싱 완료.

최종 구조 해석:
- 1행 = 헤더
- 1열 = 날짜(연도 기준)
- 2열 이후 = 지표 컬럼
- `period_type = YEAR`
- `fiscal_quarter = NULL`

적재 결과:
- `raw_observation` 247건 적재 성공
- `date_raw / fy / label / period_type=YEAR / is_estimate=0` 정상

메모:
- 일부 metric이 원본 헤더 기준으로 유사/중복 가능성 있음
- raw 레이어에서는 허용, 나중에 integrated 단계에서 정리 후보

---

## 3) 현재 DB/설계 상태

### 유지되고 있는 상위 설계
- source-driven ingest
- long-format raw storage
- source_group별 파서 분리
- `is_estimate` 필드 유지
- 향후 QDATA + 통합 선택 로직으로 확장 예정

### 아직 하지 않은 것
- QDATA parser
- metric 표준화
- 종목/회사 매칭 고도화
- integrated_observation 선택 로직
- UI/Streamlit

---

## 4) 구현 중 확인된 중요한 교훈

1. **실제 파일 구조 확인 전 추정 구현 금지**
   - KDATA1에서 구조 가정이 틀려 한 번 크게 돌아감
   - 앞으로는 debug helper로 top-left layout 먼저 확인 후 구현

2. **`.xls`는 engine/인코딩 이슈를 먼저 의심**
   - `.xls` → `xlrd`
   - 한글 깨짐 시 `encoding_override="cp949"` 확인

3. **PowerShell 명령은 항상 한 줄로 제공**
   - 사용자 선호 반영 필수

---

## 5) 다음 작업 목표
다음 milestone은 **QDATA parser 구현**이다.

우선 원칙:
- 먼저 실제 workbook 구조를 debug helper로 확인
- 그 다음 구조에 맞는 parser 구현
- `raw_observation` long-format 적재
- `is_estimate`는 실제 파일에 `(E)`, `추정`, `예상`, `estimate` 같은 단서가 있을 때만 1 처리
- KDATA1 / KDATA2는 건드리지 않음

---

## 6) 관련 파일/모듈 상태
현재 대화 기준으로 존재/수정된 핵심 흐름:
- `python/etl/parse_kdata1.py`
- `python/etl/run_kdata1_parser.py`
- `python/etl/debug_kdata1_layout.py`
- `python/etl/inspect_kdata1_load.py`
- `tests/test_parse_kdata1.py`
- `python/etl/parse_kdata2.py`
- `python/etl/run_kdata2_parser.py`
- `python/etl/debug_kdata2_layout.py`
- `python/etl/inspect_kdata2_load.py`
- `tests/test_parse_kdata2.py`

주의:
- 새 창에서는 실제 로컬 파일 상태와 대화 로그가 다를 수 있으므로, 필요하면 먼저 파일 존재 여부부터 확인

---

## 7) 새 창에서 이어갈 때 주의할 점
- 이 문서만 보면 전체 흐름은 이어갈 수 있음
- 다만 실제 코드/파일 상태는 로컬 저장본 기준이므로, 필요하면 로컬 실행 결과를 함께 붙여주는 것이 가장 정확함
- 특히 QDATA는 아직 구조를 확정하지 않았으므로, 절대 추정 구현부터 시작하면 안 됨

---

## 8) 새 창에서 바로 붙여넣을 짧은 설명
아래 문장을 새 창 첫 메시지에 그대로 붙여넣으면 됨.

```text
이 프로젝트는 financial pipeline DB 구축 작업입니다. 현재 inventory/runtime/inspection 완료 상태이고, KDATA1과 KDATA2는 실제 파일 구조를 확인해서 raw_observation long-format 적재까지 완료했습니다. KDATA1은 row-wise quarterly table로 1086건, KDATA2는 row-wise yearly table로 247건 적재됐습니다. 다음 milestone은 QDATA parser 구현이며, KDATA1 때 구조 추정이 틀렸던 경험이 있으니 QDATA도 반드시 debug helper로 실제 workbook 상단 구조를 먼저 확인한 뒤 구현해야 합니다. PowerShell 명령은 항상 한 줄로 주세요.
```

---

## 9) 현재 한 줄 판정
- KDATA1: 완료
- KDATA2: 완료
- 다음 단계: QDATA parser
- 상위 기획(raw/integrated 분리, long-format, is_estimate 유지)은 그대로 진행 중
