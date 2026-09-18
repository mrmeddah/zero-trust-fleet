"""Pages web servies par Flask (templates Jinja2) — routes alignées sur le
chapitre III : /login, /fleet, /fuel, /rapports, /admin.

Les routes /fleet et /fuel sont volontairement nommées ainsi afin de
correspondre à la règle de détection Wazuh 100001 (<url>/fuel|/fleet</url>).
"""
from datetime import date, datetime

from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, current_app, flash, jsonify)

from models import (db, Utilisateur, Role, Certificat, Vehicule, Alerte,
                    BonCarburant, Stock, JournalAcces)
from services.parc import journaliser, synthese_parc
from services.carburant import lister_bons
from services.rapports import rapport_mensuel, consommation_par_service
from services.security import AnnuaireClient, MtlsError, verification_mtls

api = Blueprint("pages", __name__)

MAPPING_GROUPES = {
    "admins": "Administrateur",
    "gestionnaires": "Gestionnaire",
    "agents": "Agent",
    "direction": "Direction",
    "auditeurs": "Auditeur",
}


def _mtls_actif():
    return bool(current_app.config.get("MTLS_VERIFY_CLIENT"))


@api.before_app_request
def exiger_certificat():
    """Refus au niveau TLS : sans certificat client, l'accès est rejeté."""
    if not _mtls_actif():
        return None
    if request.endpoint in ("static",):
        return None
    try:
        cn = verification_mtls(request.environ, require=True)
        request.environ["fleet.client_cn"] = cn
    except MtlsError:
        return ("Accès refusé : certificat client requis (mTLS).", 403)
    return None


@api.after_app_request
def journaliser_requete(reponse):
    """Journalisation structurée de toutes les requêtes (tb:ch4-logs)."""
    if request.endpoint and not request.endpoint.startswith("static"):
        utilisateur = session.get("utilisateur")
        if utilisateur:
            try:
                journaliser(utilisateur, request.method,
                            request.path, request.remote_addr)
            except Exception:
                db.session.rollback()
    return reponse


def _roles_annuaire(uid):
    annuaire = current_app.extensions.get("fleet_annuaire")
    if annuaire is None:
        return set()
    groupes = annuaire.groupes_utilisateur(uid) or set()
    return {MAPPING_GROUPES[g] for g in groupes if g in MAPPING_GROUPES}


@api.route("/login", methods=["GET", "POST"])
def pages_login():
    if request.method == "POST":
        uid = request.form.get("identifiant", "").strip()
        mot_de_passe = request.form.get("mot_de_passe", "")
        utilisateur = Utilisateur.query.filter_by(uid=uid).first()
        valide = False

        annuaire = current_app.extensions.get("fleet_annuaire")
        if annuaire is not None and annuaire.enabled:
            valide = bool(annuaire.verifier_mot_de_passe(uid, mot_de_passe))
        elif utilisateur is not None and utilisateur.mot_de_passe:
            valide = (utilisateur.mot_de_passe == mot_de_passe)

        if utilisateur is None or not valide or utilisateur.statut != "actif":
            flash("Identifiants invalides ou accès refusé.", "erreur")
            return render_template("login.html", cert_cn=_cert_cn()), 401

        roles = [r.libelle for r in utilisateur.roles] or list(_roles_annuaire(uid))
        session["utilisateur"] = {
            "uid": utilisateur.uid,
            "nom": utilisateur.nom,
            "prenom": utilisateur.prenom,
            "roles": roles,
        }
        journaliser(session["utilisateur"], "connexion", "/login", request.remote_addr)
        return redirect(url_for("pages.pages_fleet"))

    return render_template("login.html", cert_cn=_cert_cn())


def _cert_cn():
    if not _mtls_actif():
        return None
    from services.security import identifier_certificat
    return identifier_certificat(request.environ)


@api.route("/logout")
def pages_logout():
    session.pop("utilisateur", None)
    return redirect(url_for("pages.pages_login"))


def _session_requise():
    if "utilisateur" not in session:
        return redirect(url_for("pages.pages_login"))
    return None


def _role_autorise(*roles):
    return set(session.get("utilisateur", {}).get("roles", [])) & set(roles)


@api.route("/fleet")
def pages_fleet():
    redirection = _session_requise()
    if redirection:
        return redirection
    if not _role_autorise("Gestionnaire", "Direction", "Administrateur"):
        flash("Accès non autorisé à la gestion du parc.", "erreur")
        return redirect(url_for("pages.pages_login"))
    return render_template(
        "fleet.html",
        vehicules=[v.to_dict() for v in Vehicule.query.order_by(Vehicule.immatriculation).all()],
        synthese=synthese_parc(),
        alertes=[a.to_dict() for a in Alerte.query.filter_by(statut="ouverte").all()][:5],
        utilisateur=session["utilisateur"],
    )


@api.route("/fuel", methods=["GET", "POST"])
def pages_fuel():
    redirection = _session_requise()
    if redirection:
        return redirection
    if not _role_autorise("Agent", "Gestionnaire", "Administrateur"):
        flash("Accès non autorisé à la gestion du carburant.", "erreur")
        return redirect(url_for("pages.pages_login"))

    if request.method == "POST":
        from services.carburant import creer_bon
        try:
            donnees = dict(request.form)
            bon = creer_bon(donnees, session["utilisateur"])
            flash("Bon %s émis avec succès." % bon.numero_bon, "succes")
        except ValueError as exc:
            flash(str(exc), "erreur")
        return redirect(url_for("pages.pages_fuel"))

    return render_template(
        "fuel.html",
        bons=[b.to_dict() for b in lister_bons()],
        vehicules=[v.to_dict() for v in Vehicule.query.order_by(Vehicule.immatriculation).all()],
        stocks=[s.to_dict() for s in Stock.query.order_by(Stock.type_carburant).all()],
        utilisateur=session["utilisateur"],
    )


@api.route("/rapports")
def pages_rapports():
    redirection = _session_requise()
    if redirection:
        return redirection
    if not _role_autorise("Direction", "Administrateur", "Gestionnaire"):
        flash("Accès non autorisé aux rapports.", "erreur")
        return redirect(url_for("pages.pages_login"))

    debut = request.args.get("debut")
    fin = request.args.get("fin")
    mois = request.args.get("mois", type=int) or date.today().month
    annee = request.args.get("annee", type=int) or date.today().year
    par_service = [{"service": s or "Non affecté", "litres": round(l, 2), "bons": n}
                   for s, l, n in consommation_par_service(
                       _date(debut), _date(fin))]
    return render_template(
        "rapports.html",
        rapport=rapport_mensuel(mois, annee),
        par_service=par_service,
        filtres={"debut": debut or "", "fin": fin or "", "mois": mois, "annee": annee},
        utilisateur=session["utilisateur"],
    )


def _date(valeur):
    if not valeur:
        return None
    try:
        return datetime.strptime(valeur, "%Y-%m-%d").date()
    except ValueError:
        return None


@api.route("/admin")
def pages_admin():
    redirection = _session_requise()
    if redirection:
        return redirection
    if not _role_autorise("Administrateur"):
        flash("Accès réservé à l'administrateur.", "erreur")
        return redirect(url_for("pages.pages_login"))
    return render_template(
        "admin.html",
        utilisateurs=[u.to_dict() for u in Utilisateur.query.order_by(Utilisateur.uid).all()],
        roles=[r.to_dict() for r in Role.query.order_by(Role.libelle).all()],
        certificats=[c.to_dict() for c in Certificat.query.all()],
        utilisateur=session["utilisateur"],
    )