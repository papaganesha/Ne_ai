"""
NE-AI V1 — History
====================

Responsável por registrar o histórico de inputs e decisões:

- Inputs processados (texto, imagem, vídeo)
- Ações tomadas (learn, ask)
- Reforço aplicado (positivo ou negativo)
- Permite auditoria, análise e futuras melhorias no aprendizado
"""

# =========================
# IMPORTAÇÕES
# =========================
import json
import time
from typing import Dict, List
from memory.store import MEMORY_STORE  # Integração com memória principal
from core.config import STORAGE_PROCESSED  # Caminhos de armazenamento

# =========================
# VARIÁVEIS GLOBAIS
# =========================
history_log: List[Dict] = []  # Lista em memória do histórico

HISTORY_FILE = f"{STORAGE_PROCESSED}/history.json"  # Arquivo persistente

# =========================
# FUNÇÕES PRINCIPAIS
# =========================

def log_event(event_type: str, payload: Dict):
    """
    Registra um evento no histórico.

    Args:
        event_type (str): Tipo de evento (ex: 'learn', 'ask', 'reinforce')
        payload (Dict): Dados associados ao evento
    """
    timestamp = time.time()
    entry = {
        "timestamp": timestamp,
        "type": event_type,
        "payload": payload
    }

    history_log.append(entry)
    save_history()
    print(f"[History] Evento '{event_type}' registrado em {timestamp}")

def save_history():
    """
    Salva histórico em disco no arquivo HISTORY_FILE
    """
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history_log, f, indent=2)
    except Exception as e:
        print(f"[History] Erro ao salvar histórico: {e}")

def load_history():
    """
    Carrega histórico do disco para memória
    """
    global history_log
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history_log = json.load(f)
            print(f"[History] Histórico carregado com {len(history_log)} eventos")
    except FileNotFoundError:
        history_log = []
        print("[History] Nenhum histórico encontrado, iniciando vazio")
    except Exception as e:
        print(f"[History] Erro ao carregar histórico: {e}")
        history_log = []

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    load_history()
    log_event("learn", {"id": "abc123", "content": "Teste de aprendizado"})
    log_event("ask", {"question": "O que é isso?", "confidence": 0.5})
    print("[History] Conteúdo do histórico:", history_log)
