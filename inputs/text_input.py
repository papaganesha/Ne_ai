"""
NE-AI V1 — Text Input
=====================

Responsável por receber textos enviados pelo usuário (via interface web ou outra fonte),
normalizar o texto e enviar para o módulo de cognição/learner.

Funcionalidades:
- Normalização básica (remover espaços extras, letras maiúsculas, caracteres especiais)
- Transformação em dicionário padrão para a cognição
- Integração com learner (decide, learn, reinforce)
"""

# =========================
# IMPORTAÇÕES
# =========================
from cognition.learner import decide, learn  # Funções principais do learner
from perception.text_normalizer import normalize_text  # Normaliza o texto
from typing import Dict

# =========================
# FUNÇÃO PRINCIPAL
# =========================

def process_text_input(text: str, source: str = "web") -> Dict:
    """
    Recebe texto bruto, normaliza e envia para a cognição.

    Args:
        text (str): Texto recebido do usuário
        source (str): Origem do input (web, upload, comando, etc.)

    Returns:
        Dict: Resultado da decisão do learner (learn / ask)
    """
    if not text:
        return {"action": "ignore", "reason": "Texto vazio"}

    # Normaliza o texto
    normalized = normalize_text(text)

    # Monta dicionário padrão para cognição
    data = {
        "type": "text",
        "data": normalized,
        "confidence": 0.7,  # Confiança inicial padrão
        "source": source
    }

    # Passa para a cognição decidir se aprende ou pergunta
    decision = decide(data)

    # Se o learner decidir aprender, chama learn()
    if decision["action"] == "learn":
        learn(decision["payload"])

    # Retorna decisão (learn ou ask)
    return decision

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    test_texts = [
        "Botão Iniciar",
        "  abrir janela   ",
        "Enviar dados!!!"
    ]

    for t in test_texts:
        result = process_text_input(t)
        print(f"[TextInput] Texto: '{t}' -> Decisão: {result['action']}")
