# 🛡️ Home Assistant Add-on: Nym Privacy Hub

Der **Nym Privacy Hub** ist die offizielle All-in-One-Lösung, um deine gesamte Home Assistant Installation über das dezentrale **Nym Mixnet** vor Netzwerküberwachung, Metadaten-Tracking und Timing-Analysen abzusichern.

---

## 🌟 Warum Nym Mixnet statt herkömmlichem VPN?

Klassische VPNs verschlüsseln zwar den Datenstrom, leiten aber alle Daten über einen zentralen Server. Internet-Provider oder staatliche Akteure können anhand von **Paketgrößen und Zeitstempeln (Timing-Attacks)** genau analysieren, wann du im Smart Home Lichter schaltest, Sprachbefehle gibst oder das Haus verlässt.

### 🛡️ Die Nym-Vorteile auf einen Blick:
1. **Sphinx-Mehrschichtverschlüsselung**: Jedes Datenpaket wird in mehrere kryptografische Schichten gehüllt – kein Knoten kennt gleichzeitig Sender und Ziel.
2. **Dezentrale 3-Layer-Mixknoten**: Pakete werden über unabhängige globale Mixnodes gemischt, verzögert und in zufälliger Reihenfolge weitergeleitet.
3. **Anti-Einbruchs Cover Traffic**: Generiert künstliches Hintergrundrauschen, sodass niemand am Router ablesen kann, ob du schläfst, im Urlaub bist oder Alarmanlagen aktiv sind.
4. **SURBs (Single Use Reply Blocks)**: Ermöglicht Antworten aus dem Internet, ohne dass der Empfänger jemals deine IP-Adresse erfährt.

---

## 🎛️ Ausführliche Funktionsübersicht

### 1. 🧅 Universeller SOCKS5 Proxy (Port `1080`)
* Das Add-on stellt lokal unter `socks5://127.0.0.1:1080` einen SOCKS5-Proxy bereit.
* **Kompatibel mit allen HA-Diensten**: Leite Telegram-Bots, Push-Benachrichtigungen, OpenAI-/Anthropic-Integrationen oder HTTP-Sensoren direkt durch das Mixnet.

### 2. 🖥️ Integriertes Ingress Web-Dashboard (HA Seitenleiste)
* **Live Route Visualizer**: Animierte Visualisierung der Mixnet-Hops (`HA Node ➔ Layer 1 ➔ Layer 2 ➔ Layer 3 ➔ Exit Gateway`).
* **Echtzeit-Diagnostik**: Integrierter SOCKS5-Handshake & Ping-Tester zur Latenzmessung in Millisekunden.
* **One-Click Proxy Copy**: Kopiert `socks5://127.0.0.1:1080` mit einem Klick in die Zwischenablage.
* **Netzwerk-Statistiken**: Anzeige der aktiven Nym-Nodes, Gateways und Exit-Provider.

### 3. 🤖 KI & Voice Privacy Schutz
* Verschleiert Sprachanfragen und Prompts an LLMs (wie OpenAI ChatGPT, Claude, lokale Assist-Pipelines), sodass keine Rückschlüsse auf deinen Haushalt oder Standort möglich sind.

### 4. 🌦️ Wetter & Geodaten Anonymisierung
* Schützt die exakten GPS-Koordinaten deines Hauses vor Anbietern von Wetter-, Sonnenstands- oder Geolocation-APIs.

### 5. 🚨 Anti-Einbruchs-Schutz (Cover Traffic)
* Erzeugt ein konstantes Grundrauschen an Mixnet-Paketen. Selbst hochentwickelte Router-Sniffer können nicht erkennen, ob Bewohner anwesend sind oder Alarme ausgelöst wurden.

### 6. 🔐 Passphrase- & Schlüsselschutz (Eigener VPN-Account)
* Unterstützt standardmäßig vollautomatische, dezentrale Schlüsselpaare sowie optional die Eingabe einer eigenen **Passphrase** / eines **Mnemonic-Seeds** zur Identitätssicherung und Account-Bindung.

---

## 📖 Schritt-für-Schritt Bedienungsanleitung

### Schritt 1: Installation & Start (1-Klick)
1. Klicke im Home Assistant Add-on Store beim **Nym Privacy Hub** auf **Installieren**.
2. Klicke auf **Starten** und aktiviere den Schalter **In der Seitenleiste anzeigen**.
3. Öffne das Dashboard über den neuen Menüpunkt **Nym Privacy** in der linken Seitenleiste.

---

### Schritt 2: Nutzung in anderen Home Assistant Integrationen

Du kannst den Proxy in jeder beliebigen Home Assistant Integration verwenden, die SOCKS5 oder HTTP-Proxys unterstützt:

#### Beispiel A: Telegram Bot Anonymisierung
Trage in deiner `configuration.yaml` folgendes ein:
```yaml
telegram_bot:
  - platform: polling
    api_key: "DEIN_TELEGRAM_BOT_TOKEN"
    allowed_chat_ids:
      - 123456789
    proxy_url: "socks5://127.0.0.1:1080"
```

#### Beispiel B: REST / HTTP Sensoren über Mixnet
```yaml
sensor:
  - platform: rest
    name: "Anonyme IP Abfrage"
    resource: "https://api.ipify.org?format=json"
    proxy_url: "socks5://127.0.0.1:1080"
    value_template: "{{ value_json.ip }}"
```

---

## ⚙️ Konfigurationsoptionen (Reiter „Konfiguration“)

| Parameter | Typ | Standardwert | Beschreibung |
|---|---|---|---|
| `provider` | `str` | *Default Exit Provider* | Die Nym-Adresse des Exit-Gateways, über das der Internetverkehr das Mixnet verlässt. |
| `use_reply_surbs` | `bool` | `true` | Aktiviert Single Use Reply Blocks für vollkommen anonyme Antwortrouten. |
| `cover_traffic` | `bool` | `false` | Aktiviert künstlichen Hintergrund-Datenverkehr zum Schutz vor Timing-Analysen. |
| `cover_traffic_rate`| `int` | `10` | Anzahl der Cover-Traffic Pakete pro Minute (1 - 120). |
| `passphrase` | `password`| `""` | Optionale Passphrase zur Absicherung deiner kryptografischen Mixnet-Schlüssel. |
| `log_level` | `list` | `info` | Detaillierungsgrad der Protokolle (`trace`, `debug`, `info`, `warn`, `error`). |

---

## 🛠️ Home Assistant Services (Automatisierungen)

* **`nym_privacy_hub.test_connection`**: Führt einen sofortigen Verbindungstest durch und aktualisiert alle Sensoren.
* **`nym_privacy_hub.send_anonymous_request`**: Führt eine HTTP GET/POST Anfrage direkt über das Nym Mixnet aus und liefert die Antwort zurück:
```yaml
service: nym_privacy_hub.send_anonymous_request
data:
  url: "https://api.ipify.org?format=json"
  method: "GET"
```

---

## ❓ Häufige Fragen (FAQ)

**F: Verlangsamt das Nym Mixnet mein Smart Home?**  
A: Lokale Steuerungen (wie Zigbee, Z-Wave, lokale Lampen) bleiben blitzschnell und unverändert lokal im Netzwerk. Nur externe Internetabfragen (Wetter, Cloud-KI, Benachrichtigungen) werden verschlüsselt gemischt (typische Latenz ca. 300–500 ms).

**F: Bleiben meine Schlüssel bei Neustarts erhalten?**  
A: Ja! Sämtliche kryptografischen Schlüsselpaare und Konfigurationen werden dauerhaft im persistenten Home Assistant Speicher unter `/data/.nym` gesichert.
