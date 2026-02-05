"""
Cálculo de relevância de uma informação para aprendizado.

Quanto mais relevante, maior a chance de ser aprendido automaticamente.
"""

def calculate_relevance(data):
    """
    data: dicionário contendo 'type' e 'data'

    Retorna valor entre 0.0 e 1.0 indicando relevância
    """
    if data.get("type") == "text":
        # textos curtos menos relevantes, textos longos mais relevantes
        return min(1.0, len(data.get("data", "")) / 100)
    elif data.get("type") == "vision":
        # imagens e frames têm relevância média por padrão
        return 0.5
    return 0.3  # default para outros tipos
