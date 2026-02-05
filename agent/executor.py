"""
NE-AI V1 — Executor
====================

Responsável por executar ações do NE-AI V1 com base na intenção:

- Recebe payload do intent.py
- Executa ações simuladas (abrir, fechar, enviar, perceber)
- Loga ações para histórico
- Modular para futuras integrações reais (UI, automação, sistemas externos)
"""

# =========================
# IMPORTAÇÕES
# =========================
from memory.history import log_event

# =========================
# FUNÇÕES PRINCIPAIS
# =========================

def execute_action(intent_payload: dict):
    """
    Executa a ação com base na intenção.

    Args:
        intent_payload (dict): Estrutura com:
            - intent: intenção extraída
            - type: tipo do input (text/vision)
            - original_data: conteúdo original
    """
    intent = intent_payload.get("intent")
    input_type = intent_payload.get("type")
    data = intent_payload.get("original_data")

    # =========================
    # Ações simuladas
    # =========================
    if intent == "open":
        print(f"[Executor] Abrindo: {data}")
        log_event("action_open", {"data": data})
    elif intent == "close":
        print(f"[Executor] Fechando: {data}")
        log_event("action_close", {"data": data})
    elif intent == "send":
        print(f"[Executor] Enviando: {data}")
        log_event("action_send", {"data": data})
    elif intent == "perceive":
        print(f"[Executor] Processando percepção visual: {data}")
        log_event("action_perceive", {"data": data})
    elif intent == "inform":
        print(f"[Executor] Informação recebida: {data}")
        log_event("action_inform", {"data": data})
    else:
        print(f"[Executor] Intenção desconhecida: {data}")
        log_event("action_unknown", {"data": data})

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    # Exemplos de payload
    test_payloads = [
        {"intent": "open", "type": "text", "original_data": "Abrir janela"},
        {"intent": "send", "type": "text", "original_data": "Enviar relatório"},
        {"intent": "perceive", "type": "vision", "original_data": "frame_dummy"},
        {"intent": "inform", "type": "text", "original_data": "Botão iniciado"},
        {"intent": "unknown", "type": "text", "original_data": "???"},
    ]

    for payload in test_payloads:
        execute_action(payload)
