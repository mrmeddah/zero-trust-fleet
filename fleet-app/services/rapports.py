"""Couche métier --- rapports de consommation.

Synthèse par véhicule, par service et par période ; tableau mensuel.
"""
from datetime import date

from models import db, BonCarburant, Vehicule


def _period(date_debut=None, date_fin=None):
    apres = date_debut or date(date.today().year, 1, 1)
    avant = date_fin or date.today()
    return apres, avant


def consommation_par_vehicule(date_debut=None, date_fin=None):
    apres, avant = _period(date_debut, date_fin)
    return db.session.query(
        Vehicule.immatriculation,
        db.func.sum(BonCarburant.quantite),
        db.func.count(BonCarburant.id),
    ).join(BonCarburant, BonCarburant.vehicule_id == Vehicule.id)\
     .filter(BonCarburant.date_emission >= apres,
             BonCarburant.date_emission <= avant)\
     .group_by(Vehicule.immatriculation).all()


def consommation_par_service(date_debut=None, date_fin=None):
    apres, avant = _period(date_debut, date_fin)
    return db.session.query(
        Vehicule.service,
        db.func.sum(BonCarburant.quantite),
        db.func.count(BonCarburant.id),
    ).join(BonCarburant, BonCarburant.vehicule_id == Vehicule.id)\
     .filter(BonCarburant.date_emission >= apres,
             BonCarburant.date_emission <= avant)\
     .group_by(Vehicule.service).all()


def rapport_mensuel(mois=None, annee=None):
    """Synthèse mensuelle : litres et bons par service, avec période."""
    mois = mois or date.today().month
    annee = annee or date.today().year
    debut = date(annee, mois, 1)
    fin = date(annee, mois, 28)
    if mois in (1, 3, 5, 7, 8, 10, 12):
        fin = date(annee, mois, 31)
    elif mois == 2:
        fin = date(annee, 2, 29 if annee % 4 == 0 and annee % 100 != 0 or annee % 400 == 0 else 28)
    else:
        fin = date(annee, mois, 30)
    return {
        "periode": "%02d/%04d" % (mois, annee),
        "par_service": [{
            "service": s,
            "litres": round(l, 2),
            "bons": n,
        } for s, l, n in consommation_par_service(debut, fin)],
        "total_litres": round(sum(l for _, l, _ in consommation_par_service(debut, fin)), 2),
        "total_bons": sum(n for _, _, n in consommation_par_service(debut, fin)),
    }