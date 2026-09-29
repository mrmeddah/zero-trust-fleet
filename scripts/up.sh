#!/usr/bin/env bash
# Remonte le laboratoire complet. Point d'entree unique.
#
#   ./scripts/up.sh              -> stack de base (Wazuh + fleet-app)
#   ./scripts/up.sh --freeipa    -> ajoute l'annuaire FreeIPA
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
RACINE="$PWD"

ROUGE='\033[31m'; VERT='\033[32m'; GRAS='\033[1m'; FIN='\033[0m'
info() { printf "${GRAS}==>${FIN} %s\n" "$*"; }
ok()   { printf "${VERT} [ok]${FIN} %s\n" "$*"; }
err()  { printf "${ROUGE}[err]${FIN} %s\n" "$*" >&2; }

COMPOSE=(podman compose)
PROFILES=()
if [[ "${1:-}" == "--freeipa" ]]; then
  PROFILES=(--profile freeipa)
  info "Profil FreeIPA demande"
fi

# --------------------------------------------------------------- prerequisites
command -v podman >/dev/null 2>&1 || { err "podman absent — https://podman.io/getting-started/installation"; exit 1; }

if ! podman compose version >/dev/null 2>&1; then
  err "plugin compose absent pour podman"
  err "Debian/Ubuntu : sudo apt install podman-compose"
  err "puis lancez : podman-compose version"
  exit 1
fi
ok "podman $(podman --version | awk '{print $3}') + compose disponibles"

# --------------------------------------------------------------------- secrets
if [[ ! -f .env ]]; then
  cp .env.example .env
  SECRET=$(openssl rand -hex 32 2>/dev/null || head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n')
  PW=$(head -c 16 /dev/urandom | od -An -tx1 | tr -d ' \n')
  sed -i "s|^FLEET_SECRET_KEY=.*|FLEET_SECRET_KEY=${SECRET}|" .env
  sed -i "s|^WAZUH_INDEXER_PASSWORD=.*|WAZUH_INDEXER_PASSWORD=${PW}-indexer|" .env
  sed -i "s|^WAZUH_DASHBOARD_PASSWORD=.*|WAZUH_DASHBOARD_PASSWORD=${PW}-dashboard|" .env
  sed -i "s|^IPA_ADMIN_PASSWORD=.*|IPA_ADMIN_PASSWORD=${PW}-ipa-admin|" .env
  sed -i "s|^IPA_DS_PASSWORD=.*|IPA_DS_PASSWORD=${PW}-ipa-ds|" .env
  ok ".env cree avec des secrets generes (mot de passe Wazuh : ${PW}-dashboard)"
else
  ok ".env present"
fi

# ------------------------------------------------------------------ construction
info "Construction de l'image fleet-app"
"${COMPOSE[@]}" "${PROFILES[@]}" build fleet-app
ok "image construite"

# ---------------------------------------------------------------------- demarrage
info "Demarrage des services"
"${COMPOSE[@]}" "${PROFILES[@]}" up -d
ok "conteneurs lances"

info "Attente de l'indexer (demarrage froid : 1 a 3 minutes)"
for i in $(seq 1 60); do
  if podman exec pfa-wazuh-indexer curl -sk \
      -u "${WAZUH_INDEXER_USER:-admin}:$(grep '^WAZUH_INDEXER_PASSWORD=' .env | cut -d= -f2-)" \
      https://localhost:9200/_cluster/health 2>/dev/null | grep -qE '"status":"(green|yellow)"'; then
    ok "indexer pret (${i}0 s)"
    break
  fi
  [[ $i -eq 60 ]] && { err "indexer non pret apres 10 min — voir : ${COMPOSE[*]} logs wazuh-indexer"; exit 1; }
  printf "."
  sleep 10
done

# ------------------------------------------------- configuration Wazuh du labo
info "Injection de la configuration de supervision"
if ./scripts/configure-wazuh.sh; then
  ok "configuration Wazuh injectee"
else
  err "la configuration Wazuh n a pas ete injectee — stack demarree mais sans les regles du projet"
  err "relancez manuellement : ./scripts/configure-wazuh.sh"
fi

echo
"${GRAS}Laboratoire operationnel.${FIN}"
echo
printf "  Wazuh dashboard  http://localhost:5601\n"
printf "  Fleet-app        http://localhost:5000/login\n"
printf "  Indexer          https://localhost:9200 (interne)\n"
if [[ " ${PROFILES[*]} " == *" freeipa "* ]]; then
  printf "  FreeIPA          https://localhost/ipa/\n"
else
  printf "  FreeIPA          non demarre (option --freeipa)\n"
fi
echo
printf "  Identifiants Wazuh : admin / %s\n" "$(grep '^WAZUH_DASHBOARD_PASSWORD=' .env | cut -d= -f2-)"
printf "  Identifiants app   : agent1 / motdepasseagent (jeu de donnees de demonstration)\n"
echo
printf "  Verifier :  ./scripts/verify.sh\n"
printf "  Arreter  :  ./scripts/down.sh\n"
