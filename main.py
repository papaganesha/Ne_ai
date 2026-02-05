"""
NE-AI V1 — Ponto de entrada principal

Este arquivo inicia:
- Servidor web Flask
- Orquestrador (futuro controle de threads e fluxos)
"""

from api.web_server import create_app

# Cria a aplicação Flask
app = create_app()

# Executa o servidor web
if __name__ == "__main__":
    # debug=True mantém o servidor reiniciando automaticamente em alterações
    app.run(host="0.0.0.0", port=5000, debug=True)
