"""
NE-AI V1 — Orchestrator
========================

Classe central que coordena todo o sistema NE-AI V1:

- Inicializa e gerencia módulos:
    - Scheduler
    - Inputs (screen, video, upload, texto)
    - Learner e Cognition
    - Web server
- Permite ligar/desligar módulos individualmente
- Mantém estado e logs de execução
- Integra com histórico e memória persistente
"""

# =========================
# IMPORTAÇÕES
# =========================
import threading
import time
from core.scheduler import Scheduler
from inputs.screen_stream import ScreenStream
from inputs.video_stream import VideoStream
from inputs.upload_handler import handle_upload
from inputs.text_input import TextInput
from api.web_server import app  # Servidor Flask
from memory.history import log_event

# =========================
# CLASSE ORCHESTRATOR
# =========================
class Orchestrator:
    def __init__(self):
        """
        Inicializa todos os módulos com estado OFF.
        """
        self.scheduler = Scheduler()
        self.screen_stream = ScreenStream()
        self.video_stream = VideoStream()
        self.text_input = TextInput()
        self.modules = []
        self.running = False

    # =========================
    # MÉTODOS DE CONTROLE
    # =========================

    def register_module(self, module, name=None):
        """
        Registra um módulo para gerenciamento central.
        """
        self.modules.append({"module": module, "name": name or module.__class__.__name__})
        print(f"[Orchestrator] Módulo registrado: {name or module.__class__.__name__}")

    def start_module(self, module):
        """
        Inicia um módulo em thread separada, se suportado.
        """
        t = threading.Thread(target=module.run, daemon=True)
        t.start()
        print(f"[Orchestrator] Módulo iniciado: {module.__class__.__name__}")

    def start_all(self):
        """
        Inicia todos os módulos registrados.
        """
        print("[Orchestrator] Iniciando todos os módulos...")
        self.running = True

        # Registrar módulos para controle central
        self.register_module(self.scheduler)
        self.register_module(self.screen_stream)
        self.register_module(self.video_stream)
        self.register_module(self.text_input)

        # Iniciar cada módulo em thread
        for entry in self.modules:
            module = entry["module"]
            try:
                self.start_module(module)
            except AttributeError:
                print(f"[Orchestrator] Módulo sem método run(): {entry['name']}")

        # Log de inicialização
        log_event("orchestrator", {"event": "start_all"})

    def stop_all(self):
        """
        Para todos os módulos.
        """
        print("[Orchestrator] Parando todos os módulos...")
        self.running = False
        for entry in self.modules:
            module = entry["module"]
            if hasattr(module, "stop"):
                module.stop()
        log_event("orchestrator", {"event": "stop_all"})

    # =========================
    # MÉTODO DE LOOP PRINCIPAL
    # =========================
    def run(self):
        """
        Mantém orquestrador rodando, podendo monitorar ou reiniciar módulos.
        """
        self.start_all()
        print("[Orchestrator] Loop principal ativo")
        try:
            while self.running:
                # Aqui podemos adicionar monitoramento de módulos
                # e lógica de reinício automático caso algum módulo falhe
                time.sleep(1)
        except KeyboardInterrupt:
            print("[Orchestrator] Interrompido pelo usuário")
            self.stop_all()
