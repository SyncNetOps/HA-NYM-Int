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

## 🎛️ Ausführliche Funktionsübersicht der 5 Cockpit-Tabs

### 1. 📊 Tab: Live Cockpit
* **Animierter 3-Hop Route Visualizer**: Zeigt in Echtzeit den Datenfluss von Home Assistant über das Entry Gateway, Mix Layer 1, Mix Layer 2, Mix Layer 3 und den Exit-Provider ins Internet.
* **Krypto-Hop-Inspektor**: Klick auf beliebige Knoten zeigt die exakten mathematischen und kryptografischen Abläufe (z.B. Poisson Delay, Reordering, Schicht-Entschlüsselung).
* **60s Echtzeit-Durchsatz Canvas Chart**: Reibungslose Darstellung von echten Nutzdatenströmen (KB/s) und Cover-Traffic Schleifen.
* **Live Datenstrom & Proxy-Inspector**: Tabelle aller aktiven Verbindungen durch den SOCKS5-Proxy mit Ziel und Paketgrößen.
* **Live IP-Leak & Geo-Check**: Testet den SOCKS5-Tunnel und beweist die vollkommene Verschleierung der eigenen Provider-IP.

---

### 2. 🛡️ Tab: HA Datenquellen-Schutz (Dynamisches Routing)
Hier kannst du für jede Smart-Home Komponente einzeln und dynamisch festlegen, ob sie über das Nym Mixnet geschützt werden soll:

| Datenquelle | Geschützte Dienste | Verhindertes Risiko |
|---|---|---|
| **🤖 KI & Sprachassistenten** | `OpenAI`, `Anthropic`, `HA Assist Prompts`, `ElevenLabs` | Verhindert Haushalts-Profiling & Sprachbefehl-Korrelation |
| **🌦️ Wetter & Geodaten** | `Open-Meteo`, `AccuWeather`, `Nominatim`, `Sun/Astro` | Verhindert exakte GPS-Standortermittlung des Smart Homes |
| **📱 Messenger & Bots** | `Telegram Bot`, `Signal CLI`, `Discord`, `Pushover` | Maskiert Anwesenheitszustände und Alarmmeldungen vor ISP-Spionage |
| **⚡ Dynamische Strompreise** | `Tibber API`, `Nordpool`, `Entso-E` | Verhindert Analyse von Ladezyklen (Elektroauto / Wärmepumpe) |
| **☁️ Cloud-Backups & Sync** | `Nextcloud`, `Google Drive Backup`, `WebDAV` | Verschleiert Offsite-Backup Zeitstempel & Datenmengen |
| **🌐 Eigene REST & Scrape Sensoren** | Alle individuellen HTTP-Endpunkte | Verhindert IP-Korrelation über mehrere Cloud-Dienste hinweg |

---

### 3. ⚙️ Tab: Mixnet Krypto & Feintuning
* **1-Klick Presets**:
  * *⚡ Eco Mode*: 0 Cover-Traffic, minimale Latenz (~250–350 ms).
  * *🛡️ High Privacy (Standard)*: 10 Pkt/min Cover-Rauschen, SURBs aktiv, Anti-Timing-Schutz.
  * *🕵️ Ultra Stealth*: 35 Pkt/min Cover-Rauschen gegen Nachbarschafts- und Router-Sniffer.
* **Poisson-Verzögerung pro Hop (5–150 ms)**: Stochastische Paketstreuung zur Zerstörung von Timing-Mustern.
* **SURB Token Puffer (20, 50, 100, 250 Tokens)**: Vorrat an anonymen Rückkanälen für parallele Sensoren.
* **DNS-over-Mixnet Isolation**: DNS-Abfragen werden erst am Exit-Node aufgelöst.
* **Weltweite Exit-Nodes**: Auswahl zwischen 🇨🇭 Schweiz, 🇩🇪 Deutschland, 🇮🇸 Island, 🇫🇮 Finnland, 🇳🇱 Niederlande, 🇸🇬 Singapur, 🇺🇸 USA oder benutzerdefinierter Adresse.

---

### 4. 💎 Tab: Nym Premium, Fast Pass & ZK-Bandwidth Tokens
Das Nym Mixnet ist im Standard-Modus **vollkommen kostenlos und dezentral nutzbar**. Für anspruchsvolle Smart Homes bietet Nym optionale **Premium Fast-Pass / Coconut zk-nyms** Funktionen:

#### 🌟 Vorteile eines kostenpflichtigen Nym-Zugangs:
1. 🚀 **Garantierte High-Speed Bandbreite (bis 100+ Mbit/s)**:
   * Ermöglicht das unterbrechungsfreie Streaming verschlüsselter Sicherheitskameras und rasante Offsite-Backups (z. B. vollständige HA Snapshots nach Nextcloud/Drive).
2. ⚡ **VIP Low-Latency Mix Queues (<200–300 ms)**:
   * Priorisierte Weiterleitung in Mixnodes. Verhindert Paketverwerfungen bei weltweiter Netzwerkauslastung.
3. 🔐 **Statische NymID für P2P Remote-Access**:
   * Feste kryptografische Nym-Adresse für portfreigabe-freien Fernzugriff von unterwegs (Home Assistant Companion App über Mixnet ohne Cloud-Abo).
4. 🎫 **Zero-Knowledge Coconut Credentials (zk-nyms)**:
   * Der Zahlungsnachweis erfolgt kryptografisch über blinde Signaturen. Nym erfährt niemals, welches Home Assistant System zu welcher Zahlung gehört!
5. 🔐 **Passphrase- & Mnemonic-Seed Schutz**:
   * Sichere Absicherung der lokalen kryptografischen Schlüsselpaare oder Wiederherstellung bestehender Nym-Identitäten.

---

### 5. 📋 Tab: YAML Vorlagen & Integration Snippets
Fertige Kopiervorlagen für die `configuration.yaml` zur sofortigen Einbindung von Telegram-Bots, Wetter-Sensoren, IP-Checkern und Shell-Commands.

---

## 📖 Schnellstart (1-Klick)

1. Im Home Assistant Add-on Store den **Nym Privacy Hub** installieren und starten.
2. In der linken Seitenleiste auf **Nym Privacy** klicken.
3. Im Tab **🛡️ HA Datenquellen** deine gewünschten Schutzschilde aktivieren – fertig!
