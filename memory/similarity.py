"""
NE-AI V1 — Similarity
======================

Responsável por calcular similaridade entre vetores:
- Textos (TF-IDF)
- Imagens (vetores flatten)
- Integração com learner para evitar aprendizado redundante
"""

# =========================
# IMPORTAÇÕES
# =========================
import numpy as np
from typing import List

# =========================
# FUNÇÕES PRINCIPAIS
# =========================

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calcula similaridade coseno entre dois vetores.

    Args:
        vec1 (np.ndarray): Vetor 1
        vec2 (np.ndarray): Vetor 2

    Returns:
        float: Similaridade entre 0.0 e 1.0
    """
    if vec1 is None or vec2 is None:
        return 0.0

    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot / (norm1 * norm2)

def find_most_similar(target_vector: np.ndarray, vectors: List[np.ndarray]) -> (float, int):
    """
    Encontra o vetor mais similar em uma lista de vetores.

    Args:
        target_vector (np.ndarray): Vetor a ser comparado
        vectors (List[np.ndarray]): Lista de vetores para comparar

    Returns:
        (float, int): Similaridade máxima e índice do vetor mais similar
    """
    max_sim = -1
    index = -1
    for i, vec in enumerate(vectors):
        sim = cosine_similarity(target_vector, vec)
        if sim > max_sim:
            max_sim = sim
            index = i
    return max_sim, index

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    import numpy as np

    vecs = [
        np.array([1, 0, 0]),
        np.array([0, 1, 0]),
        np.array([0, 0, 1])
    ]

    target = np.array([1, 0.1, 0])

    sim, idx = find_most_similar(target, vecs)
    print(f"[Similarity] Mais similar: índice {idx} com similaridade {sim:.3f}")
