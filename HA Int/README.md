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

## 🎛️ Die 5 Einstellungs- und Cockpit-Bereiche

1. 📊 **Live Cockpit**: Animierte 3-Hop Routing Topologie mit interaktivem Krypto-Inspektor, 60s Echtzeit-Durchsatzdiagramm und Live Stream Inspector.
2. 🛡️ **HA Datenquellen-Schutz**: Dynamische Auswahl aller Smart-Home-Daten (KI & Sprachmodelle, Wetter/GPS, Messenger-Bots, dynamische Strompreise, Cloud-Backups, REST-Sensoren).
3. ⚙️ **Mixnet Krypto & Feintuning**: Presets (Eco, High, Ultra), stufenlose Poisson-Verzögerung (5–150 ms), SURB-Puffer (20–250 Tokens), DNS-over-Mixnet Isolation und weltweite Exit-Nodes.
4. 💎 **Nym Premium & Fast Pass**: Verwaltung von Bandwidth Credentials, zk-nyms (Coconut blinde Signaturen), High-Speed 100+ Mbps Queues für Backups/Kameras und Passphrase-Schutz.
5. 📋 **YAML Vorlagen**: 1-Klick Code-Snippets für die direkte Einbindung in Home Assistant.

---

## 🚀 Installation & Start

1. Add-on Repository in Home Assistant hinzufügen:
   ```text
   https://github.com/SyncNetOps/HA-NYM-Int
   ```
2. **Nym Privacy Hub** installieren, starten und in der linken Seitenleiste öffnen.
3. Im Tab **🛡️ HA Datenquellen** die gewünschten Smart-Home-Schutzschilde aktivieren!
