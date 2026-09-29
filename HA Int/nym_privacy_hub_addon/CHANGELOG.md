# Changelog

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
