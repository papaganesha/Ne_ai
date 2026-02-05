"""
NE-AI V1 — Screen Stream
========================

Responsável por capturar a tela do computador em tempo real
e enviar frames para o módulo de percepção e cognição.

Funcionalidades:
- Captura contínua de tela usando threads
- Conversão de frames para OpenCV (processamento futuro)
- Filtragem mínima para evitar frames repetidos
- Integração com o learner ou outros módulos
"""

# =========================
# IMPORTAÇÕES
# =========================
import threading          # Para rodar captura contínua sem bloquear o programa
import time               # Para controlar intervalo entre frames
import cv2                # OpenCV para manipulação de imagens
import numpy as np        # Arrays para imagens
from PIL import ImageGrab # Captura da tela
from perception.frame_filter import is_frame_unique  # Função para filtrar frames repetidos

# =========================
# VARIÁVEIS GLOBAIS
# =========================
streaming = False        # Flag global para controlar se o streaming está ativo
frame_interval = 0.5     # Intervalo entre frames (em segundos), ajustável
subscribers = []         # Lista de funções que recebem os frames capturados

# =========================
# FUNÇÕES PRINCIPAIS
# =========================

def start_stream():
    """
    Inicia a captura de tela em uma thread separada.
    """
    global streaming
    if streaming:
        print("[ScreenStream] Streaming já está ativo")
        return

    streaming = True
    thread = threading.Thread(target=_stream_loop, daemon=True)
    thread.start()
    print("[ScreenStream] Streaming iniciado")

def stop_stream():
    """
    Para a captura de tela.
    """
    global streaming
    streaming = False
    print("[ScreenStream] Streaming parado")

def subscribe(callback):
    """
    Permite que outros módulos recebam frames capturados.
    callback: função que recebe um frame (numpy array)
    """
    if callback not in subscribers:
        subscribers.append(callback)

def _stream_loop():
    """
    Loop contínuo que captura a tela e envia frames aos inscritos.
    """
    last_frame = None  # Armazena último frame para comparação
    while streaming:
        # Captura a tela inteira como imagem PIL
        screenshot = ImageGrab.grab()
        # Converte para array numpy (OpenCV usa BGR)
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Verifica se o frame é diferente do último capturado
        if is_frame_unique(frame, last_frame):
            # Atualiza último frame
            last_frame = frame.copy()
            # Envia para todos os inscritos (learner, perception, etc.)
            for callback in subscribers:
                callback(frame)

        # Espera intervalo definido antes de capturar próximo frame
        time.sleep(frame_interval)

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    def show_frame(frame):
        """
        Exemplo de callback: mostra o frame em uma janela OpenCV
        """
        cv2.imshow("Screen Stream Test", frame)
        # Fecha janela se apertar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_stream()
            cv2.destroyAllWindows()

    # Inscreve callback
    subscribe(show_frame)
    # Inicia streaming
    start_stream()
    # Mantém o loop principal vivo enquanto streaming ativo
    while streaming:
        time.sleep(1)
