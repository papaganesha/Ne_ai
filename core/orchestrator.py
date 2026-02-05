"""
Orquestrador do NE-AI V1

Responsável por controlar os fluxos:
- Streaming da tela
- Processamento de uploads
- Integração com learner
"""

import threading
from inputs.screen_stream import ScreenStream
from processing.processor import process_event
from cognition.learner import decide, learn

class Orchestrator:
    def __init__(self):
        self.streaming_thread = None
        self.streaming_running = False
        self.screen_stream = ScreenStream()

    def start_stream(self):
        """
        Inicia a thread de captura da tela
        """
        if self.streaming_thread is None or not self.streaming_thread.is_alive():
            self.streaming_running = True
            self.streaming_thread = threading.Thread(target=self._stream_loop)
            self.streaming_thread.start()

    def stop_stream(self):
        """
        Para a thread de captura da tela
        """
        self.streaming_running = False

    def _stream_loop(self):
        """
        Loop principal de captura e processamento da tela
        """
        for frame_event in self.screen_stream.capture_frames():
            if not self.streaming_running:
                break
            processed = process_event(frame_event)
            decision = decide(processed)
            if decision["action"] == "learn":
                learn(decision["payload"])
