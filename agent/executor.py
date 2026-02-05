"""
Executor de ações do agente.

Recebe ações definidas pela política e as executa.
"""

from core.orchestrator import Orchestrator

# Instância única do Orchestrator
orchestrator = Orchestrator()

def execute(action_dict):
    """
    Executa ação baseada no dicionário de ação
    """
    action = action_dict.get("action")
    if action == "start_stream":
        orchestrator.start_stream()
    elif action == "stop_stream":
        orchestrator.stop_stream()
    elif action == "process_visual":
        pass  # placeholder para processamento adicional
    elif action == "noop":
        pass
