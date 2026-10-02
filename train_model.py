
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# 1. Load our dataset
df = pd.read_csv("data/investment_messages.csv")

# 2. Basic data cleaning
df = df.dropna(subset=["text", "label"])
df = df.drop_duplicates(subset=["text"])
df["text"] = df["text"].astype(str).str.strip()
df["label"] = df["label"].astype(str).str.strip()

# Remove empty messages
df = df[df["text"] != ""]

print("Dataset loaded successfully!")
print("Total messages:", len(df))
print("\nLabel counts:")
print(df["label"].value_counts())

# 3. Separate messages (X) and labels (y)
X = df["text"]
y = df["label"]

# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print("\nTraining messages:", len(X_train))
print("Testing messages:", len(X_test))

# 5. Build the machine-learning pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=42
        )
    )
])

# 6. Train the model
model.fit(X_train, y_train)

print("\nModel training completed!")

# 7. Evaluate on messages not used for training
y_pred = model.predict(X_test)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(
    y_test,
    y_pred,
    labels=["NOT_SUSPICIOUS", "SUSPICIOUS"]
))

# 8. Save the trained model
joblib.dump(model, "investment_scam_model.pkl")

print("\nModel saved as investment_scam_model.pkl")