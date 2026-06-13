"""
app/routes.py — Todas as rotas da API de denúncias.

Endpoints disponíveis:
  GET    /denuncias        → lista todas as denúncias
  POST   /denuncias        → cria uma nova denúncia
  PUT    /denuncias/<id>   → atualiza uma denúncia (campos ou status)
  DELETE /denuncias/<id>   → exclui uma denúncia
"""

from flask import Blueprint, request, jsonify
from .db import get_db

bp = Blueprint("denuncias", __name__)

# Status permitidos para evitar valores inválidos no banco
STATUS_VALIDOS = {"aberta", "em_ajuste", "concluida", "nao_houve"}

# Tipos de problema permitidos
TIPOS_VALIDOS = {"buraco", "fiacao_solta", "alagamento", "outros"}


# ── LISTAR ────────────────────────────────────────────────────────────────────
@bp.route("/denuncias", methods=["GET"])
def listar():
    """Retorna todas as denúncias, da mais recente para a mais antiga."""
    db = get_db()
    rows = db.execute("SELECT * FROM denuncias ORDER BY data DESC").fetchall()
    return jsonify([dict(r) for r in rows])


# ── CRIAR ─────────────────────────────────────────────────────────────────────
@bp.route("/denuncias", methods=["POST"])
def criar():
    """Cria uma nova denúncia com os dados enviados no body (JSON)."""
    dados = request.get_json()

    # Validação dos campos obrigatórios
    endereco = (dados.get("endereco") or "").strip()
    tipo     = (dados.get("tipo") or "").strip()

    if not endereco:
        return jsonify({"erro": "O campo 'endereço' é obrigatório."}), 400

    if tipo not in TIPOS_VALIDOS:
        return jsonify({"erro": f"Tipo inválido. Use: {', '.join(TIPOS_VALIDOS)}"}), 400

    db = get_db()
    db.execute(
        """
        INSERT INTO denuncias (endereco, cep, ponto_referencia, tipo, descricao, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            endereco,
            dados.get("cep"),
            dados.get("ponto_referencia"),
            tipo,
            dados.get("descricao"),
            dados.get("latitude"),
            dados.get("longitude"),
        ),
    )
    db.commit()

    return jsonify({"mensagem": "Denúncia criada com sucesso!"}), 201


# ── ATUALIZAR ─────────────────────────────────────────────────────────────────
@bp.route("/denuncias/<int:id>", methods=["PUT"])
def atualizar(id):
    """Atualiza campos de uma denúncia existente."""
    db = get_db()

    # Verifica se a denúncia existe
    denuncia = db.execute("SELECT id FROM denuncias WHERE id = ?", (id,)).fetchone()
    if not denuncia:
        return jsonify({"erro": "Denúncia não encontrada."}), 404

    dados = request.get_json()

    # Monta dinamicamente apenas os campos enviados
    campos = {}

    if dados.get("endereco", "").strip():
        campos["endereco"] = dados["endereco"].strip()
    if "cep" in dados:
        campos["cep"] = dados["cep"]
    if "ponto_referencia" in dados:
        campos["ponto_referencia"] = dados["ponto_referencia"]
    if dados.get("tipo") in TIPOS_VALIDOS:
        campos["tipo"] = dados["tipo"]
    if "descricao" in dados:
        campos["descricao"] = dados["descricao"]
    if dados.get("status") in STATUS_VALIDOS:
        campos["status"] = dados["status"]
    if "latitude" in dados:
        campos["latitude"] = dados["latitude"]
    if "longitude" in dados:
        campos["longitude"] = dados["longitude"]

    if not campos:
        return jsonify({"erro": "Nenhum campo válido para atualizar."}), 400

    # Monta a query UPDATE com os campos recebidos
    set_sql = ", ".join(f"{k} = ?" for k in campos)
    valores = list(campos.values()) + [id]

    db.execute(f"UPDATE denuncias SET {set_sql} WHERE id = ?", valores)
    db.commit()

    return jsonify({"mensagem": "Denúncia atualizada com sucesso!"})


# ── EXCLUIR ───────────────────────────────────────────────────────────────────
@bp.route("/denuncias/<int:id>", methods=["DELETE"])
def excluir(id):
    """Exclui uma denúncia pelo ID."""
    db = get_db()

    denuncia = db.execute("SELECT id FROM denuncias WHERE id = ?", (id,)).fetchone()
    if not denuncia:
        return jsonify({"erro": "Denúncia não encontrada."}), 404

    db.execute("DELETE FROM denuncias WHERE id = ?", (id,))
    db.commit()

    return jsonify({"mensagem": "Denúncia excluída com sucesso!"})
