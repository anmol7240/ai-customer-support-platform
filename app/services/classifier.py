import joblib

model = joblib.load(
    "models/ticket_classifier.joblib"
)


def predict_category(message: str) -> str:
    prediction = model.predict([message])

    return prediction[0]