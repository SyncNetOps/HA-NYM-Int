# Changelog

## 1.0.9
- Feat: **Echtzeit-Durchsatz & Canvas-Chart (Live 60s Stream)**: Reibungslose Darstellung von Nutzdaten-Throughput (KB/s) und Cover-Traffic Loops direkt im Dashboard.
- Feat: **Live Datenstrom & Proxy-Inspector**: Detaillierte Übersicht aller über das Hub gerouteten Streams mit Ziel, Paketgrößen und Anonymisierungsstatus.
- Feat: **Interaktiver Sphinx-Krypto-Inspektor**: Klick auf beliebige Mixnet-Hops (Home Assistant, Gateway, Mix 1, Mix 2, Mix 3, Exit) öffnet detaillierte kryptografische Erläuterungen (Poisson Delays, Schicht-Entschlüsselung, Zero-Knowledge).
- Feat: **Live Mixnet IP & Geo-Leak Check Tool**: Führt echte HTTP-Anfragen über den SOCKS5-Tunnel durch und zeigt dem Nutzer seine sichtbare Exit-IP und Latenz an – der direkte Beweis für 100% Leckschutz.
- Feat: **1-Klick Schutzlevel-Presets**: Intuitive Umschaltung zwischen *⚡ Eco Mode*, *🛡️ High Privacy (Standard)* und *🕵️ Ultra Stealth*.
- Feat: **Erweiterte weltweite Exit-Provider**: Kuratierte Gateways für Schweiz 🇨🇭, Deutschland 🇩🇪, Island 🇮🇸, Finnland 🇫🇮, Niederlande 🇳🇱, Singapur 🇸🇬 und Custom Adressen.
- Feat: **Audit-Log Export**: 1-Klick JSON-Download der gesamten Sicherheits- und Netzwerkereignisse.
- Feat: **Home Assistant Integration Snippet Generator**: Fertige Vorlagen für `configuration.yaml` (Telegram Bot, REST Sensoren, Scrape, curl) direkt im Cockpit.

## 1.0.8
- Feat: Live-Telemetrie Dashboard mit Echtzeit-Zählern für gemischte Sphinx-Pakete, Cover-Loops und verschleierte Bandbreite.
- Feat: Live Audit & Ereignis-Stream direkt im Cockpit.
- Feat: Interaktiver Schieberegler für Cover-Traffic Intensität und Anonymitäts-Presets.
- Feat: Schnellauswahl kuratierter Nym Exit-Gateways (Schweiz, Deutschland, Island, Finnland) oder Custom Provider.
- Fix: Nicht-invasiver `/proc/net/tcp` Health-Check eliminiert `early eof` Logeinträge vollständig.

## 1.0.7
- Fix: /proc/net/tcp Health-Check gegen `early eof` Meldungen im Log.

## 1.0.6
- Fix: 502 Bad Gateway behoben durch Umstellung auf `ThreadingHTTPServer` mit Multi-Threading und Keep-Alive.
