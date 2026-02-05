# perception/video_loader.py

import cv2
import time
from perception.inputs import normalize_event

def load_video(path: str):
    """
    Lê um vídeo salvo frame por frame.
    """
    cap = cv2.VideoCapture(path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        yield normalize_event(
            event_type="frame",
            source="video",
            data=frame,
            confidence=0.7,
            meta={
                "timestamp": time.time(),
                "path": path
            }
        )

    cap.release()
