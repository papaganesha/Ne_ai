"""
NE-AI V1 — COGNIÇÃO E APRENDIZADO
Arquivo: cognition/learner.py
================================

VERSÃO ATUALIZADA — COM PERSISTÊNCIA

Este módulo representa o CÉREBRO COGNITIVO da V1.

Agora ele:
- Aprende
- Pergunta
- Reforça
- SALVA conhecimento em disco
- CARREGA conhecimento ao iniciar

Nada aqui executa ações.
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

# Ao importar o módulo, a memória já é carregada
MEMORY_STORE = load_memory()

# =========================
# RELEVÂNCIA
# =========================

def calculate_relevance(data: Dict[str, Any]) -> float:
    """
    Mede o quão importante é a informação.
    """
    if data.get("type") == "text":
        return min(1.0, len(data.get("data", "")) / 100)

    if data.get("type") == "vision":
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
    Salva novo conhecimento e persiste em disco.
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
# TESTE ISOLADO
# =========================

if __name__ == "__main__":
    sample = {"type": "text", "data": "Botão iniciar", "confidence": 0.7}
    decision = decide(sample)

    if decision["action"] == "learn":
        learn(decision["payload"])
    else:
        print(decision["question"])
