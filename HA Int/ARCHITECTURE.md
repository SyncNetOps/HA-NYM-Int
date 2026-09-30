# 📐 Architektur- und Spezifikationsdokument

## Projekt: Nym Privacy Hub für Home Assistant (v1.1.0)

### 1. Systemarchitektur

Der **Nym Privacy Hub** folgt einem modernen, zweischichtigen Architekturmodell mit vollständiger Transparenz, dynamischem Datenquellen-Routing und nativer Nym Premium Fast-Pass Integration:

```text
+-------------------------------------------------------------------------+
|                       HOME ASSISTANT OS / SUPERVISED                    |
|                                                                         |
|  +-----------------------------------+  +----------------------------+  |
|  |     🎛️ CUSTOM COMPONENT (HACS)    |  |     🐳 ADD-ON (DOCKER)     |  |
|  |                                   |  |                            |  |
|  | - Config Flow & Options Flow      |  | - nym-socks5-client        |  |
|  | - Lovelace Custom Dashboard Card  |  |   (Port 1080)              |  |
|  | - Data Coordinator (Polling 30s)  |  | - Ingress Cockpit & Tabs   |  |
|  | - Switches & Sensoren Suite       |  |   (Port 8099 / Sidebar)    |  |
|  | - Service Call Handlers           |  | - HA Data Source Router    |  |
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
|  [Geschützte Ziele: LLMs / Wetter / Web] ◄────── [Exit Gateway]         |
+-------------------------------------------------------------------------+
```

---

### 2. Spezifikation der 5 Ingress-Cockpit Module

1. **📊 Live Cockpit**: 3-Hop Route Visualizer mit Krypto-Hop-Inspektor, 60s Canvas Throughput Chart und Live Stream Tracking.
2. **🛡️ HA Datenquellen-Schutz**: Dynamischer Router für KI-Prompts, Wetter/GPS, Messenger-Bots, dynamische Strompreise, Cloud-Backups und generische Sensoren.
3. **⚙️ Mixnet Krypto & Feintuning**: Presets (Eco, High, Ultra), Poisson-Delay-Streuung (5–150 ms), SURB-Puffer (20–250 Tokens), DNS-over-Mixnet Isolation und weltweite Exit-Nodes.
4. **💎 Nym Premium & Fast Pass**: Verwaltung von Bandwidth Credentials, zk-nyms (Coconut blinde Signaturen), High-Speed 100+ Mbps Queues und Passphrase-Schutz.
5. **📋 YAML Vorlagen**: 1-Klick Code-Snippets für die direkte Einbindung in Home Assistant.
