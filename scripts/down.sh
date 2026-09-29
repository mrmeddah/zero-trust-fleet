#!/usr/bin/env bash
# Arret du laboratoire.
#
#   ./scripts/down.sh          -> arrete, conserve les volumes
#   ./scripts/down.sh --purge  -> arrete et supprime les volumes (données Wazuh,
#                                  base fleet-app, certificats)
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
RACINE="$PWD"

if [[ "${1:-}" == "--purge" ]]; then
  echo "==> Arret et suppression des volumes"
  podman compose --profile freeipa down -v --remove-orphans
  echo "[ok] volumes supprimes : index des alertes, base fleet-app, certificats"
else
  echo "==> Arret (volumes conserves)"
  podman compose --profile freeipa stop
  echo "[ok] arrete. Pour repartir : ./scripts/up.sh"
  echo "     Pour tout effacer : ./scripts/down.sh --purge"
fi
