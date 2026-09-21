import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

import joblib


# 1. Load dataset
df = pd.read_csv("data/tickets.csv")


# 2. Input and target
X = df["message"]
y = df["category"]


# 3. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# 4. Create ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2)
    )),
    ("classifier", LogisticRegression(
        max_iter=1000
    ))
])


# 5. Train model
model.fit(X_train, y_train)


# 6. Evaluate model
y_pred = model.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred))


# 7. Save model
joblib.dump(
    model,
    "models/ticket_classifier.joblib"
)

print("Model saved successfully!")