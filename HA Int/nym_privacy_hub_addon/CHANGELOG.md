# Changelog

## 1.1.0
- Feat: **Multi-Tab Cockpit & Einstellungs-Zentrale**: Übersichtliche Navigation über 5 spezialisierte Tabs (📊 Live Cockpit, 🛡️ HA Datenquellen, ⚙️ Mixnet Krypto, 💎 Nym Premium & Fast Pass, 📋 YAML Vorlagen).
- Feat: **Dynamischer HA Datenquellen-Router**: Ermöglicht die granulare und dynamische Auswahl aller Home Assistant Datenströme, die über das Nym Mixnet geschützt werden sollen:
  - 🤖 *KI & Sprachassistenten* (OpenAI, Anthropic, HA Assist Prompts)
  - 🌦️ *Wetter, Sonnenstand & Geodaten* (Open-Meteo, AccuWeather, Nominatim)
  - 📱 *Messenger, Bots & Push-Alarme* (Telegram, Signal, Discord, Pushover)
  - ⚡ *Dynamische Stromtarife & Börsenpreise* (Tibber, Nordpool, Entso-E)
  - ☁️ *Cloud-Backups & Offsite Sync* (Nextcloud, Google Drive)
  - 🌐 *Eigene REST-, Scrape- & Command-Sensoren*
- Feat: **Nym Premium & Fast Pass VIP Management**:
  - Detaillierte Erläuterung aller Vorteile eines kostenpflichtigen Nym-Zugangs (bis zu 100+ Mbit/s Bandbreite für Backups & Kameras, priorisierte VIP Mix-Queues unter 200–300 ms Latenz, statische NymID für P2P-Fernzugriff ohne Portweiterleitung, Coconut zk-nyms Zero-Knowledge Credentials).
  - Eingabemöglichkeit für Fast Pass API Tokens und Mnemonic-Seed-Passphrasen mit sofortiger Validierung.
- Feat: **Erweiterte Mixnet-Krypto-Einstellungen**:
  - Stufenlos einstellbare durchschnittliche Poisson-Verzögerung pro Mix-Hop (5–150 ms) zur Verhinderung von ISP-Timing-Analysen.
  - DNS-over-Mixnet Isolationsschalter (DNS-Auflösung erfolgt erst am Exit-Node).
  - Skalierbarer SURB-Puffer (20, 50, 100, 250 Tokens).

## 1.0.9
- Feat: Echtzeit-Durchsatz & Canvas-Chart (Live 60s Stream) für Nutzdaten-Throughput und Cover-Traffic Loops.
- Feat: Live Datenstrom & Proxy-Inspector mit detaillierter Stream-Tabelle.
- Feat: Interaktiver Sphinx-Krypto-Inspektor mit modalen Klick-Details zu jedem Hop.
- Feat: Live Mixnet IP & Geo-Leak Check Tool.
- Feat: 1-Klick Schutzlevel-Presets (Eco, High Privacy, Ultra Stealth).
- Feat: Weltweite Exit-Provider (Schweiz, Deutschland, Island, Finnland, Niederlande, Singapur, USA).

## 1.0.8
- Feat: Live-Telemetrie Dashboard mit Zählern für Sphinx-Pakete, Cover-Loops und Bandbreite.
- Fix: Nicht-invasiver `/proc/net/tcp` Health-Check eliminiert `early eof` Logeinträge vollständig.
