"""Configuration de l'application de gestion du parc et du carburant.

La configuration provient entierement de l'environnement, ce qui permet de
faire tourner la meme image en local, en CI ou en conteneur :
  - developpement  : base SQLite locale, annuaire desactive
  - conteneurise   : variables posees par compose.yaml
  - production     : chaines de connexion explicites, secrets hors depot

"""
import os

_BASE = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = os.environ.get("FLEET_SECRET_KEY", "dev-clef-de-session-a-changer")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "FLEET_DB_URI",
        "sqlite:///" + os.path.join(_BASE, "database", "fleet.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Annuaire FreeIPA ---
    FREEIPA_HOST = os.environ.get("FLEET_FREEIPA_HOST", "10.10.10.10")
    FREEIPA_PORT = int(os.environ.get("FLEET_FREEIPA_PORT", "389"))
    FREEIPA_BASE_DN = os.environ.get("FLEET_FREEIPA_BASE_DN", "dc=municipal,dc=local")
    FREEIPA_USERS_DN = os.environ.get(
        "FLEET_FREEIPA_USERS_DN", "cn=users,cn=accounts,dc=municipal,dc=local")
    FREEIPA_GROUPS_DN = os.environ.get(
        "FLEET_FREEIPA_GROUPS_DN", "cn=groups,cn=accounts,dc=municipal,dc=local")
    FREEIPA_MODE = os.environ.get("FLEET_FREEIPA_MODE", "disabled")  # enabled | disabled

    # --- mTLS ---
    MTLS_VERIFY_CLIENT = os.environ.get("FLEET_MTLS", "off") == "on"
    TLS_CERT = os.environ.get("FLEET_TLS_CERT")      # serveur  fleet-app.municipal.local
    TLS_KEY = os.environ.get("FLEET_TLS_KEY")
    TLS_CA = os.environ.get("FLEET_TLS_CA")          # ipa-ca.crt (CA interne)