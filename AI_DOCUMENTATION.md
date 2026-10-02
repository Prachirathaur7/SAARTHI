
# Investment Scam Detection System
## AI/ML Project Documentation

### 1. Project Overview
The Investment Scam Detection System analyzes investment-related
messages and identifies potential warning signs using machine
learning and rule-based text analysis.

The system returns a risk category, model confidence, reasons,
and a recommendation in JSON format.

### 2. Problem Statement
Investors may encounter messages promising unrealistic returns,
pressuring them to invest immediately, or requesting advance fees
or sensitive account information.

Our project aims to help users recognize potential warning signs
before acting on investment-related messages.

The output is an initial risk assessment, not proof of fraud.

### 3. Target Users
- New and inexperienced investors
- People receiving investment offers through messages
- Users who want to check suspicious investment communications

### 4. Technology Stack
- Python
- Pandas for dataset handling
- Scikit-learn for machine learning
- TF-IDF for text feature extraction
- Logistic Regression for text classification
- Joblib for saving and loading the model
- FastAPI for the prediction API
- Uvicorn for running the API server

### 5. Dataset
Dataset file: data/investment_messages.csv

Number of examples: 30
- NOT_SUSPICIOUS: 18
- SUSPICIOUS: 12

The current dataset consists of a small set of manually written
examples for prototype development. It is not a verified,
representative dataset of real-world investment scams.

Dataset source: Project-created examples.
External dataset license: Not applicable to these original examples.
Any future external datasets must be checked for their source,
license, permitted use, and redistribution conditions.

### 6. Data Preprocessing
The dataset was loaded using Pandas.

The dataset was checked for:
- Missing values
- Duplicate messages
- Empty text fields
- Label consistency

Text is converted into numerical features using TF-IDF so that
the classifier can process it.

The dataset is divided into training and testing subsets.

### 7. Machine Learning Model
The project uses a Scikit-learn text-classification pipeline
with TF-IDF vectorization and Logistic Regression.

Training:
The model learns patterns associated with the labels in the
training examples.

Prediction:
A new message is transformed using the fitted TF-IDF vectorizer.
The classifier predicts a category based on its learned patterns.

The trained model is saved as:
investment_scam_model.pkl

### 8. Evaluation
Initial test results:
- Test examples: 8
- Accuracy: 50%
- NOT_SUSPICIOUS precision: 0.60
- NOT_SUSPICIOUS recall: 0.60
- SUSPICIOUS precision: 0.33
- SUSPICIOUS recall: 0.33

Initial confusion matrix:

                 Predicted
                 NOT_SUSPICIOUS  SUSPICIOUS
Actual NOT_SUSPICIOUS      3          2
Actual SUSPICIOUS          2          1

These results come from a very small synthetic dataset.
They do not establish reliable real-world detection performance.

### 9. Risk Assessment and Output
The prediction function returns:

- risk: HIGH, MEDIUM, LOW, or UNKNOWN
- confidence: estimated class probability, or null when
  there is insufficient text
- reasons: detected warning phrases or classifier explanation
- recommendation: general safety guidance

HIGH is assigned when the classifier predicts SUSPICIOUS.
MEDIUM is assigned when the classifier does not flag the message
but configured warning phrases are detected.
LOW means the message was not flagged by these checks.
UNKNOWN means the input is too short to analyze.

These are prototype categories, not verified fraud probabilities.

### 10. API Integration
The project exposes a FastAPI endpoint.

Method: POST
Endpoint: /analyze
Request content type: application/json

Example request:

{
  "message": "Guaranteed 10x returns. Invest now!"
}

Example response structure:

{
  "risk": "HIGH",
  "confidence": 0.60,
  "reasons": [
    "Unrealistic profit claims",
    "Urgent payment pressure"
  ],
  "recommendation": "Verify the source independently before investing."
}

The actual prediction and confidence may differ for each input.

### 11. Testing
The API was tested through the interactive Swagger UI.

Test categories:
- Suspicious investment messages
- Ordinary investment education messages
- Short messages
- Empty messages
- Hindi/Hinglish messages
- Unrelated messages
- Invalid JSON requests

Record the actual result of each test before presenting it
as completed.

### 12. Limitations
- The dataset is small and synthetic.
- The test set contains only eight examples.
- The model may produce false positives and false negatives.
- Hindi and Hinglish performance has not been validated.
- Warning phrases are based on a limited manually defined list.
- Confidence scores are not calibrated fraud probabilities.
- The system does not verify SEBI registration or live financial data.
- A LOW result does not mean an investment is safe.

### 13. Future Improvements
- Collect larger, verified, appropriately licensed datasets.
- Add representative Hindi and Hinglish examples.
- Evaluate on a larger, independent test set.
- Measure false-positive and false-negative rates.
- Calibrate probability estimates.
- Add verified financial-source checks.
- Improve API security and input validation.
- Conduct privacy and security testing.

### 14. Conclusion
The project demonstrates a basic machine-learning workflow for
analyzing investment-related text, identifying potential warning
signs, and returning structured results through an API.

It is a prototype intended to support user awareness.
It must not be treated as a guarantee that an investment
is legitimate or fraudulent.