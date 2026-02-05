"""
Persistência da memória do NE-AI V1.

- Salva e carrega memória em arquivo JSON.
- Armazena todo conhecimento aprendido.
"""

import json
import os
from core.config import MEMORY_FILE

def load_memory():
    """
    Carrega memória do disco.
    Retorna uma lista de conhecimentos.
    """
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # arquivo corrompido, reinicia memória
                return []
    return []

def save_memory(memory_list):
    """
    Salva memória no disco.
    """
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory_list, f, ensure_ascii=False, indent=4)
