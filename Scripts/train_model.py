from pathlib import Path

import pandas as pd
import joblib

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.linear_model import (
    LogisticRegression
)

from sklearn.pipeline import (
    Pipeline
)


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


DATA_PATH = (
    BASE_DIR
    / "data"
    / "synthetic"
    / "caregiver_messages.csv"
)


MODEL_PATH = (
    BASE_DIR
    / "models"
    / "yaser_model.joblib"
)


print(
    "Loading YASER AI dataset..."
)

print(DATA_PATH)


if not DATA_PATH.exists():

    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}"
    )


data = pd.read_csv(
    DATA_PATH
)


required_columns = {
    "text",
    "label"
}


if not required_columns.issubset(
    data.columns
):

    raise ValueError(
        "CSV must contain these columns: text, label"
    )


data = data.dropna(
    subset=[
        "text",
        "label"
    ]
)


print(
    f"Training examples: {len(data)}"
)


model = Pipeline([

    (
        "tfidf",

        TfidfVectorizer(

            ngram_range=(1, 2),

            lowercase=True

        )

    ),

    (

        "classifier",

        LogisticRegression(

            max_iter=1000,

            class_weight="balanced"

        )

    )

])


model.fit(

    data["text"],

    data["label"]

)


MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


joblib.dump(
    model,
    MODEL_PATH
)


print()

print(
    "==================================="
)

print(
    "YASER AI MODEL TRAINED SUCCESSFULLY"
)

print(
    "==================================="
)

print()

print(
    "Model saved to:"
)

print(
    MODEL_PATH
)

print()

print(
    "Labels:"
)

print(
    "LOW_REVIEW"
)

print(
    "MEDIUM_REVIEW"
)

print(
    "HIGH_REVIEW"
)