"""Initialisation de la base SQLite et création des tables (db.create_all)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import creer_app


def initialiser(garder_donnees=False):
    app = creer_app()
    with app.app_context():
        from models import db
        db.create_all()
        print("Base de données initialisée :", app.config["SQLALCHEMY_DATABASE_URI"])


if __name__ == "__main__":
    initialiser()