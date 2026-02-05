# web/handlers/stream.py

import threading
from perception.screen_stream import stream_screen
from processing.processor import process_event
from cognition.learner import decide, learn

# Placeholder de provider
class DummyProvider:
    def get_frame(self):
        # Aqui você integraria mss ou pyautogui
        import numpy as np
        return np.zeros((480, 640, 3), dtype=np.uint8)

_provider = DummyProvider()
_thread = None
_running = False

def _stream_loop():
    global _running
    for event in stream_screen(_provider):
        if not _running:
            break
        processed = process_event(event)
        decision = decide(processed)
        if decision["action"] == "learn":
            learn(decision["payload"])

def start_stream():
    global _thread, _running
    if _thread is None or not _thread.is_alive():
        _running = True
        _thread = threading.Thread(target=_stream_loop)
        _thread.start()

def stop_stream():
    global _running
    _running = False
