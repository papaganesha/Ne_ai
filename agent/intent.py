"""
Interpretação de intenção do input.

Pode ser usada para:
- Diferenciar comandos do usuário
- Detectar tipo de input (ação, pergunta, informação)
"""

def detect_intent(processed_input):
    """
    Retorna string indicando intenção
    """
    input_type = processed_input.get("type")
    if input_type == "text":
        text = processed_input.get("data", "").lower()
        if any(cmd in text for cmd in ["iniciar", "começar", "start"]):
            return "start_stream"
        elif any(cmd in text for cmd in ["parar", "stop"]):
            return "stop_stream"
        else:
            return "inform"
    elif input_type == "vision":
        return "visual_info"
    return "unknown"
