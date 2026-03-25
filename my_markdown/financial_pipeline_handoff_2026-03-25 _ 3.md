# Financial Pipeline Handoff — 2026-03-25

## 1) 프로젝트 한 줄 요약
여러 원천 파일(KDATA1 / KDATA2 / QDATA)을 SQLite 기반 파이프라인으로 적재하여 `raw_observation`을 구축했고, 그 위에 **exact raw metric name 기준의 최소 통합 레이어**인 `integrated_observation`까지 구현·검증한 상태다.

---

## 2) 프로젝트 목적
장기 기업 재무/시계열 데이터를 여러 원천에서 수집하여,
- 원천 데이터는 그대로 보존하고,
- 분석용 대표값은 별도 통합 레이어에서 선택하며,
- 향후 기업 비교 / 밸류에이션 / 추정치 분석 / 시각화에 활용 가능한
**분석용 DB**를 만드는 것이 목표다.

---

## 3) 고정 설계 원칙
이 프로젝트의 상위 설계는 아래 원칙을 기준으로 유지되고 있다.

1. **SQLite first, PostgreSQL portable**
   - 우선 SQLite로 빠르게 구현
   - 나중에 PostgreSQL로 옮기기 쉬운 구조 유지

2. **raw / integrated 분리**
   - 원천값은 `raw_observation`에 그대로 저장
   - 대표 선택값은 `integrated_observation`에 별도 저장

3. **long-format 저장**
   - 엑셀/CSV의 가로형 데이터를 그대로 DB에 복사하지 않음
   - 모든 관측값을 세로형 observation row로 적재

4. **source-driven ingest**
   - 파일명 alone 사용 금지
   - 반드시 `source_group + relative_path` 기준으로 원천 식별

5. **추정치/확정치 구분 유지**
   - `is_estimate = 1` → 추정치
   - `is_estimate = 0` → 확정치

6. **지금 integrated는 최소 버전만 구현**
   - 아직 `standard_metric_name` 매핑 없음
   - 아직 종목코드/회사 매칭 고도화 없음
   - 아직 exact `raw_metric_name` 기준으로만 통합

7. **PowerShell 명령은 항상 한 줄로 제공**
   - 사용자 선호로 고정

---

## 4) canonical input
현재 canonical input은 아래 3개다.

```text
CODEX/
  data/
    input/
      KDATA1/
        오파스넷.xls
      KDATA2/
        오파스넷.xls
      QDATA/
        오파스넷_종목현황_20260322_184846.csv
```

중요 규칙:
- `data/input/` 바로 아래 loose file은 당분간 무시
- 정식 입력은 KDATA1 / KDATA2 / QDATA 폴더 내부 파일만 사용
- source_group은 파일명으로 추정하지 않고 **폴더명으로만** 결정

---

## 5) 현재까지 완료된 단계 요약

### 완료된 큰 단계
1. 프로젝트 규칙 문서화
2. base schema draft 추가
3. source-file inventory 구현
4. SQLite runtime 구현
5. inspection helper 구현
6. KDATA1 parser 구현 및 검증 완료
7. KDATA2 parser 구현 및 검증 완료
8. QDATA parser 구현 및 검증 완료
9. integrated_observation 최소 버전 구현 및 검증 완료

### 현재 한 줄 판정
- **KDATA1 완료**
- **KDATA2 완료**
- **QDATA 완료**
- **integrated 최소 버전 완료**

---

## 6) 실제 DB 적재/검증 결과

### 6.1 source_file 인식
- canonical input 3건 인식 완료
- source_group별 파일이 정상 등록됨

### 6.2 KDATA1 결과
- 실제 구조 확인 후 **row-wise quarterly table**로 파싱
- 적재 결과: `raw_observation` **1086건**
- 한글 metric 깨짐 해결 완료 (`xlrd + cp949` 경로)
- `date_raw`, `fiscal_year`, `fiscal_quarter`, `period_label_std` 정상
- anomaly summary 전부 0

### 6.3 KDATA2 결과
- 실제 구조 확인 후 **row-wise yearly table**로 파싱
- 적재 결과: `raw_observation` **247건**
- `period_type = YEAR`
- `fiscal_quarter = NULL`
- `is_estimate = 0` 정상
- 원본 엑셀 값과 DB 적재 값 대조 완료

### 6.4 QDATA 결과
- CSV 구조를 섹터별로 해석하여 적재
- 적재 결과: `raw_observation` **1264건**
- period_type 분포:
  - `QUARTER = 84`
  - `SNAPSHOT = 27`
  - `YEAR = 1153`
- `is_estimate` 분포:
  - `0 = 1263`
  - `1 = 1`
- 원본 CSV와 구역별 대조 검증 완료
  - SNAPSHOT 정상
  - QUARTER 정상
  - YEAR 정상

### 6.5 integrated 최소 버전 결과
- `integrated_observation` **2432건** 생성
- period_type 분포:
  - `QUARTER = 1158`
  - `SNAPSHOT = 27`
  - `YEAR = 1247`
- 선택 출처 분포:
  - `QDATA = 1221`
  - `KDATA1 = 1074`
  - `KDATA2 = 137`
- 선택된 추정치: `1건`
- anomaly summary 전부 0
- 최근 integrated rows도 `confirmed_qdata` 등 selection_reason이 기대대로 보임

---

## 7) 파일 구조 해석 메모 (매우 중요)
이 프로젝트에서 가장 중요한 교훈은 **실제 파일 구조를 먼저 보고 parser를 짜야 한다**는 점이다.

### KDATA1 실제 구조
- 처음엔 quarter-by-column 구조로 잘못 가정했음
- 디버그 후 실제는 **row-wise quarterly table**임이 확인됨
- 해석:
  - 1행 = header
  - 1열 = 날짜
  - 2열 이후 = 지표
  - `date_raw`에서 분기 계산
  - `period_type = QUARTER`
  - label 예: `25.4Q`

### KDATA2 실제 구조
- 실제는 **row-wise yearly table**
- 해석:
  - 1행 = header
  - 1열 = 날짜
  - 2열 이후 = 지표
  - `period_type = YEAR`
  - `fiscal_quarter = NULL`
  - label 예: `2025`

### QDATA 실제 구조
- workbook이 아니라 **CSV**
- 상단 구조 확인 결과, 아래 3개 섹터로 해석하는 것이 자연스러웠음
  1. **overview / snapshot**
  2. **yearly blocks**
  3. **quarterly blocks**
- blank row 기준으로 block 분리 후 sector별 파싱

---

## 8) QDATA 파싱 규칙 상세
QDATA는 특히 구역 분리가 중요했다.

### overview block
- 2행씩 header/value pair로 읽음
- `period_type = SNAPSHOT`
- snapshot date는 파일명 `20260322`에서 `2026/03/22`로 추출

### mixed summary block
- 한 블록 안에 연간 손익 / 분기 손익이 함께 존재
- 왼쪽은 YEAR, 오른쪽은 QUARTER로 분리 해석

### yearly investment blocks
- `투자지표*` 블록은 `period_type = YEAR`

### is_estimate 규칙
아래 문자열이 **metric / period label / value text**에 직접 있을 때만 `is_estimate = 1`
- `(E)`
- `추정`
- `예상`
- `estimate`

없으면 기본 `0`

---

## 9) integrated_observation 최소 버전 설계
이번 integrated는 **semantic merge가 아니라 exact-name selection**이다.

### 9.1 현재 integrated의 의미
- 아직 `standard_metric_name` 매핑이 없음
- 아직 기업 매칭도 없음
- 따라서 **같은 회사 + 같은 raw_metric_name + 같은 period key** 안에서
  대표 row 1건을 고르는 레이어만 구현함

### 9.2 company_key 규칙
우선 아래 coalesce 순서로 company_key를 만듦
1. `normalized_stock_code`
2. `raw_stock_code`
3. `raw_company_name`

### 9.3 통합 키 정의
- YEAR: `company_key + raw_metric_name + period_type + fiscal_year`
- QUARTER: `company_key + raw_metric_name + period_type + fiscal_year + fiscal_quarter`
- SNAPSHOT: `company_key + raw_metric_name + period_type + date_raw`

### 9.4 선택 우선순위
1. `is_estimate=0` 우선
2. source priority 적용
3. `value_numeric` 있는 row 우선
4. `ingested_at` 최신 우선
5. `raw_observation_id` 큰 값 우선

### 9.5 source priority
- YEAR: `QDATA > KDATA2 > KDATA1`
- QUARTER: `QDATA > KDATA1 > KDATA2`
- SNAPSHOT: `QDATA > KDATA2 > KDATA1`

### 9.6 selection_reason 예시
- `confirmed_qdata`
- `confirmed_kdata1`
- `confirmed_kdata2`
- `estimate_qdata_fallback`
- `estimate_kdata1_fallback`
- `estimate_kdata2_fallback`

---

## 10) 현재 알려진 작은 이슈
### inspect_integrated_load의 conflict sample 표시 이슈
- integrated 본체 데이터는 정상
- anomaly summary도 0
- 다만 `Conflict candidate samples`에서만 `selected_source_group=None`, `selected_raw_observation_id=None`로 보이는 경우가 있었음
- 이건 실제 integrated 데이터가 null이라기보다 **inspect 표시 쿼리의 NULL 비교 처리 이슈**로 판단됨
- 실데이터 버그보다 **inspection display issue**에 가까움

즉, 현재 파이프라인의 본체는 정상이고, 남은 것은 일부 inspection 보정 수준이다.

---

## 11) 폴더 / 파일 구조 (핵심만)
아래는 지금까지 작업 과정에서 중요한 파일들이다.

```text
CODEX/
  AGENTS.md
  docs/
    db_design.md
    data_rules.md
    CODEX_SESSION_STATE.md        # 있으면 여기에 최신 상태를 계속 적는 것이 좋음
  sql/
    003_create_base_financial_tables.sql
    004_create_integrated_tables.sql   # integrated 단계에서 추가되었을 가능성 큼
  data/
    financial_pipeline.sqlite3
    input/
      KDATA1/
        오파스넷.xls
      KDATA2/
        오파스넷.xls
      QDATA/
        오파스넷_종목현황_20260322_184846.csv
  python/
    etl/
      db_runtime.py
      inventory_sources.py
      run_inventory.py
      inspect_inventory.py

      parse_kdata1.py
      run_kdata1_parser.py
      debug_kdata1_layout.py
      inspect_kdata1_load.py

      parse_kdata2.py
      run_kdata2_parser.py
      debug_kdata2_layout.py
      inspect_kdata2_load.py

      parse_qdata.py
      run_qdata_parser.py
      debug_qdata_layout.py
      # inspect_qdata_load.py 는 세션마다 누락될 수 있어 실제 존재 여부 확인 필요

      build_integrated_observation.py
      run_integrated_selection.py
      inspect_integrated_load.py
  tests/
    test_inventory_sources.py
    test_parse_kdata1.py
    test_parse_kdata2.py
    test_parse_qdata.py
    test_build_integrated_observation.py
```

주의:
- 위 파일 중 일부는 새 세션/새 환경에서 저장 반영 여부를 반드시 로컬 실행으로 확인해야 한다.
- 특히 inspect helper는 세션 로그상 생성되었어도 실제 로컬에 저장되지 않은 적이 있었음.

---

## 12) 로컬 검증 시 자주 쓴 PowerShell 한 줄 명령
아래는 실제 검증에 사용한 핵심 명령들이다.

### inventory
```powershell
py -3 -m python.etl.inspect_inventory
```

### KDATA1
```powershell
py -3 -m python.etl.run_kdata1_parser; py -3 -m python.etl.inspect_kdata1_load
```

### KDATA2
```powershell
py -3 -m python.etl.debug_kdata2_layout; py -3 -m python.etl.run_kdata2_parser; py -3 -m python.etl.inspect_kdata2_load
```

### QDATA
```powershell
py -3 -m python.etl.run_qdata_parser
```

### integrated
```powershell
py -3 -m python.etl.run_integrated_selection; py -3 -m python.etl.inspect_integrated_load
```

---

## 13) 새 창 / 새 Codex 환경에서 가장 먼저 할 일
새 창이나 새 환경에서는 아래 순서로 들어가는 것이 좋다.

1. 이 handoff 문서를 먼저 읽는다.
2. repo 구조를 확인한다.
3. DB 파일과 input 파일이 실제로 있는지 확인한다.
4. 핵심 실행 명령으로 저장 상태를 검증한다.
5. 그 다음 새 작업으로 넘어간다.

권장 확인 순서:
1. `inspect_inventory`
2. `inspect_kdata1_load`
3. `inspect_kdata2_load`
4. `run_qdata_parser` 결과 확인
5. `run_integrated_selection; inspect_integrated_load`

---

## 14) 지금까지 우리가 실제로 검증한 내용
이 프로젝트는 단순히 “코드 생성”에서 끝나지 않고, 아래까지 실제로 확인했다.

- KDATA1 원본 값 ↔ DB 적재 값 대조
- KDATA2 원본 값 ↔ DB 적재 값 대조
- QDATA는 **구역별(table-by-table)** 검증
  - SNAPSHOT 블록
  - QUARTER 블록
  - YEAR 블록
- integrated row count / source 선택 / estimate 선택 여부 검증

즉 현재 상태는 “코드만 있음”이 아니라 **실제 데이터 검증까지 통과한 상태**다.

---

## 15) 다음에 진행할 구체적인 목표
다음 목표는 아래 두 가지 중 하나다.

### 옵션 A: inspection polish
- `inspect_integrated_load`의 conflict sample 표시 이슈 보정
- 파이프라인 본체는 그대로 두고 inspection만 개선

### 옵션 B: 표준화 단계 진입
- `standard_metric_name` 매핑 초안 시작
- exact raw metric name 기반 integrated를 넘어, 의미 기준 통합으로 확장

현 시점에서 더 가치가 큰 다음 milestone은 보통 **표준 지표 매핑 초안**이다.
다만 안정감을 더 원하면 inspection polish를 먼저 해도 된다.

추천 순서:
1. `inspect_integrated_load` conflict sample 표시 보정
2. `standard_metric_name` 매핑 초안
3. 이후 company matching / override / richer integrated logic

---

## 16) 새 창에서 바로 붙여넣을 짧은 설명
아래 문장을 새 창 첫 메시지에 그대로 붙여넣으면 된다.

```text
이 프로젝트는 financial pipeline DB 구축 작업입니다. 현재 SQLite 기반으로 source_file / raw_observation / integrated_observation 최소 버전까지 구현되어 있습니다. KDATA1은 row-wise quarterly table로 1086건, KDATA2는 row-wise yearly table로 247건, QDATA는 snapshot/year/quarter로 1264건 raw 적재가 완료됐고, integrated_observation은 exact raw_metric_name 기준 최소 선택 레이어로 2432건 생성됐습니다. raw 적재 3축과 integrated 최소 버전은 모두 실제 데이터 검증까지 통과했습니다. 다음 단계는 inspect_integrated_load conflict sample 표시 보정 또는 standard_metric_name 매핑 초안입니다. PowerShell 명령은 항상 한 줄로 주세요.
```

---

## 17) 최종 현재 상태 요약
- **기획 방향 유지 중**: raw/integrated 분리, long-format, is_estimate 유지
- **원천 적재 완료**: KDATA1 / KDATA2 / QDATA
- **최소 통합 완료**: integrated_observation
- **실데이터 검증 완료**
- **다음 작업 가능 상태**: inspection polish 또는 metric standardization

