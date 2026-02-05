"""
Normalização de textos.

Pode ser usado em texto manual, OCR ou uploads.
"""

import re

def normalize_text(text):
    """
    Normaliza texto:
    - Remove espaços extras
    - Remove caracteres não alfanuméricos (exceto pontuação)
    - Converte para minúsculas
    """
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,!?]', '', text)
    text = text.lower()
    return text
