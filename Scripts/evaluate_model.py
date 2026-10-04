from pathlib import Path
import json

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from app.engine import process_message


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "synthetic"
    / "pediatric_care_cases.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "synthetic"
    / "evaluation_results.json"
)


LABELS = [
    "LOW_REVIEW",
    "MEDIUM_REVIEW",
    "HIGH_REVIEW",
]


def build_model():
    """
    Build the Small AI text classification model.

    The model uses TF-IDF features and Logistic Regression.
    """

    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    lowercase=True,
                    min_df=1,
                    sublinear_tf=True,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=3000,
                    class_weight="balanced",
                ),
            ),
        ]
    )


def evaluate_ml_model(model, X_test, y_test):
    """
    Evaluate the ML classifier on the held-out test set.
    """

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision, recall, f1, _ = (
        precision_recall_fscore_support(
            y_test,
            predictions,
            labels=LABELS,
            average="macro",
            zero_division=0,
        )
    )

    report = classification_report(
        y_test,
        predictions,
        labels=LABELS,
        output_dict=True,
        zero_division=0,
    )

    matrix = confusion_matrix(
        y_test,
        predictions,
        labels=LABELS,
    )

    return {
        "accuracy": round(float(accuracy), 4),
        "macro_precision": round(float(precision), 4),
        "macro_recall": round(float(recall), 4),
        "macro_f1": round(float(f1), 4),
        "classification_report": report,
        "confusion_matrix": {
            "labels": LABELS,
            "matrix": matrix.tolist(),
        },
    }


def evaluate_multilingual_cases(model):
    """
    Evaluate the trained ML model on English,
    Arabic, and bilingual caregiver scenarios.

    These tests are separate from the main held-out
    synthetic test set.
    """

    test_cases = [
        # English
        {
            "language": "English",
            "text": "The next appointment is confirmed.",
            "expected": "LOW_REVIEW",
        },
        {
            "language": "English",
            "text": "The pharmacy does not have the medication.",
            "expected": "MEDIUM_REVIEW",
        },
        {
            "language": "English",
            "text": (
                "The medication is unavailable and "
                "care has been interrupted."
            ),
            "expected": "HIGH_REVIEW",
        },

        # Arabic
        {
            "language": "Arabic",
            "text": "الموعد مؤكد والمتابعة مستمرة.",
            "expected": "LOW_REVIEW",
        },
        {
            "language": "Arabic",
            "text": "الدواء غير متوفر.",
            "expected": "MEDIUM_REVIEW",
        },
        {
            "language": "Arabic",
            "text": (
                "الدواء غير متوفر ولم نستطع "
                "الوصول إلى المستشفى."
            ),
            "expected": "HIGH_REVIEW",
        },

        # Bilingual
        {
            "language": "Bilingual",
            "text": (
                "The medication is unavailable "
                "والإحالة معلقة."
            ),
            "expected": "HIGH_REVIEW",
        },
        {
            "language": "Bilingual",
            "text": (
                "Appointment is not confirmed "
                "والمتابعة متأخرة."
            ),
            "expected": "MEDIUM_REVIEW",
        },
    ]

    results = []

    for case in test_cases:

        try:
            prediction = model.predict(
                [case["text"]]
            )[0]

            passed = (
                prediction ==
                case["expected"]
            )

            results.append(
                {
                    "language": case["language"],
                    "text": case["text"],
                    "expected": case["expected"],
                    "predicted": str(prediction),
                    "passed": passed,
                }
            )

        except Exception as error:

            results.append(
                {
                    "language": case["language"],
                    "text": case["text"],
                    "expected": case["expected"],
                    "predicted": None,
                    "passed": False,
                    "error": str(error),
                }
            )

    total = len(results)

    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    accuracy = (
        passed / total
        if total
        else 0
    )

    language_summary = {}

    for language in [
        "English",
        "Arabic",
        "Bilingual",
    ]:

        language_results = [
            result
            for result in results
            if result["language"] == language
        ]

        language_passed = sum(
            1
            for result in language_results
            if result["passed"]
        )

        language_total = len(
            language_results
        )

        language_summary[language] = {
            "total": language_total,
            "passed": language_passed,
            "accuracy": round(
                language_passed /
                language_total,
                4
            )
            if language_total
            else 0,
        }

    return {
        "overall_accuracy": round(
            float(accuracy),
            4
        ),
        "total_cases": total,
        "passed_cases": passed,
        "failed_cases": total - passed,
        "by_language": language_summary,
        "cases": results,
    }


def evaluate_rule_engine():
    """
    Evaluate the complete YASER AI processing pipeline.

    This checks whether the bilingual NLP and rule engine
    correctly identify representative care-continuity cases.
    """

    test_cases = [
        {
            "text": (
                "The next appointment is confirmed "
                "and the medication is available."
            ),
            "expected": "LOW_REVIEW",
        },
        {
            "text": (
                "The pharmacy does not have "
                "the medication."
            ),
            "expected": "MEDIUM_REVIEW",
        },
        {
            "text": (
                "The medication is unavailable "
                "and care has been interrupted."
            ),
            "expected": "HIGH_REVIEW",
        },
        {
            "text": "الدواء غير متوفر.",
            "expected": "MEDIUM_REVIEW",
        },
        {
            "text": (
                "الدواء غير متوفر ولم نستطع "
                "الوصول إلى المستشفى."
            ),
            "expected": "HIGH_REVIEW",
        },
        {
            "text": (
                "الموعد غير مؤكد والإحالة معلقة."
            ),
            "expected": "MEDIUM_REVIEW",
        },
        {
            "text": (
                "توقف العلاج منذ 3 أسابيع."
            ),
            "expected": "HIGH_REVIEW",
        },
    ]

    results = []

    for case in test_cases:

        try:
            result = process_message(
                case["text"]
            )

            prediction = result["priority"]

            passed = (
                prediction ==
                case["expected"]
            )

            results.append(
                {
                    "text": case["text"],
                    "expected": case["expected"],
                    "predicted": prediction,
                    "score": result["score"],
                    "reasons": result["reasons"],
                    "language": result["language"],
                    "passed": passed,
                }
            )

        except Exception as error:

            results.append(
                {
                    "text": case["text"],
                    "expected": case["expected"],
                    "predicted": None,
                    "score": None,
                    "reasons": [],
                    "language": None,
                    "passed": False,
                    "error": str(error),
                }
            )

    total = len(results)

    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    return {
        "total_cases": total,
        "passed_cases": passed,
        "failed_cases": total - passed,
        "accuracy": round(
            passed / total,
            4
        )
        if total
        else 0,
        "cases": results,
    }


def evaluate_edge_cases():
    """
    Test robustness against empty and minimal inputs.
    """

    test_cases = [
        {
            "name": "Empty message",
            "text": "",
        },
        {
            "name": "Whitespace message",
            "text": "   ",
        },
        {
            "name": "Short message",
            "text": "No medication.",
        },
    ]

    results = []

    for case in test_cases:

        try:

            result = process_message(
                case["text"]
            )

            results.append(
                {
                    "name": case["name"],
                    "passed": True,
                    "priority": result["priority"],
                    "language": result["language"],
                }
            )

        except Exception as error:

            results.append(
                {
                    "name": case["name"],
                    "passed": False,
                    "error": str(error),
                }
            )

    total = len(results)

    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    return {
        "total_cases": total,
        "passed_cases": passed,
        "failed_cases": total - passed,
        "robustness_rate": round(
            passed / total,
            4
        )
        if total
        else 0,
        "cases": results,
    }


def print_section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def main():

    print_section(
        "YASER AI MODEL EVALUATION"
    )

    if not DATA_PATH.exists():

        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    data = pd.read_csv(
        DATA_PATH
    )

    required_columns = {
        "caregiver_message",
        "risk_level",
    }

    missing_columns = (
        required_columns -
        set(data.columns)
    )

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

    X = data[
        "caregiver_message"
    ].astype(str)

    y = data[
        "risk_level"
    ].astype(str)

    print(
        f"Dataset size: {len(data)}"
    )

    print()
    print("Class distribution:")

    print(
        y.value_counts()
        .sort_index()
        .to_string()
    )

    # --------------------------------------------------
    # Train / test split
    # --------------------------------------------------

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.25,
            random_state=42,
            stratify=y,
        )
    )

    print()
    print(
        f"Training cases: {len(X_train)}"
    )

    print(
        f"Test cases: {len(X_test)}"
    )

    # --------------------------------------------------
    # Train model
    # --------------------------------------------------

    model = build_model()

    model.fit(
        X_train,
        y_train,
    )

    # --------------------------------------------------
    # Main ML evaluation
    # --------------------------------------------------

    ml_metrics = evaluate_ml_model(
        model,
        X_test,
        y_test,
    )

    print_section(
        "HELD-OUT ML EVALUATION"
    )

    print(
        f"Accuracy:          "
        f"{ml_metrics['accuracy']:.2%}"
    )

    print(
        f"Macro Precision:   "
        f"{ml_metrics['macro_precision']:.2%}"
    )

    print(
        f"Macro Recall:      "
        f"{ml_metrics['macro_recall']:.2%}"
    )

    print(
        f"Macro F1:          "
        f"{ml_metrics['macro_f1']:.2%}"
    )

    # --------------------------------------------------
    # Multilingual evaluation
    # --------------------------------------------------

    multilingual = (
        evaluate_multilingual_cases(
            model
        )
    )

    print_section(
        "MULTILINGUAL ML EVALUATION"
    )

    print(
        f"Overall accuracy: "
        f"{multilingual['overall_accuracy']:.2%}"
    )

    for language, metrics in (
        multilingual[
            "by_language"
        ].items()
    ):

        print(
            f"{language}: "
            f"{metrics['accuracy']:.2%}"
        )

    # --------------------------------------------------
    # Rule engine evaluation
    # --------------------------------------------------

    rule_results = (
        evaluate_rule_engine()
    )

    print_section(
        "BILINGUAL RULE ENGINE EVALUATION"
    )

    print(
        f"Accuracy: "
        f"{rule_results['accuracy']:.2%}"
    )

    print(
        f"Passed: "
        f"{rule_results['passed_cases']}/"
        f"{rule_results['total_cases']}"
    )

    # --------------------------------------------------
    # Edge cases
    # --------------------------------------------------

    edge_results = (
        evaluate_edge_cases()
    )

    print_section(
        "ROBUSTNESS / EDGE CASES"
    )

    print(
        f"Robustness rate: "
        f"{edge_results['robustness_rate']:.2%}"
    )

    print(
        f"Passed: "
        f"{edge_results['passed_cases']}/"
        f"{edge_results['total_cases']}"
    )

    # --------------------------------------------------
    # Final evaluation package
    # --------------------------------------------------

    results = {

        "project": {
            "name": "YASER AI",
            "purpose": (
                "Small AI for Pediatric "
                "Leukemia Care Continuity"
            ),
            "evaluation_type": (
                "Prototype evaluation "
                "using synthetic data"
            ),
        },

        "dataset": {
            "name": (
                "Synthetic Pediatric "
                "Care Continuity Dataset"
            ),
            "total_cases": int(len(data)),
            "training_cases": int(
                len(X_train)
            ),
            "test_cases": int(
                len(X_test)
            ),
            "synthetic": True,
            "real_patient_data": False,
        },

        "ml_evaluation": ml_metrics,

        "multilingual_evaluation": (
            multilingual
        ),

        "rule_engine_evaluation": (
            rule_results
        ),

        "robustness_evaluation": (
            edge_results
        ),

        "methodology": {
            "model": (
                "TF-IDF + Logistic Regression"
            ),
            "text_features": (
                "Unigrams and bigrams"
            ),
            "split": "75% train / 25% test",
            "random_state": 42,
            "class_weight": "balanced",
        },

        "safety_note": (
            "The system prioritizes "
            "care-continuity review and "
            "does not diagnose disease, "
            "prescribe medication, or make "
            "autonomous clinical decisions."
        ),

        "validation_note": (
            "These results are based on "
            "synthetic scenarios and do not "
            "represent clinical validation."
        ),
    }

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print_section(
        "EVALUATION COMPLETE"
    )

    print(
        f"Results saved to:\n"
        f"{OUTPUT_PATH}"
    )

    print()
    print(
        "Important:"
    )

    print(
        "This is a synthetic prototype "
        "evaluation, not clinical validation."
    )


if __name__ == "__main__":
    main()