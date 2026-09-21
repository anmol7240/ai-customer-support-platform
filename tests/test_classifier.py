from app.services.classifier import predict_category


def test_category_prediction():
    result = predict_category(
        "My payment was deducted but order is pending"
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_account_message_prediction():
    result = predict_category(
        "I cannot login to my account"
    )

    assert isinstance(result, str)
    assert len(result) > 0