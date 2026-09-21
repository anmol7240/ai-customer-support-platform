def detect_priority(message: str) -> str:
    message = message.lower()

    critical_words = [
        "hacked",
        "fraud",
        "stolen",
        "security breach"
    ]

    high_words = [
        "urgent",
        "money deducted",
        "payment failed",
        "account blocked"
    ]

    if any(word in message for word in critical_words):
        return "CRITICAL"

    if any(word in message for word in high_words):
        return "HIGH"

    return "MEDIUM"