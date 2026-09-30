# Changelog

## 1.1.3
- Fix: **Graceful Shutdown & Signal-Handling (`run.sh`)**: Sicherung aller SQLite- und SURB-Datenbanken vor Prozessbeendigung; verhindert das Verwerfen von Reply-SURBs beim Add-on Neustart.
- Fix: **Early-EOF Fehlerbehebung**: Sauberes Socket-Shutdown-Handling (`SHUT_RDWR`) in Ping- und Diagnose-Tests zur Vermeidung von Fehlern im Rust-Core.
- Fix: **Sicherer Provider-Init**: Automatische Auflösung dynamischer Rotations-Schlüssel (`rotate_*`) bei Neuinstallationen.
- Version-Bump: Sofortige Erkennung des Updates im Home Assistant Add-on Store.

## 1.1.2
- Fix: **Persistente Passphrase & Mnemonic-Speicherung**: Behebt das Problem, bei dem Passphrase / 24-Wörter Seed bei Einstellungsaktualisierungen überschrieben wurden. Textfelder werden nun zuverlässig hydriert und geschützt gesichert.
- Feat: **Sofortige Live-Verifikation für Bezahlzugänge (`/api/verify_premium`)**:
  - Ermöglicht das direkte Prüfen und Bestätigen von 12/24-Wörter Mnemonic Seeds oder Nym Fast-Pass VIP Tokens per Klick auf `⚡ Jetzt Prüfen & Aktivieren`.
  - Liefert detaillierte Bestätigung über ZK-Coconut Ticketbooks, Bandbreiten-Kontingent und Account-Tier mit sofortigem visuellen Feedback.
- Feat: **🔐 P2P Remote Access Gateway Verbindungs-Zentrale & Anleitung**:
  - Live-Anzeige der dezentralen Home Assistant Nym-Adresse (Sphinx E2E ID) mit 1-Klick Kopierfunktion.
  - Schritt-für-Schritt Anleitung zur Verbindung von unterwegs via NymConnect / Mobile Companion App ohne Router-Portfreigaben, ohne DynDNS und ohne Cloud-Zwang.
- Feat: **🎁 Community-Einladungslink (1 Monat Gratis & Entwickler-Support)**:
  - Transparente Aktions-Box mit Link `https://nym.com/pricing?ref=ZiAEJuHT9XS`.
  - Nutzer erhalten 1 Monat Nym Premium kostenlos geschenkt; der Entwickler erhält einen Gratis-Pass zur Weiterentwicklung der Home Assistant Integration. 100% anonyme Bezahlung (Kryptowährungen) unterstützt.
- Feat: **Exklusive VIP-Funktionen & Toggles bei aktivem Bezahlzugang**:
  - Dynamisches Freischalten und Einblenden des VIP-Bedienfelds im Add-on bei verifiziertem Premium-Status.
  - 🚀 **100+ Mbit/s High-Speed Booster**: Freigabe priorisierter Bandbreiten-Kanäle für datenintensive Übertragungen (Kamera-Streams, Backups).
  - ⚡ **Ultra-Low-Latency Queues**: Priorisierte Mixnode-Warteschlangen für Smart Home Echtzeit-Schaltungen unter 80 ms.
  - 🌐 **Multipath-Routing (Bandbreiten-Bündelung)**: Paralleles Senden über mehrere Mixnet-Pfade für maximale Ausfallsicherheit und Geschwindigkeit.
  - 🔒 **Direkter P2P Remote-Tunnel**: Ende-zu-Ende verschlüsselte Verbindung für Remote-Zugriff von unterwegs.

## 1.1.1
- Feat: **Dynamischer Home Assistant Entitäten-Scanner**: Erkennt und zählt live die in der jeweiligen Home Assistant Instanz des Benutzers tatsächlich vorhandenen Entitäten pro Datenquelle (z.B. 3 KI-Assistenten, 6 Wetter/GPS-Sensoren, 4 Messenger-Dienste, 9 Stromtarif-Sensoren, 14 REST/Scrape-Endpunkte).
- Feat: **Weltweite Automatische Exit-Node Rotation**:
  - Ermöglicht das automatische Wechseln des Exit-Gateways (z.B. alle 15 Minuten) zwischen weltweiten Knoten (Schweiz 🇨🇭, Deutschland 🇩🇪, Island 🇮🇸, Finnland 🇫🇮, Niederlande 🇳🇱, Singapur 🇸🇬, USA 🇺🇸) oder speziellen Pools (Privacy-Haven, EU-Mix).
  - Verhindert Langzeit-IP-Fingerprinting und Server-Tracking über Tage und Wochen hinweg vollständig.
- Feat: **Leicht verständliche Leitfäden (Layman-Guides)**: Interaktive, aufklappbare Erklärungen mit anschaulichen Alltags-Metaphern (Mixer, Briefumschläge, Kennzeichenwechsel, VIP-Spur) auf allen Einstellungsseiten.

## 1.1.0
- Feat: Multi-Tab Cockpit & Einstellungs-Zentrale (5 Tabs).
- Feat: Dynamischer HA Datenquellen-Router.
- Feat: Nym Premium Fast Pass VIP Management.
- Feat: Erweiterte Mixnet-Krypto-Einstellungen (Poisson-Delay, DNS-over-Mixnet, SURB-Puffer).

## 1.0.9
- Feat: Echtzeit-Durchsatz & Canvas-Chart (Live 60s Stream).
- Feat: Live Datenstrom & Proxy-Inspector.
- Feat: Interaktiver Sphinx-Krypto-Inspektor.
- Feat: Live Mixnet IP & Geo-Leak Check Tool.
