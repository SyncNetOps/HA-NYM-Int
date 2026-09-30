# 📐 Architektur- und Spezifikationsdokument

## Projekt: Nym Privacy Hub für Home Assistant (v1.0.6)

### 1. Systemarchitektur

Der **Nym Privacy Hub** folgt einem modernen, zweischichtigen Architekturmodell:

```text
+-------------------------------------------------------------------------+
|                       HOME ASSISTANT OS / SUPERVISED                    |
|                                                                         |
|  +-----------------------------------+  +----------------------------+  |
|  |     🎛️ CUSTOM COMPONENT (HACS)    |  |     🐳 ADD-ON (DOCKER)     |  |
|  |                                   |  |                            |  |
|  | - Config Flow & Options Flow      |  | - nym-socks5-client        |  |
|  | - Lovelace Custom Dashboard Card  |  |   (Port 1080)              |  |
|  | - Data Coordinator (Polling 30s)  |  | - Ingress Web Dashboard    |  |
|  | - Switches & Sensoren Suite       |  |   (Port 8099 / Sidebar)    |  |
|  | - Service Call Handlers           |  | - /data/.nym Key-Storage   |  |
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

### 2. Detaillierte Funktions- und Sicherheits-Spezifikation

#### 2.1 Sphinx Packet Format
* Jedes Datenpaket wird in identisch große Sphinx-Pakete fragmentiert und mit mehreren Schichten asymmetrischer Kryptografie versehen.
* Mixknoten entfernen jeweils nur die äußerste Schicht, führen eine künstliche Verzögerung ein und mischen die Pakete unter fremden Datenverkehr.

#### 2.2 SOCKS5 Bridge Layer (Port `1080`)
* **Bind-Adresse**: `0.0.0.0:1080`
* **Protokoll**: SOCKS Version 5 (RFC 1928, RFC 1929)
* **Client-ID**: `ha_nym_client`
* **Persistenz**: Die Schlüsseldateien verbleiben dauerhaft unter `/data/.nym/socks5-clients/ha_nym_client/`.

#### 2.3 Ingress Web Cockpit Layer (Port `8099`)
* **Multi-Threaded Server**: `ThreadingHTTPServer` mit nativer Keep-Alive Unterstützung.
* **Diagnostik**: Live-Ping-Prüfung und SOCKS5-Handshake-Verifikation.
* **Passphrase-Manager**: Konfiguration und Verwaltung optionaler Mnemonics und Passphrasen.

---

### 3. Progressive Disclosure Matrix

| Feature | Einsteiger (Default Ansicht) | Profi (Advanced Options) |
|---|---|---|
| **Verbindung** | 1-Klick Start & Status-Badge | Gateway-Auswahl, Topologie-Details |
| **KI / LLM Privacy** | Einfacher Toggle | Selektive Domain-Filter & Anonyme Services |
| **Cover Traffic** | Einfacher Toggle | Traffic-Intensität (1–120 Pakete/min) |
| **Schlüsselschutz**| Automatische Schlüsselpaare | Eigene Passphrase / Mnemonic Seed |
| **Automatisierung**| Lovelace Dashboard Card | Home Assistant Services (`send_anonymous_request`) |
