"""
Módulo que gera perguntas quando o learner não tem confiança suficiente.
"""

def generate_question(data):
    """
    data: dicionário do input que precisa de confirmação
    Retorna dicionário com ação 'ask' e payload
    """
    return {
        "action": "ask",
        "question": "Não tenho certeza sobre isso. Pode confirmar?",
        "payload": data
    }
