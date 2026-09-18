"""Couche métier --- bons de carburant, mouvements de stock, imputation."""
from datetime import date

from models import db, BonCarburant, Stock, Vehicule, Utilisateur
from services.parc import journaliser

_types_valides = {"Gasoil", "Essence", "GPL"}


def lister_bons():
    return BonCarburant.query.order_by(BonCarburant.date_emission.desc()).all()


def stock_par_type():
    stocks = {s.type_carburant: s for s in Stock.query.all()}
    return stocks


def verifier_stock(type_carburant, quantite):
    """Contrôle des stocks avant émission d'un bon (couche métier)."""
    stocks = stock_par_type()
    entite = stocks.get(type_carburant)
    if entite is None or entite.quantite < quantite:
        return False
    return True


def creer_bon(donnees, utilisateur):
    """Émission d'un bon de carburant (fig:ch4-app-bon)."""
    vehicule_id = donnees.get("vehicule_id")
    type_carburant = donnees.get("type_carburant", "Gasoil")
    quantite = float(donnees.get("quantite", 0))

    if type_carburant not in _types_valides:
        raise ValueError("Type de carburant inconnu : %s" % type_carburant)
    if quantite <= 0:
        raise ValueError("Quantité invalide.")
    if vehicule_id is None:
        raise ValueError("Véhicule non sélectionné.")
    if not verifier_stock(type_carburant, quantite):
        raise ValueError("Stock insuffisant pour %s." % type_carburant)

    numero_bon = donnees.get("numero_bon") or generer_numero_bon()
    utilisateur_entite = None
    if isinstance(utilisateur, dict):
        utilisateur_entite = Utilisateur.query.filter_by(uid=utilisateur["uid"]).first()
    bon = BonCarburant(
        numero_bon=numero_bon,
        vehicule_id=vehicule_id,
        utilisateur=utilisateur_entite,           # l'agent émetteur
        type_carburant=type_carburant,
        quantite=quantite,
        date_emission=date.today(),
        statut="valide",
    )
    db.session.add(bon)

    # Débit du stock (mouvement)
    entite = stock_par_type().get(type_carburant)
    if entite is not None:
        entite.quantite -= quantite

    db.session.commit()
    journaliser(utilisateur, "emission_bon", "/api/bons/{0}".format(bon.id))
    return bon


def generer_numero_bon():
    from datetime import datetime
    seq = BonCarburant.query.count() + 1
    return "BON-%s-%04d" % (datetime.now().strftime("%Y%m%d"), seq)


def mouvements_stock():
    """Mouvements récents (bons valides + état des stocks)."""
    return {
        "bons": [b.to_dict() for b in lister_bons()],
        "stocks": [s.to_dict() for s in Stock.query.order_by(Stock.type_carburant).all()],
    }