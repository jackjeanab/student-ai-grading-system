def evaluate_rules(parsed: dict, rules: dict) -> dict:
    required_blocks = set(rules.get("required_blocks", []))
    actual_blocks = set(parsed.get("all_block_types", []))
    missing_blocks = sorted(required_blocks - actual_blocks)

    if missing_blocks:
        return {
            "rule_status": "hard_fail",
            "missing_blocks": missing_blocks,
            "final_light": "red",
            "final_grade": "待加強",
        }

    return {
        "rule_status": "pass",
        "missing_blocks": [],
        "final_light": None,
        "final_grade": None,
    }
