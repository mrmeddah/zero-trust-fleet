"""/api/vehicules --- gestion du parc."""
from flask import Blueprint, request, jsonify

from services.parc import lister_vehicules, detailler_vehicule, creer_vehicule
from services.security import besoin_session, roles_requis

api = Blueprint("vehicules", __name__)


@api.route("/api/vehicules", methods=["GET"])
@besoin_session
@roles_requis("Gestionnaire", "Direction", "Administrateur")
def liste_vehicules():
    """GET — Liste des véhicules (Gestionnaire, Direction)."""
    return jsonify([v.to_dict() for v in lister_vehicules()])


@api.route("/api/vehicules", methods=["POST"])
@besoin_session
@roles_requis("Gestionnaire", "Administrateur")
def ajouter_vehicule():
    """POST — Ajout d'un véhicule (Gestionnaire)."""
    vehicule = creer_vehicule(request.json, {"uid": request.json.get("_uid")})
    return jsonify(vehicule.to_dict()), 201


@api.route("/api/vehicules/<int:vehicule_id>", methods=["GET"])
@besoin_session
@roles_requis("Gestionnaire", "Direction", "Administrateur")
def detail_vehicule(vehicule_id):
    """GET — Détail d'un véhicule (Gestionnaire, Direction)."""
    return jsonify(detailler_vehicule(vehicule_id).to_dict())