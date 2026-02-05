"""
NE-AI V1 — MÓDULO DE INGESTÃO
============================

Este módulo é responsável por ALIMENTAR o sistema.

Ele NÃO decide.
Ele NÃO aprende.

Função única:
- Capturar dados de múltiplas fontes
- Normalizar
- Enviar para a fila de entrada

Fontes suportadas na V1:
- Streaming da tela (desktop)
- Vídeo salvo
- Upload manual
- Texto puro

Tudo roda local.
Tudo controlável.
"""

# =========================
# IMPORTAÇÕES
# =========================

import threading                 # Execução paralela
import time                      # Controle de FPS / intervalos
import queue                     # Comunicação entre módulos
from typing import Optional      # Tipagem clara

# =========================
# FILA DE ENTRADA
# =========================

# Esta fila é compartilhada com o Orchestrator
input_queue = queue.Queue()

# =========================
# CONFIGURAÇÕES
# =========================

SCREEN_CAPTURE_INTERVAL = 0.2    # segundos entre capturas de tela
VIDEO_FRAME_INTERVAL = 0.1       # segundos entre frames de vídeo

# =========================
# CLASSE BASE: INGESTOR
# =========================

class BaseIngestor(threading.Thread):
    """
    Classe base para qualquer fonte de dados.

    Cada ingestor roda em sua própria thread.
    """

    def __init__(self, source_name: str):
        super().__init__(daemon=True)
        self.source_name = source_name
        self.running = False

    def stop(self):
        """
        Encerra a thread de forma segura.
        """
        self.running = False

# =========================
# INGESTOR: TELA
# =========================

class ScreenIngestor(BaseIngestor):
    """
    Captura frames da tela.

    OBS:
    A captura real (ex: mss / pyautogui)
    será plugada depois.
    """

    def __init__(self):
        super().__init__("screen")

    def run(self):
        self.running = True
        print("[Ingestor:Screen] Iniciado")

        while self.running:
            frame = self.capture_screen()

            if frame is not None:
                input_queue.put({
                    "type": "frame",
                    "source": "screen",
                    "data": frame
                })

            time.sleep(SCREEN_CAPTURE_INTERVAL)

        print("[Ingestor:Screen] Encerrado")

    def capture_screen(self):
        """
        Aqui entrará a captura real da tela.
        Por enquanto é mock.
        """
        return "<FRAME_DA_TELA>"

# =========================
# INGESTOR: VÍDEO
# =========================

class VideoIngestor(BaseIngestor):
    """
    Lê frames de um vídeo salvo.
    """

    def __init__(self, video_path: str):
        super().__init__("video")
        self.video_path = video_path

    def run(self):
        self.running = True
        print(f"[Ingestor:Video] Lendo {self.video_path}")

        while self.running:
            frame = self.read_video_frame()

            if frame is None:
                break

            input_queue.put({
                "type": "frame",
                "source": "video",
                "data": frame
            })

            time.sleep(VIDEO_FRAME_INTERVAL)

        print("[Ingestor:Video] Finalizado")

    def read_video_frame(self):
        """
        Placeholder da leitura real.
        """
        return "<FRAME_DO_VIDEO>"

# =========================
# INGESTOR: TEXTO
# =========================

class TextIngestor:
    """
    Entrada manual de texto.
    Não precisa thread.
    """

    def ingest(self, text: str):
        input_queue.put({
            "type": "text",
            "source": "manual",
            "data": text
        })

# =========================
# INGESTOR: UPLOAD
# =========================

class UploadIngestor:
    """
    Recebe arquivos enviados pela interface web.
    """

    def ingest(self, file_path: str):
        input_queue.put({
            "type": "file",
            "source": "upload",
            "path": file_path
        })

# =========================
# TESTE ISOLADO
# =========================

if __name__ == "__main__":
    screen = ScreenIngestor()
    screen.start()

    text = TextIngestor()
    text.ingest("Olá, isso é um teste")

    time.sleep(1)
    screen.stop()
