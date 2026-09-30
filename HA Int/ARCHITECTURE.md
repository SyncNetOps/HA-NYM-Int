# 📐 Architektur- und Spezifikationsdokument

## Projekt: Nym Privacy Hub für Home Assistant (v1.0.9)

### 1. Systemarchitektur

Der **Nym Privacy Hub** folgt einem modernen, zweischichtigen Architekturmodell mit vollständiger Transparenz und integrierter Live-Telemetrie:

```text
+-------------------------------------------------------------------------+
|                       HOME ASSISTANT OS / SUPERVISED                    |
|                                                                         |
|  +-----------------------------------+  +----------------------------+  |
|  |     🎛️ CUSTOM COMPONENT (HACS)    |  |     🐳 ADD-ON (DOCKER)     |  |
|  |                                   |  |                            |  |
|  | - Config Flow & Options Flow      |  | - nym-socks5-client        |  |
|  | - Lovelace Custom Dashboard Card  |  |   (Port 1080)              |  |
|  | - Data Coordinator (Polling 30s)  |  | - Ingress Web Cockpit      |  |
|  | - Switches & Sensoren Suite       |  |   (Port 8099 / Sidebar)    |  |
|  | - Service Call Handlers           |  | - Live Throughput Canvas   |  |
|  |                                   |  | - SOCKS5 IP-Leak Check     |  |
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

### 2. Detaillierte Funktions- und Sicherheits-Spezifikation

#### 2.1 Sphinx Packet Format & Frame Consistency
* Jedes Datenpaket wird in exakt **2708 Bytes große, uniforme Sphinx-Frames** fragmentiert und mit mehreren Schichten asymmetrischer Kryptografie versehen.
* Dies eliminiert Größen-Fingerprinting und verhindert, dass Angreifer Rückschlüsse auf übertragene Datenmengen ziehen.
* Mixknoten entfernen jeweils nur die eigene äußere Krypto-Schicht, führen eine künstliche Verzögerung ein (Poisson Process) und mischen die Pakete unter fremden Datenverkehr.

#### 2.2 SOCKS5 Bridge Layer (Port `1080`)
* **Bind-Adresse**: `0.0.0.0:1080`
* **Protokoll**: SOCKS Version 5 (RFC 1928, RFC 1929)
* **Client-ID**: `ha_nym_client`
* **Persistenz**: Die Schlüsseldateien verbleiben dauerhaft unter `/data/.nym/socks5-clients/ha_nym_client/`.

#### 2.3 Ingress Web Cockpit Layer (Port `8099`)
* **Multi-Threaded Server**: `ThreadingHTTPServer` mit nativer Keep-Alive Unterstützung.
* **Live Throughput Chart**: 60 FPS HTML5 Canvas Graph für Payload Rate (KB/s) und Cover-Traffic Loops.
* **Live Streams Inspector**: Ringpuffer aktiver und kürzlicher Datenströme durch das Mixnet.
* **IP-Leak & Geo-Check**: Eingebauter SOCKS5 HTTP-Client zur Überprüfung der sichtbaren Exit-IP.
* **Passphrase-Manager**: Konfiguration und Verwaltung optionaler Mnemonics und Passphrasen.

---

### 3. Progressive Disclosure Matrix

| Feature | Einsteiger (Default Ansicht) | Profi (Advanced Options) |
|---|---|---|
| **Verbindung** | 1-Klick Start & Status-Badge | Gateway-Auswahl, Topologie-Details |
| **Schutzlevel** | 1-Klick Presets (Eco, High, Ultra) | Granularer Schieberegler (0–60 Pkt/min) |
| **Transparenz** | Live 3-Hop Route Visualizer | Krypto-Hop-Inspektor, Durchsatz-Graph & Stream-Tabelle |
| **Leak-Schutz** | Status-Anzeige | Live IP-Leak & Geo-Check Tool |
| **Schlüsselschutz**| Automatische Schlüsselpaare | Eigene Passphrase / Mnemonic Seed |
| **Integration** | Snippet-Generator | Eigene YAML Snippets & Service Calls |
