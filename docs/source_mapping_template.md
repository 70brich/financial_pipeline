# Source Mapping Template

Use this sheet to define how each source file should enter PostgreSQL.

## 1. Source files

| Source file | Type | Sheet name | Description | Refresh cycle |
| --- | --- | --- | --- | --- |
| example_customer.xlsx | Excel | Sheet1 | Customer master data | Daily |
| example_contract.xlsx | Excel | Sheet1 | Contract data | Daily |
| example_sales.csv | CSV | - | Sales transactions | Daily |

## 2. Join keys

| Entity | Primary key | Join keys used across files |
| --- | --- | --- |
| Customer | customer_id | customer_id |
| Contract | contract_id | customer_id, contract_id |
| Sales | sales_id | customer_id, contract_id |

## 3. Raw load targets

| Source file | Raw table | Notes |
| --- | --- | --- |
| example_customer.xlsx | raw.customer_source | Keep original column values as text when needed |
| example_contract.xlsx | raw.contract_source | Preserve source row number |
| example_sales.csv | raw.sales_source | Preserve source file name |

## 4. Standardized columns

| Business meaning | Source column | Target column | Target type |
| --- | --- | --- | --- |
| Customer number | 고객번호 | customer_id | text |
| Customer name | 고객명 | customer_name | text |
| Join date | 가입일 | join_date | date |
| Status | 상태 | status_code | text |

## 5. Final outputs

| Output table/view | Purpose | Main columns |
| --- | --- | --- |
| mart.customer_status | Customer status summary | customer_id, active_yn, grade |
| mart.report_base | Reporting base table | customer_id, contract_id, amount |
