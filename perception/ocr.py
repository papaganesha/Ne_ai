"""
NE-AI V1 — OCR (Optical Character Recognition)
===============================================

Responsável por extrair texto de imagens ou frames capturados
(pode ser de vídeo, streaming da tela ou uploads).

Funcionalidades:
- Recebe imagem (numpy array) e retorna texto detectado
- Integração direta com learner e text_normalizer
- Pode ser usado em conjunto com frame_filter para evitar processamento desnecessário
"""

# =========================
# IMPORTAÇÕES
# =========================
import cv2
import pytesseract  # Biblioteca OCR
import numpy as np
from perception.text_normalizer import normalize_text  # Normaliza o texto extraído

# =========================
# CONFIGURAÇÕES
# =========================
# Caso esteja usando Windows, defina o caminho para o executável do Tesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# =========================
# FUNÇÃO PRINCIPAL
# =========================

def extract_text_from_frame(frame: np.ndarray) -> str:
    """
    Extrai texto de um frame (imagem) usando OCR.

    Args:
        frame (np.ndarray): Imagem em BGR (OpenCV)

    Returns:
        str: Texto detectado e normalizado
    """
    if frame is None:
        return ""

    # Converte para escala de cinza (OCR funciona melhor)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Opcional: aplicar thresholding para melhorar contraste
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Aplica OCR
    raw_text = pytesseract.image_to_string(thresh, lang='eng')  # pode adicionar outros idiomas

    # Normaliza o texto (remove espaços extras, caracteres especiais, converte para minúsculas)
    normalized_text = normalize_text(raw_text)

    return normalized_text

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    import cv2

    # Teste com webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        text = extract_text_from_frame(frame)
        if text:
            print("[OCR] Texto detectado:", text)

        cv2.imshow("OCR Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
