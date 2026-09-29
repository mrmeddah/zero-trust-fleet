# Runbook de soutenance — 3 minutes, sans narration

État : chaîne Wazuh + application **vérifiée en direct**. FreeIPA / pfSense / Kali
restent à débloquer (voir « Blocages » en fin de document).

---

## 0. Avant de filmer (5 min de préparation)

Sur la VM Azure :

```bash
ssh azurevm@172.16.200.195          # mot de passe : root
sudo systemctl restart wazuh-manager filebeat wazuh-dashboard
```

Vérifications rapides :

```bash
sudo systemctl is-active wazuh-manager wazuh-indexer filebeat wazuh-dashboard
# attendu : active x4

sudo filebeat test output -c /etc/filebeat/filebeat.yml
# attendu : talk to server... OK

sudo tail -3 /var/ossec/logs/alerts/alerts.log
```

Onglets de navigateur à ouvrir **avant** l'enregistrement :

| Onglet | URL | Notes |
|---|---|---|
| Dashboard Wazuh | `https://172.16.200.195` | onglet principal, ne pas rafraîchir pendant le plan 2 |
| Application | `http://172.16.200.195:5000` |.agent1 / motde passeagent |
| Wazuh — règles | `https://172.16.200.195/app/rules` | filtrer `100000` / `100002` |

> Certificat Wazuh auto-signé : accepter l'avertissement une seule fois, puis
> l'onglet reste vert pour toute la soutenance.

---

## 1. Plan 0 — Architecture (0:00 → 0:30)

**Légende :** `Hyperviseur KVM/QEMU — 4 machines virtuelles — réseau virtualisé par ponts`

Afficher, sans zoom ni mouvement de souris :

- Kali `172.16.200.59`
- VM Azure / Wazuh `172.16.200.195` + WireGuard `10.99.0.2`
- FreeIPA `10.10.10.10`
- pfSense `10.10.10.1` (LAN) / `172.16.200.10` (WAN)

**⚠ Ne pas affirmationner la segmentation VLAN à l'écran tant qu'elle n'est pas
réellement configurée** (voir Blocages). Montrer le schéma, pas une capture truquée.

---

## 2. Plan 1 — Contrôles d'accès (0:30 → 1:00)

**Légende :** `FreeIPA — annuaire central — MFA activé`

Captures d'écran réelles disponibles dans `latex_exemple/figures/` :

- `fig-ch4-freeipa-user.png` — utilisateur de l'annuaire
- `fig-ch4-freeipa-ca.png` — autorité de certification
- `fig-ch4-pf-rules.png` — règles de pare-feu

---

## 3. Plan 2 — L'application et son journalisation (1:00 → 1:30)

Onglet **Application** (`http://172.16.200.195:5000`).

1. Montrer la page de connexion (1 s).
2. Se connecter en `agent1` → le tableau de bord s'affiche.
3. Ouvrir l'onglet Wazuh **Règles** filtré sur `100000` et `100002`.

**Légende :** `LeSIEM reçoit les événements applicatifs via syslog — règle 100000 : échec d'authentification`

---

## 4. Plan 3 — La démonstration de sécurité (1:30 → 2:40) ★ cœur de la soutenance

C'est la partie **réellement vivante**. La faire en direct, pas en capture.

### 4.1 Attaque depuis l'hôte (source distante réelle)

Dans un terminal, **6 requêtes d'échec** depuis `172.16.200.1` :

```bash
for i in 1 2 3 4 5 6; do
  curl -s -o /dev/null \
    -d "identifiant=agent1&mot_de_passe=WRONG$i" \
    http://172.16.200.195:5000/login
  sleep 1
done
```

Attendre ~30 s que Filebeat expédie vers l'indexeur (afficher une barre de
progression, ou couper sur l'onglet Wazuh).

### 4.2 Bascule sur le Dashboard Wazuh

Onglet Dashboard → **Security events**.

**Légende 1 :** `Cinq échecs d'authentification — règle 100000, niveau 5`

**Légende 2 :** `Agrégation temporelle — règle 100002, niveau 12 : tentative de force brute`

Cliquer sur l'alerte `100002` pour afficher le détail :

```
full_log : AUTHFAIL user=agent1 src=172.16.200.1 path=/login
```

**Légende :** `L'adresse IP de l'attaquant est conservée dans l'événement`

### 4.3 Ce que la.rule démontre réellement

| Capacité SIEM | Preuve |
|---|---|
| Collecte des logs applicatifs | `AUTHFAIL` émis par Flask, reçu par Wazuh |
| Détection unitaire | règle `100000`, niveau 5 |
| Corrélation temporelle | règle `100002` : 5 échecs / 60 s → niveau 12 |
| Traçabilité de l'attaquant | `src=172.16.200.1` |
| Pipeline complet | app → syslog:514 → wazuh-remoted → analysisd → Filebeat → indexeur → dashboard |

---

## 5. Plan 4 — Détection réseau (2:40 → 3:00)

Onglet Wazuh → **MITRE ATT&CK**, puis filtre sur la règle `87701` (drop firewall
pfSense) si une trace existe.

**Légende :** `Le pare-feu PfSense est intégré comme agent — les drops sont remontés au SIEM`

Si aucune trace `87701` n'est disponible : **ne pasClaims d'alert réseau en direct**,
utiliser `fig-ch4-pf-rules.png` et le dire honnêtement à l'oral.

---

## 6. Blocages à résoudre avant de pouvoir tout montrer en direct

Trois éléments du plan ne sont **pas encore démontrables en direct** et exigent
un accès `sudo` sur l'hôte (mot de passe non fourni à ce stade) :

| Élément | Problème | Action requise sur l'hôte |
|---|---|---|
| **FreeIPA** | `10.10.10.10` ne répond pas ; `virbr-lan` n'a pas d'adresse hôte | `sudo ip addr add 10.10.10.100/24 dev virbr-lan && sudo ip link set virbr-lan up` |
| **pfSense** | `172.16.200.10:443` fermé (règle WAN) ; GUI en `10.10.10.1` injoignable | même commande, puis vérifier le VLAN côté pfSense |
| **Kali** | aucun port ouvert, pas de SSH | démarrer `libvirtd` / ouvrir une console VM, ou exposer SSH |

Ces trois points utilisent les segments `virbr-lan` / `virbr-cloud` qui sont
attachés aux VM (vnet3, vnet6) mais sans adresse IP côté hôte — d'où l'absence de
réponse. La segmentation VLAN 10/20/30/99 annoncée dans le rapport n'est pas
encore appliquée au niveau des ponts (tout est en VLAN 1 non taggé) : il s'agit
d'un écart à corriger ou à expliciter clairement.

---

## 7. Aides à la démonstration

- **Si le dashboard ne rafraîchit pas** : c'est normal, Wazuh indexe par lots.
  Attendre 30 s, puis `Ctrl+R`. Ne pas paniquer devant le jury.
- **Si on vous demande le mot de passe Wazuh** : `admin` / `${WAZUH_INDEXER_PASSWORD}`.
- **Si on vous demande pourquoi `src` n'est pas une colonne du tableau** : le
  message applicatif est au format texte ; l'IP est dans `full_log`, ce qui est
  suffisant pour la traçabilité. (Un passage en JSON n'a pas été retenu car le
  décodeur Wazuh par défaut ne l'extrait pas et cela aurait risqué la chaîne
  fonctionnelle.)
- **Mode dégradé sans `sudo` hôte** : présenter le plan 0 (schéma), le plan 2
  (application) et le plan 3 (démonstration SIEM en direct, qui fonctionne
  parfaitement), puis utiliser les captures FreeIPA/pfSense du rapport pour les
  plans 1 et 4. Le cœur de la démonstration — la corrélation SIEM en direct —
  reste entièrement crédible.
