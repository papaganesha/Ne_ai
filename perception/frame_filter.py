"""
Filtragem de frames para reduzir redundância e uso de memória.

Exemplo:
- Remove frames repetidos ou muito similares
- Pode ser estendido para compressão de frames
"""

import numpy as np
import cv2

def is_frame_similar(frame1, frame2, threshold=0.95):
    """
    Compara dois frames usando correlação de histograma
    Retorna True se forem muito similares
    """
    if frame1 is None or frame2 is None:
        return False

    # Converte para escala de cinza
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Calcula histograma
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])

    # Normaliza
    cv2.normalize(hist1, hist1)
    cv2.normalize(hist2, hist2)

    # Correlação
    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return correlation > threshold
