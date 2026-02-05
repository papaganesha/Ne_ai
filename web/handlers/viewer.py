# web/handlers/viewer.py

from cognition.learner import MEMORY_STORE

def get_memory():
    """
    Retorna a memória atual para a interface web.
    """
    return MEMORY_STORE
