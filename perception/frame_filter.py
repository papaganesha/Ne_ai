"""
NE-AI V1 — Frame Filter
=======================

Responsável por verificar se um frame de vídeo ou captura de tela
é suficientemente diferente do anterior para ser processado.

Funcionalidades:
- Evita processamento repetitivo de frames quase iguais
- Pode ser usado tanto em streaming quanto em vídeo pré-gravado
- Integração com inputs/screen_stream.py e video_stream.py
"""

# =========================
# IMPORTAÇÕES
# =========================
import cv2
import numpy as np

# =========================
# FUNÇÕES PRINCIPAIS
# =========================

def is_frame_unique(current_frame: np.ndarray, last_frame: np.ndarray, threshold: float = 0.95) -> bool:
    """
    Compara o frame atual com o último capturado.

    Args:
        current_frame (np.ndarray): Frame atual (BGR)
        last_frame (np.ndarray): Último frame capturado
        threshold (float): Limite de similaridade (0.0 a 1.0)
                           Quanto maior, mais parecido precisa ser para ser descartado

    Returns:
        bool: True se o frame for suficientemente diferente, False caso seja repetido
    """
    # Se não houver frame anterior, considera único
    if last_frame is None:
        return True

    # Reduz tamanho para acelerar comparação (ex: 64x64)
    small_current = cv2.resize(current_frame, (64, 64))
    small_last = cv2.resize(last_frame, (64, 64))

    # Converte para escala de cinza
    gray_current = cv2.cvtColor(small_current, cv2.COLOR_BGR2GRAY)
    gray_last = cv2.cvtColor(small_last, cv2.COLOR_BGR2GRAY)

    # Calcula diferença absoluta entre frames
    diff = cv2.absdiff(gray_current, gray_last)

    # Calcula porcentagem de pixels diferentes
    non_zero_count = np.count_nonzero(diff)
    total_pixels = diff.size
    similarity = 1 - (non_zero_count / total_pixels)

    # Se similaridade maior que threshold → frame repetido
    if similarity > threshold:
        return False  # Não único
    else:
        return True   # Frame único

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    import cv2

    # Carrega dois frames de exemplo (ou use webcam)
    cap = cv2.VideoCapture(0)  # Webcam

    last = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if is_frame_unique(frame, last):
            print("[FrameFilter] Frame único detectado")
            last = frame.copy()
        else:
            print("[FrameFilter] Frame repetido ignorado")

        cv2.imshow("Frame Filter Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
