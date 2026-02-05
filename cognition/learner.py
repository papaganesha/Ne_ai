"""
Learner do NE-AI V1.

Responsável por:
- Decidir se aprende ou pergunta
- Salvar conhecimento em memória
- Reforçar aprendizado com feedback humano
"""

import uuid
from typing import Dict
from memory.store import load_memory, save_memory
from cognition.relevance import calculate_relevance
from cognition.confidence import calculate_confidence
from cognition.questioner import generate_question

# Carrega memória persistida
MEMORY_STORE = load_memory()

def decide(data: Dict):
    """
    Decide se aprende automaticamente ou pergunta.
    """
    relevance = calculate_relevance(data)
    confidence = calculate_confidence(relevance, data.get("confidence", 0))

    data["relevance"] = relevance
    data["confidence"] = confidence

    if confidence < 0.6:
        return generate_question(data)
    return {"action": "learn", "payload": data}

def learn(data: Dict):
    """
    Salva conhecimento e persiste em disco.
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

# Teste rápido
if __name__ == "__main__":
    sample = {"type": "text", "data": "Botão iniciar", "confidence": 0.7}
    decision = decide(sample)
    if decision["action"] == "learn":
        learn(decision["payload"])
    else:
        print(decision["question"])
