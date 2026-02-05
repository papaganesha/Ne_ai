# perception/upload_handler.py

from perception.inputs import normalize_event

def handle_upload(file_bytes, file_type: str):
    """
    Recebe arquivos da interface web.
    """
    return normalize_event(
        event_type=file_type,
        source="upload",
        data=file_bytes,
        confidence=0.8,
        meta={}
    )
