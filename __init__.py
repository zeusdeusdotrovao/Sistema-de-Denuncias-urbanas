"""
app/__init__.py — Fábrica da aplicação Flask.
Cria e configura o app com CORS e as rotas registradas.
"""

from flask import Flask
from flask_cors import CORS
from .routes import bp


def criar_app():
    app = Flask(__name__)

    # Permite que o frontend (HTML/JS) acesse a API sem bloqueio de CORS
    CORS(app)

    # Registra o Blueprint com todas as rotas de denúncias
    app.register_blueprint(bp)

    return app
