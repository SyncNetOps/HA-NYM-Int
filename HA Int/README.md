# 🛡️ Nym Privacy Hub für Home Assistant

[![Home Assistant Add-on](https://img.shields.io/badge/Home%20Assistant-Add--on-blue?logo=home-assistant)](https://github.com/SyncNetOps/HA-NYM-Int)
[![HACS Integration](https://img.shields.io/badge/HACS-Custom%20Integration-orange?logo=home-assistant)](https://github.com/SyncNetOps/HA-NYM-Int)
[![Nym Mixnet](https://img.shields.io/badge/Nym-Mixnet%20v2026-mint?logo=nym)](https://nym.com)

Der **Nym Privacy Hub** ist eine ganzheitliche All-in-One-Lösung, um Home Assistant über das dezentrale **Nym Mixnet** abzusichern. Er schützt Smart-Home-Metadaten, IP-Adressen und Automatisierungen vor Traffic-Analyse, Profiling und Überwachung.

---

## 🌟 Warum Nym Mixnet statt klassischem VPN?

Herkömmliche VPNs verschlüsseln zwar den Datenstrom, leiten jedoch sämtliche Daten über zentrale Server. Überwachungssysteme und Internet-Provider können anhand von **Paketgrößen und Zeitstempeln (Timing-Attacks)** genau analysieren, wann im Haus Geräte geschaltet, Sprachbefehle erteilt oder Anwesenheiten verändert werden.

| Feature | Traditionelles VPN | 🛡️ Nym Privacy Hub |
|---|---|---|
| **Verschlüsselung** | 1 Schicht (Punkt-zu-Punkt) | **Sphinx Mehrschichtverschlüsselung (3 Hops)** |
| **Metadaten-Schutz** | ❌ Gering (Zentraler VPN-Server sieht alles) | **✅ 100 % Dezentral (Zero-Knowledge Routing)** |
| **Traffic-Timing Schutz** | ❌ Nicht geschützt (Paketmuster sichtbar) | **✅ Paketverzögerung & Mixen verhindert Timing-Analyse** |
| **Anti-Einbruch Cover Traffic**| ❌ Keine Verschleierung von Ruhephasen | **✅ Einstellbares Datenrauschen maskiert Anwesenheit** |
| **Anonyme Antworten** | ❌ IP-Rückkanal bekannt | **✅ SURBs (Single Use Reply Blocks)** |

---

## 🏛️ Systemarchitektur

```mermaid
flowchart TB
    subgraph HA_OS [Home Assistant OS / Supervised]
        subgraph Addon [🐳 Nym Privacy Hub Add-on (Docker Daemon)]
            SOCKS5[nym-socks5-client :1080]
            IngressUI[Ingress Web Cockpit :8099]
            MixnetConn[Nym Gateway Link]
            SOCKS5 --> MixnetConn
            IngressUI --> SOCKS5
        end

        subgraph Integration [🎛️ Nym Custom Component & UI]
            ConfigFlow[Config Flow Assistent]
            Coordinator[Data Coordinator & Health Monitor]
            Toggles[1-Klick Privacy Switches]
            Card[Lovelace Custom Card]
            
            ConfigFlow --> Coordinator
            Coordinator --> Toggles
            Coordinator --> Card
        end

        Integration -- SOCKS5 :1080 --> Addon
    end

    subgraph External [🌐 Dezentrales Nym Mixnet]
        Gateways[Nym Mixnodes & Gateways]
        ExitNode[Nym Exit Gateway]
        MixnetConn --> Gateways --> ExitNode
    end

    subgraph Targets [Geschützte Dienste]
        LLM[OpenAI / Anthropic APIs]
        Voice[Sprachassistenten]
        Geo[Wetter- & Standort-APIs]
        ExitNode --> LLM
        ExitNode --> Voice
        ExitNode --> Geo
    end
```

---

## 🎛️ Funktionsübersicht & Bedienung

### 1. 🟢 Für Einsteiger (Plug & Play)
* **1-Klick Installation**: Vorkonfigurierte SOCKS5-Proxy-Bindung auf `127.0.0.1:1080`.
* **KI & Voice Privacy Schalter**: Routet alle LLM- und Sprachassistenten-Anfragen (OpenAI, Anthropic, HA Assist) durch das Mixnet.
* **Wetter & Geodaten Schutz**: Verschleiert Standort- und Wetterdienst-Koordinaten vor Tracking.
* **Anti-Einbruchs Cover Traffic**: Generiert Hintergrundrauschen, damit Einbrecher am Router-Traffic nicht ablesen können, ob Bewohner schlafen oder abwesend sind.
* **One-Click Proxy Copy**: Kopiert `socks5://127.0.0.1:1080` mit einem Klick zur Verwendung in Telegram-Bots, Push-Diensten oder Webhooks.

### 2. 🔴 Für Profis (Advanced Settings)
* **Custom Exit Provider**: Möglichkeit zur Hinterlegung spezifischer Nym-Exit-Nodes.
* **Passphrase- & Schlüsselschutz**: Optionale Absicherung für eigene Nym-Accounts / Mnemonic-Keys.
* **Cover Traffic Rate Controller**: Feingranulare Steuerung der Paketrate pro Minute.
* **Home Assistant Automations-Dienste**:
  * `nym_privacy_hub.test_connection`: Sofortiger Mixnet-Verbindungstest.
  * `nym_privacy_hub.send_anonymous_request`: Führt beliebige HTTP-Aufrufe über das Mixnet aus.

---

## 🚀 Installation

### 1. Add-on hinzufügen & installieren
1. Gehe in Home Assistant zu **Einstellungen ➔ Add-ons ➔ Add-on Store**.
2. Klicke oben rechts auf **drei Punkte (⋮) ➔ Repositories**.
3. Füge folgende URL hinzu:
   ```text
   https://github.com/SyncNetOps/HA-NYM-Int
   ```
4. Klicke auf **Nym Privacy Hub** ➔ **Installieren** ➔ **Starten**.
5. Aktiviere die Option **In der Seitenleiste anzeigen**.

### 2. Custom Integration (HACS)
1. Öffne HACS ➔ **Integrationen** ➔ Drei Punkte oben rechts ➔ **Benutzerdefiniertes Repository**.
2. Trage `https://github.com/SyncNetOps/HA-NYM-Int` (Kategorie: *Integration*) ein.
3. Klicke auf Herunterladen und starte Home Assistant neu.
4. Füge die Integration unter **Einstellungen ➔ Geräte & Dienste** hinzu.

### 3. Lovelace Custom Dashboard Card
Füge eine benutzerdefinierte Karte in deinem Dashboard ein:
```yaml
type: custom:nym-privacy-hub-card
title: "Nym Privacy Hub"
```

---

## 🔒 Datenschutz & Sicherheit
* Sämtliche kryptografischen Schlüssel werden **lokal auf deinem Home Assistant Server** unter `/data/.nym` gespeichert.
* Es werden zu keinem Zeitpunkt unverschlüsselte Daten oder IP-Adressen an zentrale Dritte übertragen.
