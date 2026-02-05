"""
Configurações globais do NE-AI V1
"""

import os

# Caminho principal de armazenamento
BASE_STORAGE_PATH = os.path.join(os.getcwd(), "storage")

# Caminhos de armazenamento específicos
RAW_STORAGE = os.path.join(BASE_STORAGE_PATH, "raw")
PROCESSED_STORAGE = os.path.join(BASE_STORAGE_PATH, "processed")
MEMORY_FILE = os.path.join(BASE_STORAGE_PATH, "memory.json")

# Limiares do learner
CONFIDENCE_THRESHOLD = 0.6

# Criar pastas se não existirem
os.makedirs(RAW_STORAGE, exist_ok=True)
os.makedirs(PROCESSED_STORAGE, exist_ok=True)
