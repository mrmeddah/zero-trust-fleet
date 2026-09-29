"""/api/stock --- niveau des stocks."""
from flask import Blueprint, jsonify

from models import Stock
from services.security import besoin_session, roles_requis

api = Blueprint("stock", __name__)


@api.route("/api/stock", methods=["GET"])
@besoin_session
@roles_requis("Agent", "Direction", "Gestionnaire", "Administrateur")
def niveau_stock():
    """GET — Niveau des stocks (Agent, Direction)."""
    return jsonify([s.to_dict() for s in Stock.query.order_by(Stock.type_carburant).all()])