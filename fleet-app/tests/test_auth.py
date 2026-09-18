"""Tests d'authentification et de contrôle d'accès par rôle (moindre privilège)."""
from tests.conftest import login


def test_login_ok(client):
    assert login(client, "agent1").status_code == 200


def test_login_suspendu_refuse(client, app):
    with app.app_context():
        from models import Utilisateur
        utilisateur = Utilisateur.query.filter_by(uid="agent1").first()
        utilisateur.statut = "suspendu"
        from models import db
        db.session.commit()
    reponse = login(client, "agent1")
    assert reponse.status_code == 401


def test_mauvais_mot_de_passe(client):
    reponse = client.post("/login",
                          data={"identifiant": "agent1", "mot_de_passe": "Faux"},
                          follow_redirects=True)
    assert reponse.status_code == 401


def test_acces_sans_session(client):
    assert client.get("/fleet").status_code == 302  # redirigé vers /login
    assert client.get("/api/vehicules").status_code == 401


def test_direction_voit_rapports(client):
    login(client, "direction1")
    assert client.get("/rapports").status_code == 200
    assert client.get("/api/rapports/consommation").status_code == 200


def test_agent_interdit_rapports(client):
    login(client, "agent1")
    # Page rapports -> redirection ; API rapports -> 403 (rôle Direction requis)
    assert client.get("/rapports").status_code == 302
    assert client.get("/api/rapports/consommation").status_code == 403


def test_gestionnaire_acces_parc(client):
    login(client, "gestionnaire1")
    assert client.get("/fleet").status_code == 200
    assert client.get("/api/vehicules").status_code == 200


def test_agent_interdit_gestion_vehicules(client):
    Login = login(client, "agent1")
    # AJout véhicule réservé au Gestionnaire (POST /api/vehicules -> 403)
    reponse = client.post("/api/vehicules",
                          json={"immatriculation": "J999999", "marque": "Test"})
    assert reponse.status_code == 403