def decide_final_result(rule_result: dict, ai_result: dict) -> dict:
    if rule_result.get("final_light"):
        return {
            "light": rule_result["final_light"],
            "grade": rule_result["final_grade"],
            "feedback": rule_result.get("feedback")
            or "Rule engine found required criteria that need teacher review.",
            "source": "rule_engine",
        }

    return {
        "light": ai_result["light"],
        "grade": ai_result["grade"],
        "feedback": ai_result.get("feedback") or "AI grading completed.",
        "source": "ai",
    }


def mock_ai_evaluate(parsed: dict, assignment_prompt: str) -> dict:
    block_count = len(parsed.get("all_block_types", []))
    if block_count >= 8:
        return {
            "light": "green",
            "grade": "優",
            "feedback": "Local fallback: the submission contains enough Blockly blocks for a strong first pass.",
            "source": "mock",
        }
    if block_count >= 5:
        return {
            "light": "blue",
            "grade": "良",
            "feedback": "Local fallback: the submission has several relevant blocks but may need teacher review.",
            "source": "mock",
        }
    return {
        "light": "yellow",
        "grade": "可",
        "feedback": "Local fallback: the submission is short and should be reviewed.",
        "source": "mock",
    }
