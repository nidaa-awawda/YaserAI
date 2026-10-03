from app.engine import (
    analyze_message,
    calculate_review_priority,
)


message = (
    "The child has a fever today, "
    "the last blood test was four days ago, "
    "and we have not received confirmation "
    "of the next appointment."
)


analysis = analyze_message(message)

priority = calculate_review_priority(analysis)


print("YASER AI CARE CONTINUITY ANALYSIS")
print("----------------------------------")

print("Extracted information:")
print(analysis)

print()
print("Review priority:")
print(priority["priority"])

print()
print("Score:")
print(priority["score"])

print()
print("Reasons:")

for reason in priority["reasons"]:
    print("-", reason)