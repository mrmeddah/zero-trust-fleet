"""Fixtures de test — application en mémoire, jeu de données minimal."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import creer_app
from config import Config
from models import db, Role, Utilisateur, Vehicule, Stock


class ConfigTest(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "test"
    FREEIPA_MODE = "disabled"


@pytest.fixture()
def app():
    application = creer_app(ConfigTest)
    with application.app_context():
        db.create_all()
        for libelle, niveau in (("Administrateur", 4), ("Gestionnaire", 3),
                                ("Agent", 1), ("Direction", 3), ("Auditeur", 2)):
            db.session.add(Role(libelle=libelle, niveau_acces=niveau))
        db.session.flush()
        roles = {r.libelle: r for r in Role.query.all()}

        def ajouter(uid, mdp, rnoms):
            u = Utilisateur(uid=uid, nom=uid, prenom=uid, mot_de_passe=mdp,
                            statut="actif", roles=[roles[r] for r in rnoms])
            db.session.add(u)
            return u

        ajouter("gestionnaire1", "mdp", ["Gestionnaire"])
        ajouter("agent1", "mdp", ["Agent"])
        ajouter("direction1", "mdp", ["Direction"])
        db.session.add(Vehicule(immatriculation="J200189", marque="Toyota",
                                modele="Hilux", service="Voirie",
                                carburant="Gasoil", statut="En service"))
        db.session.add(Stock(type_carburant="Gasoil", quantite=1000))
        db.session.add(Stock(type_carburant="Essence", quantite=500))
        db.session.commit()
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, uid, mdp="mdp"):
    return client.post("/login", data={"identifiant": uid, "mot_de_passe": mdp},
                       follow_redirects=True)