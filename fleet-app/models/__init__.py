"""Couche données --- modèles et schéma SQLAlchemy.

Classes : Utilisateur, Role, Certificat, Vehicule, Affectation,
BonCarburant, JournalAcces, Alerte (+ Stock pour les mouvements de carburant).
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()


def _maintenant():
    return datetime.now(datetime.UTC) if hasattr(datetime, "UTC") else datetime.utcnow()


class Utilisateur(db.Model):
    """id, nom, prenom, email, statut ; 1..* Certificat ; 0..* Role ; émet 0..* Bon."""
    __tablename__ = "utilisateur"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), unique=True, nullable=False)          # login FreeIPA
    nom = db.Column(db.String(64), nullable=False)
    prenom = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128))
    statut = db.Column(db.String(16), default="actif")                   # actif | suspendu
    mot_de_passe = db.Column(db.String(256), nullable=True)              # dev / seed uniquement

    roles = db.relationship("Role", secondary="utilisateur_role",
                            back_populates="utilisateurs")
    certificats = db.relationship("Certificat", back_populates="utilisateur")
    bons = db.relationship("BonCarburant", back_populates="utilisateur")

    def to_dict(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "statut": self.statut,
            "roles": [r.libelle for r in self.roles],
        }


class Role(db.Model):
    """id, libelle, niveau_acces ; 0..* Utilisateur."""
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(32), unique=True, nullable=False)
    niveau_acces = db.Column(db.Integer, default=1)  # 1 agent, 2 gestionnaire, 3 direction, 4 admin

    utilisateurs = db.relationship("Utilisateur", secondary="utilisateur_role",
                                   back_populates="roles")

    def to_dict(self):
        return {"id": self.id, "libelle": self.libelle, "niveau_acces": self.niveau_acces}


utilisateur_role = db.Table(
    "utilisateur_role",
    db.Column("utilisateur_id", db.Integer, db.ForeignKey("utilisateur.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
)


class Certificat(db.Model):
    """id, sujet, autorite, date_emission, date_expiration, etat ; appartient à 1 Utilisateur."""
    __tablename__ = "certificat"

    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"))
    sujet = db.Column(db.String(128), nullable=False)
    autorite = db.Column(db.String(128), nullable=False, default="CA interne municipal.local")
    date_emission = db.Column(db.Date, default=date.today)
    date_expiration = db.Column(db.Date)
    etat = db.Column(db.String(16), default="valid")   # valid | expired | revoked

    utilisateur = db.relationship("Utilisateur", back_populates="certificats")

    def to_dict(self):
        return {
            "id": self.id,
            "sujet": self.sujet,
            "autorite": self.autorite,
            "date_emission": self.date_emission.isoformat() if self.date_emission else None,
            "date_expiration": self.date_expiration.isoformat() if self.date_expiration else None,
            "etat": self.etat,
        }


class Vehicule(db.Model):
    """id, immatriculation, marque, modele, service, carburant, statut ;
    concerné par 0..* BonCarburant ; lié à 1 Affectation."""
    __tablename__ = "vehicule"

    id = db.Column(db.Integer, primary_key=True)
    immatriculation = db.Column(db.String(16), unique=True, nullable=False)
    marque = db.Column(db.String(32), nullable=False)
    modele = db.Column(db.String(32))
    service = db.Column(db.String(64))            # service affectataire
    carburant = db.Column(db.String(16), default="Gasoil")
    statut = db.Column(db.String(16), default="En service")  # En service | En maintenance | Hors service

    bons = db.relationship("BonCarburant", back_populates="vehicule")
    affectation = db.relationship("Affectation", back_populates="vehicule",
                                  uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "immatriculation": self.immatriculation,
            "marque": self.marque,
            "modele": self.modele,
            "service": self.service,
            "carburant": self.carburant,
            "statut": self.statut,
        }


class Affectation(db.Model):
    """id, date_debut, date_fin, utilisateur, vehicule ; relie 1 Vehicule et 1..* Utilisateur."""
    __tablename__ = "affectation"

    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"))
    vehicule_id = db.Column(db.Integer, db.ForeignKey("vehicule.id"))
    date_debut = db.Column(db.Date, default=date.today)
    date_fin = db.Column(db.Date, nullable=True)

    utilisateur = db.relationship("Utilisateur")
    vehicule = db.relationship("Vehicule", back_populates="affectation")

    def to_dict(self):
        return {
            "id": self.id,
            "utilisateur": self.utilisateur.uid if self.utilisateur else None,
            "vehicule": self.vehicule.immatriculation if self.vehicule else None,
            "date_debut": self.date_debut.isoformat() if self.date_debut else None,
            "date_fin": self.date_fin.isoformat() if self.date_fin else None,
        }


class BonCarburant(db.Model):
    """id, numero_bon, quantite, type_carburant, date_emission, vehicule, utilisateur, statut."""
    __tablename__ = "bon_carburant"

    id = db.Column(db.Integer, primary_key=True)
    numero_bon = db.Column(db.String(24), unique=True, nullable=False)
    vehicule_id = db.Column(db.Integer, db.ForeignKey("vehicule.id"))
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"))
    type_carburant = db.Column(db.String(16), default="Gasoil")
    quantite = db.Column(db.Float, nullable=False)
    date_emission = db.Column(db.Date, default=date.today)
    statut = db.Column(db.String(16), default="valide")  # valide | annule

    vehicule = db.relationship("Vehicule", back_populates="bons")
    utilisateur = db.relationship("Utilisateur", back_populates="bons")

    def to_dict(self):
        return {
            "id": self.id,
            "numero_bon": self.numero_bon,
            "vehicule": self.vehicule.immatriculation if self.vehicule else None,
            "vehicule_id": self.vehicule_id,
            "utilisateur": self.utilisateur.uid if self.utilisateur else None,
            "type_carburant": self.type_carburant,
            "quantite": self.quantite,
            "date_emission": self.date_emission.isoformat() if self.date_emission else None,
            "statut": self.statut,
        }


class Stock(db.Model):
    """Niveau de stock par type de carburant (API /api/stock)."""
    __tablename__ = "stock"

    id = db.Column(db.Integer, primary_key=True)
    type_carburant = db.Column(db.String(16), unique=True, nullable=False)
    quantite = db.Column(db.Float, default=0.0)          # litres disponibles

    def to_dict(self):
        return {"id": self.id, "type_carburant": self.type_carburant,
                "quantite": self.quantite}


class JournalAcces(db.Model):
    """id, timestamp, utilisateur, source_ip, action, ressource ; référence 1 Utilisateur."""
    __tablename__ = "journal_acces"

    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), nullable=True)
    timestamp = db.Column(db.DateTime, default=_maintenant)
    source_ip = db.Column(db.String(64))
    action = db.Column(db.String(64), default="acces")
    ressource = db.Column(db.String(256))

    utilisateur = db.relationship("Utilisateur")

    def to_dict(self):
        return {
            "id": self.id,
            "utilisateur": self.utilisateur.uid if self.utilisateur else None,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "source_ip": self.source_ip,
            "action": self.action,
            "ressource": self.ressource,
        }


class Alerte(db.Model):
    """id, niveau, source, description, timestamp, statut ; issue de l'analyse des journaux."""
    __tablename__ = "alerte"

    id = db.Column(db.Integer, primary_key=True)
    niveau = db.Column(db.Integer, default=3)      # 1..5 sévérité
    source = db.Column(db.String(128))
    description = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=_maintenant)
    statut = db.Column(db.String(16), default="ouverte")  # ouverte | traitee

    def to_dict(self):
        return {
            "id": self.id,
            "niveau": self.niveau,
            "source": self.source,
            "description": self.description,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "statut": self.statut,
        }

    @staticmethod
    def alertes_maintenance():
        """Alertes considérées comme des alertes de maintenance (tableau de bord)."""
        return Alerte.query.filter(Alerte.source.in_(["maintenance", "vehicule"])).all()