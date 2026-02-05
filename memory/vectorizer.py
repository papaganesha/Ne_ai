"""
NE-AI V1 — Vectorizer
======================

Responsável por transformar dados em vetores numéricos
para armazenar e buscar similaridade:

- Textos → embeddings vetoriais
- Imagens → vetores simplificados (placeholder para futuras integrações)
- Permite comparações de similaridade para aprendizado e decisões
"""

# =========================
# IMPORTAÇÕES
# =========================
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# =========================
# VARIÁVEIS GLOBAIS
# =========================
tfidf_vectorizer = TfidfVectorizer()  # Vetorizador TF-IDF para textos
text_corpus = []                       # Corpus para ajustar o vetor

# =========================
# FUNÇÕES DE TEXTO
# =========================

def fit_text_corpus(texts):
    """
    Ajusta o vetor TF-IDF a partir de um corpus de textos.

    Args:
        texts (List[str]): Lista de textos
    """
    global tfidf_vectorizer, text_corpus
    text_corpus = texts.copy()
    tfidf_vectorizer.fit(text_corpus)
    print("[Vectorizer] Corpus de texto ajustado com", len(text_corpus), "itens")

def vectorize_text(text: str) -> np.ndarray:
    """
    Converte um texto em vetor TF-IDF.

    Args:
        text (str): Texto a ser vetorizar

    Returns:
        np.ndarray: Vetor TF-IDF
    """
    if not text_corpus:
        raise ValueError("Corpus não ajustado. Use fit_text_corpus() primeiro.")

    vector = tfidf_vectorizer.transform([text]).toarray()[0]
    return vector

# =========================
# FUNÇÕES DE IMAGEM (placeholder)
# =========================

def vectorize_image(image_array: np.ndarray) -> np.ndarray:
    """
    Converte uma imagem em vetor simplificado (placeholder).

    Args:
        image_array (np.ndarray): Imagem em BGR

    Returns:
        np.ndarray: vetor flatten da imagem redimensionada
    """
    # Reduz tamanho para 32x32 e flatten
    resized = cv2.resize(image_array, (32, 32))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    vector = gray.flatten() / 255.0  # Normaliza valores entre 0 e 1
    return vector

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    # Teste de texto
    texts = ["Botão iniciar", "Abrir janela", "Enviar dados"]
    fit_text_corpus(texts)
    vec = vectorize_text("Abrir janela")
    print("[Vectorizer] Vetor de 'Abrir janela':", vec[:10], "...")  # Mostra primeiros 10 valores

    # Teste de imagem (usando numpy fake)
    import numpy as np
    dummy_img = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
    vec_img = vectorize_image(dummy_img)
    print("[Vectorizer] Vetor de imagem shape:", vec_img.shape)
