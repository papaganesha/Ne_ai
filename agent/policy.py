"""
Política de ações do agente.

Define regras sobre como reagir aos inputs.
"""

def apply_policy(intent):
    """
    Retorna ação baseada na intenção detectada
    """
    if intent == "start_stream":
        return {"action": "start_stream"}
    elif intent == "stop_stream":
        return {"action": "stop_stream"}
    elif intent == "visual_info":
        return {"action": "process_visual"}
    else:
        return {"action": "noop"}  # sem operação
