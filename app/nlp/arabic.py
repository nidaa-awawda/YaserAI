import re


ARABIC_PATTERNS = {
    "symptoms": {
        "fever": ["حمى", "حرارة", "سخونة"],
        "bleeding": ["نزيف", "ينزف", "نزف"],
        "pain": ["ألم", "وجع"],
        "vomiting": ["استفراغ", "قيء", "تقيؤ"],
        "fatigue": ["تعب", "إرهاق", "مرهق"],
    },

    "medication_unavailable": [
        "الدواء غير متوفر",
        "الدواء غير موجود",
        "لا يوجد الدواء",
        "لا يتوفر الدواء",
        "الصيدلية لا تملك الدواء",
        "الصيدلية لا يوجد لديها الدواء",
    ],

    "appointment_not_confirmed": [
        "الموعد غير مؤكد",
        "لم يتم تأكيد الموعد",
        "لا يوجد موعد",
        "الموعد لم يتأكد",
    ],

    "referral_pending": [
        "الإحالة معلقة",
        "الإحالة لم تتم",
        "الإحالة لم تكتمل",
        "بانتظار الإحالة",
    ],

    "connectivity_issue": [
        "لا نستطيع الوصول",
        "لم نستطع الوصول",
        "لا يمكننا الوصول",
        "لا نستطيع الذهاب",
        "لم نستطع الذهاب",
        "صعوبة الوصول",
        "صعوبة في الوصول",
        "تعذر الوصول",
        "تعذر الذهاب",
    ],

    "care_interruption": [
        "توقف العلاج",
        "توقفنا عن العلاج",
        "انقطاع العلاج",
        "انقطع العلاج",
        "انقطاع الرعاية",
        "توقفت المتابعة",
        "توقفنا عن المتابعة",
        "لم نتمكن من المتابعة",
    ],
}


def contains_any(text: str, patterns: list[str]) -> bool:
    text = text.lower()
    return any(pattern.lower() in text for pattern in patterns)


def extract_arabic_signals(text: str) -> dict:
    text = str(text).strip()

    symptoms = []

    for symptom, patterns in ARABIC_PATTERNS["symptoms"].items():
        if contains_any(text, patterns):
            symptoms.append(symptom)

    medication_unavailable = contains_any(
        text,
        ARABIC_PATTERNS["medication_unavailable"]
    )

    appointment_not_confirmed = contains_any(
        text,
        ARABIC_PATTERNS["appointment_not_confirmed"]
    )

    referral_pending = contains_any(
        text,
        ARABIC_PATTERNS["referral_pending"]
    )

    connectivity_issue = contains_any(
        text,
        ARABIC_PATTERNS["connectivity_issue"]
    )

    care_interruption = contains_any(
        text,
        ARABIC_PATTERNS["care_interruption"]
    )

    weeks_match = re.search(
        r"(?:منذ|قبل)\s+(\d+)\s*(?:أسبوع|أسابيع|اسبوع|اسابيع)",
        text
    )

    months_match = re.search(
        r"(?:منذ|قبل)\s+(\d+)\s*(?:شهر|أشهر|شهور)",
        text
    )

    duration_weeks = int(weeks_match.group(1)) if weeks_match else None
    duration_months = int(months_match.group(1)) if months_match else None

    return {
        "language": "ar",
        "symptoms": symptoms,
        "medication_unavailable": medication_unavailable,
        "appointment_not_confirmed": appointment_not_confirmed,
        "referral_pending": referral_pending,
        "connectivity_issue": connectivity_issue,
        "care_interruption": care_interruption,
        "duration_weeks": duration_weeks,
        "duration_months": duration_months,
    }