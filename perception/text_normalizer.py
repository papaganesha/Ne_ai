"""
NE-AI V1 — Text Normalizer
==========================

Responsável por normalizar textos recebidos de diversas fontes:
- Uploads de arquivos
- Entrada de usuário via web
- OCR de frames ou vídeos

Funcionalidades:
- Remove espaços extras
- Converte para minúsculas
- Remove caracteres especiais
- Prepara texto limpo para processamento pelo learner
"""

# =========================
# IMPORTAÇÕES
# =========================
import re  # Expressões regulares para limpar texto

# =========================
# FUNÇÃO PRINCIPAL
# =========================

def normalize_text(text: str) -> str:
    """
    Normaliza um texto bruto.

    Args:
        text (str): Texto de entrada

    Returns:
        str: Texto limpo e padronizado
    """
    if not text:
        return ""

    # Remove espaços no início e no fim
    text = text.strip()

    # Converte para minúsculas
    text = text.lower()

    # Remove caracteres especiais, mantendo letras, números e espaços
    text = re.sub(r'[^a-z0-9\s]', '', text)

    # Substitui múltiplos espaços por um único
    text = re.sub(r'\s+', ' ', text)

    return text

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    test_texts = [
        "   Olá, MUNDO!!!  ",
        "Enviar DADOS 123!!! ",
        "   TESTE--DE--NORMALIZAÇÃO   "
    ]

    for t in test_texts:
        normalized = normalize_text(t)
        print(f"[Normalizer] Original: '{t}' -> Normalizado: '{normalized}'")
