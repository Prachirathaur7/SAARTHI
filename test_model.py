
import pandas as pd
import joblib

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score
)
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# 1. Load the dataset
df = pd.read_csv("data/investment_messages.csv")

# 2. Clean the data
df = df.dropna(subset=["text", "label"])
df["text"] = df["text"].astype(str).str.strip()
df["label"] = df["label"].astype(str).str.strip().str.upper()

df = df[
    (df["text"] != "") &
    (df["label"].isin(["SUSPICIOUS", "NOT_SUSPICIOUS"]))
]
df = df.drop_duplicates(subset=["text"])

X = df["text"]
y = df["label"]

print("Dataset size:", len(df))
print("\nClass counts:")
print(y.value_counts())

# 3. Split data fairly between training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# 4. Build the machine-learning pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        sublinear_tf=True
    )),
    ("classifier", LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42
    ))
])

# 5. Train the model
model.fit(X_train, y_train)

# 6. Evaluate on messages not used for training
y_pred = model.predict(X_test)

print("\nTest accuracy:",
      round(accuracy_score(y_test, y_pred) * 100, 2), "%")

print("\nClassification report:")
print(classification_report(
    y_test,
    y_pred,
    labels=["NOT_SUSPICIOUS", "SUSPICIOUS"],
    zero_division=0
))

print("\nConfusion matrix:")
print(confusion_matrix(
    y_test,
    y_pred,
    labels=["NOT_SUSPICIOUS", "SUSPICIOUS"]
))

# 7. Cross-validation on training data
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scores = cross_val_score(
    model,
    X_train,
    y_train,
    cv=cv,
    scoring="accuracy"
)

print("\n5-fold CV scores:",
      scores.round(3))
print("Mean CV accuracy:",
      round(scores.mean() * 100, 2), "%")

# 8. Save the trained model
joblib.dump(model, "investment_scam_model.pkl")
print("\nModel saved successfully!")