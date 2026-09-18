"""Compose l'application Flask et enregistre les points de terminaison."""
import os

from flask import Flask, redirect, url_for

from config import Config
from models import db
from services.security import AnnuaireClient
from api.vehicules import api as api_vehicules
from api.bons import api as api_bons
from api.rapports import api as api_rapports
from api.stock import api as api_stock
from api.pages import api as api_pages


def _uri_absolue(app):
    uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if uri.startswith("sqlite:///"):
        chemin = uri.replace("sqlite:///", "", 1)
        if not os.path.isabs(chemin):
            base = os.path.dirname(os.path.abspath(__file__))
            return "sqlite:///" + os.path.join(base, chemin)
    return uri


def creer_app(config_object=Config):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_object)

    db.init_app(app)
    app.extensions["fleet_annuaire"] = AnnuaireClient(app)

    app.register_blueprint(api_vehicules)
    app.register_blueprint(api_bons)
    app.register_blueprint(api_rapports)
    app.register_blueprint(api_stock)
    app.register_blueprint(api_pages)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return redirect(url_for("pages.pages_login"))

    return app


if __name__ == "__main__":
    app = creer_app()
    app.run(host="0.0.0.0", port=5000, debug=True)