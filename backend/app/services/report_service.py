from __future__ import annotations


def build_assignment_report(assignment_id: int) -> dict[str, object]:
    return {
        "assignment_id": assignment_id,
        "rows": [],
    }
