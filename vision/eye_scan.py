import cv2
import numpy as np
from config.settings import (
    CAMERA_INDEX,
    WINDOW_NAME_EYE,
    EYE_REDNESS_THRESHOLD
)

def eye_scan():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    print("Eye scan started. Press 'q' to capture.")

    while True:
        ret, frame = cap.read()
        cv2.imshow(WINDOW_NAME_EYE, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Simple eye-region approximation (MVP)
    h, w, _ = frame.shape
    eye_region = frame[int(h*0.3):int(h*0.5), int(w*0.3):int(w*0.5)]

    redness_value = np.mean(eye_region[:, :, 2])
    eye_redness = 1 if redness_value > EYE_REDNESS_THRESHOLD else 0

    cap.release()
    cv2.destroyAllWindows()

    return {
        "eye_redness": eye_redness
    }
