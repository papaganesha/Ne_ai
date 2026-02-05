"""
NE-AI V1 — COGNIÇÃO E APRENDIZADO
Arquivo: cognition/learner.py
================================

Este módulo representa o CÉREBRO COGNITIVO da V1.

Aqui o sistema:
- Avalia relevância
- Calcula confiança
- Decide aprender ou perguntar
- Armazena conhecimento

IMPORTANTE:
- Não executa ações
- Não automatiza nada
- Apenas aprende e entende

Tudo é incremental e observável.
"""

# =========================
# IMPORTAÇÕES
# =========================

import uuid                     # IDs únicos para conhecimento
from typing import Dict, Any    # Tipagem clara
import math                     # Cálculos simples

# =========================
# MEMÓRIA SIMPLES (V1)
# =========================

# Armazenamento em memória (depois vira persistente)
MEMORY_STORE = []

# =========================
# FUNÇÃO: RELEVÂNCIA
# =========================

def calculate_relevance(data: Dict[str, Any]) -> float:
    """
    Avalia o quão relevante é a informação.

    Na V1:
    - Texto longo tende a ser mais relevante
    - Frames sempre começam neutros
    """
    if data.get("type") == "text":
        length = len(data.get("data", ""))
        return min(1.0, length / 100)

    if data.get("type") == "vision":
        return 0.5

    return 0.3

# =========================
# FUNÇÃO: CONFIANÇA
# =========================

def calculate_confidence(relevance: float, base_confidence: float) -> float:
    """
    Combina relevância com confiança inicial.
    """
    return max(0.0, min(1.0, (relevance + base_confidence) / 2))

# =========================
# FUNÇÃO: DECISÃO
# =========================

def decide(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decide se o sistema:
    - Aprende
    - Pergunta
    """
    relevance = calculate_relevance(data)
    confidence = calculate_confidence(relevance, data.get("confidence", 0))

    data["relevance"] = relevance
    data["confidence"] = confidence

    if confidence < 0.6:
        return {
            "action": "ask",
            "question": "Não tenho certeza sobre isso. Pode confirmar?",
            "payload": data
        }

    return {
        "action": "learn",
        "payload": data
    }

# =========================
# FUNÇÃO: APRENDER
# =========================

def learn(data: Dict[str, Any]):
    """
    Armazena conhecimento aprendido.
    """
    knowledge = {
        "id": str(uuid.uuid4()),
        "type": data.get("type"),
        "content": data.get("data"),
        "confidence": data.get("confidence"),
        "relevance": data.get("relevance"),
        "times_seen": 1
    }

    MEMORY_STORE.append(knowledge)

    print("[Learner] Conhecimento aprendido:", knowledge["id"])

# =========================
# FUNÇÃO: FEEDBACK DO USUÁRIO
# =========================

def reinforce(knowledge_id: str, positive: bool = True):
    """
    Ajusta confiança baseado no feedback humano.
    """
    for item in MEMORY_STORE:
        if item["id"] == knowledge_id:
            item["times_seen"] += 1
            if positive:
                item["confidence"] = min(1.0, item["confidence"] + 0.1)
            else:
                item["confidence"] = max(0.0, item["confidence"] - 0.1)
            break

# =========================
# TESTE ISOLADO
# =========================

if __name__ == "__main__":
    sample = {
        "type": "text",
        "data": "Botão iniciar",
        "confidence": 0.7
    }

    decision = decide(sample)

    if decision["action"] == "learn":
        learn(decision["payload"])
    else:
        print(decision["question"])
