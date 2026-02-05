"""
NE-AI V1 — Intent
===================

Responsável por interpretar intenções do input processado:

- Recebe payload do decision.py
- Analisa tipo de input (texto, visão)
- Extrai intenção principal
- Prepara estrutura para executor.py
"""

# =========================
# IMPORTAÇÕES
# =========================
from typing import Dict
from perception.text_normalizer import normalize_text

# =========================
# FUNÇÕES PRINCIPAIS
# =========================

def extract_intent(payload: Dict) -> Dict:
    """
    Interpreta o input e extrai intenção.

    Args:
        payload (Dict): Input processado (texto ou visão)

    Returns:
        Dict: Estrutura com intenção, tipo e dados
    """
    input_type = payload.get("type")
    data = payload.get("data", "")

    intent = "unknown"

    # =========================
    # Para texto
    # =========================
    if input_type == "text":
        normalized = normalize_text(data)

        # Exemplo simplificado: keywords para ação
        if "abrir" in normalized:
            intent = "open"
        elif "fechar" in normalized:
            intent = "close"
        elif "enviar" in normalized:
            intent = "send"
        else:
            intent = "inform"

    # =========================
    # Para visão (placeholder)
    # =========================
    elif input_type == "vision":
        # Futuro: analisar frames e extrair intenção
        intent = "perceive"

    # =========================
    # Retorno do payload para executor
    # =========================
    return {
        "intent": intent,
        "type": input_type,
        "original_data": data
    }

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    sample_payloads = [
        {"type": "text", "data": "Abrir janela"},
        {"type": "text", "data": "Enviar relatório"},
        {"type": "vision", "data": "frame_dummy"}
    ]

    for payload in sample_payloads:
        result = extract_intent(payload)
        print(f"[Intent] Input: {payload['data']} → Intenção: {result['intent']}")
