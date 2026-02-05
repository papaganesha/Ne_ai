"""
NE-AI V1 — Scheduler
=====================

Responsável por agendar tarefas periódicas do sistema:
- Atualização de memória
- Limpeza de memória antiga ou redundante
- Verificação de streaming ativo
- Possibilidade de adicionar futuras tarefas recorrentes

Funcionalidades:
- Roda em thread separada
- Permite adicionar múltiplos jobs com intervalo personalizado
- Não bloqueia o loop principal
"""

# =========================
# IMPORTAÇÕES
# =========================
import threading
import time
from typing import Callable, Dict, List

# =========================
# CLASSES E VARIÁVEIS
# =========================

class Job:
    """
    Representa uma tarefa agendada.
    """
    def __init__(self, func: Callable, interval: float, name: str):
        """
        Args:
            func (Callable): Função que será executada
            interval (float): Intervalo em segundos
            name (str): Nome da tarefa
        """
        self.func = func
        self.interval = interval
        self.name = name
        self.last_run = 0.0  # Timestamp da última execução

class Scheduler:
    """
    Scheduler que roda em thread separada e gerencia múltiplos jobs.
    """
    def __init__(self):
        self.jobs: List[Job] = []
        self.running = False
        self.thread = None

    def add_job(self, func: Callable, interval: float, name: str):
        """
        Adiciona um job ao scheduler.
        """
        job = Job(func, interval, name)
        self.jobs.append(job)
        print(f"[Scheduler] Job '{name}' adicionado com intervalo {interval}s")

    def start(self):
        """
        Inicia o scheduler em thread separada.
        """
        if self.running:
            print("[Scheduler] Já está rodando")
            return
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print("[Scheduler] Scheduler iniciado")

    def stop(self):
        """
        Para o scheduler.
        """
        self.running = False
        print("[Scheduler] Scheduler parado")

    def _run_loop(self):
        """
        Loop principal que verifica e executa jobs quando necessário.
        """
        while self.running:
            current_time = time.time()
            for job in self.jobs:
                # Se passou o intervalo desde a última execução, executa job
                if current_time - job.last_run >= job.interval:
                    try:
                        job.func()
                        job.last_run = current_time
                        print(f"[Scheduler] Job '{job.name}' executado")
                    except Exception as e:
                        print(f"[Scheduler] Erro ao executar job '{job.name}': {e}")
            time.sleep(0.1)  # Pequena pausa para evitar uso intenso de CPU

# =========================
# FUNÇÃO DE TESTE ISOLADO
# =========================
if __name__ == "__main__":
    def job1():
        print("[TesteJob] Executando job1")

    def job2():
        print("[TesteJob] Executando job2")

    sched = Scheduler()
    sched.add_job(job1, interval=2, name="Job1")  # Executa a cada 2s
    sched.add_job(job2, interval=3, name="Job2")  # Executa a cada 3s
    sched.start()

    # Mantém o loop principal ativo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sched.stop()
