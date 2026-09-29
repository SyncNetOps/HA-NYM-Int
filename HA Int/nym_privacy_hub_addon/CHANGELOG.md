# Changelog

## 1.0.5
- Fix: Ingress-Pfadauflösung für direkte Ping- und Status-API-Aufrufe (`getApiUrl`).
- Feat: Vollständiger SOCKS5 RFC 1928 Handshake-Check im Ping-Test.
- Feat: Passphrase & Provider Eingabeformular direkt im Ingress Web Dashboard.

## 1.0.4
- Feat: Optionale Passphrase-Eingabe (Schlüsselschutz).
- Fix: Automatischer TOML Schema-Patch für `credential_requests_database`.

## 1.0.3
- Fix: Direktes Auslesen von `/data/options.json` mit automatischem Provider-Fallback gegen 403 API-Einschränkungen.
- Fix: `hassio_api: true` und `hassio_role: default` in `config.yaml`.
- Fix: Robuste Symlink-Erstellung für `/data/.nym`.

## 1.0.2
- Fix: Umstellung auf Debian Bookworm Base-Image mit nativer Glibc-Unterstützung.
- Feat: Aktuelles Nym Release `nym-binaries-v2026.18-essaouria`.

## 1.0.1
- Fix: s6-overlay v3 Kompatibilität.
- Feat: Integriertes Ingress Dashboard auf Port 8099.
