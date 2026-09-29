# PFA — Zero Trust pour un parc de véhicules municipal

Laboratoire de démonstration d'une architecture Zero Trust appliquée à la gestion
d'un parc communal : une application métier **fleet-app** autentifiée, un SIEM
**Wazuh** qui corréle les échecs d'authentification, et un annuaire d'entreprise.

Le dépôt a **un seul objectif : être reproductible.** Un poste compatible, un
script, et le laboratoire complet tourne. Rien n'est laissé à linterpretation.

```bash
git clone https://github.com/<vous>/pfa-zero-trust-fleet.git
cd pfa-zero-trust-fleet
cp .env.example .env
./scripts/up.sh
```

`up.sh` génère les secrets, construit l'image de l'application, démarre la pile,
attend que l'indexer réponde et injecte les règles de corrélation du projet.

---

## Ce que remonte le laboratoire

| Service | Rôle | Port local | État |
|---|---|---|---|
| `wazuh-indexer` | Index et moteur de recherche des alertes | — (interne) | requis |
| `wazuh-manager` | Réception syslog, décodeurs, règles, Filebeat | 514, 1514/udp | requis |
| `wazuh-dashboard` | Interface web SIEM | https://127.0.0.1:5601 | requis |
| `fleet-app` | Application Flask de gestion du parc | http://127.0.0.1:5000 | requis |
| `freeipa` | Annuaire LDAP/Kerberos | https://127.0.0.1/ipa/ | optionnel |

L'annuaire FreeIPA est **facultatif** et désactivé par défaut :

```bash
./scripts/up.sh --freeipa
```

Son initialisation demande plusieurs minutes et échoue fréquemment en
environnement contraint. Sans lui, l'application s'autentifie sur sa base
locale : toute la démonstration de supervision fonctionne quand même.

> **Utilisez toujours `127.0.0.1` et non `localhost`.** Podman publie les ports
> en IPv4 ; sur un poste où `localhost` résout d'abord en `::1`, la connexion
> échoue sans message d'erreur clair.

## Prérequis

- Linux, 8 Go de RAM libres, 4 Go de disque
- `podman` ≥ 4
- le provider compose : Debian/Ubuntu `sudo apt install podman-compose`
- `curl` (utilisé par les contrôles de santé)

Docker fonctionne aussi : remplacez `podman compose` par `docker compose` dans
`scripts/up.sh`, `scripts/verify.sh` et `scripts/down.sh`.

## Commandes

| Commande | Effet |
|---|---|
| `./scripts/up.sh` | Remonte tout, injecte la configuration Wazuh |
| `./scripts/verify.sh` | Contrôle de santé, code de sortie 0 ou 1 |
| `./scripts/down.sh` | Arrête, conserve les volumes |
| `./scripts/down.sh --purge` | Arrête et efface toutes les données |

## La chaîne de démonstration

C'est le cœur du projet : une tentative de connexion échouée dans l'application
devient une alerte corrélée dans le tableau de bord Wazuh.

```
fleet-app  ──syslog UDP 514──▶  wazuh-manager  ──Filebeat/HTTPS──▶  wazuh-indexer  ──▶  dashboard
  échec de login                 règle 100000                      recherche
                                 corrélation 100002
                                 (5 échecs / 60 s)
```

Pour la déclencher :

```bash
for i in $(seq 1 6); do
  curl -s -o /dev/null -X POST http://127.0.0.1:5000/login \
    -d "identifiant=agent1&mot_de_passe=essai-$i"
done
```

La sixième requête franchit le seuil. Cherchez `poc` ou
`authentication_failures` dans le tableau de bord.

### Les deux règles

`scripts/configure-wazuh.sh` injecte deux règles dans
`/var/ossec/etc/rules/local_rules.xml`.

`100000` transforme un `AUTHFAIL` émis par l'application en événement
sécuritifique de niveau 5.

`100002` corrèle **5 occurrences en moins de 60 secondes** sur le champ `user`
et déclenche au niveau 10.

Cette règle ne contient volontairement **pas** `<same_source_ip/>`. En
conteneurisé, tous les événements de l'application parviennent au manager avec
l'adresse de la boucle locale : filtrer sur l'adresse IP ferait échouer la
corrélation.

## Identifiants

Les secrets sont générés par `up.sh` et stockés dans `.env`, **ignoré par git**.

| Cible | Identifiant | Mot de passe |
|---|---|---|
| Tableau de bord Wazuh | `admin` | `WAZUH_DASHBOARD_PASSWORD` dans `.env` |
| Indexer | `admin` | `WAZUH_INDEXER_PASSWORD` dans `.env` |
| fleet-app | `agent1`, `admin1`, `gestionnaire1`, `auditeur1`, `direction1` | `motdepasseagent`, `motdepasseadmin`, … |

Les comptes de l'application viennent du jeu de données de démonstration
(`fleet-app/database/seed.py`) : 15 véhicules, 5 utilisateurs, 5 rôles, 3
alertes. La base est régénérée au démarrage, elle n'est pas versionnée.

## Ce qui n'a pas été validé

Par transparence, sur ce qui a été construit et démontré :

- **L'indexation complète fonctionne** : la chaîne alertes a été vérifiée de bout
  en bout, événement applicatif, règle, corrélation, indexation, tableau de bord.
- **FreeIPA n'a jamais été opérationnel.** L'annuaire n'a pas obtenu d'adresse IP
  dans le laboratoire d'origine et ses services sont restés arrêtés. Le mode
  conteneurisé est fourni mais n'a pas été validé de bout en bout. Le
  déploiement FreeIPA du laboratoire d'origine, qui lui l'était, est décrit dans
  `docs/GUIDE_IMPLEMENTATION.md`.
- **pfSense n'est pas conteneurisé.** Un pare-feu est par nature un équipement
  réseau à bord, pas un processus. Sa configuration reste dans
  `docs/GUIDE_IMPLEMENTATION.md`.
- **Aucun service Kali n'est fourni.** Les tests d'intrusion font partie du
  périmètre pédagogique mais pas du produit : utilisez la machine de votre choix
  pour déclencher les alertes, la règle `100002` ne dépend que de
  l'application.

## Organisation du dépôt

```
compose.yaml              les 5 services, réseau et volumes
.env.example              modèle de configuration, à copier en .env
fleet-app/                application Flask (Dockerfile, code, tests)
  Dockerfile              image autonome : base créée et peuplée au démarrage
  database/seed.py        jeu de données de démonstration
  services/parc.py        émission syslog vers le SIEM
  services/security.py    authentification locale ou LDAP
scripts/
  up.sh                   remontage complet
  verify.sh               contrôle de santé
  down.sh                 arrêt
  configure-wazuh.sh      règles, allowed-ips, chaîne Filebeat
docs/
  GUIDE_IMPLEMENTATION.md     déploiement du laboratoire d'origine, VM par VM
  SOUTENANCE_RUNBOOK.md       déroulé de soutenance
  presentation_soutenance.md  support de présentation
  pfe-zero-trust-municipal-fleet.md   architecture détaillée
  rapport-pfa-zero-trust-municipal-fleet.md  mémoire
```

## Licence etConfidentialité

Projet de fin d'études. Les mots de passe, clés et identifiants de l'instance
d'origine ont été retirés du dépôt. Ne versionnez jamais un fichier `.env`.
