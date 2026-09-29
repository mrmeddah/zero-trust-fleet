import logging
import logging.handlers
import os
import socket

_SIEM = None


def _siem():
    """Logger syslog UDP vers le manager Wazuh (port 514).

    La cible et le port se lisent dans l'environnement pour que le meme code
    fonctionne en local (127.0.0.1) comme en pile conteneurisee (wazuh-manager).
    """
    global _SIEM
    if _SIEM is None:
        hote = os.environ.get("FLEET_SIEM_HOST", "127.0.0.1")
        port = int(os.environ.get("FLEET_SIEM_PORT", "514"))
        _SIEM = logging.getLogger("fleet.siem")
        if not _SIEM.handlers:
            h = logging.handlers.SysLogHandler(
                address=(hote, port), facility="local6",
                socktype=socket.SOCK_DGRAM)
            h.syslog_ident = "fleet-app"
            _SIEM.addHandler(h)
            _SIEM.setLevel(logging.INFO)
        _SIEM.propagate = False
    return _SIEM


def alerter_wazuh(evenement, **champs):
    """Emet un evenement de securite vers Wazuh pour correlation (regles 1000xx)."""
    details = " ".join(f"{k}={v}" for k, v in champs.items() if v is not None)
    ligne = f"{evenement} {details}".strip()
    try:
        _siem().info(ligne)
    except Exception:
        pass


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
    """Compteurs synthétiques du tableau de bord."""
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