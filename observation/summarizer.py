def summarize_observations(face_data, eye_data):
    observations = []

    features = face_data["features"]
    likelihoods = face_data["face_likelihoods"]

    if features["eye_fatigue"] > 0.5:
        observations.append("facial_fatigue_detected")

    if features["nasal_irritation"] > 0.5:
        observations.append("nasal_irritation_detected")

    if likelihoods["fever_likelihood"] > 0.6:
        observations.append("fever_like_pattern")

    if not observations:
        observations.append("no_visible_facial_anomalies")

    return observations
