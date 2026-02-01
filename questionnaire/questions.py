# questionnaire/questions.py
# Dynamic multiple-choice questionnaire based on observations

from config.settings import MAX_QUESTIONS


# -------------------------
# Question banks
# -------------------------

BASE_QUESTIONS = [
    ("Do you feel feverish?", ["No", "Mild", "High"]),
    ("Do you have a runny or blocked nose?", ["No", "Yes"]),
    ("Do you have a sore throat?", ["No", "Yes"]),
    ("Are you coughing?", ["No", "Occasional", "Frequent"]),
]

FATIGUE_QUESTIONS = [
    ("Do you feel unusually tired today?", ["No", "Yes"]),
    ("Do you have body aches?", ["No", "Mild", "Severe"]),
]

EYE_QUESTIONS = [
    ("Do your eyes feel itchy or watery?", ["No", "Yes"]),
    ("Are your eyes sensitive to light?", ["No", "Yes"]),
]

GENERAL_QUESTIONS = [
    ("How was your sleep last night?", ["Good", "Poor"]),
    ("How long have symptoms lasted?", ["< 1 day", "1–3 days", "> 3 days"]),
]


# -------------------------
# Questionnaire engine
# -------------------------

def questionnaire(observations):
    """
    Input:
        observations = list of observation strings

    Output:
        total_score = int
    """

    questions = []

    # Always include base questions
    questions.extend(BASE_QUESTIONS)

    # Conditional questions
    if "fatigue_detected" in observations:
        questions.extend(FATIGUE_QUESTIONS)

    if "eye_irritation_detected" in observations:
        questions.extend(EYE_QUESTIONS)

    # Fill remaining slots with general questions
    questions.extend(GENERAL_QUESTIONS)

    # Limit to MAX_QUESTIONS
    questions = questions[:MAX_QUESTIONS]

    total_score = 0

    print("\nPlease answer the following questions:\n")

    for idx, (question, options) in enumerate(questions, 1):
        print(f"{idx}. {question}")
        for i, opt in enumerate(options):
            print(f"   {i}. {opt}")

        while True:
            try:
                choice = int(input("Select option: "))
                if 0 <= choice < len(options):
                    total_score += choice
                    break
                else:
                    print("Invalid option. Try again.")
            except ValueError:
                print("Please enter a number.")

        print()

    return total_score
