#!/usr/bin/env bash
# Regles et chaines de log du projet, injectees dans le manager Wazuh.
# Invoque par up.sh ; peut aussi etre relance seul apres un redemarrage.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
set -a; [[ -f .env ]] && . ./.env; set +a

MANAGER=pfa-wazuh-manager
[[ -z "$(podman ps -q -f name=$MANAGER 2>/dev/null)" ]] && {
  echo "  manager absent : lancez d'abord ./scripts/up.sh" >&2; exit 1; }

# --- 1. Les sources autorisees a emettre vers l'indexer ---------------------
podman exec "$MANAGER" python3 - <<'PYEOF'
import re, pathlib
p = pathlib.Path("/var/ossec/etc/ossec.conf")
s = p.read_text()
want = ["<allowed-ips>172.16.200.0/24</allowed-ips>",
        "<allowed-ips>127.0.0.1/32</allowed-ips>"]
# supprime toute ancienne declaration, puis reecrit une section propre
s = re.sub(r"[ \t]*<allowed-ips>.*?</allowed-ips>\s*", "", s, flags=re.S)
block = ("  <remote>\n" + "".join("    %s\n" % w for w in want) + "  </remote>\n")
s = re.sub(r"  <remote>.*?</remote>\n", block, s, flags=re.S)
p.write_text(s)
print("  allowed-ips :", " ".join(want))
PYEOF

# --- 2. Regles de correlation du projet --------------------------------------
podman exec -i "$MANAGER" sh -c 'cat > /var/ossec/etc/rules/local_rules.xml' <<'RULEEOF'
<group name="fleet,local,">

  <!-- 100000 : evenement applicatif d'echec d'authentification -->
  <rule id="100000" level="5">
    <if_sid>87701</if_sid>
    <match>^AUTHFAIL</match>
    <description>Fleet-app : echec d'authentification</description>
    <group>auth_failed,web,fleet-app,</group>
  </rule>

  <!-- 100002 : correlation - 5 echecs en moins de 60 secondes.
       Pas de <same_source_ip/> : l'emetteur syslog local est vu par
       wazuh-remended avec l'adresse de la boucle, il faut donc correler
       sur le champ user. -->
  <rule id="100002" level="10">
    <if_matched_group>auth_failed</if_matched_group>
    <if_matched_sid>100000</if_matched_sid>
    <frequency>5</frequency>
    <timeframe>60</timeframe>
    <same_field>user</same_field>
    <description>Fleet-app : 5 echecs d'authentification en moins de 60 s</description>
    <group>authentication_failures,poc,</group>
  </rule>

</group>
RULEEOF
echo "  regles 100000 et 100002 injectees"

# --- 3. Chaine Filebeat : indexer en direct, aucune configuration par defaut --
podman exec "$MANAGER" sh -c '
  set -e
  cp /var/ossec/etc/filebeat/filebeat.yml /var/ossec/etc/filebeat/filebeat.yml.bak
  sed -i "s|^hosts:.*|hosts: [\"https://wazuh.indexer:9200\"]|;
          s|^username:.*|username: \"'"${WAZUH_INDEXER_USER:-admin}"'\"|;
          s|^password:.*|password: \"'"${WAZUH_INDEXER_PASSWORD}"'\"|;
          s|^ssl.verification_mode:.*|ssl.verification_mode: \"'"${FILEBEAT_SSL_VERIFICATION_MODE:-none}"'\"|" \
      /var/ossec/etc/filebeat/filebeat.yml
  filebeat test config && filebeat test output
'
echo "  filebeat valide"

# --- 4. Redemarrage ----------------------------------------------------------
podman exec "$MANAGER" /var/ossec/bin/wazuh-control restart
sleep 10
podman exec "$MANAGER" /var/ossec/bin/wazuh-control status
