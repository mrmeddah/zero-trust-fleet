# Zero Trust Network Architecture for Municipal Fleet Operations
**Projet de Fin d'Année (PFA) — Cybersecurity Engineering**
**Student:** Mohamed Meddah | EMSI Marrakech | 2026–2027

---

## 1. Project Summary

Design and implementation of a Zero Trust Network Architecture (ZTNA) applied to a municipal fleet and fuel management environment. The project simulates a realistic hybrid on-prem/cloud topology, enforces identity-based access control, and demonstrates active threat detection against fleet-specific attack scenarios.

No implicit trust is granted to any user, device, or service — everything must authenticate, every connection is inspected.

---

## 2. Problem Statement

Municipal fleet and fuel management systems are critical operational infrastructure yet typically run on flat, legacy networks with weak access control and no detection capability. Fuel fraud, insider threats, and unauthorized access are known risks in this environment.

Traditional perimeter-based security (firewall at the edge, trusted inside) is insufficient. This project proposes a Zero Trust redesign that is budget-realistic for a municipality: open-source stack, hybrid topology, no dependency on expensive managed cloud services.

---

## 3. Objectives

- Design a segmented network architecture enforcing Zero Trust principles
- Deploy an internal PKI and directory service to own the full trust chain
- Simulate a hybrid topology connecting on-prem infrastructure to a cloud workload via encrypted tunnel
- Implement active threat detection with custom detection rules targeting fleet-specific scenarios
- Demonstrate the architecture against three realistic attack scenarios

---

## 4. Architecture Overview

### 4.1 Topology

```
┌─────────────────────────────────────────────────────────┐
│                        ATTACKER                          │
│                   (Host Machine / Kali)                  │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│              LOCAL VM 1 — pfSense Firewall               │
│  - VLAN segmentation (Admin / Fleet / Services)          │
│  - Intrusion prevention (Suricata)                       │
│  - WireGuard VPN tunnel to Azure                         │
│  - NAT, traffic logging                                  │
└────────────┬──────────────────────────┬──────────────────┘
             │                          │ WireGuard tunnel
┌────────────▼────────────┐  ┌─────────▼──────────────────┐
│  LOCAL VM 2 — FreeIPA   │  │   AZURE VM — Fleet + SIEM   │
│  - LDAP directory        │  │  - Fuel management web app  │
│  - Kerberos (AuthN)      │  │  - Wazuh SIEM/XDR           │
│  - Internal CA (PKI)     │  │  - Log aggregation          │
│  - Cert issuance (mTLS)  │  │  - Custom detection rules   │
│  - DNS                   │  │  - Wazuh dashboard          │
└─────────────────────────┘  └─────────────────────────────┘
```

### 4.2 Network Segmentation

| VLAN | Name | Subnet | Contains |
|------|------|--------|----------|
| 10 | Admin | 10.10.10.0/24 | Management interfaces, FreeIPA |
| 20 | Fleet | 10.10.20.0/24 | Simulated fleet devices, fuel app clients |
| 30 | Services | 10.10.30.0/24 | Internal services, DNS |
| 99 | Tunnel | 10.99.0.0/30 | WireGuard point-to-point to Azure |

Inter-VLAN traffic is denied by default. Explicit allow rules only.

### 4.3 Hybrid Component Rationale

| Component | Location | Rationale |
|-----------|----------|-----------|
| Identity / PKI | On-prem (FreeIPA) | Municipalities do not externalize directory services |
| Firewall / Segmentation | On-prem (pfSense) | Full control over trust boundaries |
| Fleet App / SIEM | Azure Student VM | Represents cloud-hosted operational workload |
| Tunnel | WireGuard | Lightweight, auditable, no managed cloud networking required |

---

## 5. Technical Stack

| Role | Technology | Notes |
|------|------------|-------|
| Hypervisor | KVM/QEMU | Host machine, 3 VMs max |
| Firewall | pfSense + Suricata | VLAN routing, IPS, VPN |
| Directory + PKI | FreeIPA | LDAP, Kerberos, internal CA |
| SIEM / XDR | Wazuh | Log ingestion, detection rules, dashboards |
| Fleet App | Python Flask (custom) | Simulates fuel management system |
| VPN Tunnel | WireGuard | On-prem to Azure encrypted channel |
| Cloud Compute | Azure Student VM (Ubuntu) | Hosts fleet app + Wazuh |
| Attacker | Kali Linux (host or WSL) | Red team scenarios |

All software is open-source. Zero licensing cost.

---

## 6. VM Specifications

### VM 1 — pfSense Firewall
- **OS**: pfSense CE 2.7+
- **RAM**: 1 GB
- **vCPUs**: 1
- **NICs**: 3 (WAN, LAN trunk, WireGuard)
- **Role**: Perimeter firewall, VLAN router, IPS, VPN endpoint

### VM 2 — FreeIPA (Identity + PKI)
- **OS**: Rocky Linux 9 or AlmaLinux 9
- **RAM**: 2 GB
- **vCPUs**: 2
- **Role**: LDAP, Kerberos, DNS, internal CA, cert issuance

### Azure Student VM — Fleet App + SIEM
- **OS**: Ubuntu 22.04 LTS
- **Size**: B2s (2 vCPUs, 4 GB RAM) — within student credit
- **Role**: Wazuh server, Flask fleet app, log aggregation
- **Access**: WireGuard tunnel only — no public port exposure except WireGuard UDP

---

## 7. Network Addressing

### Local
| Host | VLAN | IP |
|------|------|----|
| pfSense LAN | - | 10.10.10.1 (gateway) |
| FreeIPA | VLAN 10 | 10.10.10.10 |
| Simulated fleet client (host) | VLAN 20 | 10.10.20.50 |
| WireGuard local endpoint | VLAN 99 | 10.99.0.1 |

### Azure
| Host | IP |
|------|----|
| Azure VM (public) | Dynamic — locked to WireGuard only |
| WireGuard Azure endpoint | 10.99.0.2 |
| Fleet app (internal) | 10.99.0.2:5000 |
| Wazuh dashboard (internal) | 10.99.0.2:443 |

---

## 8. PKI Design

```
Root CA (FreeIPA)
└── Intermediate CA (FreeIPA)
    ├── fleet-app.municipal.local       (Flask app TLS)
    ├── wazuh.municipal.local           (Wazuh dashboard TLS)
    ├── pfsense.municipal.local         (pfSense management TLS)
    └── client certs (issued per user)  (mTLS for app access)
```

All services use certificates issued by the internal CA. No self-signed certs. Client certificate required to access the fleet application — no cert, no access.

---

## 9. Detection Engineering

### 9.1 Wazuh Custom Rules (Fleet-Specific)

**Rule 1 — After-hours fleet app access**
```xml
<rule id="100001" level="10">
  <if_group>web</if_group>
  <time>18:00 - 07:00</time>
  <url>/fuel|/fleet</url>
  <description>Fleet app accessed outside business hours</description>
</rule>
```

**Rule 2 — Repeated failed authentication (brute force)**
```xml
<rule id="100002" level="12" frequency="5" timeframe="60">
  <if_matched_group>authentication_failed</if_matched_group>
  <same_source_ip/>
  <description>Brute force attempt against fleet application</description>
</rule>
```

**Rule 3 — Inter-VLAN lateral movement attempt**
```xml
<rule id="100003" level="14">
  <if_group>firewall</if_group>
  <action>block</action>
  <srcip>10.10.20.0/24</srcip>
  <dstip>10.10.10.0/24</dstip>
  <description>Fleet VLAN attempting access to Admin VLAN — blocked</description>
</rule>
```

### 9.2 Log Sources Feeding Wazuh

- pfSense firewall logs (via syslog → Wazuh)
- FreeIPA authentication logs
- Flask app access/error logs
- WireGuard tunnel events
- System auth logs (Azure VM)

---

## 10. Attack Scenarios & Expected Outcomes

### Scenario 1 — Brute Force Against Fleet App

**Setup**: Attacker (host machine) targets Flask fuel management app over WireGuard tunnel.

**Steps**:
1. Run `hydra` or `ffuf` against the login endpoint
2. Wazuh rule 100002 triggers after 5 failed attempts in 60 seconds
3. Alert fires on Wazuh dashboard with source IP, timestamp, targeted endpoint

**Expected result**: Alert at level 12, attacker IP logged, optional pfSense block rule triggered via active response.

---

### Scenario 2 — Direct Azure VM Access Attempt (Bypassing Tunnel)

**Setup**: Attacker attempts to reach Azure VM directly via its public IP, bypassing WireGuard.

**Steps**:
1. `nmap` scan against Azure VM public IP
2. Azure NSG + UFW rules drop all inbound except WireGuard UDP port
3. No response — all ports filtered

**Expected result**: Zero attack surface exposed. Demo shows nmap returning all-filtered vs. full access through tunnel. Architecture point made visually.

---

### Scenario 3 — Lateral Movement from Fleet VLAN to Admin VLAN

**Setup**: Attacker compromises a simulated fleet device (host machine on VLAN 20), attempts to reach FreeIPA on VLAN 10.

**Steps**:
1. From VLAN 20 host, attempt `ping` / `nmap` / `curl` toward 10.10.10.10
2. pfSense inter-VLAN rule denies traffic
3. pfSense logs the attempt → Wazuh ingests → rule 100003 fires

**Expected result**: Traffic blocked at firewall, alert on Wazuh dashboard, zero reachability to identity infrastructure.

---

## 11. Deliverables

| Deliverable | Description |
|-------------|-------------|
| Architecture document | Full network design with diagrams, design decisions, threat model |
| PKI documentation | CA hierarchy, cert issuance process, mTLS configuration |
| Detection rule set | Custom Wazuh rules with justification per rule |
| Attack/defense report | Results of 3 scenarios with screenshots and log evidence |
| Source code | Flask fleet app, Wazuh rule files, pfSense config export, WireGuard configs |
| Live demo | Working environment with scenario walkthroughs |

---

## 12. Project Phases

| Phase | Duration | Tasks |
|-------|----------|-------|
| 1 — Design | 2 weeks | Architecture design, IP plan, threat model, component selection |
| 2 — Infrastructure | 3 weeks | pfSense setup, VLANs, FreeIPA deploy, PKI, WireGuard tunnel |
| 3 — Application + SIEM | 2 weeks | Flask app deploy, Wazuh install, log source integration |
| 4 — Detection Engineering | 2 weeks | Custom rule development, log parsing, dashboard setup |
| 5 — Red Team Scenarios | 1 week | Execute 3 scenarios, capture evidence, document results |
| 6 — Report + Defense Prep | 2 weeks | Final report, architecture diagrams, presentation |

**Total: ~12 weeks**

---

## 13. Frameworks Referenced

- **NIST SP 800-207** — Zero Trust Architecture
- **NIST SP 800-53** — Security and Privacy Controls
- **ISO/IEC 27001:2022** — Information Security Management
- **MITRE ATT&CK** — Threat scenario mapping (lateral movement, brute force, discovery)

---

## 14. Why This Project

- Directly derived from real PFA internship context (municipal fleet/fuel department)
- Demonstrates a full security stack: network, identity, PKI, detection
- Hybrid topology adds architectural depth without managed cloud dependency
- All attack scenarios are mapped to real municipal threat vectors
- Fully reproducible on 3 VMs + one Azure student instance
- Open-source stack — zero cost, zero licensing barrier

---

*Mohamed Meddah — mohamed@meddah.systems — meddah.systems*
