"""
NE-AI V1 — Main
================

Ponto de entrada do sistema NE-AI V1:

- Inicializa memória persistente
- Inicializa histórico
- Cria diretórios necessários
- Roda servidor web para interações
- Mantém arquitetura modular e pronta para upgrade
"""

# =========================
# IMPORTAÇÕES
# =========================
import os
from memory.store import load_memory, save_memory
from memory.history import init_history
from core.config import STORAGE_RAW, STORAGE_PROCESSED, STORAGE_TMP, MEMORY_FILE
from api.web_server import app  # Servidor Flask

# =========================
# FUNÇÃO DE INICIALIZAÇÃO
# =========================

def initialize_system():
    """
    Inicializa o sistema:
    - Memória
    - Histórico
    - Pastas de armazenamento
    """
    print("[Main] Inicializando NE-AI V1...")

    # Pastas necessárias
    os.makedirs(STORAGE_RAW, exist_ok=True)
    os.makedirs(STORAGE_PROCESSED, exist_ok=True)
    os.makedirs(STORAGE_TMP, exist_ok=True)

    # Carregar memória
    memory = load_memory()
    print(f"[Main] Memória carregada com {len(memory)} itens")

    # Inicializar histórico
    init_history()
    print("[Main] Histórico inicializado")

    print("[Main] Sistema pronto para rodar")

# =========================
# EXECUÇÃO DO SISTEMA
# =========================

if __name__ == "__main__":
    # Inicialização completa
    initialize_system()

    # Rodar servidor web
    print("[Main] Rodando servidor web na porta 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
