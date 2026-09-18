"""Tests de la couche métier : parc, bons de carburant, stock, rapports."""
from datetime import date
from tests.conftest import login


def obtenir_vehicule_id(client):
    with client.application.app_context():
        from models import Vehicule
        return Vehicule.query.first().id


def test_liste_vehicules(client):
    login(client, "direction1")
    vehicules = client.get("/api/vehicules").get_json()
    assert any(v["immatriculation"] == "J200189" for v in vehicules)


def test_creation_bon_et_debit_stock(client):
    login(client, "agent1")
    vehicule_id = obtenir_vehicule_id(client)
    bon = client.post("/api/bons", json={
        "vehicule_id": vehicule_id, "type_carburant": "Gasoil", "quantite": 50,
        "_uid": "agent1"})
    assert bon.status_code == 201
    numero = bon.get_json()["numero_bon"]
    assert numero.startswith("BON-")

    # Le stock a été débité de 50 litres (1000 -> 950)
    stocks = client.get("/api/stock").get_json()
    gasoil = next(s for s in stocks if s["type_carburant"] == "Gasoil")
    assert gasoil["quantite"] == 950.0

    # Le bon apparaît dans la liste
    bons = client.get("/api/bons").get_json()
    assert any(b["numero_bon"] == numero for b in bons)


def test_bon_stock_insuffisant(client):
    login(client, "agent1")
    vehicule_id = obtenir_vehicule_id(client)
    reponse = client.post("/api/bons", json={
        "vehicule_id": vehicule_id, "type_carburant": "Essence", "quantite": 99999,
        "_uid": "agent1"})
    assert reponse.status_code == 400
    assert "Stock insuffisant" in reponse.get_json()["erreur"]


def test_bon_quantite_invalide(client):
    login(client, "agent1")
    vehicule_id = obtenir_vehicule_id(client)
    reponse = client.post("/api/bons", json={
        "vehicule_id": vehicule_id, "type_carburant": "Essence", "quantite": -5,
        "_uid": "agent1"})
    assert reponse.status_code == 400


def test_bon_type_inconnu(client):
    login(client, "agent1")
    vehicule_id = obtenir_vehicule_id(client)
    reponse = client.post("/api/bons", json={
        "vehicule_id": vehicule_id, "type_carburant": "Pétrole", "quantite": 10,
        "_uid": "agent1"})
    assert reponse.status_code == 400


def test_creation_vehicule(client):
    login(client, "gestionnaire1")
    reponse = client.post("/api/vehicules", json={
        "immatriculation": "J200999", "marque": "Renault", "modele": "Clio",
        "service": "Urbanisme", "carburant": "Essence", "_uid": "gestionnaire1"})
    assert reponse.status_code == 201
    assert reponse.get_json()["immatriculation"] == "J200999"


def test_rapport_mensuel(client):
    login(client, "direction1")
    # émettre un bon aujourd'hui pour un service donné
    from models import db, Vehicule
    from services.carburant import creer_bon
    with client.application.app_context():
        from models import Utilisateur
        agent = Utilisateur.query.filter_by(uid="agent1").first()
        vehicule = Vehicule.query.first()
        bon = creer_bon({"vehicule_id": vehicule.id,
                         "type_carburant": "Gasoil", "quantite": 30,
                         "_uid": "agent1"}, {"uid": "agent1"})
        db.session.commit()

    rapport = client.get("/api/rapports/consommation").get_json()
    assert rapport["mensuel"]["total_bons"] >= 1
    assert rapport["mensuel"]["total_litres"] >= 30