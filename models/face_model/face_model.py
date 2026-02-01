import cv2
import mediapipe as mp
import numpy as np

# =========================
# Layer 1: Face Detection
# =========================

class FaceDetector:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(rgb)

        if not result.multi_face_landmarks:
            return None

        landmarks = np.array(
            [[lm.x, lm.y, lm.z] for lm in result.multi_face_landmarks[0].landmark]
        )
        return landmarks


# =========================
# Layer 2: Feature Extraction
# =========================

class FaceFeatureExtractor:
    def __init__(self):
        self.LEFT_CHEEK = [50, 101, 118, 119]
        self.RIGHT_CHEEK = [280, 330, 347, 348]
        self.NOSE = [1, 2, 98, 327]

        self.prev_eye_open = None
        self.blinks = 0
        self.frames = 0

    def _roi_color(self, frame, landmarks, idxs):
        h, w, _ = frame.shape
        pts = [(int(landmarks[i][0]*w), int(landmarks[i][1]*h)) for i in idxs]
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillConvexPoly(mask, np.array(pts), 255)
        return np.array(cv2.mean(frame, mask=mask)[:3])

    def _redness(self, color):
        r, g, b = color
        return max(0, r - (g + b)/2) / 255.0

    def extract(self, frame, landmarks):
        left = self._roi_color(frame, landmarks, self.LEFT_CHEEK)
        right = self._roi_color(frame, landmarks, self.RIGHT_CHEEK)
        nose = self._roi_color(frame, landmarks, self.NOSE)

        facial_flushing = (self._redness(left) + self._redness(right)) / 2
        nasal_irritation = self._redness(nose)

        # Eye fatigue (simplified)
        eye_open = abs(landmarks[159][1] - landmarks[145][1])
        eye_fatigue = np.clip(1 - eye_open * 10, 0, 1)

        # Blink rate
        if self.prev_eye_open is not None:
            if self.prev_eye_open > 0.02 and eye_open < 0.015:
                self.blinks += 1
        self.prev_eye_open = eye_open
        self.frames += 1
        blink_rate = (self.blinks / max(1, self.frames)) * 1800  # per minute approx

        facial_activity = np.clip(abs(landmarks[13][1] - landmarks[14][1]) * 10, 0, 1)

        return {
            "facial_flushing": float(facial_flushing),
            "eye_fatigue": float(eye_fatigue),
            "blink_rate": float(blink_rate),
            "nasal_irritation": float(nasal_irritation),
            "facial_activity": float(facial_activity)
        }


# =========================
# Layer 3: Face-only Interpretation
# =========================

class FaceInterpreter:
    def predict(self, features):
        cold_score = (
            0.4 * features["nasal_irritation"] +
            0.3 * features["blink_rate"]/30 +
            0.3 * (1 - features["facial_activity"])
        )

        fever_score = (
            0.5 * features["facial_flushing"] +
            0.3 * features["eye_fatigue"] +
            0.2 * (1 - features["facial_activity"])
        )

        cold_likelihood = float(np.clip(cold_score, 0, 1))
        fever_likelihood = float(np.clip(fever_score, 0, 1))

        confidence = float(1 - abs(cold_likelihood - fever_likelihood))

        return {
            "cold_likelihood": cold_likelihood,
            "fever_likelihood": fever_likelihood,
            "confidence": confidence
        }


# =========================
# Unified Face Model
# =========================

class FaceModel:
    def __init__(self):
        self.detector = FaceDetector()
        self.extractor = FaceFeatureExtractor()
        self.interpreter = FaceInterpreter()

    def predict(self, frame):
        landmarks = self.detector.detect(frame)
        if landmarks is None:
            return None

        features = self.extractor.extract(frame, landmarks)
        likelihoods = self.interpreter.predict(features)

        return {
            "features": features,
            "face_likelihoods": likelihoods
        }
