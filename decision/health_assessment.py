# decision/health_assessment.py

from config.settings import (
    WEIGHT_FATIGUE,
    WEIGHT_STRESS,
    WEIGHT_EYE_REDNESS,
    LOW_RISK_MAX,
    MODERATE_RISK_MAX
)

def assess_health(face_data, eye_data, question_score):
    """
    Input:
        face_data = { "fatigue": 0/1, "stress": 0/1 }
        eye_data  = { "eye_redness": 0/1 }
        question_score = int

    Output:
        status   = string
        severity = string
    """

    risk_score = (
        face_data.get("fatigue", 0) * WEIGHT_FATIGUE +
        face_data.get("stress", 0) * WEIGHT_STRESS +
        eye_data.get("eye_redness", 0) * WEIGHT_EYE_REDNESS +
        question_score
    )

    if risk_score <= LOW_RISK_MAX:
        return "NOT SICK", "LOW"

    elif risk_score <= MODERATE_RISK_MAX:
        return "MILD COLD / FEVER-LIKE", "MODERATE"

    else:
        return "POSSIBLE FEVER / INFECTION", "HIGH"
