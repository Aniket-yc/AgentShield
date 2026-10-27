
from pathlib import Path

import joblib

MODEL_PATH = (
    Path(__file__).resolve().parents[1]
    / "models"
    / "sms_model.joblib"
)

try:
    model = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None
except Exception:
    model = None


def classify_message(text: str) -> dict:
    """Classify SMS text using the trained model, if available."""
    if model is None:
        return {
            "available": False,
            "prediction": "unavailable",
            "spam_probability": None,
            "note": "Trained model could not be loaded."
        }

    probabilities = model.predict_proba([text])[0]
    classes = list(model.classes_)

    if "spam" not in classes:
        return {
            "available": False,
            "prediction": "unavailable",
            "spam_probability": None,
            "note": "The model has no spam class."
        }

    spam_probability = float(probabilities[classes.index("spam")])

    return {
        "available": True,
        "prediction": "spam" if spam_probability >= 0.5 else "ham",
        "spam_probability": round(spam_probability, 4),
        "note": "Prediction from the trained SMS classifier."
    }
