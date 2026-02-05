from flask import Flask, render_template, request, redirect
from handlers.upload import handle_upload
from handlers.viewer import get_memory
from handlers.stream import start_stream, stop_stream
from handlers.feedback import apply_feedback

app = Flask(__name__)

# Página inicial
@app.route("/")
def index():
    memory = get_memory()
    return render_template("index.html", memory=memory)

# Upload de arquivos
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file_type = request.form.get("type", "text")
    handle_upload(file.read(), file_type)
    return redirect("/")

# Controle do streaming
@app.route("/stream/<action>")
def stream_control(action):
    if action == "start":
        start_stream()
    elif action == "stop":
        stop_stream()
    return redirect("/")

# Feedback humano
@app.route("/feedback/<knowledge_id>/<action>")
def feedback(knowledge_id, action):
    if action not in ["positive", "negative"]:
        return redirect("/")
    apply_feedback(knowledge_id, action)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
