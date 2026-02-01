# main.py
# Entry point for Health AI MVP
# Pipeline: Face Scan → Eye Scan → Questionnaire → Decision → Recommendation

from vision.face_scan import face_scan
from vision.eye_scan import eye_scan
from observation.summarizer import summarize_observations
from questionnaire.questions import questionnaire
from decision.health_assessment import assess_health
from decision.otc_advice import otc_advice


def main():
    print("\n=== HEALTH AI MVP STARTED ===\n")

    # 1. Face Scan
    print("Step 1: Face Scan")
    face_data = face_scan()
    print("Face Scan Result:", face_data)

    # 2. Eye Scan
    print("\nStep 2: Eye Scan")
    eye_data = eye_scan()
    print("Eye Scan Result:", eye_data)

    # 3. Observation Summary
    print("\nStep 3: Observation Summary")
    observations = summarize_observations(face_data, eye_data)
    print("Observations:", observations)

    # 4. Questionnaire
    print("\nStep 4: Questionnaire")
    question_score = questionnaire(observations)
    print("Questionnaire Score:", question_score)

    # 5. Health Assessment
    print("\nStep 5: Health Assessment")
    status, severity = assess_health(face_data, eye_data, question_score)

    # 6. OTC Advice
    recommendations = otc_advice(severity)

    # Final Output
    print("\n===== FINAL HEALTH REPORT =====")
    print("Health Status:", status)
    print("Severity Level:", severity)
    print("Detected Observations:", observations)

    print("\nRecommendations:")
    for rec in recommendations:
        print("-", rec)

    print("\nDisclaimer: This system is NOT a medical diagnostic tool.")
    print("=== SESSION ENDED ===\n")


if __name__ == "__main__":
    main()
