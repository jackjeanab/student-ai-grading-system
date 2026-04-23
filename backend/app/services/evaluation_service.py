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
            "feedback": "同學做得很好，你的程式已經放入足夠的 Blockly 積木，整體結構看起來很完整。接下來可以再檢查每個積木的順序與參數，讓 LED 控制更穩定。",
            "source": "mock",
        }
    if block_count >= 5:
        return {
            "light": "blue",
            "grade": "良",
            "feedback": "同學不錯喔，你已經使用了一些和任務有關的積木。可以再回頭確認是否有包含初始化、重複執行與延遲控制，讓程式更符合題目要求。",
            "source": "mock",
        }
    return {
        "light": "yellow",
        "grade": "可",
        "feedback": "同學已經完成提交，這是很好的開始。不過目前積木數量比較少，建議再檢查題目要求，把控制 LED 需要的初始化、輸出或延遲積木補完整。",
        "source": "mock",
    }
