"""Couche sécurité --- authentification LDAP/Kerberos vs FreeIPA et authentification
mutuelle par certificats (mTLS). Peut fonctionner en mode « disabled » (développement /
tests : base locale) ou en mode « enabled » (annuaire FreeIPA réel).

La vérification des mots de passe est déléguée à FreeIPA par liaison LDAP (bind),
conformément au chapitre IV : « vérification déléguée à FreeIPA ».
"""
import ssl
import logging
from functools import wraps

from flask import session, request, abort, current_app

logger = logging.getLogger("fleet.auth")


# ---------------------------------------------------------------- mTLS ---
class MtlsError(Exception):
    """Certificat client manquant, invalide ou absente de la chaîne de confiance."""


def identifier_certificat(envi):
    """Extrait le sujet (CN) du certificat client présenté au niveau TLS."""
    # Fichiers renseignés par gunicorn/nginx selon l'interface TLS.
    for k in ("SSL_CLIENT_S_DN_CN", "SSL_CLIENT_S_DN", "HTTP_SSL_CLIENT_S_DN"):
        if k in envi:
            return envi[k]
    return None


def verification_mtls(envi, require: bool):
    """Retourne le CN du client si un certificat valide est présent.

    En mode mTLS actif, l'absence de certificat client met fin à la requête
    (refus au niveau TLS, conformément à la figure fig:ch4-app-login — un
    accès sans certificat est refusé avant toute présentation de la page).
    """
    cn = identifier_certificat(envi)
    if require and not cn:
        raise MtlsError("Aucun certificat client présenté (mTLS exigé).")
    return cn


# ---------------------------------------------------------------- LDAP ---
class AnnuaireClient:
    """Client LDAP minimal vers l'annuaire FreeIPA (389-DS)."""

    def __init__(self, app=None):
        self.host = None
        self.port = None
        self.base_dn = None
        self.users_dn = None
        self.groups_dn = None
        self.enabled = False
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.host = app.config["FREEIPA_HOST"]
        self.port = app.config["FREEIPA_PORT"]
        self.base_dn = app.config["FREEIPA_BASE_DN"]
        self.users_dn = app.config["FREEIPA_USERS_DN"]
        self.groups_dn = app.config["FREEIPA_GROUPS_DN"]
        self.enabled = app.config["FREEIPA_MODE"] == "enabled"

    def _dn_utilisateur(self, uid):
        return "uid={0},{1}".format(uid, self.users_dn)

    def verifier_mot_de_passe(self, uid, mot_de_passe):
        """Bind LDAP avec les identifiants fournis ; délègue à FreeIPA."""
        if not self.enabled:
            return None  # mode dev : vérification locale (utilisateur.mot_de_passe)
        try:
            from ldap3 import Server, Connection, ALL
            server = Server(self.host, port=self.port, get_info=ALL)
            conn = Connection(server, user=self._dn_utilisateur(uid),
                              password=mot_de_passe, auto_bind=True)
            ok = conn.bound
            conn.unbind()
            return ok
        except Exception as exc:  # LDAPBindError, LDAPSocketOpenError, ...
            logger.warning("Échec du bind LDAP pour %s: %s", uid, exc)
            return False

    def groupes_utilisateur(self, uid):
        """Groupes auxquels appartient l'utilisateur (ids du groupe FreeIPA)."""
        if not self.enabled:
            return None
        try:
            from ldap3 import Server, Connection, ALL, SUBTREE
            server = Server(self.host, port=self.port, get_info=ALL)
            # Liaison anonyme suffisante pour la lecture des membres.
            conn = Connection(server, auto_bind=True)
            conn.search(self.groups_dn, "(member=uid={0},{1})".format(uid, self.users_dn),
                        SUBTREE, attributes=["cn"])
            return {entry.cn.value for entry in conn.entries if entry.cn.value}
        except Exception as exc:
            logger.warning("Lecture des groupes FreeIPA impossible : %s", exc)
            return set()


def charger_utilisateur_local(uid):
    """Charge l'utilisateur du référentiel local (miroir de l'annuaire)."""
    from models import Utilisateur
    return Utilisateur.query.filter_by(uid=uid).first()


# ----------------------------------------------------------------------- #
def besoin_session(fonction):
    """Vérifie qu'une session authentifiée existe (sinon 401)."""
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        if "utilisateur" not in session:
            abort(401)
        return fonction(*args, **kwargs)
    return enveloppe


def roles_requis(*roles):
    """Contrôle d'accès par rôle (moindre privilège).

    Chaque ressource est associée aux rôles de tb:ch3-endpoints,
    colonne « Rôle requis ».
    """
    def decorateur(fonction):
        @wraps(fonction)
        def enveloppe(*args, **kwargs):
            if "utilisateur" not in session:
                abort(401)
            roles_user = set(session["utilisateur"].get("roles", []))
            if not roles_user.intersection(set(roles)):
                abort(403)
            return fonction(*args, **kwargs)
        return enveloppe
    return decorateur