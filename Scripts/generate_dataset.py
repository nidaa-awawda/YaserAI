from pathlib import Path
import csv
import random


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = BASE_DIR / "data" / "synthetic" / "pediatric_care_cases.csv"

random.seed(42)


LOW_MESSAGES = [
    "The next appointment is confirmed.",
    "The medication is available.",
    "The child attended the planned follow-up.",
    "The next visit is scheduled.",
    "The laboratory follow-up is on schedule.",
    "The child is doing well and the next visit is confirmed.",
]

MEDIUM_MESSAGES = [
    "The medication is unavailable.",
    "The pharmacy does not have the medication.",
    "The laboratory follow-up is delayed.",
    "The referral is still pending.",
    "We are having difficulty reaching the clinic.",
    "The appointment is not confirmed.",
]

HIGH_MESSAGES = [
    "The medication is unavailable and care has been interrupted.",
    "We could not reach the hospital for two weeks.",
    "The laboratory follow-up is delayed and the medication is unavailable.",
    "The referral is pending and care has been interrupted.",
    "We have not been able to continue follow-up.",
    "The medication is unavailable and the referral has not been completed.",
]


LOCATIONS = [
    "Gaza",
    "West Bank",
]

AGE_GROUPS = [
    "0-4",
    "5-9",
    "10-14",
    "15-18",
]


def generate_low_case(index):
    return {
        "patient_id": f"YASER-{index:03d}",
        "age_group": random.choice(AGE_GROUPS),
        "location": random.choice(LOCATIONS),
        "last_visit_days": random.randint(1, 6),
        "medication_available": "Yes",
        "lab_delayed": "No",
        "referral_pending": "No",
        "connectivity": "Normal",
        "care_interruption": "No",
        "caregiver_message": random.choice(LOW_MESSAGES),
        "risk_level": "LOW_REVIEW",
    }


def generate_medium_case(index):
    message = random.choice(MEDIUM_MESSAGES)

    return {
        "patient_id": f"YASER-{index:03d}",
        "age_group": random.choice(AGE_GROUPS),
        "location": random.choice(LOCATIONS),
        "last_visit_days": random.randint(5, 10),
        "medication_available": random.choice(["Yes", "No"]),
        "lab_delayed": random.choice(["Yes", "No"]),
        "referral_pending": random.choice(["Yes", "No"]),
        "connectivity": random.choice(["Normal", "Low"]),
        "care_interruption": "No",
        "caregiver_message": message,
        "risk_level": "MEDIUM_REVIEW",
    }


def generate_high_case(index):
    return {
        "patient_id": f"YASER-{index:03d}",
        "age_group": random.choice(AGE_GROUPS),
        "location": random.choice(LOCATIONS),
        "last_visit_days": random.randint(10, 21),
        "medication_available": "No",
        "lab_delayed": "Yes",
        "referral_pending": random.choice(["Yes", "No"]),
        "connectivity": "Low",
        "care_interruption": "Yes",
        "caregiver_message": random.choice(HIGH_MESSAGES),
        "risk_level": "HIGH_REVIEW",
    }


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for index in range(1, 41):
        rows.append(generate_low_case(index))

    for index in range(41, 81):
        rows.append(generate_medium_case(index))

    for index in range(81, 121):
        rows.append(generate_high_case(index))

    fieldnames = [
        "patient_id",
        "age_group",
        "location",
        "last_visit_days",
        "medication_available",
        "lab_delayed",
        "referral_pending",
        "connectivity",
        "care_interruption",
        "caregiver_message",
        "risk_level",
    ]

    with open(
        OUTPUT_PATH,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    print("===================================")
    print("YASER AI DATASET GENERATED")
    print("===================================")
    print(f"Dataset: {OUTPUT_PATH}")
    print(f"Total cases: {len(rows)}")
    print("LOW_REVIEW: 40")
    print("MEDIUM_REVIEW: 40")
    print("HIGH_REVIEW: 40")
    print()
    print("All records are synthetic.")
    print("No real patient data is used.")


if __name__ == "__main__":
    main()