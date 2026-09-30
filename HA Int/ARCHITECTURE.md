# 📐 Architektur- und Spezifikationsdokument

## Projekt: Nym Privacy Hub für Home Assistant (v1.1.1)

### 1. Systemarchitektur

Der **Nym Privacy Hub** folgt einem modernen, zweischichtigen Architekturmodell mit vollständiger Transparenz, dynamischem Home Assistant Entitäten-Scanner und automatischer weltweiter Exit-Rotation:

```text
+-------------------------------------------------------------------------+
|                       HOME ASSISTANT OS / SUPERVISED                    |
|                                                                         |
|  +-----------------------------------+  +----------------------------+  |
|  |     🎛️ CUSTOM COMPONENT (HACS)    |  |     🐳 ADD-ON (DOCKER)     |  |
|  |                                   |  |                            |  |
|  | - Config Flow & Options Flow      |  | - nym-socks5-client        |  |
|  | - Lovelace Custom Dashboard Card  |  |   (Port 1080)              |  |
|  | - Data Coordinator (Polling 30s)  |  | - Ingress Cockpit & 5 Tabs |  |
|  | - Switches & Sensoren Suite       |  |   (Port 8099 / Sidebar)    |  |
|  | - Service Call Handlers           |  | - HA Entity Scanner        |  |
|  |                                   |  | - Automated Exit Rotation  |  |
|  |                                   |  | - Live Throughput Canvas   |  |
|  |                                   |  | - SOCKS5 IP-Leak Check     |  |
|  |                                   |  | - Nym Premium VIP Engine   |  |
|  |                                   |  | - /data/.nym Key-Storage   |  |
|  +-----------------+-----------------+  +--------------+-------------+  |
|                    |                                   |                |
|                    +====== SOCKS5 / HA API ============+                |
+----------------------------------------+--------------------------------+
                                         |
                                         v
+-------------------------------------------------------------------------+
|                         🌐 NYM MIXNET TOPOLOGIE                         |
|                                                                         |
|      [Gateway] ──► [Mix Layer 1] ──► [Mix Layer 2] ──► [Mix Layer 3]   |
|                                                              │          |
|                                                              ▼          |
|  [Geschützte Ziele: LLMs / Wetter / Web] ◄── [Rotierende Exit-Nodes]    |
+-------------------------------------------------------------------------+
```

---

### 2. Spezifikation der erweiterten Kern-Funktionen

1. **🔍 Dynamischer HA Entitäten-Scanner**: Fragt über den Supervisor-Token (`/core/api/states`) die tatsächlich installierten Integrationen und Sensoren ab und ordnet sie den 6 Schutz-Kategorien zu.
2. **🔄 Automatische Exit-Node Rotation**: Tauscht im gewählten Intervall (z.B. alle 15 Minuten) den aktiven Exit-Node unter Beibehaltung der Verbindungsstabilität aus (Pools: Weltweit, Privacy-Haven, EU-Mix).
3. **💡 Integrierte Layman-Leitfäden**: Anschauliche Erläuterungen komplexer Mixnet-Konzepte für Einsteiger.
4. **💎 Nym Fast Pass & ZK-Bandbreite**: Verwaltung blinder Signaturen (Coconut zk-nyms) für priorisierten 100+ Mbps Datenverkehr.
