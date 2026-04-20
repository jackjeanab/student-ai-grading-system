from app.services.rule_engine import evaluate_rules


def test_marks_missing_required_block_as_red() -> None:
    parsed = {
        "root_block_types": ["board_initializes_setup"],
        "all_block_types": ["board_initializes_setup", "initializes_loop"],
    }
    rules = {"required_blocks": ["delay_custom"]}

    result = evaluate_rules(parsed, rules)

    assert result["final_light"] == "red"
    assert result["final_grade"] == "待加強"
