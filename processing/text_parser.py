"""
Normalização básica de texto.
"""

import re


def parse_text(text: str, source: str = "unknown"):
    """
    Transforma texto em tokens reutilizáveis.
    """

    tokens = re.findall(r"\b\w+\b", text.lower())

    return {
        "type": "text_signal",
        "source": source,
        "tokens": tokens,
        "length": len(tokens),
        "confidence": 0.9
    }
