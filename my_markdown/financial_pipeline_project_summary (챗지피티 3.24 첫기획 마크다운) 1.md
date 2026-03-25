# 금융 데이터 파이프라인 프로젝트 요약

## 1. 프로젝트 목적

여러 출처의 기업 데이터를 수집·정리·통합하여, 최종적으로 **기업 비교 / 밸류에이션 / 차트 / 추정치 분석**에 활용할 수 있는 **분석용 데이터베이스**를 만든다.

초기 목표:
- 여러 형태의 원천 데이터를 DB화
- 출처별로 구분 관리
- 동일 지표의 이름 통합
- 출처 우선순위 기반 최종값 선택
- 추정치와 확정치 구분
- 이후 클릭형 화면 또는 자동화 분석으로 확장

---

## 2. 전체 설계 방향

초기 구현은 아래 구조로 간다.

- **언어**: Python
- **DB**: SQLite 먼저 사용
- **향후 이관**: PostgreSQL로 옮기기 쉬운 형태로 설계
- **접근 방식**
  - 원천(raw) 데이터와 통합(integrated) 데이터를 분리
  - long format 저장
  - source_group(폴더 기준)로 원천 식별
  - raw metric / standardized metric 분리
  - raw company identifier / normalized identifier 분리
  - 수동 override 가능하도록 설계

---

## 3. 핵심 원칙

### 3.1 원천과 통합 분리
- 원천 데이터는 그대로 보존
- 최종 분석용 데이터는 별도 integrated layer에서 관리

### 3.2 파일명만으로 원천 식별하지 않음
같은 파일명이 여러 폴더에 있을 수 있으므로, **파일명 alone 사용 금지**.

반드시 아래 기준 사용:
- `source_group`
- `relative_path`
- file metadata
- 필요시 `file_hash`

### 3.3 long format 저장
엑셀/CSV의 가로형 구조를 DB에 그대로 복사하지 않고, 모든 관측값을 **세로형(long-format)** observation row로 저장한다.

### 3.4 추정치와 확정치 구분
- `is_estimate = 1` : 추정치
- `is_estimate = 0` : 확정치

향후 integrated selection에서는 **확정치 우선 → 출처 우선순위 → 추정치 fallback** 방식으로 갈 계획이다.

### 3.5 지표명 통합
예:
- `영업이익률`
- `OPM(%)`

이런 원본명은 유지하되, 향후 표준 지표명으로 묶는다.

예:
- raw: `영업이익률`
- raw: `OPM(%)`
- std: `operating_margin`

### 3.6 종목코드 처리
- QDATA의 종목코드는 `A173130` 형태일 수 있음
- 표준 종목코드는 앞의 `A` 제거 후 6자리 숫자로 사용
  - 예: `A173130` → `173130`
- 종목코드가 파일에 없으면 향후 공식 소스(DART 등)를 이용한 매칭 메소드 구현 예정

---

## 4. 입력 파일 구조

현재 canonical input은 아래 세 폴더만 사용한다.

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

### 중요한 규칙
- `data/input/` 바로 아래에 있는 loose file은 **당분간 무시**
- 정식 입력은 **KDATA1 / KDATA2 / QDATA 폴더 안 파일만 사용**
- source_group은 **파일명에서 추정하지 않고 폴더명에서만 결정**

---

## 5. 파일 타입별 해석 규칙

### 5.1 KDATA1
- **분기 데이터**
- 맨 앞 날짜에서 연도와 분기를 계산
- 표준 기간 라벨 예:
  - `24.1Q`
  - `24.2Q`
- DB 기준:
  - `period_type = QUARTER`

### 5.2 KDATA2
- **연도 데이터**
- 해당 날짜가 속한 연도의 누계값 / 종가 / 최고 / 최저 등
- DB 기준:
  - `period_type = YEAR`
- 향후 `value_nature` 개념 필요 가능
  - 예: 누계, 연말종가, 연중고가, 연중저가

### 5.3 QDATA
- **보고서형 파일**
- 크게 3개 섹터
  1. 개략정보
  2. 연간 데이터
  3. 분기 데이터
- 연도 값이 붙은 항목끼리는 같은 종류의 연간 데이터로 본다
- DB 기준:
  - overview → `SNAPSHOT`
  - yearly → `YEAR`
  - quarterly → `QUARTER`
- `(E)`가 붙으면 추정치로 본다
- `연환산`은 별도 플래그/period 처리 대상

---

## 6. 기간(period) 모델

원본 날짜/문구와 해석 결과를 분리한다.

### 원본 보존
- `date_raw`
- `period_label_raw`

### 정규화 결과
- `fiscal_year`
- `fiscal_quarter`
- `period_type`
- `period_label_std`

예시:
- `2024-05-15` → `2024`, `2Q`, `24.2Q`
- `2024-12-31` → `2024`, `YEAR`
- `25년4Q(E)` → `2025`, `4Q`, `is_estimate = 1`

---

## 7. 현재까지 확정된 DB 방향

초기 핵심 테이블은 아래 4개부터 시작했다.

- `company`
- `source_file`
- `raw_observation`
- `import_log`

향후 추가 예정:
- `company_identifier_map`
- `metric_dictionary`
- `integrated_observation`
- `manual_override`

### 7.1 company
표준 회사 식별용

예상 역할:
- 표준 기업명
- 표준 종목코드
- 내부 surrogate key

### 7.2 source_file
입력 파일 메타데이터 저장

현재 중요 필드 개념:
- `source_group`
- `relative_path`
- `file_name`
- `file_extension`
- `file_size_bytes`
- `file_modified_at`
- `file_hash`
- `canonical_input`
- `discovered_at`

현재 upsert 기준:
- `(source_group, relative_path)`

### 7.3 raw_observation
원천 데이터를 long format으로 저장

향후 주요 필드:
- `source_file_id`
- `source_group`
- `metric_name_raw`
- `value_text`
- `value_numeric`
- `date_raw`
- `fiscal_year`
- `fiscal_quarter`
- `period_type`
- `period_label_raw`
- `period_label_std`
- `sector_name`
- `is_estimate`

### 7.4 import_log
수집/적재 실행 단위 기록

현재 status 허용값:
- `STARTED`
- `SUCCESS`
- `FAILED`
- `PARTIAL`
- `SKIPPED`

---

## 8. 현재까지 실제 구현 완료 상태

### 완료 1: 프로젝트 지침 문서 생성
다음 문서가 생성됨:
- `AGENTS.md`
- `docs/db_design.md`
- `docs/data_rules.md`

### 완료 2: base schema draft 추가
기존 starter를 덮어쓰지 않고, 새 SQL 초안 파일을 추가함:
- `sql/003_create_base_financial_tables.sql`

### 완료 3: source-group-aware inventory 구현
파일 인벤토리 로직이 구현됨:
- `python/etl/inventory_sources.py`

동작 방식:
- `data/input/KDATA1`
- `data/input/KDATA2`
- `data/input/QDATA`
만 스캔
- loose files 무시
- source_group은 폴더명에서만 추출
- file metadata 수집
- `source_file`에 upsert
- `import_log`에 실행 기록 저장

### 완료 4: inventory 테스트 추가
- `tests/test_inventory_sources.py`

테스트 대상:
- 폴더 경로에서 source_group 추출
- `relative_path` 생성
- loose file 무시

### 완료 5: SQLite runtime path 구현
다음 파일 생성:
- `python/etl/db_runtime.py`
- `python/etl/run_inventory.py`

SQLite DB 경로:
- `data/financial_pipeline.sqlite3`

### 완료 6: inspection helper 구현
다음 파일 생성:
- `python/etl/inspect_inventory.py`

이 helper는 아래를 쉽게 보여준다.
- 전체 `source_file` row 수
- `source_group`별 수
- 최근 `source_file` row
- 최근 `import_log` row

---

## 9. 실제 실행 확인 결과

로컬 PowerShell에서 실행 확인 완료.

### 실행 명령
```powershell
py -3 -m python.etl.run_inventory
py -3 -m python.etl.inspect_inventory
```

### 확인 결과
정상 동작 확인됨.

- SQLite DB 생성 성공
- `source_file` 총 3건
- `source_group`별:
  - `KDATA1 = 1`
  - `KDATA2 = 1`
  - `QDATA = 1`
- `import_log` 1건 기록
- 상태 `SUCCESS`

즉, **inventory/runtime/inspection까지 1차 뼈대는 정상 완료**되었다.

---

## 10. 현재 프로젝트 폴더 구조(중요 부분만)

```text
CODEX/
  AGENTS.md
  docs/
    db_design.md
    data_rules.md
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
      load_sources.py
  sql/
    001_create_schemas.sql
    002_create_tables.sql
    003_create_base_financial_tables.sql
  tests/
    test_inventory_sources.py
```

---

## 11. 현재 확정된 작업 순서

현재까지 우리는 아래 순서를 따르고 있다.

1. 프로젝트 규칙 문서화
2. base schema draft 생성
3. source-group-aware inventory
4. SQLite runtime
5. inspection helper
6. **KDATA1 parser**
7. KDATA2 parser
8. QDATA parser
9. 종목코드 매칭
10. 지표 표준화
11. integrated selection logic
12. manual override
13. 시각화 / 화면 / Streamlit

현재 시점은 **6번(KDATA1 parser)** 진입 단계이다.

---

## 12. 바로 다음 목표

다음 milestone은 **KDATA1 parser 구현**이다.

### 목표
KDATA1만 먼저 실제 파싱한다.

### 요구사항
- `data/input/KDATA1`만 읽기
- KDATA2 / QDATA는 아직 건드리지 않기
- KDATA1은 분기 데이터로 처리
- 맨 앞 날짜에서 연도/분기 계산
- 표준 분기 라벨 생성
  - 예: `24.1Q`
- long-format `raw_observation` row 생성
- 다음 값 보존:
  - `source_file_id`
  - `source_group`
  - file context에서 얻을 수 있는 company 정보
  - `metric_name_raw`
  - `value_text`
  - 가능하면 `value_numeric`
  - `date_raw`
  - `fiscal_year`
  - `fiscal_quarter`
  - `period_type = QUARTER`
  - `period_label_raw`
  - `period_label_std`
- 아직 하지 않을 것:
  - metric standardization
  - integrated selection logic
  - KDATA2 parsing
  - QDATA parsing

### 테스트 요구사항
- 날짜에서 분기 계산
- long-format row 생성
- parsed KDATA1 rows를 `raw_observation`에 넣는 흐름

---

## 13. 새 창에서 이어갈 때 붙여넣을 짧은 요약

```text
현재 프로젝트는 CODEX 폴더 기반 financial data pipeline 작업이다.
SQLite-first / PostgreSQL-portable 구조로 가고 있다.
inventory/runtime/inspection까지 완료되었고, canonical input 3개(KDATA1/KDATA2/QDATA) 인식과 SQLite 적재까지 검증됐다.
현재 다음 단계는 KDATA1 parser만 구현하는 것이다.
중요 규칙은 AGENTS.md, docs/db_design.md, docs/data_rules.md에 들어 있다.
```

---

## 14. 참고 메모

- Git은 아직 사용하지 못했다. 현재 환경에서 `git` 명령이 인식되지 않았다.
- PowerShell에서 실행할 때는 `.py` 파일에 명령을 넣는 것이 아니라, 터미널에 직접 입력해야 한다.
- `sqlalchemy`는 로컬에 설치 후 실행 확인을 완료했다.
- 긴 대화 대신 중요한 규칙은 문서 파일에 고정하고, 작업은 한 단계씩 milestone으로 끊어 진행하는 전략을 사용 중이다.
