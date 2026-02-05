"""
Busca por similaridade entre conhecimentos.

Pode ser usado futuramente para:
- Encontrar itens relacionados
- Evitar duplicações de aprendizado
"""

from sklearn.metrics.pairwise import cosine_similarity

def most_similar(vector, vectors, top_n=5):
    """
    Retorna índices dos top_n itens mais similares.
    """
    if not vectors:
        return []
    sims = cosine_similarity(vector, vectors)
    sorted_indices = sims.argsort()[0][::-1][:top_n]
    return sorted_indices
