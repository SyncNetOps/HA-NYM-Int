# Home Assistant Add-on: Nym Privacy Hub

## Installation
1. Füge dieses Repository im Home Assistant Add-on Store hinzu: `https://github.com/SyncNetOps/HA-NYM-Int`
2. Klicke auf **Installieren**.
3. Wähle im Reiter **Konfiguration** optional einen eigenen Nym Network Provider aus (oder belasse den Standard-Provider).
4. Starte das Add-on.

## Features
- **SOCKS5 Proxy auf Port 1080**: Leitet Anfragen verschlüsselt durch das Nym Mixnet.
- **Ingress Web Dashboard**: Integriertes Dashboard direkt in der Home Assistant Seitenleiste (Port 8099).
- **Persistente Schlüsselverwaltung**: Verschlüsselungs- und Authentifizierungsschlüssel bleiben unter `/data` erhalten.
- **SURB-Unterstützung**: Single Use Reply Blocks für vollkommen anonyme Antwort-Routen.
