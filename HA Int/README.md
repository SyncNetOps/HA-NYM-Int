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
| **Traffic-Timing Schutz** | ❌ Nicht geschützt (Paketmuster sichtbar) | **✅ Poisson-Verzögerung & Mixen verhindert Timing-Analyse** |
| **Frame-Uniformität** | ❌ Variierende Paketgrößen erkennbar | **✅ Exakt 2708 Byte Sphinx-Frames (Anti-Fingerprinting)** |
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
            Throughput[Live Canvas Throughput Engine]
            StreamTrack[Live Streams & Leak Inspector]
            MixnetConn[Nym Gateway Link]
            
            SOCKS5 --> MixnetConn
            IngressUI --> SOCKS5
            IngressUI --> Throughput
            IngressUI --> StreamTrack
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
* **1-Klick Schutzlevel-Presets**: Umschaltung zwischen *⚡ Eco Mode*, *🛡️ High Privacy (Standard)* und *🕵️ Ultra Stealth*.
* **KI & Voice Privacy Schalter**: Routet alle LLM- und Sprachassistenten-Anfragen (OpenAI, Anthropic, HA Assist) durch das Mixnet.
* **Wetter & Geodaten Schutz**: Verschleiert Standort- und Wetterdienst-Koordinaten vor Tracking.
* **Anti-Einbruchs Cover Traffic**: Generiert Hintergrundrauschen, damit Einbrecher am Router-Traffic nicht ablesen können, ob Bewohner schlafen oder abwesend sind.
* **One-Click Proxy Copy**: Kopiert `socks5://127.0.0.1:1080` mit einem Klick zur Verwendung in Telegram-Bots, Push-Diensten oder Webhooks.

### 2. 🔴 Für Transparenz & Profis (Advanced Cockpit)
* **Echtzeit-Durchsatz Canvas Chart**: Animiertes 60s Live-Diagramm für Nutzdaten (KB/s) und Cover-Traffic Loops.
* **Live Datenstrom & Proxy-Inspector**: Detaillierte Übersicht aller über das Hub gerouteten Streams mit Ziel, Paketgrößen und Anonymisierungsstatus.
* **Interaktiver Sphinx-Krypto-Inspektor**: Klick auf beliebige Mixnet-Hops (Home Assistant, Gateway, Mix 1, Mix 2, Mix 3, Exit) öffnet detaillierte kryptografische Erläuterungen.
* **Live Mixnet IP & Geo-Leak Check Tool**: Führt echte HTTP-Anfragen über den SOCKS5-Tunnel durch und zeigt dem Nutzer seine sichtbare Exit-IP und Latenz an.
* **Globale Exit Provider Auswahl**: Kuratierte Exit-Nodes weltweit (Schweiz 🇨🇭, Deutschland 🇩🇪, Island 🇮🇸, Finnland 🇫🇮, Niederlande 🇳🇱, Singapur 🇸🇬, USA 🇺🇸) oder benutzerdefinierte Adressen.
* **Passphrase- & Schlüsselschutz**: Optionale Absicherung für eigene Nym-Accounts / Mnemonic-Keys.
* **Audit-Log Export**: 1-Klick JSON-Download aller Sicherheitsereignisse.

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
