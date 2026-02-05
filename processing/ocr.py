"""
OCR simples (opcional na V1).
"""

import cv2
import pytesseract


def extract_text_from_image(image):
    """
    Extrai texto de uma imagem.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray)
