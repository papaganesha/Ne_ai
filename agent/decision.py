"""
Módulo de decisão do agente.

Recebe dados processados e decide ações usando learner.
"""

from cognition.learner import decide, learn

def agent_decision(processed_input):
    """
    Recebe input processado (texto ou visão) e decide ação:
    - learn: aprende automaticamente
    - ask: precisa de confirmação humana
    """
    decision_result = decide(processed_input)

    if decision_result["action"] == "learn":
        learn(decision_result["payload"])
    return decision_result
