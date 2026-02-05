# web/handlers/feedback.py

from cognition.learner import reinforce

def apply_feedback(knowledge_id: str, action: str):
    """
    Aplica reforço humano via interface web.
    """
    positive = action == "positive"
    reinforce(knowledge_id, positive)
