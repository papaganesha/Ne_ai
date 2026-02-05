# memory/store.py
"""
Módulo de persistência de memória para Ne-AI V1.

Responsabilidades:
- Carregar memória do disco ao iniciar
- Salvar memória a cada atualização
"""

import json
import os

# Caminho do arquivo de memória
MEMORY_FILE = "memory_store.json"


def load_memory():
    """
    Carrega a memória do disco.
    Retorna uma lista de dicionários representando o conhecimento.
    Se o arquivo não existir, retorna lista vazia.
    """
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                memory = json.load(f)
                print(f"[Memory] Carregadas {len(memory)} entradas da memória.")
                return memory
        except Exception as e:
            print("[Memory] Erro ao carregar memória:", e)
            return []
    else:
        print("[Memory] Arquivo de memória não encontrado, iniciando vazio.")
        return []


def save_memory(memory):
    """
    Salva a memória em disco.
    """
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)
        print(f"[Memory] Memória salva com {len(memory)} entradas.")
    except Exception as e:
        print("[Memory] Erro ao salvar memória:", e)
