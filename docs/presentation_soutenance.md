# Soutenance de Projet de Fin d'Année (PFA)

> **Thème** : Conception et mise en œuvre d'une architecture Zero Trust pour la
> gestion sécurisée du parc municipal et du carburant
> **Stagiaire** : Mohamed Meddah — Filière IIR, Option CIR / EMSI
> **Encadrants** : M. Ioounousse, M. Mourad Boukri
> **Organisme d'accueil** : Commune d'El Kelaâ des Sraghna
> **Année universitaire** : 2025/2026 — **Soutenance** : Septembre 2026

---

# 1 — Page de garde

<!-- IMAGE : latex/figures/logos/logo-commune.png + logo-emsi.png -->

## Soutenance Projet de Fin d'Année

- **Thème** : Architecture Zero Trust pour la gestion du parc municipal et du carburant
- **Présenté par** : Mohamed Meddah
- **Filière** : Ingénierie Informatique et Réseaux (IIR) — Option Cybersécurité des Infrastructures et des Réseaux (CIR)
- **Établissement** : EMSI (École Marocaine des Sciences de l'Ingénieur)
- **Encadrants** : M. Ioounousse — M. Mourad Boukri
- **Réalisé au sein de** : Commune d'El Kelaâ des Sraghna
- **Année universitaire 2025/2026 — Septembre 2026**

*Notes orateur* : Se présenter brièvement, remercier le jury et les encadrants, annoncer le thème en une phrase.

---

# 2 — Plan de la présentation

## Plan

1. **Introduction** — contexte du stage
2. **Contexte général du projet** — commune, existant, problématique, solution proposée
3. **Analyse et conception** — acteurs, besoins, modélisation UML
4. **Architecture et technologies** — topologie hybride, segmentation, outils
5. **Réalisation** — les cinq modules livrés et les tests
6. **Conclusion et perspectives**

*Notes orateur* : Passer en revue le plan en 20 secondes, annoncer la durée prévue.

---

<!-- ============================================================ -->
# PARTIE 1 — INTRODUCTION
<!-- ============================================================ -->

# 3 — Contexte du stage

## L'organisme d'accueil

- Stage effectué au sein de la **Commune d'El Kelaâ des Sraghna** (Province d'El Kelaâ des Sraghna, Région Marrakech-Safi).
- Rattachement : **Direction des Services → Division Technique → Service Travaux et Suivi des Projets**.
- Implantation du stage : **Bureau de l'Informatique, de la Digitalisation et de la Maintenance** du matériel informatique et technique.

<!-- IMAGE : Figure « organisation de la commune » (schéma ou organigramme) -->

*Notes orateur* : Situer le lieu du stage et le rattachement administratif ; montrer l'organigramme en image.

---

<!-- ============================================================ -->
# PARTIE 2 — CONTEXTE GÉNÉRAL DU PROJET
<!-- ============================================================ -->

# 4 — Présentation de la commune

## La Commune d'El Kelaâ des Sraghna en chiffres

| Élément | Chiffre clé |
|---|---|
| Population (RGPH 2024) | 106 418 habitants |
| Effectif communal | Environ 320 agents |
| Taille du parc automobile | Une soixantaine de véhicules |
| Statut juridique | Collectivité territoriale de droit public |
| Cadre légal | Loi organique n° 113-14 relative aux communes |
| Compétences | État civil, urbanisme, voirie, déchets, éclairage public, espaces verts |

- La gestion du parc et du carburant relève du **Bureau des approvisionnements, du stockage et des moyens**.

*Notes orateur* : Insister sur l'importance du parc automobile comme outil opérationnel critique (mobilité des agents, collecte des déchets, travaux).

---

# 5 — L'existant et ses limites

## État des lieux de la gestion du parc et du carburant

L'existant repose sur des outils hétérogènes :

- **Registres papier** : affectations de véhicules, bons de carburant ;
- **Tableurs Excel** : suivi des consommations, rapports périodiques ;
- **Application web locale** : enregistrement des véhicules et des bons, accès par simple identifiant/mot de passe ;
- **Réseau local plat** : aucune segmentation, communication libre entre tous les postes.

**Limites critiques** :

- Absence de segmentation → mouvement latéral possible ;
- Authentification faible et partagée (aucune imputation individuelle) ;
- Absence de PKI et de chiffrement ;
- Aucune capacité de détection d'intrusion ;
- Vulnérabilité de la distribution de carburant (fraude interne).

*Notes orateur* : Décrire le quotidien des agents (registres, partage de comptes) puis énoncer les limites une par une.

---

# 6 — Problématique

## Modèle « périmètre » vs modèle « Zero Trust »

| Critère | Modèle périmètre | Modèle Zero Trust (NIST SP 800-207) |
|---|---|---|
| Confiance | Implicite à l'intérieur | Aucune : tout est vérifié |
| Contrôle d'accès | Basé sur l'IP | Basé sur l'identité et le contexte |
| Mouvement latéral | Possible | **Bloqué par défaut** |
| Vérification | Ponctuelle | Continue |
| Adaptation au cloud | Non | Oui |

**Problématique générale** :

> Comment sécuriser la gestion du parc municipal et du carburant — accès non autorisés,
> fraude, mouvement latéral — tout en étendant, de manière sûre, une partie des services
> vers le cloud, avec des outils libres et un coût maîtrisé ?

*Notes orateur* : Opposer les deux modèles, puis poser la problématique telle qu'écrite dans le mémoire.

---

# 7 — Solution proposée

## Architecture Zero Trust en cinq piliers

1. **Segmentation réseau stricte** — VLAN Administration, Flotte, Services, Tunnel ; rejet par défaut (pfSense + Suricata IPS) ;
2. **Gestion centralisée des identités et de la PKI** — FreeIPA : annuaire LDAP, Kerberos, DNS interne, CA interne ;
3. **Topologie hybride sécurisée** — tunnel chiffré WireGuard entre le site local et la VM Azure ;
4. **Détection active des menaces** — Wazuh (SIEM/XDR), règles personnalisées ciblées ;
5. **Validation par scénarios d'attaque** — red team : force brute, accès direct cloud, mouvement latéral.

**Objectifs** : sécuriser, segmenter, authentifier mutuellement, détecter — le tout en **open-source, coût de licence nul**.

*Notes orateur* : Énoncer les 5 piliers comme la réponse structurée à la problématique.

---

# 8 — Méthodologie

## Conduite du projet en méthode agile Scrum

- **Sprints** : 6 sprints sur 12 semaines, livraisons incrémentales ;
- **Rôles** : Product Owner (M. Mourad Boukri), Scrum Master & équipe de développement (le stagiaire) ;
- **Rituels** : sprint planning, daily, revue de sprint, rétrospective ;
- **Échéancier** : Infrastructure (sem. 3–5), Application + SIEM (sem. 6–7), Détection (8–9), Red team (10), Mémoire (11–12).

<!-- IMAGE : latex/figures/fig-ch1-gantt.png (Diagramme de Gantt) -->

*Notes orateur* : Justifier Scrum pour un projet mêlant réseau, identité, application et tests ; montrer le Gantt.

---

<!-- ============================================================ -->
# PARTIE 3 — ANALYSE ET CONCEPTION
<!-- ============================================================ -->

# 9 — Acteurs du système

## Identification des acteurs

| Acteur | Rôle principal |
|---|---|
| Administrateur de l'architecture | Configure et supervise tout (pfSense, FreeIPA, Wazuh, WireGuard) |
| Administrateur FreeIPA | Comptes, groupes, politiques, certificats |
| Gestionnaire du parc | Gère véhicules, affectations, maintenance |
| Agent du carburant | Enregistre bons, mouvements de stock, consommations |
| Direction | Consulte rapports et tableaux de bord |
| Auditeur de sécurité / utilisateur SIEM | Consulte journaux, alertes, conformité |
| Services système (Azure, FreeIPA, pfSense) | Interagissent entre eux (tunnel, PKI, supervision) |
| Attaquant (red team) | Teste l'architecture (force brute, mouvement latéral) |

*Notes orateur* : Insister sur le principe : chaque interaction sera vérifiée puis autorisée selon l'identité et le contexte (moindre privilège).

---

# 10 — Besoins fonctionnels et non fonctionnels

## Spécification des besoins

**Fonctionnels (extraits)** :

- **BF-01** Authentification centralisée via l'annuaire ; **BF-02** mTLS par certificats ;
- **BF-03/04/05** Segmentation VLAN + refus par défaut + règles explicites ;
- **BF-06/07** Tunnel chiffré + publication uniquement via le tunnel ;
- **BF-08/09/10/11** Gestion des véhicules, bons & stocks, consommations, rapports ;
- **BF-12/13/14/15** Collecte de journaux, règles de détection, alertes, réponse active ;
- **BF-16/17** Gestion des certificats, journalisation des refus.

**Non fonctionnels (extraits)** :

- Moindre privilège (BNF-01), chiffrement systématique (BNF-02), rejet par défaut (BNF-03) ;
- Latence de détection < 60 s (BNF-04), disponibilité ≥ 99 % (BNF-05) ;
- **Open-source, coût de licence nul** (BNF-08), conformité NIST/ATT&CK (BNF-09), traçabilité (BNF-10).

*Notes orateur* : Présenter les 17 besoins fonctionnels synthétiquement, puis les contraintes de qualité.

---

# 11 — Cas d'utilisation

## Modélisation UML — cas d'utilisation

- Diagramme de **cas d'utilisation global** : toutes les fonctionnalités et leurs acteurs ;
- Vues **par rôle** : Administrateur, Gestionnaire du parc, Agent du carburant, Direction ;
- Trois UC critiques détaillés : **S'authentifier** (UC-01), **Gérer les certificats** (UC-02), **Se connecter via le tunnel** (UC-03).

<!-- IMAGE : latex/figures/fig-ch2-uc-global.png (Cas d'utilisation global) -->
<!-- IMAGE : latex/figures/fig-ch2-uc-admin.png + fig-ch2-uc-gestionnaire.png + fig-ch2-uc-agent.png + fig-ch2-uc-direction.png -->

*Notes orateur* : Expliquer le UC-01 « S'authentifier » : présentation du certificat client (mTLS), vérification Kerberos/LDAP, session établie.

---

# 12 — Diagrammes séquence, activité, classes

## Modélisation UML — comportement et structure

- **Séquences** : Authentification et accès à l'application ; de la détection à l'alerte ; blocage d'un mouvement latéral ;
- **Activités** : Connexion à l'application ; traitement d'une alerte ; déroulement d'un scénario de test ;
- **Classes** : Utilisateur, Role, Certificat, Vehicule, Affectation, BonCarburant, JournalAcces, Alerte.

<!-- IMAGE : latex/figures/fig-ch2-seq-auth.png + fig-ch2-seq-alerte.png + fig-ch2-seq-lateral.png -->
<!-- IMAGE : latex/figures/fig-ch2-act-connexion.png + fig-ch2-act-alerte.png + fig-ch2-act-scenario.png -->
<!-- IMAGE : latex/figures/fig-ch2-classes.png (Diagramme de classes) -->

*Notes orateur* : Focus sur le diagramme de classes (socle de l'application) ; les autres diagrammes illustrent le comportement.

---

<!-- ============================================================ -->
# PARTIE 4 — ARCHITECTURE ET TECHNOLOGIES
<!-- ============================================================ -->

# 13 — Architecture : vue d'ensemble

## Topologie hybride locale / cloud

- **Plan réseau** : pare-feu **pfSense** — routeur inter-VLAN, filtrage, extrémité du tunnel WireGuard ;
- **Plan identité et confiance** : **FreeIPA** — annuaire LDAP, Kerberos, DNS interne, CA (PKI) ;
- **Plan applicatif et supervision** : **VM Azure** — application Flask (port 5000) + **Wazuh** (port 443) ;
- **Tunnel chiffré WireGuard** : Site local ↔ VM Azure, sans exposition publique.

<!-- IMAGE : latex/figures/fig-ch3-topologie.png (Topologie globale) -->

*Notes orateur* : Positionner les trois plans sur la topologie ; insister sur « aucun service exposé publiquement, tout passe par le tunnel ».

---

# 14 — Segmentation et plan d'adressage

## VLAN et adressage (deny by default)

| VLAN | Nom | Sous-réseau | Contenu |
|---|---|---|---|
| 10 | Administration | 10.10.10.0/24 | FreeIPA (10.10.10.10), gestion |
| 20 | Flotte | 10.10.20.0/24 | Simulateurs véhicules, clients carburant |
| 30 | Services | 10.10.30.0/24 | Services internes, DNS |
| 99 | Tunnel | 10.99.0.0/30 | Liaison WireGuard (10.99.0.1 ↔ 10.99.0.2) |

**Matrice de flux** :

- VLAN 10 → 99 : autorisé (supervision, application) ;
- VLAN 20 → 99 : port 5000 du tunnel (application carburant) ;
- VLAN 20 → 10 : **refusé** ;
- Tout autre inter-VLAN : **refusé par défaut**.

*Notes orateur* : Montrer que le seul moyen d'accéder à l'application depuis la flotte est le chemin VLAN 20 → tunnel.

---

# 15 — Composants et outils

## Technologies utilisées

| Outil | Rôle |
|---|---|
| KVM/QEMU | Hyperviseur des VM locales (pfSense, FreeIPA) |
| pfSense CE 2.7 | Pare-feu, routeur inter-VLAN, NAT, journalisation |
| Suricata | Moteur IDS/IPS intégré à pfSense |
| FreeIPA | Annuaire LDAP, Kerberos, DNS, autorité de certification |
| WireGuard | Tunnel chiffré locale ↔ Azure |
| Wazuh | SIEM/XDR : ingestion, corrélation, alertes |
| Microsoft Azure | VM Ubuntu 22.04 B2s (application + Wazuh) |
| Python / Flask / Jinja2 | Backend et templates de l'application |
| SQLite | Base de données de l'application |
| Kali Linux | Machine de l'attaquant (red team) |

*Notes orateur* : Souligner le choix 100 % open-source (coût de licence nul — BNF-08).

---

<!-- ============================================================ -->
# PARTIE 5 — RÉALISATION
<!-- ============================================================ -->

# 16 — Module infrastructure et segmentation

## Réalisation — pfSense

- **Interfaces** : WAN, LAN, interface dédiée au tunnel WireGuard ;
- **VLAN 10 / 20 / 30 / 99** créés avec leurs adresses et passerelles ;
- **Règles de filtrage** : politique deny-by-default, autorisations minimales explicites ;
- **Suricata** activé en **mode IPS** sur les VLAN, jeux de règles mis à jour.

<!-- IMAGE : fig:ch4-pf-interfaces (Interfaces / Assignments) -->
<!-- IMAGE : fig:ch4-pf-rules (Firewall / Rules) -->
<!-- IMAGE : fig:ch4-suricata (Suricata IPS running) -->

*Notes orateur* : Expliquer la configuration des interfaces puis montrer l'ordre des règles de pare-feu.

---

# 17 — Module identité et PKI

## Réalisation — FreeIPA

- Déploiement sur Rocky Linux 9, domaine **municipal.local** ;
- Services intégrés : LDAP (389-DS), **Kerberos**, **DNS interne**, **CA** ;
- Hiérarchie de certification à deux niveaux : CA racine **municipal.local** + CA intermédiaire FreeIPA ;
- Certificats émis pour les services (**fleet-app**, wazuh, pfsense) et pour les **utilisateurs** ;
- Règle d'or : **pas de certificat, pas d'accès** (mTLS).

<!-- IMAGE : fig:ch4-freeipa-user (page utilisateur + certificat) -->
<!-- IMAGE : fig:ch4-freeipa-ca (gestion des certificats) -->

*Notes orateur* : Montrer un utilisateur et son certificat ; expliquer que l'application refuse toute connexion sans certificat de la CA interne.

---

# 18 — Application de gestion du parc et du carburant

## Réalisation — application Flask

- Accessible uniquement via le tunnel, après **authentification mutuelle** (certificat client) ;
- **Écrans** : connexion → tableau de bord du parc → bons de carburant → rapports de consommation ;
- **Tableau de bord** : compteurs (véhicules, alertes maintenance) + tableau des véhicules (J200189…) ;
- **Bon de carburant** : véhicule, type, quantité, n° de bon, validation (avec contrôle du stock) ;
- **Rapports** : consommations par service (graphique en barres), synthèse mensuelle, filtre par période.

<!-- IMAGE : fig:ch4-app-login (page de connexion, mention certificat) -->
<!-- IMAGE : fig:ch4-app-dashboard (tableau de bord du parc) -->
<!-- IMAGE : fig:ch4-app-bon (émission d'un bon) -->
<!-- IMAGE : fig:ch4-app-rapport (rapport de consommation) -->

<!-- VIDEO : courte démonstration (login → bon → rapport), 30–60 s -->

*Notes orateur* : Faire la démo rapide si possible ; sinon montrer les 4 captures et décrire le parcours utilisateur.

---

# 19 — Module supervision et tunnel

## Réalisation — Wazuh + WireGuard

- **Wazuh** : collecte des journaux (syslog pfSense/FreeIPA, journaux application) et règles personnalisées :
  - **100001 (niv. 10)** : accès hors horaires de service (`/fuel`, `/fleet`) ;
  - **100002 (niv. 12)** : force brute — 5 échecs / 60 s, même source ;
  - **100003 (niv. 14)** : mouvement latéral VLAN 20 → VLAN 10 bloqué ;
- **WireGuard** : pfSense (10.99.0.1) ↔ VM Azure (10.99.0.2), port UDP 51820, clés Curve25519 ;
- **Azure** : NSG + UFW n'autorisent que le port UDP du tunnel.

<!-- IMAGE : fig:ch4-wg-state (état du tunnel WireGuard) -->
<!-- IMAGE : fig:ch4-wazuh-rules (règles 100001-100003) -->
<!-- IMAGE : fig:ch4-wazuh-dash (tableau de bord Wazuh) -->
<!-- IMAGE : fig:ch4-azure-nsg (règles NSG Azure) -->

*Notes orateur* : Relier la détection aux scénarios d'attaque de la partie finale (force brute, accès cloud, mouvement latéral).

---

<!-- ============================================================ -->
# PARTIE 6 — CONCLUSION ET PERSPECTIVES
<!-- ============================================================ -->

# 20 — Évaluation : scénarios d'attaque

## Résultats des tests (red team)

| Scénario | Menace | Outil | Résultat | Règle |
|---|---|---|---|---|
| 1 — Force brute | Compromission d'identifiants | Hydra | **Détectée** | 100002 (niv. 12) |
| 2 — Accès direct cloud | Exposition de la ressource | nmap | **Bloquée** (ports filtered) | — |
| 3 — Mouvement latéral | Escalade interne | ping/nmap/curl | **Bloquée + détectée** | 100003 (niv. 14) |

**Zoom composants** : plusieurs services derrière mTLS (app, Wazuh, pfSense), 3 règles de détection actives, coût de licence **nul**.

<!-- IMAGE : fig:ch4-sc1-alert (alerte force brute Wazuh) -->
<!-- IMAGE : fig:ch4-sc2-nmap (scan nmap : ports filtered, 51820 open) -->
<!-- IMAGE : fig:ch4-sc3-alert (alerte mouvement latéral) -->

*Notes orateur* : Conclure la phase de validation : la force brute est corrélée, la ressource cloud inaccessible publiquement, le mouvement latéral bloqué et signalé.

---

# 21 — Conclusion et perspectives

## Bilan et suites

**Résultats obtenus** :

- Micro-segmentation en 4 VLAN + deny-by-default : mouvement latéral empêché ;
- mTLS adossé à FreeIPA : seuls identités et équipements vérifiés accèdent ;
- Wazuh : détection en temps réel (force brute, mouvements latéraux) ;
- WireGuard : accès cloud sans exposition publique ;
- 100 % open-source, zéro coût de licence.

**Perspectives** :

- Généraliser la réponse active sur toutes les règles ;
- Intégrer la 5ᵉ source de journaux (système VM Azure) ;
- Module de facturation et **ouverture mobile** aux agents de terrain (loi 09-08) ;
- Mise en conformité progressive avec **ISO/IEC 27001** ;
- Sensibilisation et formation des agents.

**Appréciation personnelle** : un projet formateur — de l'analyse du besoin au test d'attaques simulées, en passant par le déploiement d'une infrastructure réelle.

*Notes orateur* : Terminer sur le bilan, annoncer les perspectives, remercier le jury, répondre aux questions.

---

# Merci — Questions

<!-- IMAGE : latex/figures/logos/logo-commune.png + logo-emsi.png -->

## Merci de votre attention

**Questions ?**

*Notes orateur* : Remercier le jury, les encadrants et l'équipe de la commune ; rester disponible pour la démonstration.