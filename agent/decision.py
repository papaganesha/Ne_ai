"""
NE-AI V1 — Decision
====================

Responsável por tomar decisões de aprendizado do agente:

- Recebe input processado (texto ou imagem)
- Verifica similaridade com memória existente
- Decide entre:
    - Aprender
    - Perguntar ao humano
- Integra com learner.py e history.py
"""

# =========================
# IMPORTAÇÕES
# =========================
from memory.vectorizer import vectorize_text, vectorize_image
from memory.similarity import find_most_similar
from memory.store import MEMORY_STORE
from cognition.learner import learn
from memory.history import log_event
from core.config import LEARNER_DEFAULT_CONFIDENCE

# =========================
# FUNÇÕES PRINCIPAIS
# =========================

def decide_action(input_data: dict) -> dict:
    """
    Decide a ação do agente com base no input.

    Args:
        input_data (dict): Estrutura com:
            - type: 'text' ou 'vision'
            - data: conteúdo do input
            - confidence: confiança inicial (opcional)

    Returns:
        dict: Decisão com ação e payload
    """
    input_type = input_data.get("type")
    content = input_data.get("data")
    confidence = input_data.get("confidence", LEARNER_DEFAULT_CONFIDENCE)

    # =========================
    # Vetorização
    # =========================
    if input_type == "text":
        input_vector = vectorize_text(content)
        mem_vectors = [vectorize_text(item["content"]) for item in MEMORY_STORE if item["type"] == "text"]
    elif input_type == "vision":
        # Placeholder: já vetoriza imagem antes de enviar
        input_vector = vectorize_image(content)
        mem_vectors = [vectorize_image(item["content"]) for item in MEMORY_STORE if item["type"] == "vision"]
    else:
        # Tipo desconhecido
        log_event("unknown_type", input_data)
        return {"action": "ignore", "payload": input_data}

    # =========================
    # Similaridade
    # =========================
    if mem_vectors:
        sim, idx = find_most_similar(input_vector, mem_vectors)
    else:
        sim, idx = 0.0, -1

    # =========================
    # Decisão
    # =========================
    threshold = 0.8  # Similaridade acima disso considera conhecido

    if sim >= threshold:
        # Conhecimento já existe → reforça
        log_event("reinforce", {"existing_id": MEMORY_STORE[idx]["id"], "similarity": sim})
        return {"action": "reinforce", "payload": MEMORY_STORE[idx]}
    else:
        # Conhecimento novo → aprende
        payload = {
            "type": input_type,
            "data": content,
            "confidence": confidence
        }
        learn(payload)
        log_event("learn", payload)
        return {"action": "learn", "payload": payload}

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    from perception.text_normalizer import normalize_text

    # Teste de decisão com texto
    sample_text = normalize_text("Abrir janela")
    decision = decide_action({"type": "text", "data": sample_text})
    print(f"[Decision] Ação tomada: {decision['action']}")
