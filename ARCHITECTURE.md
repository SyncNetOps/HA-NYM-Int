# 📐 Architektur- und Spezifikationsdokument

## Projekt: Nym Privacy Hub für Home Assistant

### 1. Systemarchitektur

Der **Nym Privacy Hub** ist nach dem Prinzip der modularen Entkopplung aufgebaut:
1. **Engine Layer (Home Assistant Add-on)**: Verantwortlich für Netzwerkprozesse, Daemon-Management, Binary-Ausführung, Key-Storage im persistenten Speicher (`/data`) und SOCKS5 Socket-Bindung.
2. **Control & UI Layer (Custom Component)**: Verantwortlich für Benutzerinteraktion, Entitätsverwaltung (`sensor`, `switch`, `button`), Health Checks und Vermittlung von Proxy-Anfragen an Home Assistant Services.

---

### 2. Detaillierte Komponenten-Spezifikation

#### 2.1 HA Add-on (`nym_privacy_hub_addon`)
- **Base Image**: Alpine Linux / Debian-slim mit minimalem Footprint.
- **Binaries**: Offizieller `nym-socks5-client` (unterstützt x86_64, aarch64 für Raspberry Pi 4/5, armv7).
- **Konfiguration (`config.yaml`)**:
  - `host`: `0.0.0.0` / `127.0.0.1`
  - `port`: `1080` (SOCKS5 Proxy)
  - `provider`: Nym Exit Gateway Provider Address (Standardmäßig voreingestellte zuverlässige Exit-Nodes oder dynamisch gewählt via Explorer / Harbourmaster)
  - `use_reply_surbs`: Boolean (`true` für anonyme Antworten / SURBs)
  - `cover_traffic`: Schalter & Ratensteuerung
- **Persistenz**:
  - `/data/.nym`: Speicherung der generierten Identitäts-, Verschlüsselungs- und Gateway-Schlüssel, damit der Client bei Neustarts nicht neu registriert werden muss.

#### 2.2 Custom Component (`custom_components/nym_privacy_hub`)
- **Domain**: `nym_privacy_hub`
- **Config Flow**:
  - Auto-Erkennung des Add-ons via HA Supervisor API.
  - Test-Ping über SOCKS5-Proxy zur Verifikation der Mixnet-Konnektivität.
- **Entitäten**:
  - **Sensoren**:
    - `sensor.nym_mixnet_status` (`connected`, `connecting`, `disconnected`)
    - `sensor.nym_latency` (Round-trip Latenz in ms)
    - `sensor.nym_gateway_id` (Aktuell verbundenes Gateway)
    - `sensor.nym_proxy_endpoint` (`socks5://127.0.0.1:1080`)
  - **Switches (Einsteiger-Features)**:
    - `switch.nym_ai_voice_privacy` (Routet OpenAI/Anthropic/Voice Assistant Traffic)
    - `switch.nym_geo_weather_privacy` (Verschleiert Geodaten- & Wetterabfragen)
    - `switch.nym_cover_traffic` (Aktiviert konstantes Datenrauschen)
  - **Buttons**:
    - `button.nym_copy_proxy_url` (Kopiert Proxy-Adresse)
    - `button.nym_reconnect_mixnet` (Startet Verbindung mit neuem Mixnet-Pfad neu)
  - **Erweiterte Einstellungen (Option Flow für Profis)**:
    - Custom Exit Provider Address
    - Cover Traffic Multiplier / Delay Intervals
    - P2P Remote Ingress Setup

---

### 3. Progressive Disclosure Matrix

| Feature | Einsteiger (Default View) | Profi (Advanced Options) |
|---|---|---|
| **Verbindung** | 1-Klick Connect, Status-Badge | Gateway-Auswahl, Topologie-Details |
| **KI / LLM Privacy** | Einfacher Toggle | Selektive Domain-Filter & Header-Stripping |
| **Cover Traffic** | Einfacher Toggle | Traffic-Intensität, Paketintervall |
| **Remote Access** | N/A (deaktiviert) | SURB-basiertes Ingress & P2P Sync |
