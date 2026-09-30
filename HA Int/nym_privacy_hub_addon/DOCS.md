# 🛡️ Home Assistant Add-on: Nym Privacy Hub

Der **Nym Privacy Hub** ist die offizielle All-in-One-Lösung, um deine gesamte Home Assistant Installation über das dezentrale **Nym Mixnet** vor Netzwerküberwachung, Metadaten-Tracking und Timing-Analysen abzusichern.

---

## 🌟 Warum Nym Mixnet statt herkömmlichem VPN?

Klassische VPNs verschlüsseln zwar den Datenstrom, leiten aber alle Daten über einen zentralen Server. Internet-Provider oder staatliche Akteure können anhand von **Paketgrößen und Zeitstempeln (Timing-Attacks)** genau analysieren, wann du im Smart Home Lichter schaltest, Sprachbefehle gibst oder das Haus verlässt.

### 🛡️ Die Nym-Vorteile auf einen Blick:
1. **Sphinx-Mehrschichtverschlüsselung**: Jedes Datenpaket wird in mehrere kryptografische Schichten gehüllt – kein Knoten kennt gleichzeitig Sender und Ziel.
2. **Dezentrale 3-Layer-Mixknoten**: Pakete werden über unabhängige globale Mixnodes gemischt, verzögert und in zufälliger Reihenfolge weitergeleitet.
3. **Anti-Einbruchs Cover Traffic**: Generiert künstliches Hintergrundrauschen, sodass niemand am Router ablesen kann, ob du schläfst, im Urlaub bist oder Alarmanlagen aktiv sind.
4. **SURBs (Single Use Reply Blocks)**: Ermöglicht Antworten aus dem Internet, ohne dass der Empfänger jemals deine IP-Adresse erfährt.
5. **Gleichförmige 2708-Byte Frames**: Verhindert jegliche Identifizierung von Geräten oder Protokollen anhand variierender Paketgrößen.
6. **Automatische weltweite Exit-Rotation**: Wechselt die sichtbare Internet-IP in regelmäßigen Intervallen zur Verhinderung von Langzeit-Profiling.

---

## 💡 Einfach erklärt: Die 5 Bereiche des Cockpits

### 1. 📊 Tab: Live Cockpit
* **Die Küchenmixer-Metapher**: Deine Daten werden wie in einem Mixer in kleine, identische 2708-Byte Päckchen zerlegt, mit künstlichem Rauschen vermischt und über 3 Server verteilt.
* **Live Route & Inspektor**: Klicke auf die Knoten, um zu sehen, was bei jedem Schritt passiert.
* **Canvas Durchsatz-Chart**: Zeigt in Echtzeit, wie viele Nutzdaten (`KB/s`, grün) und Cover-Loops (violett) fließen.

---

### 2. 🛡️ Tab: HA Datenquellen-Schutz (Dynamischer Scanner & Router)
Das Add-on scannt automatisch deine Home Assistant Instanz und zählt deine aktiven Sensoren:

| Datenquelle | Erkennung in deiner HA Instanz | Warum schützen? |
|---|---|---|
| **🤖 KI & Sprachassistenten** | Erkennt OpenAI, Anthropic, HA Assist | Verhindert, dass Cloud-KIs Sprachmuster und Tagesabläufe protokollieren. |
| **🌦️ Wetter & Geodaten** | Erkennt Open-Meteo, AccuWeather, Sun/Astro | Verhindert, dass Wetter-APIs deine exakten GPS-Hauskoordinaten erfahren. |
| **📱 Messenger & Bots** | Erkennt Telegram, Signal, Discord, Push | Maskiert Anwesenheits- und Alarmmeldungen vor neugierigen Providern. |
| **⚡ Dynamische Strompreise** | Erkennt Tibber, Nordpool, PV-Sensoren | Verhindert Rückschlüsse auf Ladezeiten von E-Autos oder Wärmepumpen. |
| **☁️ Cloud-Backups & Sync** | Erkennt Google Drive, Nextcloud, WebDAV | Verschleiert Zeitstempel und Upload-Mengen deiner Backups. |
| **🌐 Eigene REST / Scrape Sensoren** | Erkennt alle HTTP/REST/Scrape Entitäten | Verhindert IP-Korrelation über verschiedene externe Dienste hinweg. |

---

### 3. ⚙️ Tab: Mixnet Krypto & Automatische Exit-Rotation
* **Ist weltweite Exit-Rotation sinnvoll? JA, absolut!**
  * Wer monatelang immer dieselbe Exit-IP nutzt, kann von Webseiten wiedererkannt werden.
  * Bei aktivierter Rotation wechselt das Gateway (z.B. alle 15 Minuten) automatisch:
    * 🔄 **Weltweiter Pool**: Schweiz 🇨🇭 ➔ Deutschland 🇩🇪 ➔ Island 🇮🇸 ➔ Finnland 🇫🇮 ➔ Niederlande 🇳🇱 ➔ Singapur 🇸🇬 ➔ USA 🇺🇸.
    * 🏔️ **Privacy-Haven Pool**: Nur Länder mit extrem starken Datenschutzgesetzen (Schweiz, Island, Finnland).
    * 🇪🇺 **Europäischer Mix**: Schweiz, Deutschland, Island, Finnland, Niederlande.
* **Poisson-Verzögerung (5–150 ms)**: Zufällige Mikroverzögerungen zerstören Timing-Muster.
* **DNS-over-Mixnet**: DNS-Anfragen verlassen das Mixnet erst am Exit-Node.

---

### 4. 💎 Tab: Nym Premium, Fast Pass & ZK-Tokens
* **Kostenfrei vs. Fast Pass verständlich erklärt**:
  * *Kostenfreier Modus*: Wie eine sichere Landstraße – perfekt für Textmeldungen und Sensoren.
  * *Fast Pass VIP*: Wie eine reservierte VIP-Spur auf der Autobahn mit **über 100 Mbit/s Bandbreite** für Full-HD Kameras und Cloud-Backups.
* **Zero-Knowledge Nachweis (zk-nyms)**: Durch blinde kryptografische Signaturen weiß das Netzwerk, dass bezahlt wurde, **ohne deine Identität oder dein Smart Home zu kennen!**

---

### 5. 📋 Tab: YAML Vorlagen
Fertige Snippets für `configuration.yaml` (Telegram, REST Sensoren, Scrape, curl).
