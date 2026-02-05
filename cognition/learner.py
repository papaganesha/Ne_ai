"""
NE-AI V1 — INTEGRAÇÃO PERCEPÇÃO → PROCESSAMENTO → LEARNER
Arquivo: cognition/learner.py (V1 finalizado para integração)
================================

Este módulo agora funciona integrado com o processamento de eventos brutos.
Todos os eventos da percepção (tela, vídeo, upload, texto) passam pelo pipeline de processamento
antes de chegar aqui.

Responsabilidades:
- Decidir aprender ou perguntar
- Aprender incrementalmente
- Reforço humano
- Persistência de memória
"""

# =========================
# IMPORTAÇÕES
# =========================

import uuid                     # IDs únicos
from typing import Dict, Any

# Persistência
from memory.store import load_memory, save_memory

# =========================
# MEMÓRIA (CARREGADA DO DISCO)
# =========================

MEMORY_STORE = load_memory()

# =========================
# RELEVÂNCIA
# =========================

def calculate_relevance(data: Dict[str, Any]) -> float:
    """
    Mede quão relevante é a informação recebida.
    """
    if data.get("type") == "text_signal":
        return min(1.0, len(data.get("tokens", [])) / 100)
    if data.get("type") == "visual_signal":
        return 0.5
    return 0.3

# =========================
# CONFIANÇA
# =========================

def calculate_confidence(relevance: float, base_confidence: float) -> float:
    """
    Combina relevância com confiança inicial.
    """
    return max(0.0, min(1.0, (relevance + base_confidence) / 2))

# =========================
# DECISÃO COGNITIVA
# =========================

def decide(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decide se aprende ou pergunta ao humano.
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

    return {"action": "learn", "payload": data}

# =========================
# APRENDER
# =========================

def learn(data: Dict[str, Any]):
    """
    Salva novo conhecimento processado e persiste em disco.
    """
    knowledge = {
        "id": str(uuid.uuid4()),
        "type": data.get("type"),
        "content": data.get("features", data.get("tokens")),
        "confidence": data.get("confidence"),
        "relevance": data.get("relevance"),
        "times_seen": 1
    }

    MEMORY_STORE.append(knowledge)
    save_memory(MEMORY_STORE)

    print("[Learner] Conhecimento salvo:", knowledge["id"])

# =========================
# REFORÇO HUMANO
# =========================

def reinforce(knowledge_id: str, positive: bool = True):
    """
    Ajusta confiança com base no feedback humano.
    """
    for item in MEMORY_STORE:
        if item["id"] == knowledge_id:
            item["times_seen"] += 1
            if positive:
                item["confidence"] = min(1.0, item["confidence"] + 0.1)
            else:
                item["confidence"] = max(0.0, item["confidence"] - 0.1)
            break

    save_memory(MEMORY_STORE)

# =========================
# TESTE DE INTEGRAÇÃO
# =========================

if __name__ == "__main__":
    # Simulando evento processado (vindo do pipeline de processamento)
    sample = {
        "type": "text_signal",
        "tokens": ["botao", "iniciar"],
        "confidence": 0.7,
        "source": "manual"
    }

    decision = decide(sample)

    if decision["action"] == "learn":
        learn(decision["payload"])
    else:
        print(decision["question"])
