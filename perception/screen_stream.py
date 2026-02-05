# perception/screen_stream.py

import time
from perception.inputs import normalize_event

def stream_screen(frame_provider):
    """
    Recebe frames da tela (ex: mss, pyautogui, opencv).
    Não processa, apenas empacota.
    """
    while True:
        frame = frame_provider.get_frame()

        event = normalize_event(
            event_type="frame",
            source="screen",
            data=frame,
            confidence=0.6,
            meta={
                "timestamp": time.time()
            }
        )

        yield event
