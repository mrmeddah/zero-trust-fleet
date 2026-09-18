"""/api/bons --- bons de carburant et mouvements de stock (tb:ch3-endpoints)."""
from flask import Blueprint, request, jsonify

from services.carburant import lister_bons, creer_bon
from services.security import besoin_session, roles_requis

api = Blueprint("bons", __name__)


@api.route("/api/bons", methods=["GET"])
@besoin_session
@roles_requis("Agent", "Direction", "Gestionnaire", "Administrateur")
def liste_bons():
    """GET — Liste des bons de carburant (Agent, Direction)."""
    return jsonify([b.to_dict() for b in lister_bons()])


@api.route("/api/bons", methods=["POST"])
@besoin_session
@roles_requis("Agent", "Gestionnaire", "Administrateur")
def creer_nouveau_bon():
    """POST — Création d'un bon de carburant (Agent)."""
    donnees = request.get_json(force=True, silent=True) or request.form.to_dict()
    donnees["_uid"] = request.json.get("_uid") if hasattr(request, "json") and request.json else None
    try:
        bon = creer_bon(donnees, {"uid": donnees.get("_uid")})
    except ValueError as exc:
        return jsonify({"erreur": str(exc)}), 400
    return jsonify(bon.to_dict()), 201