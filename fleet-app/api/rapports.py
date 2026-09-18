"""/api/rapports/consommation --- synthèse des consommations (tb:ch3-endpoints)."""
from flask import Blueprint, request, jsonify

from services.rapports import (
    consommation_par_vehicule, consommation_par_service, rapport_mensuel)
from services.security import besoin_session, roles_requis

api = Blueprint("rapports", __name__)


def _date_param(nom):
    from datetime import datetime
    valeur = request.args.get(nom)
    return datetime.strptime(valeur, "%Y-%m-%d").date() if valeur else None


@api.route("/api/rapports/consommation", methods=["GET"])
@besoin_session
@roles_requis("Direction", "Administrateur", "Gestionnaire")
def consommation():
    """GET — Synthèse des consommations (Direction)."""
    debut = _date_param("debut")
    fin = _date_param("fin")
    mois = request.args.get("mois", type=int)
    annee = request.args.get("annee", type=int)
    return jsonify({
        "par_vehicule": [{
            "vehicule": v, "litres": round(l, 2), "bons": n,
        } for v, l, n in consommation_par_vehicule(debut, fin)],
        "par_service": [{
            "service": s, "litres": round(l, 2), "bons": n,
        } for s, l, n in consommation_par_service(debut, fin)],
        "mensuel": rapport_mensuel(mois, annee),
    })