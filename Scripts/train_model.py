from pathlib import Path

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "synthetic"
    / "pediatric_care_cases.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "yaser_model.joblib"
)


def main():
    print("===================================")
    print("YASER AI MODEL TRAINING")
    print("===================================")

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    data = pd.read_csv(DATA_PATH)

    required_columns = {
        "caregiver_message",
        "risk_level",
    }

    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    data = data.dropna(
        subset=[
            "caregiver_message",
            "risk_level",
        ]
    )

    print(f"Training cases: {len(data)}")

    print()
    print("Class distribution:")

    print(
        data["risk_level"]
        .value_counts()
        .sort_index()
    )

    model = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    lowercase=True,
                    min_df=1,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                ),
            ),
        ]
    )

    model.fit(
        data["caregiver_message"],
        data["risk_level"],
    )

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    print()
    print("===================================")
    print("MODEL TRAINED SUCCESSFULLY")
    print("===================================")
    print()
    print(f"Model saved to:")
    print(MODEL_PATH)
    print()
    print("Classes:")

    for label in model.classes_:
        print(f"- {label}")


if __name__ == "__main__":
    main()