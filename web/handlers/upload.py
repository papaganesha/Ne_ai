# web/handlers/upload.py

from perception.upload_handler import handle_upload as ph_handle_upload
from processing.processor import process_event
from cognition.learner import decide, learn

def handle_upload(file_bytes, file_type: str):
    # Cria evento de percepção
    event = ph_handle_upload(file_bytes, file_type)

    # Processa evento
    processed = process_event(event)

    # Envia para learner
    decision = decide(processed)
    if decision["action"] == "learn":
        learn(decision["payload"])
