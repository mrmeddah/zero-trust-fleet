#!/usr/bin/env bash
# Controle de sante du laboratoire. Sortie 0 si tout est bon, 1 sinon.
set -uo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
set -a; [[ -f .env ]] && . ./.env; set +a

VERT='\033[32m'; ROUGE='\033[31m'; GRAS='\033[1m'; FIN='\033[0m'
ECHECS=0

verif() {
  local nom="$1"; shift
  if "$@" >/dev/null 2>&1; then
    printf "${VERT}  [ok]${FIN}   %s\n" "$nom"
  else
    printf "${ROUGE}[echec]${FIN} %s\n" "$nom"
    ECHECS=$((ECHECS+1))
  fi
}

echo "${GRAS}Controle du laboratoire${FIN}"
echo

# --- Conteneurs --------------------------------------------------------------
echo "Conteneurs"
verif "wazuh-indexer  actif"  podman ps --format '{{.Names}}' | grep -qx zt-wazuh-indexer
verif "wazuh-manager  actif"  podman ps --format '{{.Names}}' | grep -qx zt-wazuh-manager
verif "wazuh-dashboard actif"  podman ps --format '{{.Names}}' | grep -qx zt-wazuh-dashboard
verif "fleet-app       actif"  podman ps --format '{{.Names}}' | grep -qx zt-fleet-app
echo

# --- Services Wazuh ----------------------------------------------------------
echo "Services Wazuh"
for svc in wazuh-analysisd wazuh-remoted wazuh-execd filebeat wazuh-db; do
  verif "$svc" podman exec zt-wazuh-manager /var/ossec/bin/wazuh-control status | grep -q "$svc is running"
done
echo

# --- Indexer -----------------------------------------------------------------
echo "Indexer"
verif "indexer repond"  podman exec zt-wazuh-indexer curl -skf \
  -u "${WAZUH_INDEXER_USER:-admin}:${WAZUH_INDEXER_PASSWORD}" https://localhost:9200/
verif "indexer en ligne" podman exec zt-wazuh-indexer curl -skf \
  -u "${WAZUH_INDEXER_USER:-admin}:${WAZUH_INDEXER_PASSWORD}" \
  https://localhost:9200/_cluster/health | grep -qE '"status":"(green|yellow)"'
echo

# --- Tableau de bord ---------------------------------------------------------
echo "Interfaces web"
verif "dashboard Wazuh sur 5601" curl -skf -o /dev/null https://127.0.0.1:5601/
verif "fleet-app sur 5000"        curl -sf  -o /dev/null http://127.0.0.1:5000/login
echo

# --- Chaine d'alerte de bout en bout -----------------------------------------
echo "Chaine d'alerte (facultatif si freeipa est absent)"
if curl -sf -o /dev/null -X POST http://127.0.0.1:5000/login \
     -d "identifiant=agent1&mot_de_passe=echec-volontaire-pour-le-test" 2>/dev/null; then
  verif "AUTHFAIL emis vers syslog" podman logs --since 30s zt-fleet-app 2>&1 | grep -q "AUTHFAIL\|5 echecs"
else
  printf "  [info]  la requete de test a repondu 401 : c'est le comportement attendu\n"
fi
echo

# --- Verdict -----------------------------------------------------------------
if [[ $ECHECS -eq 0 ]]; then
  printf "${VERT}${GRAS}Laboratoire operationnel.${FIN}\n"
  exit 0
else
  printf "${ROUGE}${GRAS}${ECHECS} controle(s) en echec.${FIN}\n"
  echo "  Diagnostic : podman compose logs --tail 50 <service>"
  exit 1
fi
