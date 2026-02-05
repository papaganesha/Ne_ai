"""
NE-AI V1 — MÓDULO DE PROCESSAMENTO
=================================

Este módulo é responsável por TRANSFORMAR dados brutos
em informações úteis.

Ele NÃO aprende.
Ele NÃO decide ações.

Responsabilidades:
- Receber dados da fila de entrada
- Identificar tipo (frame, texto, arquivo)
- Extrair apenas o necessário
- Evitar frames redundantes
- Enviar dados processados para cognição

Objetivo central:
- NÃO desperdiçar CPU
- NÃO desperdiçar espaço
"""

# =========================
# IMPORTAÇÕES
# =========================

import threading                # Execução paralela
import time                     # Controle de loop
import queue                    # Comunicação entre módulos
from typing import Any, Dict    # Tipagem clara

# =========================
# FILAS (COMPARTILHADAS)
# =========================

input_queue = queue.Queue()       # Recebe dados brutos
processed_queue = queue.Queue()   # Envia dados limpos

# =========================
# CONFIGURAÇÕES
# =========================

PROCESS_LOOP_DELAY = 0.05        # Pausa do loop
FRAME_DIFF_THRESHOLD = 0.1       # Sensibilidade a mudanças

# =========================
# CLASSE: PROCESSOR
# =========================

class Processor(threading.Thread):
    """
    Thread responsável pelo processamento central.
    """

    def __init__(self):
        super().__init__(daemon=True)
        self.running = False
        self.last_frame_signature = None

    # ---------------------
    # LOOP PRINCIPAL
    # ---------------------
    def run(self):
        self.running = True
        print("[Processor] Iniciado")

        while self.running:
            try:
                if not input_queue.empty():
                    payload = input_queue.get()
                    self.process(payload)

                time.sleep(PROCESS_LOOP_DELAY)

            except Exception as e:
                print(f"[Processor] Erro: {e}")

        print("[Processor] Encerrado")

    # ---------------------
    # PROCESSAMENTO
    # ---------------------
    def process(self, payload: Dict[str, Any]):
        """
        Direciona o processamento conforme o tipo.
        """
        data_type = payload.get("type")

        if data_type == "frame":
            self.process_frame(payload)

        elif data_type == "text":
            self.process_text(payload)

        elif data_type == "file":
            self.process_file(payload)

    # ---------------------
    # FRAME
    # ---------------------
    def process_frame(self, payload: Dict[str, Any]):
        frame = payload.get("data")

        signature = self.frame_signature(frame)

        if self.last_frame_signature == signature:
            # Frame redundante → ignorar
            return

        self.last_frame_signature = signature

        processed_queue.put({
            "type": "vision",
            "source": payload.get("source"),
            "data": frame,
            "confidence": 0.5  # confiança inicial
        })

    # ---------------------
    # TEXTO
    # ---------------------
    def process_text(self, payload: Dict[str, Any]):
        text = payload.get("data")

        processed_queue.put({
            "type": "text",
            "source": payload.get("source"),
            "data": text,
            "confidence": 0.9
        })

    # ---------------------
    # ARQUIVO
    # ---------------------
    def process_file(self, payload: Dict[str, Any]):
        path = payload.get("path")

        processed_queue.put({
            "type": "file",
            "source": payload.get("source"),
            "path": path,
            "confidence": 0.7
        })

    # ---------------------
    # ASSINATURA DE FRAME
    # ---------------------
    def frame_signature(self, frame: Any) -> str:
        """
        Gera uma assinatura simples do frame.
        Na V1 é propositalmente leve.
        """
        return str(hash(str(frame)))


# =========================
# TESTE ISOLADO
# =========================

if __name__ == "__main__":
    processor = Processor()
    processor.start()

    input_queue.put({"type": "text", "source": "manual", "data": "Teste"})
    input_queue.put({"type": "frame", "source": "screen", "data": "FRAME1"})
    input_queue.put({"type": "frame", "source": "screen", "data": "FRAME1"})

    time.sleep(1)
    processor.running = False
