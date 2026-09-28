# 🛡️ Nym Privacy Hub für Home Assistant

Der **Nym Privacy Hub** ist eine ganzheitliche All-in-One-Lösung, um Home Assistant über das dezentrale **Nym Mixnet** abzusichern. Er schützt Metadaten, IP-Adressen und Smart-Home-Kommunikation vor Traffic-Analyse und Überwachung.

---

## 🏛️ Architekturübersicht

Das System setzt sich aus zwei Kernkomponenten zusammen:

```mermaid
flowchart TB
    subgraph HA_OS [Home Assistant OS / Supervised]
        subgraph Addon [Nym Privacy Hub Add-on (Docker Engine)]
            SOCKS5[nym-socks5-client]
            ProxyPort[SOCKS5 Proxy: 127.0.0.1:1080]
            MixnetConn[Nym Mixnet Cryptographic Gateway Link]
            SOCKS5 --> ProxyPort
            SOCKS5 --> MixnetConn
        end

        subgraph Integration [Nym Privacy Hub Custom Component]
            ConfigFlow[Config Flow / UI Dashboard]
            Coordinator[Data Coordinator & Health Monitor]
            Toggles[Privacy Toggles (LLM / Voice / Geo)]
            ProxyHelper[Outbound SOCKS5 Proxy Service]
            
            ConfigFlow --> Coordinator
            Coordinator --> Toggles
            Toggles --> ProxyHelper
        end

        Integration -- HA Add-on API / SOCKS5:1080 --> Addon
    end

    subgraph External [Nym Decentralized Mixnet]
        Gateways[Nym Mixnodes & Gateways]
        ExitNode[Nym Exit Gateway / Network Requester]
        MixnetConn --> Gateways --> ExitNode
    end

    subgraph Targets [Protected Targets]
        LLM[OpenAI / Anthropic APIs]
        Weather[Weather & Geo Services]
        RemoteHA[Peer Home Assistant Instances]
        ExitNode --> LLM
        ExitNode --> Weather
        ExitNode --> RemoteHA
    end
```

---

## 📦 Komponenten

1. **HA Add-on (`nym_privacy_hub_addon/`)**:
   - Docker-basierter Hintergrunddienst im Home Assistant OS.
   - Initialisiert und verwaltet den offiziellen `nym-socks5-client`.
   - Öffnet den lokalen SOCKS5-Proxy (Port `1080`).
   - Verwaltet kryptografische Schlüsselpaare und Gateway-Verbindungen.

2. **Custom Component (`custom_components/nym_privacy_hub/`)**:
   - HACS-kompatible Integration mit moderner Home Assistant UI.
   - Steuerung & Status-Monitoring des Add-ons via Home Assistant API.
   - Ein-Klick-Toggles für Einsteiger (KI & Voice Privacy, Geo-Data Protection, Cover Traffic).
   - Erweiterte Konfiguration für Profis (Custom Service Providers, Remote Ingress, Traffic-Raten, Multi-Node Sync).

---

## 🚀 Roadmap

- [x] **Projekt-Setup & Architektur-Design**
- [ ] **Phase 1: Basis-Add-on (SOCKS5 Bridge)**
  - Dockerfile, `config.yaml`, `build.yaml`, `run.sh`
  - Multi-Architektur Support (amd64, aarch64, armv7)
  - Automatische Key-Initialisierung & Persistenz
- [ ] **Phase 2: Custom Component Integration**
  - Config Flow & Options Flow
  - Sensor- & Switch-Entitäten
  - SOCKS5-Proxy-Weiterleitung für Cloud/LLM-Dienste
- [ ] **Phase 3: P2P Remote Access & SURB Messaging**
  - Single Use Reply Blocks (SURBs)
  - Portfreigabe-freier Zugriff & Multi-Instanz-Synchronisation
