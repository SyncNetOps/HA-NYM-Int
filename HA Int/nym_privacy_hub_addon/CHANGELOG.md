# Changelog

## 1.0.6
- Fix: 502 Bad Gateway behoben durch Umstellung auf `ThreadingHTTPServer` mit Multi-Threading und Keep-Alive.
- Fix: Status-Caching (2s) verhindert Socket-Sättigung bei häufigem Polling.
- Fix: Ingress-Pfadstrukturierung und robustes Exception-Handling.

## 1.0.5
- Fix: Ingress-Pfadauflösung für direkte Ping- und Status-API-Aufrufe (`getApiUrl`).
- Feat: Vollständiger SOCKS5 RFC 1928 Handshake-Check im Ping-Test.
- Feat: Passphrase & Provider Eingabeformular direkt im Ingress Web Dashboard.

## 1.0.4
- Feat: Optionale Passphrase-Eingabe (Schlüsselschutz).
- Fix: Automatischer TOML Schema-Patch für `credential_requests_database`.
