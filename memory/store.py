"""
NE-AI V1 — Store
=================

Gerencia a memória persistente do NE-AI V1:

- Carrega memória de disco ao iniciar
- Salva novos conhecimentos
- Integra com learner.py
- Mantém consistência do arquivo memory.json
"""

# =========================
# IMPORTAÇÕES
# =========================
import json
import os
from core.config import MEMORY_FILE, STORAGE_PROCESSED

# =========================
# VARIÁVEIS GLOBAIS
# =========================
MEMORY_STORE = []  # Lista de conhecimentos carregados em memória

# =========================
# FUNÇÕES PRINCIPAIS
# =========================

def load_memory() -> list:
    """
    Carrega a memória persistente do arquivo MEMORY_FILE.
    """
    global MEMORY_STORE
    if not os.path.exists(MEMORY_FILE):
        MEMORY_STORE = []
        print(f"[Store] Nenhum arquivo de memória encontrado. Criando novo em {MEMORY_FILE}")
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        save_memory(MEMORY_STORE)
    else:
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                MEMORY_STORE = json.load(f)
            print(f"[Store] Memória carregada com {len(MEMORY_STORE)} itens")
        except Exception as e:
            print(f"[Store] Erro ao carregar memória: {e}")
            MEMORY_STORE = []
    return MEMORY_STORE

def save_memory(store: list):
    """
    Salva a memória persistente no disco.
    """
    try:
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(store, f, indent=2)
        print(f"[Store] Memória salva com {len(store)} itens")
    except Exception as e:
        print(f"[Store] Erro ao salvar memória: {e}")

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    # Teste de carga e salvamento
    mem = load_memory()
    print("[Store] Conteúdo inicial:", mem)

    # Adiciona item teste
    test_item = {
        "id": "abc123",
        "type": "text",
        "content": "Teste de memória",
        "confidence": 0.7,
        "relevance": 0.5,
        "times_seen": 1
    }
    mem.append(test_item)
    save_memory(mem)
    print("[Store] Conteúdo após salvar:", mem)
