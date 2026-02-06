"""
NE-AI V1 — Web Server
=======================

Servidor web simples para receber uploads e interagir com NE-AI V1:

- Recebe arquivos via POST (texto, imagem, vídeo)
- Envia para inputs/upload_handler para processamento
- Integra com learner, history e executor
- Fornece endpoints para status e teste
"""

# =========================
# IMPORTAÇÕES
# =========================
from flask import Flask, request, jsonify
from inputs.upload_handler import handle_upload
from agent.decision import decide_action
from agent.intent import extract_intent
from agent.executor import execute_action
import os

# =========================
# CONFIGURAÇÃO
# =========================
app = Flask(__name__)

# Pasta temporária para uploads antes do processamento
UPLOAD_TEMP = "./storage/tmp"
os.makedirs(UPLOAD_TEMP, exist_ok=True)

# =========================
# ENDPOINTS PRINCIPAIS
# =========================

@app.route("/")
def index():
    return "NE-AI V1 Web Server Online"

@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Recebe upload via POST e processa.
    Espera campo 'file' no form-data.
    """
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "Nenhum arquivo enviado"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"status": "error", "message": "Nome de arquivo vazio"}), 400

    # Salva temporariamente
    temp_path = os.path.join(UPLOAD_TEMP, uploaded_file.filename)
    uploaded_file.save(temp_path)

    # Processa upload (learner, history, vectorizer)
    handle_upload(temp_path, uploaded_file.filename)

    return jsonify({"status": "success", "message": f"Arquivo {uploaded_file.filename} processado"}), 200

@app.route("/action_text", methods=["POST"])
def action_text():
    """
    Recebe texto para NE-AI V1 e executa ação completa.
    """
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"status": "error", "message": "Texto vazio"}), 400

    # Decision → Intent → Executor
    decision_payload = decide_action({"type": "text", "data": text})
    intent_payload = extract_intent(decision_payload.get("payload", {}))
    execute_action(intent_payload)

    return jsonify({"status": "success", "intent": intent_payload.get("intent")})

# =========================
# ENDPOINT DE STATUS
# =========================
@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "online", "uploads_temp": len(os.listdir(UPLOAD_TEMP))})

# =========================
# RODAR SERVIDOR
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
