"""
NE-AI V1 — PERSISTÊNCIA DE MEMÓRIA
Arquivo: memory/store.py
================================

Este módulo garante que tudo o que a NE-AI aprende
NÃO seja perdido ao desligar o sistema.

Função única:
- Salvar memória em disco
- Carregar memória ao iniciar

Nada de inteligência aqui.
Apenas consistência e segurança.
"""

# =========================
# IMPORTAÇÕES
# =========================

import json                     # Serialização simples
import os                       # Verificação de arquivos
from typing import List, Dict   # Tipagem clara

# =========================
# CONFIGURAÇÃO
# =========================

MEMORY_PATH = "storage/memory.json"

# =========================
# FUNÇÃO: CARREGAR MEMÓRIA
# =========================

def load_memory() -> List[Dict]:
    """
    Carrega a memória do disco.
    Se não existir, retorna lista vazia.
    """
    if not os.path.exists(MEMORY_PATH):
        return []

    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# =========================
# FUNÇÃO: SALVAR MEMÓRIA
# =========================

def save_memory(memory: List[Dict]):
    """
    Salva toda a memória no disco.
    """
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)

    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

# =========================
# TESTE ISOLADO
# =========================

if __name__ == "__main__":
    test_memory = [
        {"id": "1", "content": "teste", "confidence": 0.9}
    ]

    save_memory(test_memory)
    loaded = load_memory()
    print("Memória carregada:", loaded)
