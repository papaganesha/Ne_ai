# perception/inputs.py

from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class PerceptionEvent:
    """
    Representa qualquer informação percebida pelo sistema.
    Tudo no sistema passa por aqui antes de qualquer decisão.
    """
    type: str          # text, image, frame, metadata, etc
    source: str        # screen, video, upload, manual
    data: Any          # conteúdo bruto
    confidence: float  # confiança inicial (0.0 a 1.0)
    meta: Dict[str, Any]  # infos extras (timestamp, fps, origem...)

def normalize_event(
    event_type: str,
    source: str,
    data: Any,
    confidence: float = 0.5,
    meta: Dict[str, Any] | None = None
) -> PerceptionEvent:
    """
    Normaliza qualquer entrada para um único formato.
    """
    return PerceptionEvent(
        type=event_type,
        source=source,
        data=data,
        confidence=confidence,
        meta=meta or {}
    )
