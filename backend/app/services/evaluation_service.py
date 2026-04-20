def decide_final_result(rule_result: dict, ai_result: dict) -> dict:
    if rule_result.get("final_light"):
        return {
            "light": rule_result["final_light"],
            "grade": rule_result["final_grade"],
            "source": "rule_engine",
        }

    return {
        "light": ai_result["light"],
        "grade": ai_result["grade"],
        "source": "ai",
    }


def mock_ai_evaluate(parsed: dict, assignment_prompt: str) -> dict:
    block_count = len(parsed.get("all_block_types", []))
    if block_count >= 8:
        return {"light": "green", "grade": "優"}
    if block_count >= 5:
        return {"light": "blue", "grade": "良"}
    return {"light": "yellow", "grade": "可"}
