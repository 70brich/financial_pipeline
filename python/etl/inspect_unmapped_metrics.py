from __future__ import annotations

from collections import Counter

from sqlalchemy import text

from python.etl.build_integrated_observation import execute_integrated_schema
from python.etl.build_integrated_observation_enriched import execute_metric_mapping_schema
from python.etl.db_runtime import DEFAULT_SQLITE_DB_PATH, create_sqlite_engine, ensure_runtime_schema
from python.etl.standard_metric_master import classify_deferred_metric_family, suggest_standard_metric_candidates


def print_section(title: str) -> None:
    print()
    print(f"=== {title} ===")


def main() -> None:
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)
    execute_integrated_schema(engine)
    execute_metric_mapping_schema(engine)

    with engine.begin() as connection:
        unmapped_rows = connection.execute(
            text(
                """
                SELECT
                    raw_metric_name,
                    normalized_metric_key,
                    COUNT(*) AS row_count
                FROM integrated_observation_enriched
                WHERE standard_metric_id IS NULL
                GROUP BY raw_metric_name, normalized_metric_key
                ORDER BY row_count DESC, raw_metric_name
                """
            )
        ).fetchall()

    deferred_family_counts: Counter[str] = Counter()
    high_confidence_rows: list[tuple[str, str, str, int]] = []
    ambiguous_rows: list[tuple[str, str, list[str], int]] = []
    no_suggestion_rows: list[tuple[str, str, int]] = []

    for row in unmapped_rows:
        suggestions = suggest_standard_metric_candidates(row.raw_metric_name)
        deferred_family = classify_deferred_metric_family(row.raw_metric_name)
        if deferred_family:
            deferred_family_counts[deferred_family] += int(row.row_count or 0)

        if len(suggestions) == 1:
            high_confidence_rows.append(
                (row.raw_metric_name, row.normalized_metric_key, suggestions[0], int(row.row_count or 0))
            )
        elif len(suggestions) > 1:
            ambiguous_rows.append(
                (row.raw_metric_name, row.normalized_metric_key, suggestions, int(row.row_count or 0))
            )
        else:
            no_suggestion_rows.append((row.raw_metric_name, row.normalized_metric_key, int(row.row_count or 0)))

    print("Unmapped metric inspection")
    print(f"Database: {DEFAULT_SQLITE_DB_PATH}")

    print_section("Unmapped summary")
    print(f"distinct unmapped raw_metric_name rows: {len(unmapped_rows)}")
    print(f"high confidence suggestions: {len(high_confidence_rows)}")
    print(f"ambiguous suggestions: {len(ambiguous_rows)}")
    print(f"no suggestion rows: {len(no_suggestion_rows)}")

    print_section("Deferred family counts")
    if deferred_family_counts:
        for family_name, row_count in deferred_family_counts.most_common():
            print(f"{family_name}: {row_count}")
    else:
        print("No deferred-family unmapped rows detected.")

    print_section("High confidence suggestion samples")
    if high_confidence_rows:
        for raw_metric_name, normalized_metric_key, suggested_standard_metric, row_count in high_confidence_rows[:50]:
            print(
                f"{raw_metric_name} | normalized={normalized_metric_key} | "
                f"suggested={suggested_standard_metric} | rows={row_count}"
            )
    else:
        print("No high-confidence unmapped suggestions found.")

    print_section("Ambiguous suggestion samples")
    if ambiguous_rows:
        for raw_metric_name, normalized_metric_key, suggestions, row_count in ambiguous_rows[:50]:
            print(
                f"{raw_metric_name} | normalized={normalized_metric_key} | "
                f"suggestions={', '.join(suggestions)} | rows={row_count}"
            )
    else:
        print("No ambiguous unmapped suggestions found.")

    print_section("Top unmapped without suggestion")
    for raw_metric_name, normalized_metric_key, row_count in no_suggestion_rows[:50]:
        print(f"{raw_metric_name} | normalized={normalized_metric_key} | rows={row_count}")


if __name__ == "__main__":
    main()
