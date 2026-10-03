import re

from typing import Dict
from typing import Any

from .ml_engine import (
    predict_review_priority
)


SYMPTOMS = [
    "fever",
    "bleeding",
    "pain",
    "vomiting",
    "fatigue"
]


def extract_information(
    text: str
) -> Dict[str, Any]:

    text_lower = text.lower()

    extracted = {

        "symptoms": [],

        "lab_days_ago": None,

        "appointment_status": None,

        "medication_status": None,

        "referral_status": None,

        "connectivity_issue": False,

    }


    for symptom in SYMPTOMS:

        if symptom in text_lower:

            extracted[
                "symptoms"
            ].append(symptom)


    lab_patterns = [

        r"blood test.*?(\d+)\s*days?",

        r"laboratory test.*?(\d+)\s*days?",

        r"lab.*?(\d+)\s*days?",

    ]


    for pattern in lab_patterns:

        match = re.search(
            pattern,
            text_lower
        )

        if match:

            extracted[
                "lab_days_ago"
            ] = int(
                match.group(1)
            )

            break


    if (
        "appointment" in text_lower
        and (
            "not confirmed"
            in text_lower
            or "unconfirmed"
            in text_lower
            or "waiting"
            in text_lower
            or "delayed"
            in text_lower
        )
    ):

        extracted[
            "appointment_status"
        ] = "not_confirmed"

    elif (
        "appointment" in text_lower
        and "confirmed" in text_lower
    ):

        extracted[
            "appointment_status"
        ] = "confirmed"


    if (
        "medication" in text_lower
        or "medicine" in text_lower
        or "pharmacy" in text_lower
    ):

        if (
            "unavailable" in text_lower
            or "does not have" in text_lower
            or "not available" in text_lower
            or "out of stock" in text_lower
        ):

            extracted[
                "medication_status"
            ] = "unavailable"

        elif "available" in text_lower:

            extracted[
                "medication_status"
            ] = "available"


    if "referral" in text_lower:

        if (
            "pending" in text_lower
            or "delayed" in text_lower
        ):

            extracted[
                "referral_status"
            ] = "pending"

        else:

            extracted[
                "referral_status"
            ] = "mentioned"


    connectivity_words = [

        "network problem",

        "cannot contact",

        "can't contact",

        "unable to contact",

        "no network",

        "connectivity",

    ]


    for phrase in connectivity_words:

        if phrase in text_lower:

            extracted[
                "connectivity_issue"
            ] = True

            break


    return extracted


def calculate_rule_score(
    extracted: Dict[str, Any]
):

    score = 0

    reasons = []


    if extracted["symptoms"]:

        score += 2

        reasons.append(
            "Caregiver reported a symptom."
        )


    lab_days = extracted[
        "lab_days_ago"
    ]


    if lab_days is not None:

        if lab_days >= 7:

            score += 2

            reasons.append(
                "Laboratory follow-up may be delayed."
            )

        elif lab_days >= 4:

            score += 1

            reasons.append(
                "Laboratory follow-up is several days old."
            )


    if (
        extracted[
            "appointment_status"
        ]
        == "not_confirmed"
    ):

        score += 2

        reasons.append(
            "Appointment is not confirmed."
        )


    if (
        extracted[
            "medication_status"
        ]
        == "unavailable"
    ):

        score += 2

        reasons.append(
            "Medication access may be disrupted."
        )


    if (
        extracted[
            "referral_status"
        ]
        == "pending"
    ):

        score += 1

        reasons.append(
            "Referral is pending or delayed."
        )


    if extracted[
        "connectivity_issue"
    ]:

        score += 1

        reasons.append(
            "Connectivity or communication problem detected."
        )


    if score >= 5:

        priority = "HIGH_REVIEW"

    elif score >= 2:

        priority = "MEDIUM_REVIEW"

    else:

        priority = "LOW_REVIEW"


    return (
        score,
        priority,
        reasons
    )


PRIORITY_LEVEL = {

    "LOW_REVIEW": 1,

    "MEDIUM_REVIEW": 2,

    "HIGH_REVIEW": 3,

}


def highest_priority(
    first: str,
    second: str
):

    if (
        PRIORITY_LEVEL.get(
            first,
            0
        )
        >=
        PRIORITY_LEVEL.get(
            second,
            0
        )
    ):

        return first

    return second


def process_message(
    text: str
) -> Dict[str, Any]:

    if not text or not text.strip():

        return {

            "score": 0,

            "priority": "LOW_REVIEW",

            "reasons": [
                "No caregiver message provided."
            ],

            "extracted_data": {},

            "ml_prediction": None,

            "ml_confidence": None,

            "ml_probabilities": {},

            "ml_available": False,

            "human_review_required": True,

            "clinical_decision": False,

        }


    extracted = extract_information(
        text
    )


    (
        rule_score,
        rule_priority,
        rule_reasons
    ) = calculate_rule_score(
        extracted
    )


    ml_result = predict_review_priority(
        text
    )


    ml_priority = ml_result.get(
        "prediction"
    )

    ml_confidence = ml_result.get(
        "confidence"
    )


    if ml_priority:

        final_priority = highest_priority(
            rule_priority,
            ml_priority
        )

    else:

        final_priority = rule_priority


    reasons = list(
        rule_reasons
    )


    if ml_priority:

        if ml_priority == final_priority:

            reasons.append(
                f"ML model classified the message as {ml_priority}."
            )

        elif (
            PRIORITY_LEVEL.get(
                ml_priority,
                0
            )
            >
            PRIORITY_LEVEL.get(
                rule_priority,
                0
            )
        ):

            reasons.append(
                "ML model identified a higher review priority."
            )

        else:

            reasons.append(
                "Safety rules retained or increased the review priority."
            )

    else:

        reasons.append(
            "ML model unavailable; rule-based safety layer used."
        )


    reasons.append(
        "Final output is a care-continuity review priority and requires human health-worker review."
    )


    return {

        "score": rule_score,

        "priority": final_priority,

        "reasons": reasons,

        "extracted_data": extracted,

        "ml_prediction": ml_priority,

        "ml_confidence": ml_confidence,

        "ml_probabilities":
            ml_result.get(
                "probabilities",
                {}
            ),

        "ml_available":
            ml_result.get(
                "available",
                False
            ),

        "human_review_required": True,

        "clinical_decision": False,

    }