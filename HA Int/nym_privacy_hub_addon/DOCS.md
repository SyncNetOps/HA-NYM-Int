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
5. **Gleichförmige 2708-Byte Frames**: Verhindert jegliche Identifizierung von Geräten oder Protokollen anhand variierender Paketgrößen.

---

## 🎛️ Ausführliche Funktionsübersicht & Live-Cockpit

### 1. 🖥️ Integriertes Ingress Web-Cockpit (HA Seitenleiste)
* **Animierter 3-Hop Live Route Visualizer**: Zeigt in Echtzeit den Fluss von Home Assistant über das Entry Gateway, Mix Layer 1 (Delay), Mix Layer 2 (Reordering), Mix Layer 3 (Entschlüsselung) und den Exit-Provider ins Ziel-Internet.
* **Interaktiver Krypto-Hop-Inspektor**: Ein Klick auf einen beliebigen Knoten im Pfad öffnet eine detaillierte Aufschlüsselung der dort stattfindenden kryptografischen Aktionen.
* **Echtzeit-Durchsatz & Canvas Chart (60s Stream)**: Flüssiges Live-Diagramm von Nutzdatenströmen (KB/s) und Cover-Traffic Loops.
* **Live Datenstrom & Proxy-Inspector**: Übersichtliche Tabelle aktiver Streams (z.B. Wetterabfragen, KI-Prompts, Gateway Heartbeats) mit Ziel, Paketgrößen und Anonymisierungsstatus.
* **Live Mixnet IP & Geo-Check**: Testet den SOCKS5-Tunnel und zeigt die verschleierte Exit-IP an – der direkte Beweis für absolute IP-Leck-Freiheit.

### 2. 🧅 Universeller SOCKS5 Proxy (Port `1080`)
* Das Add-on stellt lokal unter `socks5://127.0.0.1:1080` einen SOCKS5-Proxy bereit.
* **Kompatibel mit allen HA-Diensten**: Leite Telegram-Bots, Push-Benachrichtigungen, OpenAI-/Anthropic-Integrationen oder HTTP-Sensoren direkt durch das Mixnet.

### 3. 🎯 1-Klick Schutzlevel-Presets & Schieberegler
* **⚡ Eco Mode**: 0 Cover-Traffic, minimale Latenz (~250-400ms), optimal für Cloud-Sensoren & Wetterabfragen.
* **🛡️ High Privacy (Standard Empfohlen)**: 10 Pkt/min Cover-Traffic Rauschen, SURBs aktiv, vollkommener Anti-Timing-Schutz.
* **🕵️ Ultra Stealth**: 35 Pkt/min Cover-Traffic, permanenter Scheindatenstrom zur Täuschung von ISP- und Router-Spionen.
* **Granularer Schieberegler**: Stufenlose Anpassung des Cover-Traffics von 0 bis 60 Pakete/min mit Live-Berechnung der Bandbreite (~2.7 KB pro Paket).

### 4. 🌍 Globale Exit-Provider Auswahl
Wähle mit einem Klick das Land, aus dem deine Smart-Home-Anfragen im Internet erscheinen:
* 🇨🇭 **Schweiz** (SpectreDAO Exit Node)
* 🇩🇪 **Deutschland** (Nym Core Exit)
* 🇮🇸 **Island** (Privacy Haven Node)
* 🇫🇮 **Finnland** (Nordic Mix Exit)
* 🇳🇱 **Niederlande** (Amsterdam Mix Exit)
* 🇸🇬 **Singapur** (Asia Pacific Hub)
* ⚙️ **Benutzerdefiniert**: Beliebige Nym Exit Node Adresse einbinden.

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
    api_key: !secret telegram_token
    allowed_chat_ids:
      - 123456789
    proxy_url: socks5://127.0.0.1:1080
```

#### Beispiel B: REST / HTTP Sensoren über Mixnet
```yaml
sensor:
  - platform: rest
    name: "Anonyme Wetterdaten"
    resource: "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"
    proxy_url: socks5://127.0.0.1:1080
    value_template: "{{ value_json.current_weather.temperature }}"
    unit_of_measurement: "°C"
```

#### Beispiel C: Shell Command mit SOCKS5 Proxy
```yaml
shell_command:
  send_secure_alert: "curl -x socks5h://127.0.0.1:1080 -X POST https://webhook.site/my-uuid -d 'status=alarm'"
```

---

## ⚙️ Konfigurationsoptionen

| Parameter | Typ | Standardwert | Beschreibung |
|---|---|---|---|
| `provider` | `str` | *Schweiz Exit* | Nym-Adresse des Exit-Gateways, über das Daten das Mixnet verlassen. |
| `use_reply_surbs` | `bool` | `true` | Aktiviert Single Use Reply Blocks für vollkommen anonyme Antwortrouten. |
| `cover_traffic` | `bool` | `false` | Aktiviert künstlichen Hintergrund-Datenverkehr zum Schutz vor Timing-Analysen. |
| `cover_traffic_rate`| `int` | `10` | Anzahl der Cover-Traffic Pakete pro Minute (1 - 60). |
| `surb_buffer_size` | `int` | `50` | Größe des vorgehaltenen SURB-Token-Puffers (20, 50, 100). |
| `anonymity_mode` | `list` | `high_privacy` | Vorkonfiguriertes Schutzlevel (`eco`, `high_privacy`, `ultra_stealth`). |
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
