
import joblib

# Load the trained TF-IDF + Logistic Regression pipeline
model = joblib.load("investment_scam_model.pkl")


def analyze_message(message):
    message = message.strip()

    if len(message) < 10:
        return {
            "risk": "UNKNOWN",
            "confidence": None,
            "reasons": ["Insufficient text to analyze"],
            "recommendation": "Enter a longer investment-related message."
        }

    # Predict the message category
    prediction = model.predict([message])[0]

    probabilities = model.predict_proba([message])[0]
    class_index = list(model.classes_).index(prediction)
    confidence = round(float(probabilities[class_index]), 2)

    # Check for common warning signs
    text = message.lower()

    warning_signs = {
        "Guaranteed returns": [
            "guaranteed returns",
            "guaranteed profit",
            "guaranteed daily"
        ],
        "Unrealistic profit claims": [
            "10x returns",
            "double your money",
            "100 percent returns",
            "zero risk"
        ],
        "Urgent payment pressure": [
            "immediately",
            "limited slots",
            "invest now",
            "pay now"
        ],
        "Potential account security risk": [
            "share your otp",
            "share your password"
        ],
        "Upfront fee request": [
            "registration fee",
            "withdrawal fee",
            "activation fee"
        ]
    }

    reasons = []

    for reason, phrases in warning_signs.items():
        if any(phrase in text for phrase in phrases):
            reasons.append(reason)

    if prediction == "SUSPICIOUS":
        risk = "HIGH"
        recommendation = (
            "Do not transfer money based on this message. "
            "Verify the source independently before investing."
        )

        if not reasons:
            reasons.append(
                "The classifier detected patterns associated "
                "with suspicious training examples."
            )

    else:
        risk = "LOW"
        recommendation = (
            "This message was not flagged by the model. "
            "That does not establish legitimacy. Verify the "
            "provider and investment details independently."
        )

        if not reasons:
            reasons.append("No configured warning phrases were detected.")

    return {
        "risk": risk,
        "confidence": confidence,
        "reasons": reasons,
        "recommendation": recommendation
    }