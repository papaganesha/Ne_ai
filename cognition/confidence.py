"""
Cálculo de confiança de aprendizado.

Combina confiança inicial com relevância para decidir se aprende sozinho ou pergunta.
"""

def calculate_confidence(relevance, base_confidence):
    """
    Retorna valor entre 0.0 e 1.0
    """
    return max(0.0, min(1.0, (relevance + base_confidence) / 2))
