import os
import joblib

MODEL_PATH = os.getenv("MODEL_PATH", "models/scam_model.pkl")
POSITIVE_LABEL = "SUSPICIOUS"
_model = None
_idx = None
_tried = False


def _load():
    global _model, _idx, _tried
    _tried = True
    if not os.path.exists(MODEL_PATH):
        print("Model file not found:", MODEL_PATH)
        return
    try:
        m = joblib.load(MODEL_PATH)
        classes = list(m.classes_)
        _idx = classes.index(POSITIVE_LABEL)
        _model = m
        print("ML model loaded, classes:", classes)
    except Exception as e:
        print("Model failed to load:", e)


def predict(text: str):
    if not _tried:
        _load()
    if _model is None:
        return None
    return float(_model.predict_proba([text])[0][_idx])