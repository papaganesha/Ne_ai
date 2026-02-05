"""
Vetorização de textos ou frames para busca de similaridade futura.

Por enquanto apenas estrutura inicial.
"""

from sklearn.feature_extraction.text import TfidfVectorizer

class Vectorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.corpus = []

    def fit(self, texts):
        self.corpus = texts
        self.vectorizer.fit(texts)

    def transform(self, text):
        return self.vectorizer.transform([text])
