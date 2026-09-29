# GUIDE D'IMPLEMENTATION

Projet PFA — Commune d'El Kelaâ des Sraghna
**Architecture Zero Trust hybride pour la gestion du parc et du carburant**
Filière IIR — Option CIR / EMSI
Stagiaire : Mohamed Meddah — Encadrants : M. Ioounousse, M. Mourad Boukri

Ce document est le **guide pas-à-pas unique** qui permet de rendre la solution
fonctionnelle, exactement telle qu'elle est décrite dans le rapport (`latex/`). Chaque
phase est alignée sur un chapitre du rapport, fournit les commandes prêtes à copier-coller,
les fichiers de configuration complets, les résultats attendus, les vérifications et les
captures d'écran à réaliser pour illustrer les figures.

> **Hyperviseur.** Le rapport comme l'environnement d'exécution de ce PFA utilisent
> **KVM/QEMU + libvirt**. Aucune commande, aucune adresse,
> aucune configuration ni capture du rapport ne change.

---

## Lecture rapide (sommaire)

- [Phase 0 — Préalables et décisions](#phase-0-préalables-et-decisions)
- [Phase 1 — Préparation du laboratoire KVM](#phase-1-préparation-du-laboratoire-kvm)
- [Phase 2 — VM 1 : pfSense (pare-feu, routeur inter-VLAN, Suricata IPS)](#phase-2-vm-1--pfsense)
- [Phase 3 — VM 2 : FreeIPA (annuaire, PKI, Kerberos)](#phase-3-vm-2--freeipa)
- [Phase 4 — Tunnel WireGuard + VM cloud (application Flask + mTLS + Wazuh)](#phase-4-tunnel-wireguard--vm-cloud)
- [Phase 5 — Red team : Kali Linux, 3 scénarios](#phase-5-red-team--kali-linux)
- [Phase 6 — Vérifications, métriques, captures et synthèse](#phase-6-vérifications-métriques-captures-et-synthèse)
- [Annexe — Répertoire des captures du rapport](#annexe--répertoire-des-captures-du-rapport)

---

## Tableau d'adressage de référence (tiré du rapport, tb:ch3-adressage & tb:ch4-flux)

| Élément | Réseau / adresse | Rôle |
|---|---|---|
| WAN pfSense | `en0 (default)` | Internet de sortie (réseau hôte) — WAN de pfSense |
| VLAN 10 — Administration | `10.10.10.0/24` — gw `10.10.10.1` | FreeIPA `10.10.10.10`, gestion |
| VLAN 20 — Flotte | `10.10.20.0/24` — gw `10.10.20.1` | Simulateurs véhicules `10.10.20.50`, clients de l'application |
| VLAN 30 — Services | `10.10.30.0/24` — gw `10.10.30.1` | Services internes, DNS |
| VLAN 99 — Tunnel | `10.99.0.0/30` — gw `10.99.0.1` | Tunnel WireGuard (`10.99.0.1` pfSense ↔ `10.99.0.2` VM cloud) |
| VM cloud « Azure » | tunnel `10.99.0.2`, app `10.99.0.2:5000`, Wazuh `10.99.0.2:443` | Application Flask mTLS + Wazuh |
| Tunnel WireGuard | UDP `51820` | pfSense ↔ VM Azure, annexe B |
| FreeIPA domaine | `municipal.local` | Annuaire + CA + Kerberos, au niveau `ipa.municipal.local` |

---

## Phase 0 — Préalables et décisions

Récapitulatif des choix actés avec l'étudiant (voir plan validé) :

1. **Hyperviseur** : KVM/QEMU + libvirt (✓ opérationnel, état vérifié ci-dessous).
2. **Cloud** : pas de compte Azure disponible → la solution est **simulée localement**
   par une VM « Azure » sur un réseau de tunnel isolé, avec la même configuration WireGuard
   (annexe B). Une section dédiée (fin du guide) explique la bascule vers un vrai compte
   Azure : seules les adresses changent, aucun fichier de configuration ne bouge.
3. **Livrable** : un document unique (celui-ci), complet et exécutable.

### Vérification de l'environnement d'exécution

Ouvrir un terminal et exécuter :

```bash
# droits libvirt (appartenance aux groupes libvirt et qemu)
groups
# vérifier l'accès à l'hyperviseur sans mot de passe
virsh -c qemu:///system list --all
virsh -c qemu:///system pool-list
virsh -c qemu:///system net-list --all
ls -l /dev/kvm /dev/tun /dev/vhost-net
```

Résultats attendus sur cette machine (constatés le 18/09/2026) :

- groupes `libvirt` et `qemu` présents pour l'utilisateur `med` ;
- pools `boot`, `default`, `Downloads` actifs ;
- réseau `default` actif ; VM `Debian13` présente (éteinte) ;
- `virt-install` disponible dans le PATH ;
- espace disque disponible : **185 G** (suffisant pour 4 VM).

> **Note :** les commandes qui modifient l'hyperviseur (création de pools, de réseaux, de
> VM) nécessitent les droits `libvirt` — disponibles sans `sudo` sur cette machine. Les
> téléchargements d'ISO se font dans `~/.cache` ou dans `/home/med/Downloads` (pool
> `Downloads` déjà défini et accessible en écriture pour l'utilisateur).

---

## Phase 1 — Préparation du laboratoire KVM

### 1.1 Téléchargement des ISO

Les ISO sont stockés dans le pool `Downloads` (chemin `/home/med/Downloads`), donc dans une
zone accessible en écriture par l'utilisateur, puis rendus disponibles à l'installateur via
le pool `boot`.

| VM | Système | Fichier | Source officielle |
|---|---|---|---|
| pfSense | pfSense CE 2.7.0 amd64 | `pfSense-CE-2.7.0-RELEASE-amd64.iso.gz` | https://atxfiles.netgate.com/mirror/downloads/ |
| FreeIPA | Rocky Linux 9 x86_64 minimal | `Rocky-9.6-x86_64-minimal.iso` | https://download.rockylinux.org/pub/rocky/ |
| VM cloud | Ubuntu Server 22.04 LTS amd64 | `ubuntu-22.04.5-live-server-amd64.iso` | https://releases.ubuntu.com/22.04/ |
| Red team | Kali Linux (live amd64) | `kali-linux-2026.1-live-amd64.iso` | https://cdimage.kali.org/ |

```bash
mkdir -p /home/med/Downloads/iso && cd /home/med/Downloads/iso

# pfSense CE 2.7.0
wget -c https://atxfiles.netgate.com/mirror/downloads/pfSense-CE-2.7.0-RELEASE-amd64.iso.gz

# Rocky Linux 9 Minimal (base FreeIPA)
wget -c https://download.rockylinux.org/pub/rocky/9/isos/x86_64/Rocky-9.6-x86_64-minimal.iso

# Ubuntu 22.04 Server (VM cloud / Wazuh / application)
wget -c https://releases.ubuntu.com/22.04/ubuntu-22.04.5-live-server-amd64.iso

# Kali Linux live (red team)
wget -c https://cdimage.kali.org/kali-2026.1/kali-linux-2026.1-live-amd64.iso
```

> Les volumes sont importants (2–4 G par image) : lancer ces téléchargements en parallèle
> (`-c` reprend les téléchargements interrompus). Une fois téléchargés, les décompresser
> (pfSense) et les copier dans `/var/lib/libvirt/boot` (pool `boot`).

```bash
cd /home/med/Downloads/iso
gunzip -k pfSense-CE-2.7.0-RELEASE-amd64.iso.gz
# copie dans le pool boot (ou définir un nouveau pool de stockage sur ~/Downloads/iso)
sudo cp pfSense-CE-2.7.0-RELEASE-amd64.iso Rocky-9.6-x86_64-minimal.iso \
        ubuntu-22.04.5-live-server-amd64.iso kali-linux-2026.1-live-amd64.iso \
        /var/lib/libvirt/boot/
```

**Vérification :** `virsh -c qemu:///system vol-list boot` doit lister les quatre ISO.

### 1.2 Réseaux virtuels

Créer les trois réseaux libvirt conformes au plan (tb:ch3-adressage) :

| Réseau libvirt | Rôle | Adressage | Bridge |
|---|---|---|---|
| `wan-net` | Internet simulé — WAN de pfSense | 172.16.200.0/24 — DHCP | `virbr-wan` |
| `lan-trunk` | Trunk inter-VLAN (VLAN 10/20/30/99) | 10.10.0.0/16 — sans IP d'hôte | `virbr-lan` |
| `cloud-net` | Zone « Azure » isolée (app + Wazuh) | 10.99.0.0/30 | `virbr-cloud` |

Fichier `wan-net.xml` :

```xml
<network>
  <name>wan-net</name>
  <forward mode='nat'>
    <nat><port start='1024' end='65535'/></nat>
  </forward>
  <bridge name='virbr-wan' stp='on' delay='0'/>
  <ip address='172.16.200.1' netmask='255.255.255.0'>
    <dhcp><range start='172.16.200.10' end='172.16.200.200'/></dhcp>
  </ip>
</network>
```

Fichier `lan-trunk.xml` :

```xml
<network>
  <name>lan-trunk</name>
  <forward mode='bridge'/>
  <bridge name='virbr-lan' stp='on' delay='0'/>
</network>
```

Fichier `cloud-net.xml` :

```xml
<network>
  <name>cloud-net</name>
  <forward mode='bridge'/>
  <bridge name='virbr-cloud' stp='on' delay='0'/>
</network>
```

Import et démarrage :

```bash
for net in wan-net lan-trunk cloud-net; do
  virsh -c qemu:///system net-define ${net}.xml
  virsh -c qemu:///system net-start $net
  virsh -c qemu:///system net-autostart $net
done
virsh -c qemu:///system net-list --all
```

> **Note sur tronçon « Azure ».** Le réseau `cloud-net` est un bridge sans NAT : il
> matérialise le côté « cloud » du tunnel. La VM « Azure » y est raccordée et n'atteint le
> reste que via l'extrémité WireGuard.

### 1.3 Création des VM avec `virt-install`

PFADRESSE — schéma des VM (cohérent avec tb:ch3-vms du rapport) :

| VM | vCPU | RAM | Disque | Réseaux |
|---|---|---|---|---|
| `pfSense` | 1 | 1024 M | 8 G (3 interfaces) | wan-net (WAN), lan-trunk (LAN trunk) |
| `freeipa` | 2 | 2048 M | 20 G | lan-trunk (VLAN 10, via pfSense. Il sera branché sur le trunk) |
| `vm-azure` | 2 | 4096 M | 20 G | cloud-net ; wan-net (pour accès Internet d'installation, retiré ensuite) |
| `kali` | 2 | 3072 M | 30 G | wan-net |

```bash
# pfSense
sudo virt-install \
  --name pfSense \
  --vcpus 1 --memory 1024 \
  --disk path=/var/lib/libvirt/images/pfSense.qcow2,size=8,format=qcow2 \
  --os-variant freebsd12.2 \
  --network network=wan-net,model=virtio \
  --network network=lan-trunk,model=virtio \
  --network network=cloud-net,model=virtio \
  --cdrom /var/lib/libvirt/boot/pfSense-CE-2.7.0-RELEASE-amd64.iso \
  --noautoconsole
```

> **Composition des interfaces pfSense dans KVM.** La segmentation VLAN réside dans
> pfSense lui-même (il crée les VLAN 10/20/30/99 sur son interface LAN trunk) : le rapport
> l'expique au ch. IV avec l'interface `vtnet1` connectée au trunk. KVM fournit des réseaux
> séparés comme solution équivalente : on relie pfSense à `lan-trunk` (une seule carte
> « trunk ») puis le routage inter-VLAN est fait par les règles pfSense avec la même matrice
> de flux.

```bash
# FreeIPA (Rocky 9) — branché sur le trunk ; son IP 10.10.10.10 est posée à l'installation
sudo virt-install \
  --name freeipa \
  --vcpus 2 --memory 2048 \
  --disk path=/var/lib/libvirt/images/freeipa.qcow2,size=20,format=qcow2 \
  --os-variant rocky9 \
  --network network=lan-trunk,model=virtio \
  --network network=wan-net,model=virtio \
  --cdrom /var/lib/libvirt/boot/Rocky-9.6-x86_64-minimal.iso \
  --noautoconsole

# VM cloud « Azure » (Ubuntu Server + WireGuard + Flask + Wazuh)
sudo virt-install \
  --name vm-azure \
  --vcpus 2 --memory 4096 \
  --disk path=/var/lib/libvirt/images/vm-azure.qcow2,size=20,format=qcow2 \
  --os-variant ubuntu22.04 \
  --network network=cloud-net,model=virtio \
  --network network=wan-net,model=virtio \
  --cdrom /var/lib/libvirt/boot/ubuntu-22.04.5-live-server-amd64.iso \
  --noautoconsole

# Kali (red team)
sudo virt-install \
  --name kali \
  --vcpus 2 --memory 3072 \
  --disk path=/var/lib/libvirt/images/kali.qcow2,size=30,format=qcow2 \
  --os-variant debian12 \
  --network network=wan-net,model=virtio \
  --cdrom /var/lib/libvirt/boot/kali-linux-2026.1-live-amd64.iso \
  --noautoconsole
```

**Vérification `virsh -c qemu:///system list --all`** : les 4 VM + `Debian13`.

---

## Phase 2 — VM 1 : pfSense

> Chapitre IV, § « Module infrastructure et segmentation ». Pare-feu, routeur inter-VLAN,
> **deny by default**, Suricata en mode IPS. Adresses : VLAN 10 `10.10.10.0/24`,
> VLAN 20 `10.10.20.0/24`, VLAN 30 `10.10.30.0/24`, VLAN 99 `10.99.0.0/30`.

### 2.1 Installation

1. Démarrer `pfSense` (console spiced/serial : démarrer l'installeur, choisir **Install**).
2. Choisir le clavier et le type de partitionnement (défaut ZFS/USB ou UFS simple).
3. Configurer l'utilisateur `admin` et le mot de passe.

### 2.2 Interfaces et VLAN

Après reboot, l'assistant de pfSense demande d'affecter les interfaces :

```
Should VLANs be set up now?  y
pri : vtnet0  (WAN — wan-net)
LAN : vtnet1  (LAN — lan-trunk)
```

Créer ensuite dans l'interface web (**Interfaces ▸ Assignments ▸ VLANs**) les VLAN
suivants sur l'interface LAN, puis leur **Assignments** (OPT1..OPT4) :

| VLAN | Nom | Interface virtuelle | Adresse | Passerelle |
|---|---|---|---|---|
| 10 | Administration | `vlan10` | 10.10.10.1/24 | 10.10.10.1 |
| 20 | Flotte | `vlan20` | 10.10.20.1/24 | 10.10.20.1 |
| 30 | Services | `vlan30` | 10.10.30.1/24 | 10.10.30.1 |
| 99 | Tunnel | `vlan99` | 10.99.0.1/30 | 10.99.0.1 |

**Résultat attendu / capture fig:ch4-pf-interfaces** : la page
**Interfaces ▸ Assignments** avec les interfaces WAN, LAN et les 4 interfaces VLAN
virtuelles et leurs adresses IP.

### 2.3 Règles pare-feu — politique « deny by default »

Conformément à tb:ch4-flux, aucune règle inter-VLAN n'existe par défaut. On ajoute
explicitement (Firewall ▸ Rules, GILF VLAN 10 / 20 / 30) :

| VLAN source | Destination | Service | Action |
|---|---|---|---|
| 10 | 99 | tout | pass (supervision, admin) |
| 20 | 99 :5000 | TCP 5000 | pass (accès application carburant) |
| 30 | 99 :443 | TCP 443 | pass (console Wazuh) |
| 30 | (DNS) | TCP/UDP 53 | pass (résolution) |
| tout autre inter-VLAN | — | — | **deny (défaut)** |

**Capture fig:ch4-pf-rules** : liste des règles des VLAN montrant l'ordre et l'action.

### 2.4 Suricata (IPS)

1. **System ▸ Package Manager** ▸ installer **Suricata** et **pfBlockerNG** (optionnel).
2. **Services ▸ Suricata ▸ Global Settings** : activer IPS ; **Interfaces** : activer
   Suricata sur `vlan10`, `vlan20`, `vlan30`, `vlan99` (mode IPS/inline).
3. Mettre à jour les règles (ET Open).

**Capture fig:ch4-suricata** : page Suricata montrant le mode IPS et l'état `running`.

### 2.5 Journalisation vers Wazuh

- **Status ▸ System Logs ▸ Settings** ▸ *Remote Logging Options* :
  `Enable remote logging` → serveur syslog = `10.99.0.2:514` (la VM cloud).
- Toujours dans pfSense : DHCP (VLAN 10 only), règles de flux → Syslog.
- **Capture fig:ch4-pf-logging** : écran des paramètres de journalisation distant.

---

## Phase 3 — VM 2 : FreeIPA

> Chapitre IV, § « Module identité et PKI ». Annuaire + Kerberos + PKI (CA interne),
> domaine `municipal.local`, mTLS. IP : `10.10.10.10`.

### 3.1 Installation Rocky + configuration réseau

À l'installation de Rocky : nom d'hôte `ipa.municipal.local`, réseau statique
`10.10.10.10/24`, passerelle `10.10.10.1`, DNS `1.1.1.1`.

### 3.2 Installation FreeIPA

```bash
sudo hostnamectl set-hostname ipa.municipal.local
# synchronisation NTP + résolution locale
sudo dnf -y install ipa-server ipa-server-dns
sudo ipa-server-install \
  --realm MUNICIPAL.LOCAL \
  --domain municipal.local \
  --ds-password "$IPA_DS_PASSWORD" \
  --admin-password "$IPA_ADMIN_PASSWORD" \
  --setup-dns --auto-forwarders --no-ntp
sudo systemctl enable --now ipa
kinit admin
```

### 3.3 PKI et certificats (mTLS)

FreeIPA embarque une CA. Émettre les certificats :

- **serveurs** : `fleet-app.municipal.local` (Flask), `wazuh.municipal.local`,
  `pfsense.municipal.local`, `ipa.municipal.local` ;
- **clients** : un certificat par utilisateur/groupe (authentification mutuelle).

```bash
# Émission pour l'application (exemple)
ipa cert-request --principal=HTTP/fleet-app.municipal.local
# Vérification des certificats émis
ipa cert-show --id=<ID> --output=/tmp/cert.pem
```

**Captures** : fig:ch4-freeipa-user (page utilisateur + onglet certificats) et
fig:ch4-freeipa-ca (gestion des certificats de la CA).

### 3.4 Comptes, groupes et rôles par acteur

Reprendre les acteurs du cas UML (ch. II) : groupes `admins`, `gestionnaires`, `agents`,
`direction`, `auditeurs`.

```bash
for g in admins gestionnaires agents direction auditeurs; do
  ipa group-add "$g"
done
ipa user-add agent1 --first=A --last=Agent --mail=agent1@municipal.local --random
ipa group-add-member agents --users=agent1
```

---

## Phase 4 — Tunnel WireGuard + VM cloud

> Chapitre IV, § « Tunnel hybride sécurisé » (annexe B). WireGuard :
> pfSense `10.99.0.1` ↔ VM Azure `10.99.0.2`, UDP 51820.

### 4.1 Côté pfSense (interface wg99)

Installer le paquet **WireGuard** (System ▸ Package Manager), puis dans
**VPN ▸ WireGuard** :

- **Tunnels ▸ Add** : `Description = wg99`, `Listen Port = 51820`, `Addresses =
  10.99.0.1/30` (server) — générer les clés ;
- **Peers ▸ Add** : `Public Key = <clé_VM_cloud>`, `Allowed IPs = 10.99.0.2/32`,
  Endpoint = `<adresse_publique_vm_cloud>:51820`, `Persistent Keepalive = 25`.

Vérification sur pfSense : **Diagnostics ▸ WireGuard** — statut « up », bytes transférés.

### 4.2 Côté VM cloud (wg0) — annexe B

```bash
# /etc/wireguard/wg0.conf (VM Azure) — annexe B
[Interface]
PrivateKey = <cle_privee_vm_cloud>
Address    = 10.99.0.2/30

[Peer]
PublicKey  = <cle_publique_pfsense>
AllowedIPs = 10.10.0.0/16   # restriction : uniquement le réseau local de la commune
Endpoint   = <adresse_publique_pfsense>:51820
PersistentKeepalive = 25
```

```bash
sudo apt -y install wireguard
sudo systemctl enable --now wg-quick@wg0
sudo wg show
ping -c 3 10.99.0.1            # pfSense joignable via le tunnel
```

**Vérification croisée :** depuis pfSense, `ping 10.99.0.2` répond ; les routes sont en
place (tb:ch4-wg). **Capture fig:ch4-wg-state** : état du tunnel (statut actif, clés,
octets) sur pfSense.

### 4.3 Application Flask « Parc & Carburant » (mTLS)

Sur la VM cloud (`/opt/fleet-app`) :

```bash
mkdir -p /opt/fleet-app && cd /opt/fleet-app
python3 -m venv venv && source venv/bin/activate
pip install flask flask-sqlalchemy requests gunicorn pyOpenSSL
```

Application `app.py` — configuration Flask avec authentification mTLS
(dossier `/etc/fleet-app/certs`, certificats émis par FreeIPA) :

```python
from flask import Flask, request
import ssl, os

app = Flask(__name__)
CERTS = "/etc/fleet-app/certs"

# mTLS : le serveur exige le certificat client émis par la CA FreeIPA
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_verify_locations(cafile=os.path.join(CERTS, "ipa-ca.crt"))
context.verify_mode = ssl.CERT_REQUIRED              # pas de cert client = refus
context.load_cert_chain(os.path.join(CERTS, "server.crt"),
                        os.path.join(CERTS, "server.key"))

@app.route("/login")
def login():
    # identité libre du certificat client (subject CN)
    return "mTLS OK — CN = %s" % request.environ.get("SSL_CLIENT_S_DN", "inconnu")

if __name__ == "__main__":
    certfile = os.path.join(CERTS, "server.crt")
    keyfile = os.path.join(CERTS, "server.key")
    app.run(host="0.0.0.0", port=5000,
            ssl_context=(certfile, keyfile), debug=False)
```

Lancer et tester l'absence d'accès sans certificat :

```bash
cd /opt/fleet-app && source venv/bin/activate
gunicorn -w 2 -b 0.0.0.0:5000 app:app &
curl -k https://10.99.0.2:5000/login        # ÉCHEC : TLS handshake refusé (pas de cert client)
curl -k --cert client.crt --key client.key https://10.99.0.2:5000/login   # OK : mTLS validé
```

> **Captures rel. figures app (ch. IV / annexe D « captures de l'application »)** :
> page de connexion (mentions mTLS), tableau de bord du parc, bon de carburant, rapport de
> consommation. Ce sont les figures `fig:ch4-app-*`.

### 4.4 Wazuh (SIEM/XDR) sur la VM cloud

```bash
# Ubuntu : paquets + installation officielle monocase (indexer+manager+dashboard)
curl -sO https://packages.wazuh.com/4.9/wazuh-install.sh
sudo bash wazuh-install.sh -a
# noter le mot de passe administrateur affiché en fin d'install
```

Sources de journaux (tb:ch4-logs, référence « 4/5 sources » du rapport) :

| Source | Protocole/transport | Journal |
|---|---|---|
| pfSense | syslog UDP 514 → 10.99.0.2:514 | rejets pare-feu, loopback |
| FreeIPA | syslog UDP 514 | tentatives d'authentification, émissions de certs |
| Application Flask | journaux d'application (agent Wazuh) | accès `.5000`, échecs |
| WireGuard | journaux système | connexions/déconnexions du tunnel |
| VM cloud (système) | agent Wazuh | connexions SSH, auth |

### 4.5 Règles personnalisées Wazuh (annexe A — 100001 à 100003)

Rédiger le fichier `/var/ossec/etc/rules/local_rules.xml` (extrait :

```xml
<group name="application,carburant,">
  <!-- 100001 : accès hors horaires de service -->
  <rule id="100001" level="10">
    <if_group>web</if_group>
    <time>18:00 - 07:00</time>
    <description>Accès à l'application hors horaires de service</description>
  </rule>

  <!-- 100002 : force brute (5 échecs / 60 s, même source) -->
  <rule id="100002" level="12" frequency="5" timeframe="60">
    <if_matched_group>authentication_failed</if_matched_group>
    <same_source_ip/>
    <description>Tentative de force brute contre l'application</description>
  </rule>

  <!-- 100003 : mouvement latéral VLAN 20 -> VLAN 10 -->
  <rule id="100003" level="14">
    <if_group>firewall</if_group>
    <action>block</action>
    <srcip>10.10.20.0/24</srcip>
    <dstip>10.10.10.0/24</dstip>
    <description>Mouvement latéral VLAN Flotte vers VLAN Administration — bloqué</description>
  </rule>
</group>
```

Recharger : `sudo /var/ossec/bin/wazuh-control restart` puis vérifier dans la console
(Wazuh ▸ Rules : 100001/100002/100003 présentes).

**Captures Wazuh du rapport** : fig:ch4-wazuh-rules (liste des 3 règles), dashboard
fig:ch4-wazuh-dash (alertes par sévérité, compteurs).

---

## Phase 5 — Red team : Kali Linux

> Chapitre IV, § « Évaluation — scénarios d'attaque ». Les 3 scénarios du chapitre :
> force brute (1), accès direct cloud (2), mouvement latéral (3).

```bash
# Depuis Kali : outils utilisés
which hydra nmap curl
```

### Scénario 1 — Force brute sur l'application (via tunnel)

```bash
# Cible : application de l'application de gestion (10.99.0.2:5000) via le tunnel
# Obs. : à travers le tunnel, la cible est 10.99.0.2 ; le rapport visait
# l'adresse publique de la VM. Les deux convergent vers la même application.
hydra -t 4 -l agent1 -P /usr/share/wordlists/rockyou.txt \
  10.99.0.2 -s 5000 http-ssl-post-form \
  "/login:user=^USER^&pass=^PASS^:erreur"
```

**Résultat attendu.** Après 5 échecs consécutifs en 60 s depuis la même source, Wazuh
émet l'**alerte 100002 (niveau 12)**. La console (outil d'analyse « Security events »)
l'affiche. **Capture fig:ch4-sc1-alert** (tb:ch4-sc1).

### Scénario 2 — Accès direct à la VM cloud (contournement du tunnel)

Depuis Kali, scanner la surface d'accès de la VM cloud comme si on visait l'exposition
publique :

```bash
nmap -sT -Pn -p 5000,443,22,51820 <addr_public_vm_cloud>
```

**Résultat attendu.** Seul `51820/udp` est ouvert (tunnel) ; 5000/443/22 sont
**`filtered`** (NSG/pare-feu fermés par défaut) — tb:ch4-sc2. **Capture fig:ch4-sc2-nmap**.

> **Simulation locale :** sur la VM `vm-azure`, fermer 5000/443 vis-à-vis de toute source
> autre que `10.99.0.0/30` (UFW) et bloquer `22` publiquement ; confirmer un lieu
> uniquement `51820/udp`.

### Scénario 3 — Mouvement latéral VLAN Flotte → VLAN Administration

Depuis un poste du VLAN 20 (`10.10.20.50`) compromis :

```bash
ping 10.10.10.10            # FreeIPA — attente : sans réponse (bloqué)
nmap -Pn 10.10.10.10        # ports : aucun ouvert depuis VLAN 20
curl -k https://10.10.10.10 # échec
```

**Résultat attendu.** Chaque tentative est **refusée** par le pare-feu (règle pfSense,
deny inter-VLAN 20→10) ; cette action `block` alimente Wazuh qui déclenche la
**règle 100003 (niveau 14)** — mouvement latéral. **Capture fig:ch4-sc3-alert**
(tb:ch4-sc3).

---

## Phase 6 — Vérifications, métriques, captures et synthèse

### 6.1 Métriques de qualité et de performance (tb:ch4-qualite / tb:ch4-perf)

Après la mise en place, relever (à partir de la console Wazuh et des journaux pfSense) :

- taux de détection : alertes émises par scénario ;
- temps de corrélation (déclenchement après les 5 échecs Hydra) ;
- nombre d'alertes fausses positives ;
- latence du tunnel WireGuard (ping 10.99.0.2, `ping -M do`) ;
- débit mesuré (test simple avec `iperf3` sur 10.99.0.0/30 si installé).

### 6.2 Correspondance besoins ↔ réalisations (tb:ch4-correspondance)

Reprendre le modèle d'évaluation final du ch. IV : cocher chaque besoin fonctionnel
ch. II (annuaire, mTLS, segmentation, deny-by-default, tunnel, supervision, collecte).
Remplir le tableau récapitulatif du rapport (dans le chapitre 4).

### 6.3 Synthèse des tests (tb:ch4-synthese)

| Scénario | Alerte | Niveau | Résultat |
|---|---|---|---|
| 1 — force brute | 100002 | 12 | Détectée |
| 2 — accès direct cloud | — | — | Bloquée (ports filtered) |
| 3 — mouvement latéral | 100003 | 14 | Bloquée + détectée |

### 6.4 Images à produire pour le rapport

La production des 13 schémas (12 UML ch. II + topologie ch. III) est **déjà réalisée**
(PNG 300 dpi, palette EMSI, dans `latex/figures/`). Les captures d'écran de la
réalisation (figures `fig:ch4-*`) sont les écrans listés dans l'annexe ci-dessous —
prendre les captures au fil des étapes précédentes aux emplacements indiqués.

---

## Bascule vers un vrai compte Azure

Lorsque l'accès à un abonnement Azure sera disponible, la **VM cloud simulée est
remplacée par une VM Azure réelle** (ex. B2s, Ubuntu 22.04) avec :

1. **NSG (Network Security Group)** autorisant **uniquement `UDP 51820`** depuis
   Internet, tout le reste refusé (tb:ch4-sc2, NSG comme « firewall cloud ») ;
2. **WireGuard identique** : `wg0` = `10.99.0.2/30`, Endpoint = adresse publique pfSense
   (annexe B) — **aucun changement** de configuration WireGuard ;
3. **UFW** sur la VM : `ubuntu ufw default deny incoming ; ufw allow 51820/udp ; ufw enable` ;
4. **Wazuh + application Flask** déjà déployés: seules les adresses IP publiques changent.

**Le reste de ce guide (phases 2–6) reste valable à l'identique.** Seul le maillage réseau
hôte diffère : remplacer `cloud-net` par le réseau Azure et ajuster l'adresse publique
dans l'`Endpoint` WireGuard.

---

## Annexe — Répertoire des captures du rapport

| Figure | Contenu | Réalisée à la phase |
|---|---|---|
| fig:ch4-pf-install | accueil/installateur pfSense | 2.1 |
| fig:ch4-pf-interfaces | Interfaces ▸ Assignments (VLAN 10/20/30/99) | 2.2 |
| fig:ch4-pf-rules | Firewall ▸ Rules, matrice | 2.3 |
| fig:ch4-suricata | Suricata IPS « running » | 2.4 |
| fig:ch4-pf-logging | syslog → Wazuh | 2.5 |
| fig:ch4-freeipa-user | page utilisateur FreeIPA + certificat | 3.4 |
| fig:ch4-freeipa-ca | certificats de la CA FreeIPA | 3.3 |
| fig:ch4-app-login | connexion application (mTLS) | 4.3 |
| fig:ch4-app-dashboard | tableau de bord du parc | 4.3 |
| fig:ch4-app-bon | bon de carburant | 4.3 |
| fig:ch4-app-rapport | rapport de consommation | 4.3 |
| fig:ch4-wg-state | état tunnel WireGuard | 4.1/4.2 |
| fig:ch4-wazuh-rules | règles 100001–100003 | 4.5 |
| fig:ch4-wazuh-dash | tableau de bord Wazuh | 4.4 |
| fig:ch4-sc1-alert | alerte force brute (100002) | 5.1 |
| fig:ch4-sc2-nmap | nmap → ports filtered, 51820 open | 5.2 |
| fig:ch4-sc3-alert | alerte mouvement latéral (100003) | 5.3 |

> **Conformité avec le rapport.** Vérifier que chaque capture insérée correspond bien à
> l'emplacement `\placeholder` cité dans le `.tex` du rapport (aucun modification des
> fichiers `.tex` n'est nécessaire).
