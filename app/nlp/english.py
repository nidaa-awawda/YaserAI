import re


ENGLISH_PATTERNS = {
    "symptoms": {
        "fever": ["fever", "temperature"],
        "bleeding": ["bleeding", "blood"],
        "pain": ["pain", "hurt"],
        "vomiting": ["vomiting", "vomit"],
        "fatigue": ["fatigue", "tired", "weakness"],
    },

    "medication_unavailable": [
        "medication is unavailable",
        "medication unavailable",
        "medication is not available",
        "medicine is unavailable",
        "medicine is not available",
        "pharmacy does not have the medication",
        "pharmacy does not have the medicine",
    ],

    "appointment_not_confirmed": [
        "appointment is not confirmed",
        "appointment not confirmed",
        "appointment is not scheduled",
        "no appointment",
    ],

    "referral_pending": [
        "referral is pending",
        "referral pending",
        "referral has not been completed",
    ],

    "connectivity_issue": [
        "cannot reach",
        "cannot access",
        "could not reach",
        "could not access",
        "unable to reach",
        "unable to access",
        "difficulty reaching",
        "difficulty accessing",
    ],

    "care_interruption": [
        "care interruption",
        "treatment interruption",
        "care was interrupted",
        "treatment was interrupted",
        "follow-up stopped",
        "could not continue care",
    ],
}


def contains_any(text: str, patterns: list[str]) -> bool:
    text = text.lower()
    return any(pattern.lower() in text for pattern in patterns)


def extract_english_signals(text: str) -> dict:
    text = str(text).strip()

    symptoms = []

    for symptom, patterns in ENGLISH_PATTERNS["symptoms"].items():
        if contains_any(text, patterns):
            symptoms.append(symptom)

    medication_unavailable = contains_any(
        text,
        ENGLISH_PATTERNS["medication_unavailable"]
    )

    appointment_not_confirmed = contains_any(
        text,
        ENGLISH_PATTERNS["appointment_not_confirmed"]
    )

    referral_pending = contains_any(
        text,
        ENGLISH_PATTERNS["referral_pending"]
    )

    connectivity_issue = contains_any(
        text,
        ENGLISH_PATTERNS["connectivity_issue"]
    )

    care_interruption = contains_any(
        text,
        ENGLISH_PATTERNS["care_interruption"]
    )

    weeks_match = re.search(
        r"(?:for|since)\s+(\d+)\s+weeks?",
        text.lower()
    )

    months_match = re.search(
        r"(?:for|since)\s+(\d+)\s+months?",
        text.lower()
    )

    duration_weeks = int(weeks_match.group(1)) if weeks_match else None
    duration_months = int(months_match.group(1)) if months_match else None

    return {
        "language": "en",
        "symptoms": symptoms,
        "medication_unavailable": medication_unavailable,
        "appointment_not_confirmed": appointment_not_confirmed,
        "referral_pending": referral_pending,
        "connectivity_issue": connectivity_issue,
        "care_interruption": care_interruption,
        "duration_weeks": duration_weeks,
        "duration_months": duration_months,
    }