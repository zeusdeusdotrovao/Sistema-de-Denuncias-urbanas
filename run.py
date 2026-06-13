"""
run.py — Ponto de entrada do servidor Flask.
Execute com: python run.py
"""

from app import criar_app

app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
