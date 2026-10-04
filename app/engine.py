from .nlp import extract_signals
from .ml_engine import predict_review_priority


def calculate_rule_score(signals: dict) -> tuple[int, list[str]]:
    score = 0
    reasons = []

    symptoms = signals.get("symptoms", [])

    if symptoms:
        score += 2
        reasons.append(
            "A reported symptom requires human review."
        )

    if signals.get("medication_unavailable"):
        score += 2
        reasons.append(
            "Medication access barrier detected."
        )

    if signals.get("appointment_not_confirmed"):
        score += 2
        reasons.append(
            "Follow-up appointment is not confirmed."
        )

    if signals.get("referral_pending"):
        score += 1
        reasons.append(
            "Referral is still pending."
        )

    if signals.get("connectivity_issue"):
        score += 1
        reasons.append(
            "Care access or connectivity issue detected."
        )

    if signals.get("care_interruption"):
        score += 2
        reasons.append(
            "Prolonged care interruption detected."
        )

    duration_weeks = signals.get("duration_weeks")

    if duration_weeks is not None:
        if duration_weeks >= 2:
            score += 2
            reasons.append(
                "Care disruption has continued for two or more weeks."
            )
        elif duration_weeks >= 1:
            score += 1
            reasons.append(
                "Care disruption has continued for at least one week."
            )

    return score, reasons


def priority_from_score(score: int) -> str:
    if score >= 5:
        return "HIGH_REVIEW"

    if score >= 2:
        return "MEDIUM_REVIEW"

    return "LOW_REVIEW"


def merge_priorities(
    rule_priority: str,
    ml_prediction: str | None
) -> str:

    priority_order = {
        "LOW_REVIEW": 0,
        "MEDIUM_REVIEW": 1,
        "HIGH_REVIEW": 2,
    }

    if ml_prediction not in priority_order:
        return rule_priority

    if priority_order[ml_prediction] > priority_order[rule_priority]:
        return ml_prediction

    return rule_priority


def process_message(text: str) -> dict:
    text = str(text).strip()

    if not text:
        return {
            "language": "en",
            "priority": "LOW_REVIEW",
            "score": 0,
            "reasons": [],
            "extracted_data": {},
            "ml": {
                "available": False,
                "prediction": None,
                "confidence": None,
                "probabilities": {},
            },
            "human_review_required": False,
        }

    signals = extract_signals(text)

    rule_score, reasons = calculate_rule_score(signals)

    rule_priority = priority_from_score(rule_score)

    ml_result = predict_review_priority(text)

    final_priority = merge_priorities(
        rule_priority,
        ml_result.get("prediction")
    )

    human_review_required = final_priority in {
        "MEDIUM_REVIEW",
        "HIGH_REVIEW",
    }

    return {
        "language": signals.get("language", "en"),
        "priority": final_priority,
        "score": rule_score,
        "reasons": reasons,
        "extracted_data": signals,
        "ml": ml_result,
        "human_review_required": human_review_required,
    }