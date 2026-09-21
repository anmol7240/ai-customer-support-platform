from app.services.priority import detect_priority


def test_critical_priority():
    result = detect_priority("My account was hacked")

    assert result == "CRITICAL"


def test_high_priority():
    result = detect_priority("My payment failed")

    assert result == "HIGH"


def test_medium_priority():
    result = detect_priority("I want to update my profile")

    assert result == "MEDIUM"