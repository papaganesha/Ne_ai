"""
Orquestrador de processamento.

Recebe eventos da percepção e decide
qual extrator usar.
"""

from processing.vision import process_frame
from processing.ocr import extract_text_from_image
from processing.text_parser import parse_text


def process_event(event):
    """
    Roteia o evento para o processamento correto.
    """

    # Frame vindo de vídeo ou tela
    if event.type == "frame":
        return process_frame(event)

    # Imagem estática (upload, screenshot)
    if event.type == "image":
        text = extract_text_from_image(event.data)
        return parse_text(text, source="ocr")

    # Texto puro
    if event.type == "text":
        return parse_text(event.data, source=event.source)

    # Tipo não suportado
    return None
