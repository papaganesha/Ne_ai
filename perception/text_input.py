# perception/text_input.py

from perception.inputs import normalize_event

def text_event(text: str, source="manual"):
    """
    Texto puro: páginas web, anotações, descrições humanas.
    """
    return normalize_event(
        event_type="text",
        source=source,
        data=text,
        confidence=0.9,
        meta={}
    )
