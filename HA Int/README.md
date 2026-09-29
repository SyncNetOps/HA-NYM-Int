# 🛡️ Nym Privacy Hub für Home Assistant

Der **Nym Privacy Hub** ist eine ganzheitliche All-in-One-Lösung, um Home Assistant über das dezentrale **Nym Mixnet** abzusichern. Er schützt Metadaten, IP-Adressen und Smart-Home-Kommunikation vor Traffic-Analyse und Überwachung.

---

## 🏛️ Architekturübersicht

```mermaid
flowchart TB
    subgraph HA_OS [Home Assistant OS / Supervised]
        subgraph Addon [Nym Privacy Hub Add-on (Docker Engine)]
            SOCKS5[nym-socks5-client :1080]
            IngressUI[Ingress Web Dashboard :8099]
            MixnetConn[Nym Mixnet Gateway Link]
            SOCKS5 --> MixnetConn
            IngressUI --> SOCKS5
        end

        subgraph Integration [Nym Privacy Hub Custom Component]
            ConfigFlow[Config Flow / UI Dashboard]
            Coordinator[Data Coordinator & Health Monitor]
            Toggles[Privacy Toggles: LLM / Voice / Geo]
            Card[Lovelace Custom Card]
            
            ConfigFlow --> Coordinator
            Coordinator --> Toggles
            Coordinator --> Card
        end

        Integration -- SOCKS5:1080 --> Addon
    end

    subgraph External [Nym Decentralized Mixnet]
        Gateways[Nym Mixnodes & Gateways]
        ExitNode[Nym Exit Gateway / Network Requester]
        MixnetConn --> Gateways --> ExitNode
    end
```

---

## 📦 Installation in Home Assistant

### 1. Add-on installieren
1. Gehe in Home Assistant zu **Einstellungen ➔ Add-ons ➔ Add-on Store**.
2. Klicke auf die drei Punkte oben rechts ➔ **Repositories**.
3. Füge folgende URL hinzu:
   ```text
   https://github.com/SyncNetOps/HA-NYM-Int
   ```
4. Installiere und starte das Add-on **„Nym Privacy Hub“**.

### 2. Custom Integration (HACS)
1. Öffne HACS ➔ **Integrationen** ➔ Drei Punkte oben rechts ➔ **Benutzerdefiniertes Repository**.
2. Füge `https://github.com/SyncNetOps/HA-NYM-Int` (Kategorie: *Integration*) hinzu.
3. Lade die Integration herunter und starte Home Assistant neu.
4. Füge die Integration unter **Einstellungen ➔ Geräte & Dienste** hinzu.
