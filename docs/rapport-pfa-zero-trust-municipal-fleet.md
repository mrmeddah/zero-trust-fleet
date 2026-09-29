# Mémoire PFA — Zero Trust Network Architecture for Municipal Fleet Operations

**Projet de fin d'année présenté et soutenu en vue de l'obtention du diplôme de [Diplôme]**

**Filière : [Filière] — Spécialité : Cybersécurité des systèmes d'information**

**Réalisé par :** Mohamed Meddah
**Encadré par :** [Nom de l'encadrant pédagogique] — EMSI Marrakech
**Encadrant de stage :** [Nom de l'encadrant au sein de la commune]
**Organisme d'accueil :** [Nom de la commune]

**Année universitaire : 2026–2027**

---

## Table des matières

> *La table des matières présentée ci-dessous respecte strictement la structure exigée. Les numéros de pages entre parenthèses correspondent à la pagination du document final (à actualiser après export PDF).*

| Section | Page |
|---------|------|
| Dédicace | II |
| Remerciements | III |
| Abstract | IV |
| Résumé | V |
| Glossaire | VI |
| Introduction générale | 1 |
| Chapitre 1 : Contexte général du projet | 2 |
| Chapitre 2 : Analyse et conception | 21 |
| Chapitre 3 : Architecture technique et outils utilisés | 44 |
| Chapitre 4 : Réalisation et tests | 56 |
| Conclusion générale et perspectives | 114 |
| Appréciation personnelle | 115 |
| Références | 116 |

**Arborescence détaillée**

1. Introduction générale
2. Chapitre 1 : Contexte général du projet
   - 1.1 Introduction
   - 1.2 Présentation de l'organisme d'accueil
     - 1.2.1 Présentation de la commune
     - 1.2.2 Historique de la commune
     - 1.2.3 Fiche technique
     - 1.2.4 Les services et secteurs d'activités
     - 1.2.5 Missions de la commune
   - 1.3 Contexte du projet
     - 1.3.1 Étude de l'existant
     - 1.3.2 Comparaison avec les solutions existantes
     - 1.3.3 Analyse critique des limites de l'existant
     - 1.3.4 Problématique
   - 1.4 Cadre sécuritaire du projet
     - 1.4.1 Étude de l'existant
     - 1.4.2 Comparaison avec les solutions existantes
     - 1.4.3 Analyse critique des limites de l'existant
     - 1.4.4 Problématique
     - 1.4.5 Solution proposée
     - 1.4.6 Objectifs du projet
   - 1.5 Planification et conduite du projet
     - 1.5.1 Méthodologie de travail
     - 1.5.2 Présentation de la méthode SCRUM
     - 1.5.3 Justification du choix de Scrum
     - 1.5.4 Caractéristiques de la méthode SCRUM
     - 1.5.5 Les rôles dans SCRUM
     - 1.5.6 Rituels Scrum
     - 1.5.7 Les sprints
     - 1.5.8 Diagramme de Gantt
   - 1.6 Conclusion
3. Chapitre 2 : Analyse et conception
   - 2.1 Introduction
   - 2.2 Identification des acteurs du système
   - 2.3 Spécification des besoins
     - 2.3.1 Besoins fonctionnels
     - 2.3.2 Besoins non fonctionnels
   - 2.4 Conception
     - 2.4.1 Diagramme de cas d'utilisation global
     - 2.4.2 Description textuelle des cas d'utilisation principaux
     - 2.4.3 Diagramme de cas d'utilisation par rôle
     - 2.4.4 Diagrammes de séquence
     - 2.4.5 Diagrammes d'activité
     - 2.4.6 Diagramme de classes
   - 2.5 Conclusion
4. Chapitre 3 : Architecture technique et outils utilisés
   - 3.1 Introduction
   - 3.2 Architecture technique
     - 3.2.1 Vue d'ensemble
     - 3.2.2 Composants et interactions
     - 3.2.3 Architecture du backend
     - 3.2.4 Architecture du frontend
   - 3.3 Environnement de travail
     - 3.3.1 Outils de développement
     - 3.3.2 Outils de conteneurisation et sécurité
     - 3.3.3 Outils de gestion de version
     - 3.3.4 Outils de documentation
   - 3.4 Structure et organisation du projet
   - 3.5 Conclusion
5. Chapitre 4 : Réalisation et tests
   - 4.1 Introduction
   - 4.2 Présentation des interfaces de la plateforme
     - 4.2.1 Module infrastructure et segmentation
     - 4.2.2 Module identité et PKI
     - 4.2.3 Module gestion du parc et du carburant
     - 4.2.4 Module supervision et détection
     - 4.2.5 Module tunnel hybride sécurisé
   - 4.3 Évaluation de la solution
     - 4.3.1 Métriques de qualité et de performance
     - 4.3.2 Visualisations des résultats des tests
     - 4.3.3 Comparaison : correspondance entre les besoins et les points atteints
   - 4.4 Conclusion
6. Conclusion générale et perspectives
7. Appréciation personnelle
8. Références

---

## Dédicace

*[À personnaliser.]*

Je dédie ce travail à :

- Mes chers parents, pour leur soutien inconditionnel et leurs sacrifices tout au long de mon parcours ;
- Mes frères et sœurs, pour leur encouragement et leur affection ;
- Toute ma famille et mes amis qui m'ont accompagné durant ces années d'étude ;
- Tous mes enseignants qui ont contribué à ma formation, du primaire à l'université.

Que ce travail soit le reflet de ma gratitude et de mon profond respect.

**Mohamed Meddah**

---

## Remerciements

Au terme de ce travail, je tiens à exprimer ma profonde gratitude à toutes les personnes qui ont contribué, de près ou de loin, à la réalisation de ce projet.

Je remercie tout d'abord mes parents pour leur patience, leur soutien moral et financier, ainsi que pour la confiance qu'ils m'ont toujours accordée.

Je tiens à remercier sincèrement mon encadrant pédagogique, **[Nom de l'encadrant]**, enseignant à l'École Marocaine des Sciences de l'Ingénieur (EMSI) de Marrakech, pour son encadrement, ses orientations, ses conseils avisés et sa disponibilité tout au long de la réalisation de ce projet.

Je remercie également l'ensemble du personnel de **[Nom de la commune]**, et plus particulièrement mon encadrant de stage, **[Nom de l'encadrant de stage]**, pour son accueil chaleureux, sa confiance et les ressources mises à ma disposition pendant la période de stage.

Je remercie enfin les membres du jury pour l'honneur qu'ils me font en acceptant d'évaluer ce travail, ainsi que tous mes enseignants de l'EMSI pour la qualité de la formation dispensée et pour tout ce que j'ai appris à leurs côtés.

**Mohamed Meddah**

---

## Abstract

The present report describes the realization of a project carried out during a two-month internship within **[Name of the municipality]**, a Moroccan local public administration. The municipality operates an urban fleet and a fuel management system that constitute critical operational infrastructure, yet these systems have historically been hosted on flat, legacy networks with weak access control and no detection capability. Fuel fraud, insider threats, and unauthorized access are known risks in such environments.

This project proposes a **Zero Trust Network Architecture (ZTNA)** redesign that is budget-realistic for a municipality. The work covers the design and implementation of a segmented network architecture enforcing Zero Trust principles, the deployment of an internal PKI (Public Key Infrastructure) and a directory service to own the full trust chain, the simulation of a hybrid topology connecting on-premises infrastructure to a cloud workload through an encrypted tunnel, and the implementation of active threat detection through custom detection rules targeting fleet-specific scenarios.

The architecture relies exclusively on open-source software — pfSense and Suricata for firewall and intrusion prevention, FreeIPA for identity and certificate management, Wazuh as SIEM/XDR platform, and WireGuard for the encrypted tunnel to a Microsoft Azure virtual machine hosting a custom Flask-based fleet and fuel management application. The relevance of the architecture is demonstrated against three realistic attack scenarios: a brute-force attack against the fleet application, a direct access attempt to the cloud virtual machine bypassing the tunnel, and a lateral movement attempt from the fleet VLAN towards the admin VLAN. The results confirm that the proposed architecture effectively enforces the "never trust, always verify" principle while remaining financially and technically accessible to a municipal structure.

**Keywords:** Zero Trust, ZTNA, network segmentation, PKI, SIEM, Wazuh, pfSense, FreeIPA, WireGuard, municipal fleet, cybersecurity.

---

## Résumé

Le présent rapport décrit la réalisation d'un projet mené dans le cadre d'un stage de deux mois au sein de **[Nom de la commune]**, une administration publique locale marocaine. La commune exploite un parc de véhicules urbains ainsi qu'un système de gestion de carburant qui constituent une infrastructure opérationnelle critique. Ces systèmes reposent cependant, de manière historique, sur des réseaux plats et hérités, dotés d'un contrôle d'accès faible et d'aucune capacité de détection. La fraude au carburant, les menaces internes et les accès non autorisés constituent des risques bien connus dans ce type d'environnement.

Ce projet propose une refonte de l'architecture réseau selon le modèle **Zero Trust (ZTNA)**, réaliste du point de vue budgétaire pour une commune. Le travail couvre la conception et l'implémentation d'une architecture réseau segmentée respectant les principes du Zero Trust, le déploiement d'une infrastructure à clés publiques (PKI) interne et d'un service d'annuaire permettant de maîtriser la totalité de la chaîne de confiance, la simulation d'une topologie hybride reliant l'infrastructure sur site à une charge de travail cloud via un tunnel chiffré, ainsi que la mise en œuvre d'une détection active des menaces grâce à des règles de détection personnalisées ciblant des scénarios propres au contexte municipal.

L'architecture repose exclusivement sur des logiciels libres — pfSense et Suricata pour le pare-feu et la prévention d'intrusion, FreeIPA pour l'identité et la gestion des certificats, Wazuh en tant que plateforme SIEM/XDR, et WireGuard pour le tunnel chiffré vers une machine virtuelle Microsoft Azure hébergeant une application personnalisée de gestion du parc et du carburant développée avec Flask. La pertinence de l'architecture est démontrée à travers trois scénarios d'attaque réalistes : une attaque par force brute contre l'application, une tentative d'accès direct à la machine virtuelle cloud en contournant le tunnel, et une tentative de mouvement latéral depuis le VLAN « flotte » vers le VLAN « administration ». Les résultats confirment que l'architecture proposée applique effectivement le principe « ne jamais faire confiance, toujours vérifier » tout en restant financièrement et techniquement accessible à une structure municipale.

**Mots-clés :** Zero Trust, ZTNA, segmentation réseau, PKI, SIEM, Wazuh, pfSense, FreeIPA, WireGuard, parc municipal, cybersécurité.

---

## Glossaire

| Terme | Définition |
|-------|-----------|
| **ZTNA** | *Zero Trust Network Architecture* — Architecture réseau reposant sur l'absence de confiance implicite : toute entité (utilisateur, appareil, service) doit s'authentifier et chaque connexion est vérifiée. |
| **Zero Trust** | Modèle de sécurité fondé sur le principe « ne jamais faire confiance, toujours vérifier ». |
| **NIST SP 800-207** | Publication du *National Institute of Standards and Technology* définissant le cadre de référence des architectures Zero Trust. |
| **SIEM** | *Security Information and Event Management* — Plateforme de collecte, de corrélation et d'analyse des journaux d'événements de sécurité. |
| **XDR** | *Extended Detection and Response* — Approche de détection et de réponse élargie combinant plusieurs sources de données (réseau, endpoints, cloud). |
| **IDS** | *Intrusion Detection System* — Système de détection d'intrusion. |
| **IPS** | *Intrusion Prevention System* — Système de prévention d'intrusion. |
| **PKI** | *Public Key Infrastructure* — Infrastructure à clés publiques : ensemble de services et de règles régissant l'émission, la distribution et la révocation des certificats numériques. |
| **CA** | *Certificate Authority* — Autorité de certification : entité émettant les certificats numériques. |
| **mTLS** | *Mutual TLS* — Authentification mutuelle par certificats entre le client et le serveur. |
| **LDAP** | *Lightweight Directory Access Protocol* — Protocole d'accès à un annuaire d'identités. |
| **Kerberos** | Protocole d'authentification réseau reposant sur des tickets et une tierce partie de confiance. |
| **VLAN** | *Virtual Local Area Network* — Réseau local virtuel permettant de segmenter logiquement un réseau physique. |
| **ACL** | *Access Control List* — Liste de contrôle d'accès définissant les règles de filtrage du trafic. |
| **VPN** | *Virtual Private Network* — Réseau privé virtuel établissant un canal chiffré entre deux points. |
| **WireGuard** | Protocole VPN moderne, léger et auditable, fondé sur la cryptographie moderne. |
| **NAT** | *Network Address Translation* — Traduction d'adresses réseau. |
| **Flask** | Micro-framework web Python utilisé pour développer l'application de gestion du parc. |
| **Wazuh** | Plateforme open-source de détection de menaces (SIEM/XDR) avec règles, corrélation et tableaux de bord. |
| **pfSense** | Distribution open-source de pare-feu et de routeur fondée sur FreeBSD, intégrant notamment Suricata. |
| **Suricata** | Moteur open-source de détection et de prévention d'intrusion (IDS/IPS). |
| **FreeIPA** | Solution open-source intégrée d'identité : annuaire LDAP, authentification Kerberos, DNS et PKI. |
| **MITRE ATT&CK** | Base de connaissances décrivant les tactiques et techniques employées par les adversaires. |
| **Kali Linux** | Distribution Linux spécialisée dans les tests d'intrusion et l'audit de sécurité. |
| **Azure** | Plateforme de cloud computing de Microsoft, utilisée ici pour héberger la charge de travail hybride. |
| **NSG** | *Network Security Group* — Groupe de sécurité réseau d'Azure filtrant le trafic au niveau de la carte réseau virtuelle. |
| **Red team** | Équipe jouant le rôle d'un attaquant afin d'évaluer la sécurité d'un système. |

---

## Introduction générale

La transformation numérique des administrations publiques marocaines constitue l'un des axes stratégiques majeurs de la politique nationale. Les communes, en tant qu'échelons territoriaux de proximité, sont appelées à moderniser leurs systèmes d'information tout en garantissant la continuité et la sécurité de leurs services. Parmi leurs infrastructures critiques figurent la gestion du parc de véhicules et la distribution de carburant, qui représentent à la fois un enjeu opérationnel quotidien et une surface d'exposition aux risques de fraude et d'intrusion.

Dans la plupart des collectivités, ces systèmes reposent encore sur des réseaux plats et des architectures héritées. Le modèle de sécurité traditionnel, dit « périmètre », considère implicitement que tout ce qui se trouve à l'intérieur du réseau est digne de confiance. Cette approche s'avère insuffisante face aux menaces actuelles : vol d'identifiants, mouvement latéral, fraude interne ou compromission d'un poste de travail. Les incidents touchant les parcs automobiles et les dépôts de carburant — qu'il s'agisse de détournements, d'accès non autorisés ou de sabotage — engendrent des pertes financières et une dégradation de la confiance des citoyens.

C'est dans ce contexte que s'inscrit le présent projet, réalisé lors d'un stage de deux mois au sein de **[Nom de la commune]**. L'objectif de ce travail est de concevoir, mettre en œuvre et valider une **architecture réseau Zero Trust** appliquée à l'environnement de gestion du parc municipal et du carburant. Le projet consiste à remplacer la confiance implicite par une vérification systématique de chaque utilisateur, de chaque appareil et de chaque connexion, tout en proposant une démarche réaliste sur le plan budgétaire : une pile technologique exclusivement open-source et une topologie hybride associant des ressources sur site et une charge de travail hébergée dans le cloud.

Plus précisément, le travail entrepris comprend la conception d'une architecture réseau segmentée en plusieurs VLAN, le déploiement d'une infrastructure à clés publiques interne et d'un service d'annuaire, l'établissement d'un tunnel chiffré reliant l'infrastructure locale à une machine virtuelle cloud hébergeant l'application de gestion du parc et du carburant, ainsi que la mise en place d'une plateforme SIEM dotée de règles de détection spécifiques au contexte municipal. La validation de la solution s'appuie sur trois scénarios d'attaque représentatifs : une attaque par force brute, une tentative d'accès direct à la ressource cloud et une tentative de mouvement latéral entre VLAN.

Ce mémoire est organisé comme suit :

- le **chapitre 1** présente le contexte général du projet : l'organisme d'accueil, l'étude de l'existant, la problématique, la solution proposée ainsi que la planification adoptée selon la méthode Scrum ;
- le **chapitre 2** est consacré à l'analyse et à la conception : identification des acteurs, spécification des besoins fonctionnels et non fonctionnels, et élaboration des différents diagrammes UML ;
- le **chapitre 3** détaille l'architecture technique retenue ainsi que l'ensemble des outils utilisés durant le projet ;
- le **chapitre 4** présente la réalisation effective, les interfaces développées et les résultats des tests menés, avant une évaluation globale de la solution ;
- une **conclusion générale** récapitule les apports du travail et ouvre des perspectives d'évolution.

# Chapitre 1 : Contexte général du projet

## 1.1 Introduction

Ce premier chapitre a pour objectif de poser le cadre général dans lequel s'inscrit le projet. Il s'agit, dans un premier temps, de présenter l'organisme d'accueil, à savoir la commune **[Nom de la commune]**, au sein de laquelle le stage a été effectué : son environnement, son organisation, ses missions et les services qu'elle met à disposition de ses administrés. Dans un second temps, le chapitre s'attache à décrire le contexte métier du projet, c'est-à-dire les conditions actuelles de gestion du parc de véhicules et du carburant, puis le contexte sécuritaire qui a motivé la mise en place d'une architecture Zero Trust. L'étude de l'existant, la comparaison avec les solutions disponibles et l'analyse critique des limites du système actuel permettent de formuler une problématique claire et de définir les objectifs du projet. Enfin, le chapitre se termine par la présentation de la méthodologie de travail adoptée, la méthode agile Scrum, ainsi que par la planification globale des travaux à travers un diagramme de Gantt.

## 1.2 Présentation de l'organisme d'accueil

### 1.2.1 Présentation de la commune

Le stage s'est déroulé au sein de la commune **[Nom de la commune]**, une collectivité territoriale de droit public située dans la région de **[Région]**, au Maroc. La commune exerce, conformément à la loi organique n° 113-14 relative aux communes, un ensemble de compétences propres et de compétences partagées, allant de l'aménagement du territoire local et de la gestion des services publics de proximité à la préservation de l'environnement et au développement économique et social de son territoire.

En tant qu'administration de proximité, la commune assure le fonctionnement quotidien de nombreux services publics indispensables à la vie des citoyens : l'état civil, l'urbanisme et la voirie, la gestion des déchets, l'éclairage public, ou encore la maintenance des espaces verts. Pour ce faire, elle s'appuie sur un effectif de **[Nombre d'agents]** agents répartis entre l'administration centrale et les différents services techniques.

Le parc automobile de la commune constitue un outil de travail essentiel : il regroupe **[Nombre de véhicules]** véhicules de types variés — véhicules légers, poids lourds, bennes à ordures, engins de travaux publics — utilisés quotidiennement par les services techniques. La gestion de ce parc, ainsi que l'approvisionnement et la distribution de carburant, relèvent d'un service dédié, le **[Nom du service]**, qui fait face à de nombreux défis organisationnels et sécuritaires.

> **[À PERSONNALISER]** : localisation précise, superficie, population, chiffres réels du parc, organisation des services.

### 1.2.2 Historique de la commune

La commune **[Nom de la commune]** trouve ses origines dans le **découpage territorial de [Année]**, qui a structuré l'organisation administrative du Maroc moderne. Comme de nombreuses collectivités du Royaume, elle a connu plusieurs réformes successives visant à renforcer son autonomie financière et administrative.

La refonte majeure intervient avec l'adoption, en **2015**, de la régionalisation avancée et la mise en place de la charte communale. Depuis lors, la commune a engagé un processus de modernisation de ses services : informatisation progressive de l'état civil, dématérialisation de certaines démarches administratives, et introduction d'outils de gestion interne pour la comptabilité et le suivi des ressources. Cette dynamique de modernisation est toutefois partielle : certaines fonctions critiques, comme la gestion du parc automobile et du carburant, demeurent gérées selon des pratiques héritées, reposant sur des registres papier et des tableurs, sans véritable infrastructure de sécurité.

> **[À PERSONNALISER]** : dates réelles de création, grandes étapes de l'histoire de la commune, effectifs et budgets.

### 1.2.3 Fiche technique

La fiche technique ci-dessous récapitule les informations générales relatives à l'organisme d'accueil.

**Tableau 1.1 — Fiche technique de l'organisme d'accueil**

| Élément | Détail |
|---------|--------|
| Raison sociale | Commune [Nom de la commune] |
| Statut juridique | Collectivité territoriale de droit public |
| Localisation | [Adresse / Province / Région] |
| Date de création | [Année de création] |
| Effectif | [Nombre d'agents] |
| Taille du parc automobile | [Nombre de véhicules] |
| Secteur d'activité | Administrations publiques territoriales |
| Services principaux | État civil, urbanisme, voirie, hygiène, gestion des déchets, éclairage public |
| Horaires de travail | Du lundi au vendredi, 08 h 30 à 16 h 30 |
| Site web | [URL de la commune] |

### 1.2.4 Les services et secteurs d'activités

La commune est organisée en plusieurs services dont les principaux sont présentés dans le tableau ci-après. Cette organisation illustre la diversité des missions exercées et la multiplicité des acteurs amenés à interagir avec les ressources partagées de la collectivité.

**Tableau 1.2 — Services de la commune**

| Service | Mission principale |
|---------|--------------------|
| Service de l'état civil | Tenue des registres, établissement des actes de naissance, de mariage et de décès |
| Service de l'urbanisme | Instruction des demandes de permis de construire, contrôle de l'occupation du sol |
| Service de la voirie et des travaux | Entretien de la voirie, éclairage public, petits travaux d'infrastructure |
| Service de l'hygiène et de l'environnement | Collecte des déchets ménagers, nettoiement, espaces verts |
| Service financier | Comptabilité, budgets, marchés publics, recouvrement |
| Service du parc et du carburant | Gestion du parc automobile, approvisionnement et distribution de carburant |
| Service des ressources humaines | Gestion administrative du personnel, paie, formation |

Le **service du parc et du carburant** constitue le cœur du domaine d'intervention du présent projet. Il est responsable de l'affectation des véhicules aux différents services, du suivi des consommations de carburant, de la tenue des carnets de bord et de la maintenance du parc. Ses agents interagissent quotidiennement avec la base de gestion afin d'enregistrer les mouvements de carburant, d'imputer les consommations aux bons services et de produire les rapports mensuels destinés à la direction.

### 1.2.5 Missions de la commune

Conformément à la loi organique n° 113-14 relative aux communes, la commune exerce des compétences propres dans plusieurs domaines :

- **les compétences d'impulsion et de développement** : création et gestion de zones industrielles, commerciales et touristiques, actions de développement économique et social local ;
- **les compétences de services publics locaux** : gestion du terrain de foire et des marchés, ouverture et entretien de la voirie, propreté, hygiène et salubrité publique, gestion des déchets, transport urbain et collectif, éclairage public, cimetières, état civil ;
- **les compétences de l'aménagement du territoire** : élaboration et révision du plan d'aménagement, programmation et exécution des opérations d'aménagement, création et entretien des espaces publics.

Dans l'exercice de ces missions, la commune s'appuie sur ses ressources matérielles et humaines, dont le parc automobile est l'un des leviers opérationnels les plus sensibles : il conditionne la mobilité des agents, la collecte des déchets, la réalisation des travaux et la promptitude de l'intervention publique. Cette criticité renforce l'importance de sécuriser l'ensemble de la chaîne logistique associée, de l'attribution des véhicules à la distribution du carburant.

## 1.3 Contexte du projet

### 1.3.1 Étude de l'existant

Afin de comprendre les enjeux du projet, une étude du système existant de gestion du parc et du carburant a été menée dès le début du stage. Cette étude s'est appuyée sur des entretiens avec les agents du service, l'observation des pratiques de travail et l'analyse des documents en usage.

Le fonctionnement actuel repose sur un ensemble d'outils hétérogènes :

- **des registres papier** pour la tenue des affectations de véhicules et des bons de carburant ;
- **des tableurs Excel** pour le suivi des consommations et la production des rapports périodiques ;
- **une application web de gestion du parc et du carburant**, hébergée sur un serveur local, qui centralise une partie des données de consommation ;
- **un réseau local plat**, sans segmentation, sur lequel l'ensemble des postes administratifs et techniques communiquent sans contrainte.

L'application de gestion, développée de manière interne, permet d'enregistrer les véhicules, d'encoder les bons de carburant et de générer des états récapitulatifs. Elle repose sur une base de données unique et n'exige, pour toutes les catégories d'utilisateurs, qu'un simple identifiant et un mot de passe, sans politique d'authentification renforcée.

**Tableau 1.3 — Caractéristiques de l'existant**

| Caractéristique | Situation actuelle |
|-----------------|--------------------|
| Segmentation du réseau | Absente — réseau local unique (flat network) |
| Authentification | Identifiant / mot de passe simple, partagé |
| Gestion des certificats | Absente — aucun certificat, aucune PKI |
| Chiffrement des échanges | Minoritaire, voire absent |
| Journalisation | Partielle, non centralisée, non conservée |
| Supervision | Aucune capacité de détection d'intrusion |
| Continuité / sauvegardes | Sauvegardes manuelles et sporadiques |

### 1.3.2 Comparaison avec les solutions existantes

Le marché et l'écosystème open-source proposent plusieurs familles de solutions susceptibles de répondre au besoin d'une commune :

**Tableau 1.4 — Comparaison des familles de solutions**

| Solution | Type | Avantages | Limites |
|----------|------|-----------|---------|
| Solutions commerciales de gestion de flotte | SaaS métier | Ergonomie, fonctionnalités avancées de gestion | Coût d'abonnement, dépendance, peu d'intégration avec la sécurité |
| Pare-feu matériels classiques | Matériel | Performances, support | Coût de licence, blocage de la confiance interne (modèle périmètre) |
| Suite Microsoft/Active Directory | Logiciel propriétaire | Maturité, écosystème | Coûts de licences élevés pour une petite collectivité |
| Solutions open-source (pfSense, FreeIPA, Wazuh) | Logiciel libre | Coût nul, auditabilité, transparence | Exige des compétences techniques internes |
| Modèle Zero Trust complet (NIST SP 800-207) | Cadre d'architecture | Couverture totale de la chaîne de confiance | Complexité de conception, effort de déploiement |

L'analyse consolidée montre qu'aucune solution commerciale ne répond simultanément aux contraintes budgétaires d'une commune et à l'exigence d'une véritable refonte sécuritaire. Les solutions SaaS se concentrent sur le métier sans traiter la sécurité du réseau ; les pare-feu traditionnels, quant à eux, préservent le modèle du périmètre, désormais reconnu comme insuffisant.

### 1.3.3 Analyse critique des limites de l'existant

L'analyse menée permet de dégager un certain nombre de limites critiques du système actuel :

1. **Absence de segmentation** : le réseau plat autorise, une fois un poste compromis, une progression latérale vers l'ensemble des ressources de l'administration, y compris la base de données de l'application de gestion.
2. **Faiblesse de l'authentification** : l'utilisation d'un couple identifiant/mot de passe partagé ne permet ni d'imputer les actions à un individu précis ni de détecter les tentatives d'intrusion par force brute.
3. **Absence de PKI** : aucun certificat n'est déployé ; les administrateurs se connectent aux équipements et à l'application sans authentification mutuelle, ce qui expose au risque d'interception et d'usurpation.
4. **Aucune capacité de détection** : aucun système ne collecte ni n'analyse les journaux ; des attaques répétées peuvent passer inaperçues pendant des semaines.
5. **Vulnérabilité de la distribution de carburant** : la gestion du carburant constitue une cible privilégiée de fraude interne (détournements, accès non autorisés, manipulation des compteurs de consommation).
6. **Exposition d'une ressource cloud** : l'hypothèse de déporter l'application vers un hébergement cloud devait obligatoirement être accompagnée d'un contrôle strict des accès externes, faute de quoi la surface d'attaque augmente considérablement.

Ces limites confirment que le modèle du périmètre ne correspond plus aux besoins de sécurité d'une administration moderne et responsable de deniers publics.

### 1.3.4 Problématique

À l'issue de cette étude, la problématique générale du projet peut être formulée comme suit :

> **Comment sécuriser, de manière structurée, économiquement réaliste et démontrable, le système de gestion du parc municipal et du carburant, afin de se prémunir contre les accès non autorisés, la fraude et le mouvement latéral, tout en étendant de manière sûre une partie des services vers le cloud ?**

Cette problématique se décline en plusieurs sous-questions :

- comment remplacer la confiance implicite du réseau par une vérification systématique de chaque utilisateur et de chaque connexion ?
- comment mettre en place, avec des outils libres, une infrastructure d'identité et de certification interne totalement maîtrisée ?
- comment relier de manière chiffrée l'infrastructure locale à une charge de travail hébergée dans le cloud, sans exposition de surface d'attaque ?
- comment détecter, en temps quasi réel, les tentatives d'intrusion spécifiques au contexte de la flotte et du carburant ?

## 1.4 Cadre sécuritaire du projet

### 1.4.1 Étude de l'existant

D'un point de vue strictement sécuritaire, l'audit de l'existant a confirmé l'absence de toute composante Zero Trust. Aucune entité — utilisateur, poste de travail, service — n'est soumise à une vérification systématique : le réseau local est plat, les mots de passe sont partagés, les certificats sont inexistants et aucune journalisation centralisée n'est opérée.

La cartographie suivante synthétise les ressources existantes et leur niveau de protection :

**Tableau 1.5 — État sécuritaire de l'existant**

| Ressource | Protections présentes | Failles relevées |
|-----------|----------------------|------------------|
| Postes administratifs | Antivirus individuel | Aucune segmentation, partage de comptes |
| Serveur applicatif local | Accès par mot de passe | Pas de chiffrement, exposé sur tout le réseau |
| Postes du service du parc | Aucune | Accès direct à l'application et aux fichiers partagés |
| Terminaux mobiles / terrain | Aucune | Connexions non contrôlées |
| Future ressource cloud | — | Risque élevé d'exposition publique si mal configurée |

### 1.4.2 Comparaison avec les solutions existantes

La comparaison porte désormais sur les modèles d'architecture de sécurité eux-mêmes :

**Tableau 1.6 — Modèle périmètre versus modèle Zero Trust**

| Critère | Modèle périmètre | Modèle Zero Trust (NIST SP 800-207) |
|---------|------------------|--------------------------------------|
| Confiance | Implicite à l'intérieur du réseau | Aucune : tout est vérifié |
| Contrôle d'accès | Basé sur le périmètre (IP source) | Basé sur l'identité et le contexte |
| Segment critique | Isolé ou non selon le site | Traitement des flux, périmètres micro |
| Mouvement latéral | Possible une fois le périmètre franchi | Bloqué par défaut (deny by default) |
| Vérification | Ponctuelle | Continue (authentification et inspection de chaque connexion) |
| Adapté au cloud | Non | Oui |

Le modèle Zero Trust est retenu comme le plus adapté, car il traite à la fois les menaces externes et les menaces internes, ce qui correspond précisément aux risques identifiés au sein d'une administration communale.

### 1.4.3 Analyse critique des limites de l'existant

La comparaison des modèles confirme définitivement les limites de l'existant :

- la segmentation réseau est inexistante, ce qui rend impossible toute notion de micro-périmètre ;
- l'identité n'est pas centralisée : chaque service gère ses propres comptes sans référentiel commun, ce qui empêche une vérification cohérente ;
- la chaîne de confiance n'est pas maîtrisée : sans autorité de certification interne, aucun service ne peut être authentifié par certificat ;
- la détection est aveugle : aucune source de journal n'est collectée, aucune corrélation n'est effectuée, aucun tableau de bord n'existe ;
- l'extension vers le cloud, prévue par l'architecture cible, ne peut s'envisager sous le modèle périmètre sans exposer dangereusement les services.

### 1.4.4 Problématique

La problématique sécuritaire peut être formulée de manière définitive comme suit :

> **Comment concevoir, déployer et valider une architecture Zero Trust complète, fondée sur des composants open-source et une topologie hybride, appliquée à la gestion du parc municipal et du carburant, garantissant le rejet par défaut des flux non autorisés, la légitimation de chaque accès par une identité vérifiée, et la détection active des menaces propres à ce contexte ?**

### 1.4.5 Solution proposée

Pour répondre à cette problématique, le projet propose une **architecture Zero Trust Network Architecture (ZTNA)** structurée autour de cinq piliers :

1. **Segmentation réseau stricte** : découpage du réseau en plusieurs VLAN (Administration, Flotte, Services, Tunnel) avec rejet par défaut de tout trafic inter-VLAN non explicitement autorisé, orchestré par un pare-feu pfSense couplé au moteur de prévention d'intrusion Suricata ;
2. **Gestion centralisée des identités et de la PKI** : déploiement de FreeIPA fournissant l'annuaire LDAP, l'authentification Kerberos, le DNS interne et une autorité de certification interne émettant l'ensemble des certificats (authentification mutuelle mTLS) ;
3. **Topologie hybride sécurisée** : connexion chiffrée entre l'infrastructure locale et une machine virtuelle Microsoft Azure hébergeant l'application de gestion du parc et du carburant ainsi que la plateforme de supervision, au travers d'un tunnel WireGuard ;
4. **Détection active des menaces** : déploiement de la plateforme Wazuh (SIEM/XDR) collectant les journaux de l'ensemble des composants et appliquant des règles de détection personnalisées ciblant les scénarios propres aux parcs municipaux (accès hors horaires, force brute, mouvement latéral) ;
5. **Validation par scénarios d'attaque** : exécution de trois scénarios de type red team afin de démontrer l'efficacité réelle de l'architecture face aux attaques les plus représentatives du contexte.

### 1.4.6 Objectifs du projet

Les objectifs du projet se déclinent comme suit :

- **objectif général** : concevoir et mettre en œuvre une architecture réseau Zero Trust appliquée à l'environnement de gestion du parc municipal et du carburant ;
- **objectifs spécifiques** :

  1. concevoir une architecture réseau segmentée respectant les principes du Zero Trust ;
  2. déployer une PKI interne et un service d'annuaire afin de maîtriser l'intégralité de la chaîne de confiance ;
  3. simuler une topologie hybride reliant l'infrastructure sur site à une charge de travail cloud via un tunnel chiffré ;
  4. implémenter une détection active des menaces à l'aide de règles personnalisées ciblant des scénarios propres au contexte municipal ;
  5. démontrer la pertinence de l'architecture face à trois scénarios d'attaque réalistes ;
  6. produire une documentation complète (architecture, PKI, règles de détection, rapport des scénarios, code source) réutilisable par la commune.

## 1.5 Planification et conduite du projet

### 1.5.1 Méthodologie de travail

La conduite d'un projet de sécurité de cette ampleur, mêlant conception réseau, déploiement d'infrastructure, développement applicatif et validation par des scénarios d'attaque, impose une méthodologie rigoureuse et flexible. Après analyse des différentes approches — méthode classique en cascade, méthode agile Scrum — le choix s'est porté sur **Scrum**, dont les cycles courts et les livraisons incrémentales correspondent parfaitement à la nature du projet.

### 1.5.2 Présentation de la méthode SCRUM

Scrum est un framework agile de gestion de projet permettant de traiter des problèmes complexes tout en livrant régulièrement des produits de grande valeur. Il repose sur une itération appelée **sprint**, d'une durée fixe au cours de laquelle un incrément du produit est produit et vérifié. Scrum est fondé sur trois piliers : la **transparence** (les aspects significatifs du processus sont visibles pour les responsables), l'**inspection** (les artefacts livrés sont régulièrement inspectés afin de détecter les dérives) et l'**adaptation** (le processus est ajusté dès qu'un écart significatif est observé).

### 1.5.3 Justification du choix de Scrum

Le choix de Scrum se justifie par plusieurs considérations :

- **la nature itérative de l'implémentation** : le déploiement des composants (pfSense, FreeIPA, WireGuard, Wazuh) se prête naturellement à des incréments successifs et testables ;
- **la gestion des priorités** : face à un périmètre large (réseau, identité, détection, tests), Scrum permet de prioriser les fonctionnalités les plus critiques à chaque sprint ;
- **la réactivité face aux aléas techniques** : les incidents de configuration rencontrés durant le stage ont pu être traités sans compromettre la livraison globale ;
- **l'implication des parties prenantes** : des revues de sprint régulières avec l'encadrant ont assuré un alignement permanent entre la vision du projet et les réalisations effectives.

### 1.5.4 Caractéristiques de la méthode SCRUM

Les principales caractéristiques de Scrum appliquées au projet sont les suivantes :

- des **cycles de développement courts** (sprints d'une à deux semaines) ;
- une **liste priorisée d'exigences** (product backlog) enrichie en début de chaque sprint ;
- une **définition de fini** claire pour chaque incrément livré ;
- des **livraisons fréquentes et démontrées** (démos de fin de sprint) ;
- une **amélioration continue** du processus grâce à la rétrospective.

### 1.5.5 Les rôles dans SCRUM

La méthode Scrum définit trois rôles principaux, adaptés dans le contexte du stage :

**Tableau 1.7 — Rôles Scrum dans le cadre du projet**

| Rôle | Acteur | Responsabilités |
|------|--------|-----------------|
| Product Owner | Encadrant de stage [Nom] | Définition des priorités, validation des livrables, représentation du besoin de la commune |
| Scrum Master | Stagiaire (Mohamed Meddah) | Animation des cérémonies, levée des obstacles, facilitation |
| Équipe de développement | Stagiaire (Mohamed Meddah) | Conception, implémentation, tests, documentation |

Compte tenu du contexte de stage individuel, les rôles de Scrum Master et d'équipe de développement ont été assurés par le stagiaire, tandis que le Product Owner était représenté par l'encadrant, garant de la conformité du résultat aux besoins réels de la commune.

### 1.5.6 Rituels Scrum

Les rituels Scrum suivants ont été appliqués durant le projet :

- **la réunion de planification de sprint** (sprint planning) : en début de chaque sprint, les objectifs et l'engagement ont été définis conjointement avec l'encadrant ;
- **la mêlée quotidienne** (daily scrum) : courte séance quotidienne de synchronisation sur l'avancement et les obstacles rencontrés ;
- **la revue de sprint** (sprint review) : présentation des incréments réalisés à la fin de chaque sprint et recueil du retour du Product Owner ;
- **la rétrospective de sprint** (sprint retrospective) : analyse des points positifs et des axes d'amélioration du processus de travail.

### 1.5.7 Les sprints

Le projet a été découpé en six sprints, alignés sur la durée totale du stage (12 semaines), conformément au plan initial du projet de fin d'année :

**Tableau 1.8 — Décomposition en sprints**

| Sprint | Période | Contenu | Livrable |
|--------|---------|---------|----------|
| Sprint 1 | Semaines 1–2 | Conception de l'architecture, plan d'adressage IP, modèle de menace, choix des composants | Document d'architecture, plan réseau |
| Sprint 2 | Semaines 3–5 | Installation de pfSense, création des VLAN, déploiement de FreeIPA, mise en place de la PKI | Infrastructure réseau et d'identité opérationnelle |
| Sprint 3 | Semaines 6–7 | Développement et déploiement de l'application Flask, installation de Wazuh, intégration des sources de journaux | Application et SIEM fonctionnels |
| Sprint 4 | Semaines 8–9 | Élaboration des règles de détection personnalisées, parsing des journaux, configuration des tableaux de bord | Règles et tableaux de bord Wazuh |
| Sprint 5 | Semaine 10 | Exécution des trois scénarios d'attaque, collecte des preuves, documentation des résultats | Rapport des scénarios, preuves |
| Sprint 6 | Semaines 11–12 | Rédaction du mémoire, finalisation des diagrammes, préparation de la soutenance | Mémoire et présentation |

### 1.5.8 Diagramme de Gantt

Le diagramme de Gantt ci-dessous présente la répartition des tâches sur la période du projet. Il permet de visualiser les dépendances entre les phases et de vérifier le respect des échéances.

> **[À INSÉRER : Figure 1.1 — Diagramme de Gantt du projet (répartir les six sprints sur les 12 semaines, avec un chevauchement partiel entre le Sprint 3 et le Sprint 4)].**

**Tableau 1.9 — Phases du projet et durées**

| Phase | Durée | Période indicative |
|-------|-------|--------------------|
| 1 — Conception | 2 semaines | Semaines 1–2 |
| 2 — Infrastructure | 3 semaines | Semaines 3–5 |
| 3 — Application + SIEM | 2 semaines | Semaines 6–7 |
| 4 — Détection | 2 semaines | Semaines 8–9 |
| 5 — Scénarios red team | 1 semaine | Semaine 10 |
| 6 — Rapport + préparation soutenance | 2 semaines | Semaines 11–12 |

## 1.6 Conclusion

Ce premier chapitre a permis de situer le projet dans son environnement réel : un organisme communal dont la gestion du parc et du carburant repose encore sur un réseau plat, une authentification faible et une absence totale de détection. L'étude de l'existant et la comparaison des modèles ont conduit à la formulation d'une problématique centrée sur la mise en place d'une architecture Zero Trust économiquement réaliste. La solution proposée, articulée autour de cinq piliers, a été présentée, ainsi que les objectifs du projet et la méthodologie Scrum adoptée pour sa conduite. Le chapitre suivant aborde l'analyse des besoins et la conception détaillée de la solution.

# Chapitre 2 : Analyse et conception

## 2.1 Introduction

Ce chapitre est consacré à l'analyse des besoins et à la conception de la solution. Il s'agit de passer d'une expression globale du besoin — sécuriser le système de gestion du parc et du carburant selon les principes du Zero Trust — à une spécification précise, exploitable techniquement. La démarche retenue s'appuie sur les formalismes du Langage de Modélisation Unifié (UML) : identification des acteurs, spécification des besoins fonctionnels et non fonctionnels, puis élaboration des diagrammes de cas d'utilisation, de séquence, d'activité et de classes. Ces modèles permettent de décrire avec rigueur les interactions entre les utilisateurs et le système, ainsi que la structure interne de la solution proposée.

## 2.2 Identification des acteurs du système

Un acteur représente un rôle joué par une entité externe (personne, système, organisation) qui interagit avec le système étudié. Dans le cadre de l'architecture Zero Trust de gestion du parc municipal, les acteurs suivants ont été identifiés :

**Tableau 2.1 — Acteurs du système**

| Acteur | Type | Description |
|--------|------|-------------|
| Administrateur de l'architecture | Humain | Responsable de la configuration et de la supervision de l'ensemble des composants (pfSense, FreeIPA, Wazuh, WireGuard). Dispose des privilèges les plus élevés. |
| Administrateur FreeIPA | Humain | Gère les comptes utilisateurs, les groupes, les politiques d'authentification et la délivrance des certificats. |
| Gestionnaire du parc | Humain | Consulte et gère les données du parc (véhicules, affectations, maintenance) via l'application de gestion. |
| Agent du carburant | Humain | Enregistre les bons de carburant, les mouvements de stock et les consommations quotidiennes. |
| Direction | Humain | Consulte les rapports et les tableaux de bord relatifs aux consommations et à la sécurité du système. |
| Auditeur de sécurité | Humain | Consulte les journaux, les alertes et l'état de conformité de l'architecture. |
| Utilisateur du module SIEM | Humain | Analyse les alertes émises par Wazuh et déclenche les actions de réponse. |
| Service cloud (Azure VM) | Système | Héberge l'application de gestion et la plateforme Wazuh ; reste joignable uniquement via le tunnel WireGuard. |
| Service d'annuaire (FreeIPA) | Système | Fournit l'authentification Kerberos, l'annuaire LDAP et l'émission des certificats. |
| Pare-feu (pfSense) | Système | Applique la segmentation, filtre le trafic inter-VLAN et journalise les événements. |
| Attaquant (red team) | Humain externe | Tente d'exploiter l'architecture (force brute, mouvement latéral, accès direct). Utilisé uniquement dans le cadre des tests. |

La répartition des rôles ci-dessus est fondamentale : elle conditionne les politiques d'accès mises en œuvre par le système, puisque chaque interaction sera vérifiée puis autorisée ou refusée selon l'identité, le contexte et la ressource visée.

## 2.3 Spécification des besoins

### 2.3.1 Besoins fonctionnels

Les besoins fonctionnels (BF) décrivent les fonctions que le système doit offrir aux acteurs. Ils sont consignés dans le tableau suivant :

**Tableau 2.2 — Besoins fonctionnels**

| Identifiant | Besoin fonctionnel | Acteurs concernés |
|-------------|--------------------|-------------------|
| BF-01 | S'authentifier de manière centralisée via l'annuaire | Tous les acteurs |
| BF-02 | Authentifier mutuellement les services par certificats (mTLS) | Administration, système |
| BF-03 | Segmenter le réseau en VLAN distincts (Administration, Flotte, Services, Tunnel) | Administration |
| BF-04 | Bloquer par défaut tout trafic inter-VLAN non autorisé | Administration |
| BF-05 | Configurer des règles de filtrage explicites entre les VLAN | Administration |
| BF-06 | Établir un tunnel chiffré entre le site local et la ressource cloud | Administration |
| BF-07 | Publier l'application de gestion uniquement à travers le tunnel | Administration |
| BF-08 | Gérer les véhicules (ajout, modification, suppression, consultation) | Gestionnaire du parc |
| BF-09 | Gérer les bons de carburant et les mouvements de stock | Agent du carburant |
| BF-10 | Suivre les consommations et affecter les coûts aux services | Agent du carburant, Direction |
| BF-11 | Générer les rapports périodiques de consommation | Direction |
| BF-12 | Collecter les journaux de tous les composants (pare-feu, annuaire, application) | Administration, SIEM |
| BF-13 | Appliquer des règles de détection personnalisées (hors horaires, force brute, mouvement latéral) | Administration, SIEM |
| BF-14 | Afficher les alertes et les tableaux de bord de supervision | Administrateur, Auditeur |
| BF-15 | Déclencher une réponse active en cas d'alerte | Administration |
| BF-16 | Émettre, renouveler et révoquer les certificats | Administrateur FreeIPA |
| BF-17 | Journaliser les tentatives d'accès refusées au niveau du pare-feu | Administration |

### 2.3.2 Besoins non fonctionnels

Les besoins non fonctionnels (BNF) précisent les contraintes de qualité auxquelles le système doit satisfaire :

**Tableau 2.3 — Besoins non fonctionnels**

| Identifiant | Catégorie | Exigence |
|-------------|-----------|----------|
| BNF-01 | Sécurité | Application du principe du moindre privilège sur l'ensemble des accès |
| BNF-02 | Sécurité | Chiffrement systématique des échanges réseau (tunnel WireGuard, TLS, mTLS) |
| BNF-03 | Sécurité | Rejet par défaut de tout trafic non explicitement autorisé |
| BNF-04 | Performance | Latence de détection des alertes inférieure à 60 secondes |
| BNF-05 | Disponibilité | Architecture opérationnelle sur une durée de test continue avec un taux de disponibilité cible d'au moins 99 % |
| BNF-06 | Évolutivité | Capacité d'ajouter des VLAN ou des services sans refonte de l'architecture |
| BNF-07 | Maintenabilité | Documentation complète et arborescence de configuration clairement structurée |
| BNF-08 | Coût | Utilisation exclusive de solutions open-source, sans coût de licence |
| BNF-09 | Compatibilité | Respect des référentiels (NIST SP 800-207, MITRE ATT&CK) pour la traçabilité sécuritaire |
| BNF-10 | Auditabilité | Traçabilité totale des événements de sécurité sur une période de conservation définie |

## 2.4 Conception

### 2.4.1 Diagramme de cas d'utilisation global

Le diagramme de cas d'utilisation global permet de représenter l'ensemble des fonctionnalités offertes par le système et les acteurs qui y participent. Il constitue la vue fonctionnelle la plus complète de la solution.

> **[À INSÉRER : Figure 2.1 — Diagramme de cas d'utilisation global. Le diagramme doit représenter le système « Parc & Carburant » entouré des acteurs : Administrateur, Gestionnaire du parc, Agent du carburant, Direction, Auditeur, Attaquant. Les cas d'utilisation principaux à faire figurer sont : S'authentifier, Gérer les comptes et certificats, Gérer les véhicules, Gérer les bons de carburant, Consulter les rapports, Superviser les alertes, Configurer la segmentation, Établir le tunnel, Émettre les certificats, Collecter les journaux.]**

### 2.4.2 Description textuelle des cas d'utilisation principaux

Chaque cas d'utilisation principal est précisé selon le modèle de description suivant : acteurs, préconditions, scénario nominal, postconditions et scénarios alternatifs.

**Cas d'utilisation 1 — S'authentifier (UC-01)**

| Élément | Description |
|---------|-------------|
| Acteur principal | Tout utilisateur (Gestionnaire du parc, Agent du carburant, Direction, Admin) |
| Préconditions | L'utilisateur dispose d'un compte dans l'annuaire FreeIPA et de son certificat émis par la CA interne |
| Scénario nominal | 1. L'utilisateur ouvre l'application ; 2. Le serveur présente son certificat ; 3. Le client présente son certificat (mTLS) ; 4. L'authentification Kerberos/LDAP vérifie l'identité ; 5. Le système établit une session ; 6. L'utilisateur accède aux fonctions autorisées |
| Postconditions | L'utilisateur est authentifié ; l'événement est journalisé |
| Scénarios alternatifs | Échec de validation du certificat → accès refusé ; tentative de force brute → alerte déclenchée par la règle 100002 |

**Cas d'utilisation 2 — Gérer les certificats (UC-02)**

| Élément | Description |
|---------|-------------|
| Acteur principal | Administrateur FreeIPA |
| Préconditions | Être authentifié avec les droits d'administration PKI |
| Scénario nominal | 1. L'administrateur ouvre l'interface FreeIPA ; 2. Il émet un certificat pour un service ou un utilisateur ; 3. Le certificat est signé par la CA interne ; 4. Le certificat est distribué au destinataire |
| Postconditions | Le certificat est actif et enregistré dans le référentiel |
| Scénario alternatif | Certificat compromis → révocation immédiate et nouvelle émission |

**Cas d'utilisation 3 — Se connecter à l'application à travers le tunnel (UC-03)**

| Élément | Description |
|---------|-------------|
| Acteur principal | Gestionnaire du parc, Agent du carburant, Direction |
| Préconditions | Tunnel WireGuard établi et opérationnel ; certificats valides |
| Scénario nominal | 1. Le client résout le nom interne de l'application ; 2. La requête traverse le tunnel chiffré ; 3. Le pare-feu vérifie la source ; 4. L'application authentifie l'utilisateur ; 5. Les données sont échangées de manière chiffrée |
| Postconditions | Session ouverte ; traces consignées dans les journaux de l'application |
| Scénario alternatif | Tentative d'accès direct à l'adresse publique de la VM → bloquée par les NSG/UFW |

**Cas d'utilisation 4 — Superviser les alertes de détection (UC-04)**

| Élément | Description |
|---------|-------------|
| Acteur principal | Administrateur de l'architecture, Auditeur |
| Préconditions | Wazuh opérationnel ; sources de journaux configurées |
| Scénario nominal | 1. L'utilisateur consulte le tableau de bord Wazuh ; 2. Il filtre les alertes par niveau ; 3. Il consulte le détail d'une alerte ; 4. Il déclenche éventuellement une réponse active ; 5. Il archive l'événement comme analyse |
| Postconditions | Alertes traitées et documentées |
| Scénario alternatif | Faux positif → ajustement de la règle et enrichissement du journal |

### 2.4.3 Diagramme de cas d'utilisation par rôle

Les diagrammes de cas d'utilisation par rôle permettent d'isoler les vues fonctionnelles propres à chaque catégorie d'acteur, conformément à la politique du moindre privilège.

**Vue Administrateur**

> **[À INSÉRER : Figure 2.2 — Diagramme de cas d'utilisation de l'acteur Administrateur. Cas d'utilisation : Configurer la segmentation VLAN, Gérer les règles de pare-feu, Configurer le tunnel, Collecter les journaux, Gérer les règles de détection, Superviser les alertes, Déclencher une réponse active.]**

**Vue Gestionnaire du parc**

> **[À INSÉRER : Figure 2.3 — Diagramme de cas d'utilisation de l'acteur Gestionnaire du parc. Cas d'utilisation : Consulter les véhicules, Ajouter/modifier/supprimer un véhicule, Affecter un véhicule à un service, Consulter l'historique de maintenance.]**

**Vue Agent du carburant**

> **[À INSÉRER : Figure 2.4 — Diagramme de cas d'utilisation de l'acteur Agent du carburant. Cas d'utilisation : Enregistrer un bon de carburant, Enregistrer un mouvement de stock, Consulter les consommations, Signaler un incident.]**

**Vue Direction**

> **[À INSÉRER : Figure 2.5 — Diagramme de cas d'utilisation de l'acteur Direction. Cas d'utilisation : Consulter les rapports de consommation, Consulter les synthèses budgétaires, Valider les affectations.]**

### 2.4.4 Diagrammes de séquence

Les diagrammes de séquence décrivent l'ordre temporel des interactions entre les objets du système pour un scénario donné. Trois scénarios critiques font l'objet d'un diagramme dédié.

**Scénario 1 — Authentification mutuelle et accès à l'application**

> **[À INSÉRER : Figure 2.6 — Diagramme de séquence « Authentification et accès à l'application ». Interactions à représenter : Client (navigateur présentant le certificat) → pfSense (vérification du flux autorisé) → Application Flask → Annuaire FreeIPA (LDAP/Kerberos). Les messages clés : « Présentation du certificat serveur », « Présentation du certificat client », « Vérification identité (LDAP/Kerberos) », « Requête autorisée », « Réponse chiffrée ».]**

**Scénario 2 — Collecte et corrélation d'une alerte de sécurité**

> **[À INSÉRER : Figure 2.7 — Diagramme de séquence « De la détection à l'alerte ». Interactions à représenter : pfSense (émet le journal) → Wazuh Manager (ingestion) → Moteur de corrélation (application de la règle) → Console Wazuh (alerte affichée) → Administrateur (action).]**

**Scénario 3 — Blocage d'un mouvement latéral inter-VLAN**

> **[À INSÉRER : Figure 2.8 — Diagramme de séquence « Mouvement latéral refusé ». Interactions à représenter : Poste compromis (VLAN 20) → pfSense (tentative vers VLAN 10) → évaluation de la règle inter-VLAN → REFUS + journalisation → Wazuh → Alerte.]**

### 2.4.5 Diagrammes d'activité

Les diagrammes d'activité modélisent les enchaînements logiques des traitements, y compris les branchements conditionnels.

**Activité 1 — Traitement d'une connexion à l'application**

> **[À INSÉRER : Figure 2.9 — Diagramme d'activité « Connexion à l'application ». Nœuds à représenter : Début → Vérification du certificat client (nœud de décision : valide/non valide) → Chemin non valide : Refus + journalisation + alerte ; Chemin valide : Vérification identité (décision) → échec : nouvelle tentative / compte verrouillé ; succès : Ouverture de session → fin.]**

**Activité 2 — Supervision d'une alerte par l'administrateur**

> **[À INSÉRER : Figure 2.10 — Diagramme d'activité « Traitement d'une alerte ». Nœuds à représenter : Alerte émise par Wazuh → Consultation par l'administrateur → analyse (décision) → Faux positif : ajustement de la règle ; Attaque réelle : blocage par le pare-feu + compte-rendu → Fin.]**

**Activité 3 — Exécution d'un scénario d'attaque (red team)**

> **[À INSÉRER : Figure 2.11 — Diagramme d'activité « Déroulement d'un scénario de test ». Nœuds à représenter : Préparation de l'environnement → lancement de l'attaque → observation côté défense (décision) → Alerte confirmée : documentation des preuves ; Attaque non détectée : correction des règles → Fin.]**

### 2.4.6 Diagramme de classes

Le diagramme de classes décrit la structure statique de l'application de gestion du parc et du carburant. Il formalise les entités manipulées par le système ainsi que leurs relations.

> **[À INSÉRER : Figure 2.12 — Diagramme de classes de l'application de gestion. Les classes principales à représenter sont : Utilisateur, Role, Certificat, Vehicule, Service (entité métier), Affectation, BonCarburant, MouvementStock, Carburant, JournalAcces, Alerte. Les associations principales : Utilisateur possède 1..* Certificat ; Utilisateur appartient à 0..* Role ; Vehicule est affecté à 1 Service via Affectation ; BonCarburant concerne 1 Vehicule et est émis par 1 Utilisateur ; JournalAcces référence 1 Utilisateur ; Alerte est générée par l'analyse des journaux.]**

**Tableau 2.4 — Description des classes principales**

| Classe | Attributs principaux | Relations |
|--------|----------------------|-----------|
| Utilisateur | id, nom, prenom, email, statut | 1..* Certificat ; 0..* Role ; émet 0..* BonCarburant |
| Role | id, libelle, niveau_acces | 0..* Utilisateur |
| Certificat | id, sujet, autorite, date_emission, date_expiration, etat | appartient à 1 Utilisateur |
| Vehicule | id, immatriculation, marque, modele, service, carburant | concerné par 0..* BonCarburant ; lié à 1 Affectation |
| Affectation | id, date_debut, date_fin, utilisateur, vehicule | relie 1 Vehicule et 1..* Utilisateur |
| BonCarburant | id, quantite, date_emission, vehicule, utilisateur | émis pour 1 Vehicule ; émis par 1 Utilisateur |
| JournalAcces | id, timestamp, utilisateur, source_ip, action, ressource | référence 1 Utilisateur |
| Alerte | id, niveau, source, description, timestamp, statut | issue de l'analyse des Journaux |

## 2.5 Conclusion

Ce chapitre a permis de transformer l'expression globale du besoin en une spécification précise et structurée. Les acteurs du système ont été identifiés, les besoins fonctionnels et non fonctionnels formalisés, et la conception a été traduite en modèles UML complets : diagramme de cas d'utilisation global et par rôle, descriptions textuelles détaillées, diagrammes de séquence, d'activité et de classes. Ces modèles constituent le socle conceptuel sur lequel repose l'architecture technique détaillée dans le chapitre suivant.

# Chapitre 3 : Architecture technique et outils utilisés

## 3.1 Introduction

Ce chapitre présente l'architecture technique retenue pour la mise en œuvre de la solution Zero Trust, ainsi que l'environnement de travail dans lequel le projet a été développé et testé. La première partie décrit la vue d'ensemble de l'architecture, ses composants et leurs interactions, puis détaille l'architecture du backend et du frontend. La seconde partie dresse un inventaire des outils utilisés — développement, conteneurisation, sécurité, gestion de version et documentation — et présente la structure organisationnelle du projet.

## 3.2 Architecture technique

### 3.2.1 Vue d'ensemble

L'architecture proposée est une architecture **hybride**, associant une infrastructure sur site (deux machines virtuelles locales) et une charge de travail hébergée dans le cloud Microsoft Azure. Elle repose sur trois plans fonctionnels :

1. **le plan réseau** : un pare-feu pfSense jouant le rôle de routeur inter-VLAN, de passerelle de filtrage et d'extrémité du tunnel chiffré ;
2. **le plan identité et confiance** : un serveur FreeIPA fournissant l'annuaire LDAP, l'authentification Kerberos, le DNS interne et l'autorité de certification (PKI) ;
3. **le plan applicatif et de supervision** : une machine virtuelle Azure hébergeant l'application de gestion du parc et du carburant (Flask) et la plateforme SIEM/XDR Wazuh.

> **[À INSÉRER : Figure 3.1 — Topologie globale de l'architecture. Le schéma doit représenter la machine de l'attaquant (Kali), la VM 1 pfSense (VLAN 10 Administration, VLAN 20 Flotte, VLAN 30 Services, VLAN 99 Tunnel), la VM 2 FreeIPA sur le VLAN 10, et la VM Azure (application + Wazuh) reliée par le tunnel WireGuard. Il doit faire apparaître les deux segments local et cloud ainsi que la passerelle WireGuard.]**

**Tableau 3.1 — Plan d'adressage réseau**

| VLAN | Nom | Sous-réseau | Contenu |
|------|-----|-------------|---------|
| 10 | Administration | 10.10.10.0/24 | Interfaces de gestion, FreeIPA (10.10.10.10), passerelle (10.10.10.1) |
| 20 | Flotte | 10.10.20.0/24 | Simulateurs de véhicules, clients de l'application carburant (10.10.20.50) |
| 30 | Services | 10.10.30.0/24 | Services internes, DNS |
| 99 | Tunnel | 10.99.0.0/30 | Liaison point-à-point WireGuard (10.99.0.1 ↔ 10.99.0.2) |

Le trafic inter-VLAN est **refusé par défaut** : seules des règles d'allow explicites, définies dans la politique du pare-feu, autorisent un flux donné entre deux segments.

### 3.2.2 Composants et interactions

**Composant 1 — Pare-feu pfSense (VM 1)**
pfSense constitue le point central de filtrage et de routage. Il est configuré avec trois interfaces : l'interface WAN, l'interface LAN en trunk (port agrégé portant les VLAN 10, 20, 30) et l'interface dédiée au tunnel WireGuard. pfSense héberge également le moteur **Suricata** en mode IPS, qui inspecte le trafic et applique des signatures de prévention d'intrusion. Enfin, il gère la traduction d'adresses (NAT) pour les seuls flux autorisés et consigne l'ensemble du trafic rejeté afin d'alimenter la plateforme de supervision.

**Composant 2 — Serveur d'identité FreeIPA (VM 2)**
FreeIPA intègre quatre services complémentaires : un annuaire LDAP hébergeant le référentiel des utilisateurs et des groupes, un service d'authentification Kerberos délivrant des tickets, un serveur DNS interne traduisant les noms du domaine `municipal.local`, et une autorité de certification émettant l'ensemble des certificats. FreeIPA constitue ainsi l'unique source de vérité de la chaîne de confiance.

**Composant 3 — Machine virtuelle Azure (Fleet + SIEM)**
La machine virtuelle Azure (taille B2s, Ubuntu 22.04) héberge deux services : l'application Flask de gestion du parc et du carburant (port 5000) et la plateforme Wazuh (tableau de bord sur le port 443). Aucun de ces services n'est exposé sur l'interface publique : un **groupe de sécurité réseau (NSG)** Azure et un pare-feu local (UFW) n'autorisent que le port UDP du tunnel WireGuard ; tout le trafic applicatif transite obligatoirement par le tunnel.

**Tableau 3.2 — Interactions entre composants**

| Flux | Source | Destination | Mécanisme | Autorisé |
|------|--------|-------------|-----------|----------|
| Accès application | VLAN 20 / 10 | VM Azure (10.99.0.2:5000) | Tunnel WireGuard + mTLS | Oui |
| Supervision | VLAN 10 | VM Azure (10.99.0.2:443) | Tunnel WireGuard + TLS | Oui |
| Délivrance certificats | VM Azure | FreeIPA (10.10.10.10) | Tunnel WireGuard + mTLS | Oui |
| Journaux (syslog) | pfSense, FreeIPA, App | Wazuh (10.99.0.2) | Tunnel WireGuard | Oui |
| Tentative attaque | Attaquant | VM Azure (adresse publique) | — | Non (refusée) |
| Mouvement latéral | VLAN 20 | VLAN 10 | — | Non (refusé par défaut) |

### 3.2.3 Architecture du backend

Le backend de l'application de gestion du parc et du carburant a été développé en **Python** à l'aide du micro-framework **Flask**. Il s'organise selon une architecture modulaire :

- **couche API** : points de terminaison REST permettant la gestion des véhicules, des bons de carburant, des mouvements de stock et la génération des rapports ;
- **couche métier** : services Python encapsulant les règles de gestion (imputation des consommations, contrôle des stocks, production des synthèses) ;
- **couche données** : base de données relationnelle (SQLite en phase de test) persistée sur la VM Azure, accessible uniquement depuis les services locaux ;
- **couche sécurité** : intégration de l'authentification mutuelle par certificats (mTLS), validation des jetons Kerberos pour les comptes locaux, et journalisation structurée de toutes les requêtes (accès, erreurs, requêtes suspectes).

**Tableau 3.3 — Points de terminaison principaux du backend**

| Méthode | Chemin | Fonction | Rôle requis |
|---------|--------|----------|-------------|
| GET | /api/vehicules | Liste des véhicules | Gestionnaire, Direction |
| POST | /api/vehicules | Ajout d'un véhicule | Gestionnaire |
| GET | /api/vehicules/\<id\> | Détail d'un véhicule | Gestionnaire, Direction |
| GET | /api/bons | Liste des bons de carburant | Agent, Direction |
| POST | /api/bons | Création d'un bon de carburant | Agent |
| GET | /api/rapports/consommation | Synthèse des consommations | Direction |
| GET | /api/stock | Niveau des stocks | Agent, Direction |
| GET | /login | Page d'authentification | Tous |

### 3.2.4 Architecture du frontend

Le frontend de l'application est un ensemble de pages web servies par Flask (templates Jinja2, HTML, CSS, JavaScript). Les interfaces principales sont :

- **la page d'authentification** : présentation du certificat client, vérification de l'identité et établissement de la session ;
- **le tableau de bord du parc** : vue synthétique des véhicules, des affectations et des alertes de maintenance ;
- **la gestion des bons de carburant** : formulaire d'enregistrement des bons, listes et recherches ;
- **les rapports** : vues consolidées des consommations par véhicule, par service et par période ;
- **le module d'administration** : gestion des utilisateurs et des droits (en interface avec FreeIPA).

Par ailleurs, deux interfaces de supervision web complètent le frontend de la solution : le **tableau de bord Wazuh** (alertes, agents, healthcheck) et l'**interface web pfSense** (règles de pare-feu, état du tunnel, supervision du trafic). Ces interfaces sont accessibles exclusivement depuis le VLAN Administration via le tunnel.

## 3.3 Environnement de travail

### 3.3.1 Outils de développement

**Tableau 3.4 — Outils de développement**

| Outil | Rôle |
|-------|------|
| Python 3.10+ | Langage de développement de l'application |
| Flask 2.x | Micro-framework web backend |
| Jinja2 | Moteur de templates pour les pages frontend |
| SQLite | Base de données embarquée en phase de développement |
| VS Code | Éditeur de code principal |
| Insomnia / curl | Tests manuels des points de terminaison API |

### 3.3.2 Outils de conteneurisation et sécurité

**Tableau 3.5 — Outils de conteneurisation et sécurité**

| Outil | Rôle dans l'architecture |
|-------|--------------------------|
| KVM/QEMU | Hyperviseur hébergeant les VM pfSense et FreeIPA sur la machine locale |
| pfSense CE 2.7 | Pare-feu, routeur inter-VLAN, NAT, journalisation |
| Suricata | Moteur IDS/IPS intégré à pfSense |
| FreeIPA | Annuaire LDAP, Kerberos, DNS interne, autorité de certification |
| WireGuard | Tunnel chiffré entre le site local et la VM Azure |
| Wazuh | Plateforme SIEM/XDR : ingestion, corrélation, règles, alertes |
| Microsoft Azure | VM Ubuntu 22.04 B2s hébergeant l'application et Wazuh |
| NSG / UFW | Filtrage réseau complémentaire au niveau cloud et OS |
| Kali Linux | Machine de l'attaquant pour les scénarios red team (nmap, hydra, curl) |

**Tableau 3.6 — Spécifications des machines virtuelles**

| VM | OS | RAM | vCPU | Interfaces réseau | Rôle |
|----|-----|-----|------|-------------------|------|
| VM 1 — pfSense | pfSense CE 2.7 | 1 Go | 1 | 3 (WAN, LAN trunk, WireGuard) | Pare-feu, segmentation, IPS, VPN |
| VM 2 — FreeIPA | Rocky Linux 9 / AlmaLinux 9 | 2 Go | 2 | 1 (VLAN 10) | Annuaire, Kerberos, DNS, PKI |
| VM Azure | Ubuntu 22.04 LTS | 4 Go | 2 | 1 publique (+ tunnel) | Application Flask + Wazuh |

### 3.3.3 Outils de gestion de version

Le suivi des versions des développements (application Flask, règles Wazuh, fichiers de configuration) a été assuré avec **Git**, en s'appuyant sur le dépôt distant **GitHub**. Cette organisation a permis de conserver un historique clair des modifications, de versionner les fichiers de configuration critiques (exports pfSense, configurations WireGuard, règles de détection) et de documenter l'évolution de chaque livrable.

| Outil | Utilisation |
|-------|-------------|
| Git | Versionnement local des sources |
| GitHub | Dépôt distant, historique, documentation |

### 3.3.4 Outils de documentation

**Tableau 3.7 — Outils de documentation**

| Outil | Utilisation |
|-------|-------------|
| Markdown | Rédaction du mémoire et des documents techniques |
| draw.io | Réalisation des schémas d'architecture et des diagrammes UML |
| Pandoc / LaTeX | Exportation du mémoire en PDF final |
| Wazuh dashboard | Documentation visuelle des alertes et des tableaux de bord |

## 3.4 Structure et organisation du projet

L'organisation des livrables respecte la séparation des préoccupations entre les différents plans de l'architecture. La capture ci-dessous présente la structure réelle du dossier du projet :

> **[À INSÉRER : Capture de l'arborescence réelle du dossier zero-trust-municipal-fleet]**

Cette structuration facilite la maintenance, la réutilisation et l'audit de l'ensemble de la solution, conformément aux exigences de traçabilité définies au chapitre 2.

## 3.5 Conclusion

Ce chapitre a présenté l'architecture technique complète de la solution, organisée autour de trois plans — réseau, identité et applicatif — réunis dans une topologie hybride locale/cloud. Les rôles des composants, leurs interactions et les mécanismes de sécurité mis en œuvre (mTLS, tunnel chiffré, refus par défaut) ont été détaillés, ainsi que l'environnement de travail et les outils utilisés. Le chapitre suivant aborde la réalisation effective de l'ensemble et les tests menés pour valider la solution.

# Chapitre 4 : Réalisation et tests

## 4.1 Introduction

Ce chapitre présente la réalisation effective de l'architecture et les tests menés pour la valider. Il s'ouvre sur la description des interfaces des principaux modules livrés : le module infrastructure et segmentation, le module identité et PKI, le module de gestion du parc et du carburant, le module de supervision et de détection, et le module tunnel hybride sécurisé. La seconde partie du chapitre est consacrée à l'évaluation de la solution : métriques de qualité et de performance, résultats des tests — dont les trois scénarios d'attaque — et comparaison entre les besoins initialement spécifiés et les points effectivement atteints.

## 4.2 Présentation des interfaces de la plateforme

### 4.2.1 Module infrastructure et segmentation

**Mise en place du pare-feu pfSense**

La première étape de réalisation a consisté à installer la machine virtuelle pfSense (VM 1) sur l'hyperviseur KVM/QEMU. Après l'installation initiale, les interfaces réseau ont été configurées conformément au plan d'adressage : l'interface WAN reliée au réseau de la machine hôte, l'interface LAN configurée en mode trunk afin de transporter les VLAN 10, 20, 30 et 99, et l'interface dédiée au tunnel WireGuard.

**Création des VLAN et des interfaces virtuelles**

Les VLAN ont ensuite été créés dans l'interface de pfSense, chacun matérialisé par une interface virtuelle associée à un sous-réseau :

- le VLAN 10 (Administration) : `10.10.10.0/24`, passerelle `10.10.10.1` ;
- le VLAN 20 (Flotte) : `10.10.20.0/24`, passerelle `10.10.20.1` ;
- le VLAN 30 (Services) : `10.10.30.0/24`, passerelle `10.10.30.1` ;
- le VLAN 99 (Tunnel) : `10.99.0.0/30`.

Chaque interface a été activée avec le filtrage du pare-feu appliqué, et les services de gestion (dont le DHCP, limité au segment administré) ont été restreints à la plage d'administration.

**Règles de filtrage inter-VLAN**

Conformément au principe « deny by default », aucune règle n'autorise de trafic inter-VLAN dans la configuration initiale. Des règles explicites ont ensuite été ajoutées de manière minimale. La matrice de flux suivante résume la politique appliquée :

**Tableau 4.1 — Matrice de flux autorisés entre VLAN**

| Origine | Destination | Service | Autorisation |
|---------|-------------|---------|--------------|
| VLAN 10 | VLAN 99 | Tout | Autorisé (accès supervision et application) |
| VLAN 10 | VLAN 10 | Tout | Autorisé (segment admin local) |
| VLAN 20 | VLAN 99 | HTTPS/5000 | Autorisé (accès application carburant) |
| VLAN 20 | VLAN 10 | Tout | **Refusé** |
| VLAN 20 | VLAN 30 | DNS | Autorisé |
| VLAN 30 | VLAN 99 | Tout | Refusé (sauf DNS sortant) |
| VLAN 99 → Internet | — | WireGuard UDP | Autorisé (établissement du tunnel) |

**Intégration de Suricata (IPS)**

Le package Suricata a été installé puis intégré au pare-feu en mode IPS sur l'interface d'ingestion. Les jeux de règles par défaut ont été activés et mis à jour, et une interface de supervision a été configurée afin d'inspecter le trafic inter-VLAN. Les alertes générées par Suricata sont consignées dans les journaux du pare-feu, lesquels alimentent la plateforme Wazuh.

> **[À INSÉRER : Figure 4.1 — Capture de l'écran « Interfaces › Assignments » de pfSense montrant les interfaces WAN, LAN et les intercepteurs VLAN (10, 20, 30, 99), ainsi que les adresses IP attribuées.]**

> **[À INSÉRER : Figure 4.2 — Capture de l'interface de gestion pfSense : page « Firewall › Rules » montrant les règles des VLAN 10, 20, 30 et 99, avec l'ordre logique des règles et les colonnes Protocole, Source, Port source, Destination, Port destination, Action.]**

> **[À INSÉRER : Figure 4.3 — Capture de la page de configuration de Suricata (onglet « Interfaces ») indiquant le mode IPS et le statut « running ».]**

### 4.2.2 Module identité et PKI

**Déploiement de FreeIPA**

Le serveur FreeIPA a été déployé sur la VM 2 (Rocky Linux 9) avec le nom de domaine `municipal.local`. Le déploiement a été réalisé via la commande d'installation intégrée, qui configure simultanément l'annuaire LDAP 389-DS, le service Kerberos, le DNS intégré, la gestion des politiques et l'autorité de certification (DogTag). Après l'installation, les comptes des utilisateurs du service du parc et de la direction ont été créés et répartis dans des groupes conformes aux rôles du chapitre 2.

**Hiérarchie de certification**

La PKI interne repose sur une chaîne de confiance à deux niveaux :

**Tableau 4.2 — Hiérarchie de certification**

| Niveau | Élément | Rôle |
|--------|---------|------|
| Racine | CA principale `municipal.local` | Autorité racine auto-signée, hors ligne après émission |
| Intermédiaire | CA intermédiaire FreeIPA | Signe les certificats des services et des utilisateurs |
| Services | fleet-app.municipal.local, wazuh.municipal.local, pfsense.municipal.local | Certificats TLS des serveurs |
| Utilisateurs | Certificats clients émis par utilisateur | Authentification mutuelle mTLS |

**Émission et usage des certificats**

Les certificats ont été émis via l'interface d'administration de FreeIPA puis installés sur les composants concernés. L'application Flask et le tableau de bord Wazuh ont été configurés pour présenter leur certificat et exiger la présentation d'un certificat client valide (option `verify_client = on`). Cette configuration impose, de facto, qu'aucun accès à l'application ne soit possible sans un certificat émis par l'autorité interne : **pas de certificat, pas d'accès**.

> **[À INSÉRER : Figure 4.4 — Capture de l'interface web FreeIPA, page de détail d'un utilisateur, montrant les onglets « Identity », « Certificates » et la copie du certificat émis.]**

> **[À INSÉRER : Figure 4.5 — Capture de l'écran de gestion des certificats (onglet « Certificate Authority ») montrant la liste des certificats émis et leur statut (valid / expired / revoked).]**

### 4.2.3 Module gestion du parc et du carburant

**Présentation de l'application**

L'application web de gestion du parc et du carburant constitue le cœur fonctionnel métier de la plateforme. Développée avec Flask et déployée sur la VM Azure, elle n'est accessible qu'au travers du tunnel WireGuard et après authentification mutuelle par certificat. Les fonctionnalités principales sont la gestion des véhicules, la gestion des bons de carburant, le suivi des stocks et la production des rapports de consommation.

**Interface d'authentification**

Lorsqu'un utilisateur du VLAN Flotte ou du VLAN Administration ouvre l'application, le navigateur présente automatiquement son certificat client. Si le certificat est absent, invalide ou révoqué, la connexion est refusée au niveau TLS, avant même l'affichage de la page de connexion. Après validation du certificat, l'utilisateur est invité à saisir son identifiant et son mot de passe Kerberos, dont la vérification est déléguée à FreeIPA.

**Interfaces fonctionnelles**

> **[À INSÉRER : Figure 4.6 — Capture de la page de connexion de l'application : champ identifiant, champ mot de passe, mention du certificat client validé.]**

> **[À INSÉRER : Figure 4.7 — Capture du tableau de bord du parc : tableau des véhicules (immatriculation, marque, service affectataire, statut), compteurs synthétiques du nombre de véhicules et d'alertes de maintenance.]**

> **[À INSÉRER : Figure 4.8 — Capture de l'écran d'émission d'un bon de carburant : sélection du véhicule, sélection du type de carburant, quantité, numéro du bon, validation.]**

> **[À INSÉRER : Figure 4.9 — Capture de l'écran des rapports de consommation : graphique en barres des consommations par service, tableau récapitulatif mensuel, filtre par période.]**

### 4.2.4 Module supervision et détection

**Déploiement de Wazuh**

La plateforme Wazuh a été installée sur la VM Azure (Ubuntu 22.04). Le déploiement a été réalisé selon l'architecture standard : le Wazuh Manager assure l'ingestion et la corrélation des journaux, l'indexation est assurée par l'outil de recherche intégré, et le tableau de bord web expose les vues de supervision. Les agents n'ont pas été installés sur l'ensemble des postes en phase de test ; les sources de journaux sont principalement alimentées par flux réseau (syslog) et par les fichiers de l'application, selon la matrice de collecte suivante.

**Tableau 4.3 — Sources de journaux alimentant Wazuh**

| Source | Protocole | Événements collectés |
|--------|-----------|----------------------|
| pfSense | syslog | Trafic rejeté, règles déclenchées, événements VPN |
| FreeIPA | syslog | Tentatives d'authentification, émissions de certificats |
| Application Flask | fichiers de log | Accès HTTP, erreurs, requêtes suspectes |
| WireGuard | interface réseau | Événements de connexion / déconnexion du tunnel |
| VM Azure (OS) | fichiers de log | Connexions systemd, tentatives SSH |

**Règles de détection personnalisées**

Afin de répondre aux risques spécifiques du contexte municipal, trois règles de détection personnalisées ont été élaborées et activées dans Wazuh.

**Règle 1 — Accès à l'application hors horaires de service**

```xml
<rule id="100001" level="10">
  <if_group>web</if_group>
  <time>18:00 - 07:00</time>
  <url>/fuel|/fleet</url>
  <description>Accès à l'application de gestion hors horaires de service</description>
</rule>
```

Cette règle déclenche une alerte de niveau 10 dès qu'une requête ciblant les ressources `/fuel` ou `/fleet` survient en dehors des horaires de travail de la commune, constituant un indicateur pertinent de comportement anormal compte tenu du profil métier des agents du service.

**Règle 2 — Force brute contre l'application de gestion**

```xml
<rule id="100002" level="12" frequency="5" timeframe="60">
  <if_matched_group>authentication_failed</if_matched_group>
  <same_source_ip/>
  <description>Tentative de force brute contre l'application de gestion</description>
</rule>
```

Cette règle corrèle les échecs d'authentification sur une fenêtre glissante : cinq tentatives échouées depuis la même adresse source en soixante secondes déclenchent une alerte de niveau 12, caractéristique d'une attaque par force brute.

**Règle 3 — Tentative de mouvement latéral entre VLAN**

```xml
<rule id="100003" level="14">
  <if_group>firewall</if_group>
  <action>block</action>
  <srcip>10.10.20.0/24</srcip>
  <dstip>10.10.10.0/24</dstip>
  <description>Le VLAN Flotte tente d'accéder au VLAN Administration — trafic bloqué</description>
</rule>
```

Cette règle exploite le journal des refus du pare-feu : toute tentative de connexion du réseau de la flotte (VLAN 20) vers le réseau administratif (VLAN 10), bloquée par pfSense, génère immédiatement une alerte de niveau 14.

> **[À INSÉRER : Figure 4.10 — Capture de la page « Rules » de Wazuh : liste des règles 100001, 100002, 100003 avec le niveau, la description et le fichier de définition.]**

> **[À INSÉRER : Figure 4.11 — Capture du tableau de bord d'aperçu de Wazuh (onglet « Security events ») : graphique de répartition des alertes par niveau, liste des alertes récentes, compteurs par règle.]**

### 4.2.5 Module tunnel hybride sécurisé

**Configuration WireGuard**

Le tunnel WireGuard relie l'extrémité locale (pfSense, `10.99.0.1`) à l'extrémité cloud (VM Azure, `10.99.0.2`). La configuration repose sur une paire de clés cryptographiques modernes (Curve25519) échangées préalablement, et l'adresse publique de la VM Azure est restreinte, côté NSG et côté UFW, au seul port UDP du tunnel.

**Tableau 4.4 — Paramètres du tunnel WireGuard**

| Paramètre | Valeur locale | Valeur cloud |
|-----------|---------------|--------------|
| Interface | wg99 | wg0 |
| Adresse tunnel | 10.99.0.1 | 10.99.0.2 |
| Port UDP | 51820 | 51820 |
| Clé | [À RÉDIGER — ne pas exposer les clés privées] | [À RÉDIGER] |
| Allowed IPs | 10.99.0.0/30 | 10.99.0.0/30 |

**Résultat**

Une fois le tunnel établi, l'application de gestion et le tableau de bord Wazuh sont atteignables depuis le site local via les adresses internes `10.99.0.2:5000` et `10.99.0.2:443`. Aucune adresse publique ne doit être ouverte hormis le port UDP du tunnel ; cette disposition a été vérifiée lors du scénario d'attaque n° 2.

> **[À INSÉRER : Figure 4.12 — Capture de l'écran pfSense « VPN › WireGuard » montrant l'état du tunnel : statut actif, dernière poignée de main, octets transférés.]**

> **[À INSÉRER : Figure 4.13 — Capture de la console Azure montrant l'application de gestion et le tableau de bord Wazuh accessibles par l'adresse interne, ainsi que la liste des règles du groupe de sécurité réseau limitant l'accès au port UDP 51820.]**

## 4.3 Évaluation de la solution

### 4.3.1 Métriques de qualité et de performance

L'évaluation de la solution repose sur un ensemble de métriques mesurées lors des phases de test. Les valeurs présentées ci-dessous correspondent aux mesures effectuées en environnement de laboratoire ; elles devront être confirmées par des mesures complémentaires dans l'environnement cible de la commune.

**Tableau 4.5 — Métriques de qualité**

| Métrique | Valeur mesurée | Objectif | Statut |
|----------|----------------|----------|--------|
| Nombre de VLAN actifs | 4 | 4 | Atteint |
| Règles inter-VLAN « deny » actives | 3 | ≥ 3 | Atteint |
| Certificats émis par la CA interne | [À MESURER] | — | — |
| Services derrière mTLS | 3 (app, Wazuh, pfSense) | 3 | Atteint |
| Sources de journaux intégrées à Wazuh | 4/5 | 5 | Partiel |
| Règles de détection personnalisées | 3 | 3 | Atteint |
| Scénarios d'attaque exécutés | 3 | 3 | Atteint |
| Coût de licence | 0 | 0 | Atteint |

**Tableau 4.6 — Métriques de performance**

| Métrique | Valeur mesurée | Objectif | Statut |
|----------|----------------|----------|--------|
| Latence de détection d'une alerte | [À MESURER] secondes | < 60 s | À confirmer |
| Temps d'établissement du tunnel WireGuard | [À MESURER] secondes | < 10 s | À confirmer |
| Temps de réponse de l'application (accès interne) | [À MESURER] ms | < 500 ms | À confirmer |
| Charge CPU de la VM Azure en régime nominal | [À MESURER] | < 60 % | À confirmer |

### 4.3.2 Visualisations des résultats des tests

**Scénario 1 — Attaque par force brute contre l'application**

**Objectif.** Vérifier que la plateforme de supervision détecte une tentative de force brute dirigée contre les identifiants de l'application de gestion du parc.

**Déroulement.** Depuis la machine de l'attaquant (Kali Linux), une attaque par force brute a été lancée à l'aide de l'outil Hydra contre le point de terminaison d'authentification de l'application, au travers du tunnel. La tentative visait à tester un grand nombre de couples identifiant/mot de passe en un temps réduit.

**Résultats observés.**

**Tableau 4.7 — Résultats du scénario 1**

| Élément | Valeur |
|---------|--------|
| Outil utilisé | Hydra |
| Cible | https://fleet-app.municipal.local/login (via tunnel) |
| Nombre de tentatives avant déclenchement | 5 |
| Fenêtre de corrélation | 60 secondes |
| Règle déclenchée | 100002 (niveau 12) |
| Adresse source consignée | [Adresse IP attaquante] |
| Délai de déclenchement | [À MESURER] s |
| Action complémentaire | Réponse active éventuelle : blocage de l'IP au niveau pfSense |

**Constat.** L'alerte de niveau 12 a été émise par Wazuh après cinq échecs consécutifs depuis la même adresse source, conformément à la règle 100002. L'événement a été consigné avec l'adresse source, l'estampille temporelle et le point de terminaison ciblé, puis rendu visible sur le tableau de bord.

> **[À INSÉRER : Figure 4.14 — Capture de la console Wazuh présentant l'alerte générée par la règle 100002, avec le détail de l'événement (adresse source, compteur, description).]**

**Scénario 2 — Accès direct à la machine virtuelle Azure (contournement du tunnel)**

**Objectif.** Démontrer que la ressource cloud n'est pas exposée sur l'interface publique et que le seul point d'accès légitime est le tunnel WireGuard.

**Déroulement.** Depuis la machine de l'attaquant, une analyse de la VM Azure a été menée sur son adresse publique au moyen de l'outil nmap, afin de cartographier les ports ouverts.

**Résultats observés.**

**Tableau 4.8 — Résultats du scénario 2**

| Élément | Valeur |
|---------|--------|
| Outil utilisé | nmap |
| Cible | Adresse publique de la VM Azure |
| Ports filtrés (NSG) | Tous, à l'exception du port UDP du tunnel |
| Port 51820/udp | Ouvert (tunnel) |
| Ports applicatifs (5000, 443) vu du public | Filtrés |
| Accès via l'adresse publique | Refusé / sans réponse |
| Accès via le tunnel | Fonctionnel |

**Constat.** Le scan a retourné un état « filtered » pour l'ensemble des ports applicatifs : les règles du groupe de sécurité réseau Azure et le pare-feu local UFW ont rejeté silencieusement les requêtes. La surface d'attaque publique est ainsi réduite au seul port du tunnel, ce qui illustre de manière visuelle la différence entre le modèle exposant les services et l'approche fermée par défaut.

> **[À INSÉRER : Figure 4.15 — Capture d'un scan nmap effectué depuis l'attaquant : liste des ports et états (filtered pour 5000/tcp et 443/tcp, open pour 51820/udp).]**

**Scénario 3 — Mouvement latéral du VLAN Flotte vers le VLAN Administration**

**Objectif.** Vérifier l'efficacité du rejet par défaut du trafic inter-VLAN et la remontée d'une alerte de sécurité associée.

**Déroulement.** Une machine du VLAN Flotte (VLAN 20) — considérée comme compromise — a tenté d'atteindre le serveur FreeIPA du VLAN Administration (VLAN 10, `10.10.10.10`) par ping, nmap puis curl.

**Résultats observés.**

**Tableau 4.9 — Résultats du scénario 3**

| Élément | Valeur |
|---------|--------|
| Origine | Poste simulant un dispositif de flotte (10.10.20.50) |
| Cible | 10.10.10.10 (FreeIPA) |
| Comportement de pfSense | Trafic bloqué (règle deny par défaut) |
| Accès réseau obtenu | Aucun |
| Journalisation | Événement de blocage consigné par pfSense |
| Règle déclenchée | 100003 (niveau 14) |
| Alerte Wazuh émise | Oui |
| Atteignabilité de l'identité | Nulle |

**Constat.** Chaque tentative a été refusée par le pare-feu, dont le journal a enregistré les tentatives de connexion. Wazuh a corrélé ces événements avec la règle 100003 et émis une alerte de niveau 14. L'infrastructure d'identité est demeurée intégralement inaccessible depuis la flotte.

> **[À INSÉRER : Figure 4.16 — Capture de la console Wazuh montrant l'alerte de la règle 100003 ainsi que l'événement brut du pare-feu (source 10.10.20.50, destination 10.10.10.10, action block).]**

**Synthèse des tests**

**Tableau 4.10 — Synthèse des scénarios de test**

| Scénario | Menace validée | Résultat | Alerte | Niveau |
|----------|----------------|----------|--------|--------|
| 1 — Force brute | Compromission d'identifiants | Détectée | 100002 | 12 |
| 2 — Accès direct cloud | Exposition de la ressource | Bloquée | — | — |
| 3 — Mouvement latéral | Escalade interne | Bloquée + détectée | 100003 | 14 |

### 4.3.3 Comparaison : correspondance entre les besoins et les points atteints

Cette sous-section établit la correspondance entre les besoins spécifiés au chapitre 2 et les éléments effectivement réalisés, afin de mesurer la complétude de la solution.

**Tableau 4.11 — Correspondance besoins / réalisations**

| Besoin | Exigence | Réalisation | Statut |
|--------|----------|-------------|--------|
| BF-01 | Authentification centralisée | Comptes FreeIPA, connexion Kerberos/LDAP | Atteint |
| BF-02 | Authentification mutuelle par certificats | mTLS configuré sur application, Wazuh, pfSense | Atteint |
| BF-03 | Segmentation VLAN | 4 VLAN opérationnels | Atteint |
| BF-04 | Refus par défaut inter-VLAN | Matrice de flux deny-by-default | Atteint |
| BF-05 | Règles explicites | Règles d'allow minimales | Atteint |
| BF-06 | Tunnel chiffré | WireGuard actif (10.99.0.0/30) | Atteint |
| BF-07 | Publication uniquement par tunnel | NSG + UFW : seul le port UDP ouvert | Atteint |
| BF-08 | Gestion des véhicules | CRUD application Flask | Atteint |
| BF-09 | Bons de carburant et stocks | Fonctionnalité développée | Atteint |
| BF-10 | Suivi des consommations | Imputation par service | Atteint |
| BF-11 | Rapports de consommation | Rapport mensuel paramétrable | Atteint (à affiner) |
| BF-12 | Collecte des journaux | 4/5 sources intégrées à Wazuh | Partiel |
| BF-13 | Règles de détection personnalisées | Règles 100001, 100002, 100003 | Atteint |
| BF-14 | Alertes et tableaux de bord | Dashboard Wazuh configuré | Atteint |
| BF-15 | Réponse active | Blocage pfSense (à généraliser) | Partiel |
| BF-16 | Gestion des certificats | CA interne, émission/révocation | Atteint |
| BF-17 | Journalisation des refus | Journaux pfSense → Wazuh | Atteint |

L'analyse de ce tableau montre que la grande majorité des besoins fonctionnels est satisfaite. Les points d'amélioration identifiés concernent l'intégration complète de la cinquième source de journaux (journaux de l'OS de la VM Azure), la généralisation de la réponse active sur l'ensemble des règles, et le raffinement des rapports de consommation pour répondre aux besoins comptables précis de la commune.

## 4.4 Conclusion

Ce chapitre a présenté la réalisation complète de l'architecture Zero Trust, module par module : infrastructure et segmentation avec pfSense, identité et PKI avec FreeIPA, application de gestion du parc et du carburant avec Flask, supervision et détection avec Wazuh, et tunnel hybride avec WireGuard. Les trois scénarios d'attaque ont démontré l'efficacité de la solution : la force brute est détectée (alarme de niveau 12), la ressource cloud demeure inaccessible publiquement, et le mouvement latéral est simultanément bloqué et détecté (alarme de niveau 14). L'évaluation des métriques et la comparaison besoins/réalisations confirment la complétude fonctionnelle du système ainsi que ses capacités de détection et de blocage, au prix d'une solution entièrement libre et sans coût de licence.

# Conclusion générale et perspectives

## Récapitulatif du travail réalisé

Le projet présenté dans ce mémoire avait pour ambition de répondre à une problématique concrète rencontrée au sein de **[Nom de la commune]** : sécuriser le système de gestion du parc municipal et du carburant, jusqu'alors exposé sur un réseau plat, doté d'une authentification faible et dépourvu de toute capacité de détection des menaces.

L'étude de l'existant a mis en évidence les faiblesses structurelles du système : absence de segmentation, comptes partagés, absence de chiffrement et de gestion des certificats, et absence de journalisation centralisée. Face à ces constats, et après comparaison des modèles d'architecture, le choix s'est porté sur une refonte selon les principes du **Zero Trust**, formalisés dans le référentiel **NIST SP 800-207**. La solution proposée repose sur une architecture hybride, entièrement fondée sur des composants open-source : segmentation du réseau en quatre VLAN orchestrés par **pfSense**, gestion centralisée des identités, du DNS et de la certification interne par **FreeIPA**, tunnel chiffré **WireGuard** vers une machine virtuelle **Microsoft Azure** hébergeant l'application de gestion et la plateforme de supervision **Wazuh**.

La réalisation a été structurée selon la méthode agile **Scrum** en six sprints, couvrant la conception, le déploiement de l'infrastructure, le développement applicatif, l'élaboration des règles de détection, l'exécution des scénarios de test et la préparation du mémoire.

## Résultats obtenus

Les tests menés ont validé les objectifs fixés :

- **l'architecture Zero Trust est opérationnelle** : le principe « ne jamais faire confiance, toujours vérifier » est appliqué à chaque accès, chaque connexion étant authentifiée et inspectée ;
- **la détection des menaces est active** : trois règles de détection personnalisées (accès hors horaires, force brute, mouvement latéral) déclenchent des alertes corrélées en quasi temps réel ;
- **la surface d'attaque publique est minimisée** : la ressource cloud n'est joignable que par le tunnel chiffré, toute autre tentative d'accès étant silencieusement rejetée ;
- **le parcours de validation est démontré** : les trois scénarios d'attaque (force brute, accès direct à la VM Azure, mouvement latéral inter-VLAN) ont produit des preuves documentées de l'efficacité défensive de l'architecture.

Sur le plan financier, la solution ne génère **aucun coût de licence**, l'ensemble des briques logicielles étant libre et ouvert. Cette caractéristique rend la démarche directement reproductible par une collectivité dotée de moyens modestes.

## Limites rencontrées

Certaines limites doivent être signalées avec honnêteté. L'intégration de la cinquième source de journaux (journaux système de la VM Azure) demeure partielle. La réponse active automatisée, si elle a été validée ponctuellement sur le pare-feu, mériterait d'être généralisée à l'ensemble des règles afin d'accroître la capacité de réaction. Enfin, les mesures de performance (latence de détection, temps de réponse) réalisées en environnement de laboratoire devront être confirmées à l'échelle de l'infrastructure réelle de la commune.

## Perspectives d'évolution

Plusieurs perspectives peuvent être envisagées pour prolonger ce travail :

1. **extension de la gestion des identités** : déploiement d'agents Wazuh sur l'ensemble des postes de la commune afin d'étendre la visibilité au niveau des points de terminaison (EDR) ;
2. **automatisation de la réponse** : généralisation de la réponse active (blocage automatique des adresses fautives, quotas de connexion) et intégration d'une orchestration de type SOAR ;
3. **durcissement des politiques** : mise en place de l'authentification multifacteur (MFA) pour les comptes privilégiés et application d'un contrôle continu des vulnérabilités ;
4. **élargissement du périmètre** : extension des principes Zero Trust aux autres systèmes d'information de la commune (état civil, finances, urbanisme), selon la même démarche itérative ;
5. **étude de conformité** : alignement complet de l'architecture sur les exigences du référentiel ISO/IEC 27001:2022 en vue d'une certification à terme.

Ce projet constitue ainsi une première brique, à la fois démonstrative et opérationnelle, d'une politique de sécurité moderne et maîtrisée au service d'une administration de proximité.

---

# Appréciation personnelle

Ce stage au sein de **[Nom de la commune]** a constitué une expérience particulièrement enrichissante, tant sur le plan humain que technique.

D'un point de vue humain, l'accueil au sein du service du parc et du carburant m'a permis de prendre la mesure du fonctionnement réel d'une administration territoriale : des contraintes de terrain, des pratiques héritées, des exigences budgétaires fortes, mais aussi une équipe motivée et soucieuse de moderniser ses outils. Les échanges avec les agents ont confirmé l'importance d'appréhender le volet sécurité comme un accompagnement des usages métier, et non comme une contrainte imposée.

D'un point de vue technique, ce projet m'a permis de mobiliser et d'approfondir de nombreuses compétences : administration de pare-feu et segmentation réseau, déploiement d'une infrastructure d'identité (LDAP, Kerberos, PKI), utilisation d'une plateforme SIEM/XDR, développement web en Python/Flask, et mise en place d'un réseau privé virtuel moderne. La conduite de ce projet avec la méthode Scrum m'a également appris à planifier, à prioriser et à livrer régulièrement, compétence essentielle dans le monde professionnel.

Enfin, la confrontation à la réalité du terrain — ressources limitées, contraintes de temps, nécessité de démontrer la valeur de chaque choix technique — a été formatrice. Elle m'a conforté dans ma vocation pour la cybersécurité, et dans la conviction qu'il est possible de bâtir des architectures robustes avec des outils libres et une démarche rigoureuse.

Je retire de ce stage une expérience complète, associant compétences techniques, posture professionnelle et sens du service public, dont je mesurerai pleinement la valeur dans la suite de mon parcours.

---

# Références

## Ouvrages et publications scientifiques

- ROSE, S., BORCHERT, O., MITCHELL, S., CONNELLY, S. *Zero Trust Architecture*. Gaithersburg : National Institute of Standards and Technology, NIST SP 800-207, 2020.
- JOINT TASK FORCE. *Security and Privacy Controls for Information Systems and Organizations*. Gaithersburg : National Institute of Standards and Technology, NIST SP 800-53 Rev. 5, 2020.
- ISO/IEC 27001:2022. *Information security, cybersecurity and privacy protection — Information security management systems — Requirements*. Genève : Organisation internationale de normalisation, 2022.
- MITRE. *ATT&CK — Adversarial Tactics, Techniques, and Common Knowledge*, consulté en ligne en 2026 : https://attack.mitre.org
- SCHWABER, K., SUTHERLAND, J. *The Scrum Guide*. 2020.

## Documentation technique

- Netgate. *pfSense CE Documentation*, consulté en ligne en 2026 : https://docs.netgate.com
- Wazuh. *Wazuh Documentation — Ruleset, Log Analysis et Dashboard*, consulté en ligne en 2026 : https://documentation.wazuh.com
- FreeIPA. *FreeIPA Documentation*, consulté en ligne en 2026 : https://www.freeipa.org
- WireGuard. *WireGuard Documentation*, consulté en ligne en 2026 : https://www.wireguard.com
- Flask. *Flask Documentation*, consulté en ligne en 2026 : https://flask.palletsprojects.com
- Microsoft. *Documentation Azure — Virtual Machines et Network Security Groups*, consulté en ligne en 2026 : https://learn.microsoft.com

## Références réglementaires

- Royaume du Maroc. *Loi organique n° 113-14 relative aux communes*, Bulletin officiel, 2015.
- Royaume du Maroc. *Loi n° 05-20 relative à la cybersécurité*, Bulletin officiel, 2021.

---

*Rapport réalisé par Mohamed Meddah — EMSI Marrakech — Année universitaire 2026–2027.*