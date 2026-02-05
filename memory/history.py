"""
Histórico de eventos aprendidos.

Permite registrar ações importantes para auditoria ou estatísticas.
"""

from datetime import datetime

HISTORY = []

def add_event(event_type, description, related_id=None):
    """
    Adiciona evento ao histórico
    """
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": event_type,
        "description": description,
        "related_id": related_id
    }
    HISTORY.append(event)

def get_history():
    """
    Retorna histórico completo
    """
    return HISTORY
