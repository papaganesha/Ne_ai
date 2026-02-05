"""
Servidor web do NE-AI V1 usando Flask.

Funcionalidades:
- Upload de arquivos (texto, imagem, vídeo)
- Início/parada do streaming da tela
- Visualização da memória aprendida
- Feedback humano (positivo/negativo)
"""

from flask import Flask, request, render_template, jsonify
from inputs.upload_handler import save_upload, handle_text_upload
from inputs.video_stream import video_to_frames
from cognition.learner import MEMORY_STORE, reinforce
from agent.decision import agent_decision
from agent.intent import detect_intent
from agent.policy import apply_policy
from agent.executor import execute

def create_app():
    app = Flask(__name__, template_folder="../web/templates", static_folder="../web/static")

    @app.route("/")
    def index():
        # Página principal, exibe memória e interface de controle
        return render_template("index.html", memory=MEMORY_STORE)

    @app.route("/upload_text", methods=["POST"])
    def upload_text():
        # Recebe texto do usuário via formulário
        text_data = request.form.get("text")
        if not text_data:
            return jsonify({"error": "No text provided"}), 400

        # Reaproveitando handle_text_upload existente
        processed = handle_text_upload(text_data)
        decision = agent_decision(processed)
        return jsonify(decision)

    @app.route("/upload_file", methods=["POST"])
    def upload_file():
        # Recebe upload de arquivo (imagem ou vídeo)
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        filename = file.filename
        if not filename:
            return jsonify({"error": "No selected file"}), 400

        # Reaproveitando save_upload
        saved_path = save_upload(file.read(), filename)

        # Se for vídeo, reaproveita video_to_frames
        if filename.lower().endswith((".mp4", ".avi", ".mov")):
            for frame_event in video_to_frames(saved_path):
                # Reaproveitando agent_decision
                agent_decision(frame_event)

        return jsonify({"status": "uploaded", "filename": filename})

    @app.route("/execute_intent", methods=["POST"])
    def execute_intent_route():
        # Recebe texto de comando e executa via agente
        text_data = request.form.get("text")
        if not text_data:
            return jsonify({"error": "No text provided"}), 400

        # Reaproveita fluxo de processamento existente
        processed = {"type": "text", "data": text_data, "confidence": 0.7}
        intent = detect_intent(processed)
        action_dict = apply_policy(intent)
        execute(action_dict)
        return jsonify({"intent": intent, "action": action_dict})

    @app.route("/feedback", methods=["POST"])
    def feedback():
        # Recebe feedback humano para reforço
        knowledge_id = request.form.get("id")
        positive = request.form.get("positive") == "true"
        if knowledge_id:
            reinforce(knowledge_id, positive)
            return jsonify({"status": "feedback_received", "id": knowledge_id})
        return jsonify({"error": "No knowledge id provided"}), 400

    @app.route("/memory", methods=["GET"])
    def memory_view():
        # Retorna memória completa para visualização
        return jsonify(MEMORY_STORE)

    return app
