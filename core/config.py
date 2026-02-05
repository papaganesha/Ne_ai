"""
NE-AI V1 — Configurações
=========================

Arquivo central de configurações da V1.

Responsável por:
- Definir caminhos de armazenamento (raw, processed, memory)
- Thresholds para processamento de frames
- Intervalos de streaming e scheduler
- Configurações de OCR e normalização
- Parâmetros iniciais do learner
"""

# =========================
# CAMINHOS DE ARMAZENAMENTO
# =========================
STORAGE_RAW = "storage/raw"              # Onde ficam arquivos brutos (vídeo, upload)
STORAGE_PROCESSED = "storage/processed"  # Onde ficam arquivos processados (frames filtrados, textos)
MEMORY_FILE = "storage/memory.json"      # Arquivo de memória persistente

# =========================
# STREAMING
# =========================
STREAM_FRAME_INTERVAL = 0.5   # Intervalo entre frames do streaming (em segundos)
SCREEN_STREAM_RESIZE = (64, 64)  # Redimensionamento para filtragem e comparação

# =========================
# FRAME FILTER
# =========================
FRAME_SIMILARITY_THRESHOLD = 0.95  # Threshold de similaridade para considerar frame repetido

# =========================
# OCR
# =========================
OCR_THRESHOLD_VALUE = 150           # Thresholding para melhorar contraste
OCR_LANG = "eng"                    # Idioma padrão do Tesseract

# =========================
# LEARNER
# =========================
LEARNER_DEFAULT_CONFIDENCE = 0.7    # Confiança inicial de novos inputs
LEARNER_CONFIDENCE_MIN = 0.0        # Confiança mínima
LEARNER_CONFIDENCE_MAX = 1.0        # Confiança máxima
LEARNER_CONFIDENCE_INCREMENT = 0.1  # Incremento ao reforçar positivamente
LEARNER_CONFIDENCE_DECREMENT = 0.1  # Decremento ao reforçar negativamente

# =========================
# SCHEDULER
# =========================
SCHEDULER_DEFAULT_SLEEP = 0.1  # Intervalo de loop interno (em segundos)

# =========================
# OUTRAS CONFIGURAÇÕES
# =========================
MAX_UPLOAD_SIZE_MB = 50  # Tamanho máximo de upload permitido
ALLOWED_UPLOAD_TYPES = ["txt", "pdf", "png", "jpg", "mp4"]  # Tipos permitidos

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    print("[Config] Caminhos:")
    print(f"Raw: {STORAGE_RAW}")
    print(f"Processed: {STORAGE_PROCESSED}")
    print(f"Memory: {MEMORY_FILE}")

    print("\n[Config] Thresholds e Parâmetros:")
    print(f"Frame similarity: {FRAME_SIMILARITY_THRESHOLD}")
    print(f"Stream interval: {STREAM_FRAME_INTERVAL}s")
    print(f"OCR threshold: {OCR_THRESHOLD_VALUE}")
    print(f"Learner default confidence: {LEARNER_DEFAULT_CONFIDENCE}")
