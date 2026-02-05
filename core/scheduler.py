"""
Scheduler simples para tarefas periódicas do NE-AI V1
Exemplo: salvar memória periodicamente ou limpeza de logs
"""

import threading
import time

class Scheduler:
    def __init__(self):
        self.jobs = []
        self.running = False

    def add_job(self, interval_sec, func, *args, **kwargs):
        """
        Adiciona uma tarefa repetitiva
        """
        self.jobs.append((interval_sec, func, args, kwargs))

    def start(self):
        self.running = True
        threading.Thread(target=self._run).start()

    def stop(self):
        self.running = False

    def _run(self):
        while self.running:
            for interval, func, args, kwargs in self.jobs:
                threading.Thread(target=func, args=args, kwargs=kwargs).start()
            time.sleep(1)  # loop a cada segundo
