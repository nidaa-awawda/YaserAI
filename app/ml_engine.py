from pathlib import Path

import joblib


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "yaser_model.joblib"
)


_model = None


def load_model():

    global _model

    if _model is not None:
        return _model

    if not MODEL_PATH.exists():
        return None

    try:

        _model = joblib.load(
            MODEL_PATH
        )

        return _model

    except Exception:

        return None


def model_available():

    return MODEL_PATH.exists()


def predict_review_priority(text: str):

    model = load_model()

    if model is None:

        return {
            "available": False,
            "prediction": None,
            "confidence": None,
            "probabilities": {}
        }

    text = str(text).strip()

    if not text:

        return {
            "available": False,
            "prediction": None,
            "confidence": None,
            "probabilities": {}
        }

    try:

        prediction = model.predict(
            [text]
        )[0]

        confidence = None

        probabilities = {}

        if hasattr(
            model,
            "predict_proba"
        ):

            probability_values = (
                model.predict_proba([text])[0]
            )

            classes = model.classes_

            probabilities = {
                str(label): round(
                    float(probability),
                    4
                )
                for label, probability
                in zip(
                    classes,
                    probability_values
                )
            }

            confidence = round(
                float(
                    max(probability_values)
                ),
                4
            )

        return {

            "available": True,

            "prediction": str(
                prediction
            ),

            "confidence": confidence,

            "probabilities":
                probabilities

        }

    except Exception as error:

        return {

            "available": False,

            "prediction": None,

            "confidence": None,

            "probabilities": {},

            "error": str(error)

        }