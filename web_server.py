"""
NE-AI V1 — INTERFACE WEB (BACKEND)
Arquivo: api/web_server.py
================================

Este módulo expõe a NE-AI para o mundo humano.

Aqui NÃO existe inteligência.
Aqui NÃO existe aprendizado.

Função única:
- Servir uma API web local
- Permitir interação humana
- Conectar UI ↔ Core

A interface web é o USO PRINCIPAL da V1.
"""

# =========================
# IMPORTAÇÕES
# =========================

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import threading
import queue
import os

# =========================
# IMPORTA FILAS GLOBAIS
# =========================

from core.orchestrator import Orchestrator
from cognition.learner import MEMORY_STORE, reinforce
from ingestion.ingestors import input_queue
from core.orchestrator import question_queue

# =========================
# APLICAÇÃO FASTAPI
# =========================

app = FastAPI(title="NE-AI V1")

# =========================
# INSTÂNCIA DO SISTEMA
# =========================

orchestrator = Orchestrator()

# =========================
# CONTROLE DO SISTEMA
# =========================

@app.post("/start")
def start_system():
    """
    Liga o sistema cognitivo.
    """
    orchestrator.start()
    return {"status": "sistema iniciado"}


@app.post("/stop")
def stop_system():
    """
    Desliga o sistema cognitivo.
    """
    orchestrator.stop()
    return {"status": "sistema parado"}

# =========================
# UPLOAD DE ARQUIVOS
# =========================

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """
    Recebe arquivos para aprendizado.
    """
    save_path = os.path.join("storage/raw", file.filename)

    with open(save_path, "wb") as f:
        f.write(file.file.read())

    input_queue.put({
        "type": "file",
        "source": "upload",
        "path": save_path
    })

    return {"status": "arquivo recebido", "file": file.filename}

# =========================
# TEXTO MANUAL
# =========================

@app.post("/text")
def send_text(payload: dict):
    """
    Envia texto manual para o sistema.
    """
    input_queue.put({
        "type": "text",
        "source": "web",
        "data": payload.get("text")
    })

    return {"status": "texto enviado"}

# =========================
# PERGUNTAS DA IA
# =========================

@app.get("/questions")
def get_questions():
    """
    Retorna perguntas pendentes da IA.
    """
    questions = []

    while not question_queue.empty():
        questions.append(question_queue.get())

    return questions

# =========================
# RESPOSTA HUMANA
# =========================

@app.post("/answer")
def answer_question(payload: dict):
    """
    Recebe feedback humano.
    """
    knowledge_id = payload.get("knowledge_id")
    positive = payload.get("positive", True)

    reinforce(knowledge_id, positive)

    return {"status": "feedback registrado"}

# =========================
# VISUALIZAR MEMÓRIA
# =========================

@app.get("/memory")
def get_memory():
    """
    Exibe tudo que foi aprendido.
    """
    return MEMORY_STORE

# =========================
# EXECUÇÃO LOCAL
# =========================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
