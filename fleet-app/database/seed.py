"""Jeu de données de démonstration (cohérent avec ch. II et ch. IV).

Véhicules : immatriculations du type J200189, J200190, ... (format demandé).
Rôles : Administrateur, Gestionnaire, Agent, Direction, Auditeur.
"""
import os
import sys
import logging
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("seed")

from app import creer_app
from models import (db, Role, Utilisateur, Vehicule, Stock, Alerte,
                    Certificat, BonCarburant)

ROLES = [
    ("Administrateur", 4),
    ("Gestionnaire", 3),
    ("Agent", 1),
    ("Direction", 3),
    ("Auditeur", 2),
]

UTILISATEURS = [
    ("admin1", "Meddah", "Mohamed", "admin1@municipal.local", "motdepasseadmin",
     ["Administrateur"]),
    ("gestionnaire1", "Boukri", "Mourad", "gestionnaire1@municipal.local", "motdepassegestion",
     ["Gestionnaire"]),
    ("agent1", "Agent", "Ahmed", "agent1@municipal.local", "motdepasseagent",
     ["Agent"]),
    ("direction1", "Direction", "Salma", "direction1@municipal.local", "motdepassedirection",
     ["Direction"]),
    ("auditeur1", "Auditeur", "Yassine", "auditeur1@municipal.local", "motdepasseaudit",
     ["Auditeur"]),
]

IMMATRICULATIONS = [
    "J200189", "J200190", "J200191", "J200192", "J200193", "J200194",
    "J200195", "J200196", "J200197", "J200198", "J200199", "J200200",
    "J200201", "J200202", "J200203",
]

VEHICULES = [
    # (immatriculation, marque, modele, service, carburant, statut)
    ("J200189", "Toyota", "Hilux", "Travaux et Suivi des Projets", "Gasoil", "En service"),
    ("J200190", "Peugeot", "406", "Urbanisme", "Essence", "En service"),
    ("J200191", "Renault", "Kangoo", "Hygiene", "Gasoil", "En service"),
    ("J200192", "Dacia", "Logan", "Etat Civil", "Essence", "En service"),
    ("J200193", "Iveco", "Daily benne", "Voirie", "Gasoil", "En maintenance"),
    ("J200194", "Fiat", "Ducato", "Dechets", "Gasoil", "En service"),
    ("J200195", "Mercedes", "Sprinter", "Eclairage public", "Essence", "En service"),
    ("J200196", "Ford", "Ranger", "Eaux et Assainissement", "Gasoil", "En service"),
    ("J200197", "Volkswagen", "Amarok", "Espaces verts", "Gasoil", "En service"),
    ("J200198", "Isuzu", "D-Max", "Ressources", "Gasoil", "Hors service"),
    ("J200199", "Kia", "Sportage", "Direction", "Essence", "En service"),
    ("J200200", "Toyota", "Yaris", "Urbanisme", "Essence", "En maintenance"),
    ("J200201", "Renault", "Master", "Dechets", "Gasoil", "En service"),
    ("J200202", "Hyundai", "H-1", "Etat Civil", "Gasoil", "En service"),
    ("J200203", "Peugeot", "508", "Direction", "Gasoil", "En service"),
]

ALERTES = [
    (3, "maintenance", "Vidange prévue pour le véhicule J200193 (12 400 km)"),
    (4, "vehicule", "Pneumatiques usés sur le véhicule J200200"),
    (2, "maintenance", "Contrôle technique à renouveler pour J200198"),
]


def nettoyer():
    for table in (BonCarburant, Certificat, Alerte, Stock, Vehicule,
                  Utilisateur, Role):
        table.query.delete()


def semer():
    app = creer_app()
    with app.app_context():
        nettoyer()

        for libelle, niveau in ROLES:
            db.session.add(Role(libelle=libelle, niveau_acces=niveau))
        db.session.flush()
        roles = {r.libelle: r for r in Role.query.all()}

        for uid, nom, prenom, email, mdp, rnoms in UTILISATEURS:
            utilisateur = Utilisateur(
                uid=uid, nom=nom, prenom=prenom, email=email,
                mot_de_passe=mdp, statut="actif",
                roles=[roles[r] for r in rnoms])
            db.session.add(utilisateur)
            db.session.flush()
            db.session.add(Certificat(
                utilisateur=utilisateur,
                sujet="CN={0},O=Commune El Kelaâ des Sraghna".format(uid),
                date_emission=date(2025, 9, 1),
                date_expiration=date(2026, 9, 1),
                etat="valid"))

        for imm, marque, modele, service, carburant, statut in VEHICULES:
            db.session.add(Vehicule(
                immatriculation=imm, marque=marque, modele=modele,
                service=service, carburant=carburant, statut=statut))

        for type_carburant, quantite in (("Gasoil", 4200), ("Essence", 1800),
                                         ("GPL", 900)):
            db.session.add(Stock(type_carburant=type_carburant, quantite=quantite))

        for niveau, source, description in ALERTES:
            db.session.add(Alerte(
                niveau=niveau, source=source, description=description,
                timestamp=date.today() - timedelta(days=1), statut="ouverte"))

        db.session.commit()
        log.info("Jeu de données inséré : %d véhicules, %d utilisateurs, %d rôles.",
                 Vehicule.query.count(), Utilisateur.query.count(), Role.query.count())


if __name__ == "__main__":
    semer()