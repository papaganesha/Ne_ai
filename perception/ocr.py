"""
OCR para extrair texto de imagens e frames.
Usa pytesseract.
"""

import pytesseract
import cv2

def extract_text_from_image(image):
    """
    Recebe um frame ou imagem e retorna texto extraído
    """
    # Converte para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Limpeza básica: threshold adaptativo
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 2)

    # Extrai texto com pytesseract
    text = pytesseract.image_to_string(gray, lang="eng")
    return text.strip()
