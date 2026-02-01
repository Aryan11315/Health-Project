import cv2
from models.face_model.face_model import FaceModel


def face_scan():
    """
    Uses FaceModel to:
    - detect face
    - extract facial features
    - compute face-only likelihoods
    """

    model = FaceModel()
    cap = cv2.VideoCapture(1)

    print("Face scan started. Press 'q' to capture.")

    while True:
        ret, frame = cap.read()
        cv2.imshow("Face Scan", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    output = model.predict(frame)

    if output is None:
        print("No face detected.")
        return None

    return output
