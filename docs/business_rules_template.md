# Business Rules Template

Document rules here before implementing them in SQL or Python.

## Rule catalog

| Rule ID | Target table | Column | Condition | Result | Priority |
| --- | --- | --- | --- | --- | --- |
| R001 | mart.customer_status | active_yn | contract_end_date < current_date | N | 1 |
| R002 | mart.customer_status | grade | total_sales >= 1000000 | VIP | 2 |
| R003 | mart.customer_status | status_code | source status is blank | INACTIVE | 3 |

## Code mapping

| Source system | Source value | Standard value | Notes |
| --- | --- | --- | --- |
| customer_source | 정상 | ACTIVE | Korean source value |
| customer_source | 해지 | CLOSED | Closed account |

## Data quality checks

| Check ID | Table | Check logic | Action |
| --- | --- | --- | --- |
| DQ001 | stg.customer | customer_id is null | Reject row |
| DQ002 | stg.contract | duplicate contract_id | Keep latest row |
| DQ003 | stg.sales | amount < 0 | Review manually |
