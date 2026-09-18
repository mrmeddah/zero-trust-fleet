"""Couche métier --- gestion du parc (véhicules, affectations, maintenance)."""
from datetime import date

from models import db, Vehicule, Affectation, Alerte, JournalAcces, Utilisateur
from services.security import besoin_session


def journaliser(utilisateur, action, ressource, source_ip=None):
    """Journalisation structurée de l'accès (JournalAcces, alimente Wazuh)."""
    uid = utilisateur["uid"] if isinstance(utilisateur, dict) else getattr(utilisateur, "uid", None)
    utilisateur_entite = Utilisateur.query.filter_by(uid=uid).first() if uid else None
    db.session.add(JournalAcces(
        utilisateur=utilisateur_entite,
        source_ip=source_ip,
        action=action,
        ressource=ressource,
    ))
    db.session.commit()


def lister_vehicules():
    return Vehicule.query.all()


def detailler_vehicule(vehicule_id):
    return Vehicule.query.get_or_404(vehicule_id)


def creer_vehicule(donnees, utilisateur):
    vehicule = Vehicule(
        immatriculation=donnees.get("immatriculation", "").upper().strip(),
        marque=donnees.get("marque", "").strip(),
        modele=donnees.get("modele", "").strip(),
        service=donnees.get("service", "").strip(),
        carburant=donnees.get("carburant", "Gasoil"),
        statut=donnees.get("statut", "En service"),
    )
    db.session.add(vehicule)
    db.session.commit()
    journaliser(utilisateur, "creation", "/api/vehicules/{0}".format(vehicule.id))
    return vehicule


def synthese_parc():
    """Compteurs synthétiques du tableau de bord (fig:ch4-app-dashboard)."""
    total = Vehicule.query.count()
    en_service = Vehicule.query.filter_by(statut="En service").count()
    en_maintenance = Vehicule.query.filter(
        Vehicule.statut.in_(["En maintenance", "Hors service"])).count()
    alertes = Alerte.query.filter_by(statut="ouverte").count()
    return {
        "total": total,
        "en_service": en_service,
        "en_maintenance": en_maintenance,
        "alertes_maintenance": alertes,
    }


def besoins_session_fournisseur():
    """Fournisseur de rôle — voir services/security.py (besoin_session)."""
    return besoin_session