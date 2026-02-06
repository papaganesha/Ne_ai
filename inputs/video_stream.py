"""
NE-AI V1 — Video Stream
=========================

Módulo responsável por:

- Ler vídeos de arquivos
- Extrair frames em sequência
- Filtrar frames relevantes (futuro: frame_filter)
- Enviar frames para aprendizado (learner)
- Rodar como thread para integração com Orchestrator
"""

# =========================
# IMPORTAÇÕES
# =========================
import cv2
import time
from cognition.learner import learn
from memory.vectorizer import vectorize_frame
from memory.history import log_event

# =========================
# CLASSE VIDEO STREAM
# =========================
class VideoStream:
    def __init__(self, video_path=None, frame_interval=1.0):
        """
        Inicializa VideoStream.

        :param video_path: caminho do arquivo de vídeo
        :param frame_interval: tempo entre frames em segundos
        """
        self.video_path = video_path
        self.frame_interval = frame_interval
        self.running = False

    # =========================
    # MÉTODO DE PARADA
    # =========================
    def stop(self):
        """
        Para o streaming de vídeo.
        """
        self.running = False
        print("[VideoStream] Streaming parado")

    # =========================
    # MÉTODO PRINCIPAL
    # =========================
    def run(self):
        """
        Loop principal de captura de frames do vídeo.
        """
        if not self.video_path:
            print("[VideoStream] Nenhum vídeo definido")
            return

        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            print(f"[VideoStream] Falha ao abrir vídeo: {self.video_path}")
            return

        self.running = True
        print(f"[VideoStream] Iniciando vídeo: {self.video_path}")

        while self.running:
            ret, frame = cap.read()
            if not ret:
                print("[VideoStream] Fim do vídeo ou erro na captura")
                break

            # =========================
            # Processar frame
            # =========================
            # Vetorizar frame para memória
            vector = vectorize_frame(frame)

            # Criar payload para learner
            data = {
                "type": "vision",
                "data": vector,
                "confidence": 0.5  # valor inicial
            }

            # Enviar para aprendizagem
            learn(data)

            # Log simples
            log_event("video_stream", {"frame_processed": True})

            # Aguardar intervalo antes de capturar próximo frame
            time.sleep(self.frame_interval)

        cap.release()
        print("[VideoStream] Encerrando VideoStream")
