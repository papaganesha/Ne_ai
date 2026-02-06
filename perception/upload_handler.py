"""
NE-AI V1 — Upload Handler
===========================

Responsável por receber arquivos enviados pelo usuário:

- Tipos suportados: texto (.txt), imagem (.png, .jpg), vídeo (.mp4)
- Salva arquivos em storage/raw/
- Processa arquivos para aprendizado:
    - Texto → learner + vectorizer
    - Imagem → learner + vectorizer
    - Vídeo → extrai frames para análise futura
- Loga eventos no history
- Prepara payload para pipeline decision → intent → executor
"""

# =========================
# IMPORTAÇÕES
# =========================
import os
import shutil
import uuid
import cv2
import json
from memory.vectorizer import vectorize_text, vectorize_image
from cognition.learner import learn
from memory.history import log_event
from core.config import STORAGE_RAW, STORAGE_PROCESSED

# =========================
# FUNÇÕES AUXILIARES
# =========================

def save_file(uploaded_path: str, filename: str) -> str:
    """
    Salva arquivo enviado em storage/raw/ com ID único.
    
    Args:
        uploaded_path (str): caminho temporário do arquivo enviado
        filename (str): nome original do arquivo

    Returns:
        str: caminho final do arquivo salvo
    """
    ext = os.path.splitext(filename)[1]
    unique_name = f"{uuid.uuid4()}{ext}"
    final_path = os.path.join(STORAGE_RAW, unique_name)
    os.makedirs(STORAGE_RAW, exist_ok=True)
    shutil.copy2(uploaded_path, final_path)
    print(f"[UploadHandler] Arquivo salvo: {final_path}")
    return final_path

def process_text_file(file_path: str):
    """
    Processa arquivo de texto para aprendizado.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Vetorizar e aprender
    vector = vectorize_text(content)  # Para uso futuro em similarity
    learn({"type": "text", "data": content, "confidence": 0.7})
    log_event("upload_text", {"file": file_path, "vector_length": len(vector)})

def process_image_file(file_path: str):
    """
    Processa imagem para aprendizado.
    """
    import numpy as np
    img = cv2.imread(file_path)
    if img is None:
        print(f"[UploadHandler] Erro ao ler imagem: {file_path}")
        return
    vector = vectorize_image(img)
    learn({"type": "vision", "data": img, "confidence": 0.7})
    log_event("upload_image", {"file": file_path, "vector_length": len(vector)})

def process_video_file(file_path: str, frame_interval: int = 30):
    """
    Processa vídeo, extrai frames e aprende com eles.

    Args:
        file_path (str): caminho do vídeo
        frame_interval (int): pular frames (ex.: 30 → 1 frame por segundo se 30fps)
    """
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print(f"[UploadHandler] Erro ao abrir vídeo: {file_path}")
        return

    frame_count = 0
    learned_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            vector = vectorize_image(frame)
            learn({"type": "vision", "data": frame, "confidence": 0.7})
            learned_frames += 1

        frame_count += 1

    cap.release()
    log_event("upload_video", {"file": file_path, "frames_learned": learned_frames})
    print(f"[UploadHandler] Vídeo processado: {file_path}, frames aprendidos: {learned_frames}")

# =========================
# FUNÇÃO PRINCIPAL
# =========================

def handle_upload(uploaded_path: str, filename: str):
    """
    Função principal para lidar com qualquer upload.

    Args:
        uploaded_path (str): caminho temporário do arquivo
        filename (str): nome original do arquivo
    """
    saved_path = save_file(uploaded_path, filename)
    ext = os.path.splitext(filename)[1].lower()

    if ext in [".txt"]:
        process_text_file(saved_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        process_image_file(saved_path)
    elif ext in [".mp4", ".mov"]:
        process_video_file(saved_path)
    else:
        print(f"[UploadHandler] Tipo de arquivo não suportado: {filename}")
        log_event("upload_unknown", {"file": saved_path})

# =========================
# TESTE ISOLADO
# =========================
if __name__ == "__main__":
    # Simulação de upload de arquivos
    test_files = [
        ("./tests/sample.txt", "sample.txt"),
        ("./tests/sample.jpg", "sample.jpg"),
        ("./tests/sample.mp4", "sample.mp4")
    ]

    for path, name in test_files:
        handle_upload(path, name)
