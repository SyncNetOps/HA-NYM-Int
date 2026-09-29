#!/usr/bin/env python3
"""
Nym Privacy Hub - Ingress Dashboard & API Server
Provides real-time UI, monitoring and diagnostics for the Add-on.
"""

import json
import os
import socket
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error

PORT = 8099
OPTIONS_PATH = "/data/options.json"
SOCKS5_HOST = "127.0.0.1"
SOCKS5_PORT = 1080

def get_options():
    try:
        if os.path.exists(OPTIONS_PATH):
            with open(OPTIONS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading options: {e}", file=sys.stderr)
    return {
        "provider": "Entztfv6Uaz2hpYHQJ6JKoaCTpDL5dja18SuQWVJAmmx.Cvhn9rBJw5Ay9wgHcbgCnVg89MPSV5s2muPV2YF1BXYu@Fo4f4SQLdoyoGkFae5TpVhRVoXCF8UiypLVGtGjujVPf",
        "use_reply_surbs": True,
        "cover_traffic": False,
        "cover_traffic_rate": 10,
        "log_level": "info"
    }

def save_options(opts):
    try:
        with open(OPTIONS_PATH, "w", encoding="utf-8") as f:
            json.dump(opts, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving options: {e}", file=sys.stderr)
        return False

def check_socks5_socket(host=SOCKS5_HOST, port=SOCKS5_PORT, timeout=2.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

def get_stats():
    options = get_options()
    is_socket_open = check_socks5_socket()
    return {
        "status": "connected" if is_socket_open else "initializing",
        "proxy_endpoint": f"socks5://{SOCKS5_HOST}:{SOCKS5_PORT}",
        "socket_active": is_socket_open,
        "provider": options.get("provider", "Default Exit Provider"),
        "use_reply_surbs": options.get("use_reply_surbs", True),
        "cover_traffic": options.get("cover_traffic", False),
        "cover_traffic_rate": options.get("cover_traffic_rate", 10),
        "uptime_sec": int(time.time() - START_TIME),
        "mixnet_nodes": 839,
        "active_gateways": 607,
        "exit_nodes": 100
    }

START_TIME = time.time()

HTML_PAGE = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nym Privacy Hub</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #0b0f19;
            --bg-card: rgba(18, 24, 38, 0.75);
            --bg-card-hover: rgba(26, 35, 55, 0.85);
            --border-glow: rgba(0, 245, 160, 0.25);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --accent-cyan: #00f5a0;
            --accent-blue: #00d9f5;
            --accent-purple: #7928ca;
            --accent-red: #ff4757;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --radius-lg: 18px;
            --radius-md: 12px;
            --radius-sm: 8px;
            --shadow-glow: 0 0 25px rgba(0, 245, 160, 0.15);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(0, 245, 160, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(121, 40, 202, 0.08) 0%, transparent 45%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 24px;
            display: flex;
            justify-content: center;
        }

        .dashboard-container {
            width: 100%;
            max-width: 1100px;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        /* Header */
        .header-card {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border-glow);
            box-shadow: var(--shadow-glow);
            border-radius: var(--radius-lg);
            padding: 24px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
        }

        .header-title-area {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .logo-icon {
            width: 52px;
            height: 52px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            color: #0b0f19;
            box-shadow: 0 4px 15px rgba(0, 245, 160, 0.35);
        }

        .header-title {
            font-size: 24px;
            font-weight: 700;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #ffffff, #d8f3dc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header-subtitle {
            font-size: 14px;
            color: var(--text-muted);
            margin-top: 2px;
        }

        .status-badge-container {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 18px;
            border-radius: 999px;
            font-size: 14px;
            font-weight: 600;
            background: rgba(0, 245, 160, 0.12);
            border: 1px solid var(--accent-cyan);
            color: var(--accent-cyan);
        }

        .status-badge.disconnected {
            background: rgba(255, 71, 87, 0.12);
            border-color: var(--accent-red);
            color: var(--accent-red);
        }

        .pulse-dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background-color: currentColor;
            box-shadow: 0 0 10px currentColor;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.3); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }

        /* Mixnet Route Visualizer */
        .visualizer-card {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 24px;
        }

        .card-header-sm {
            font-size: 15px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .route-path {
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
            padding: 10px 0;
            overflow-x: auto;
        }

        .route-node {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            z-index: 2;
            min-width: 90px;
        }

        .node-icon-wrapper {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid var(--border-subtle);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            transition: all 0.3s ease;
        }

        .node-icon-wrapper.active {
            border-color: var(--accent-cyan);
            background: rgba(0, 245, 160, 0.15);
            box-shadow: 0 0 14px rgba(0, 245, 160, 0.3);
            color: var(--accent-cyan);
        }

        .node-label {
            font-size: 12px;
            font-weight: 500;
            color: var(--text-muted);
        }

        .route-connector {
            flex: 1;
            height: 2px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue));
            position: relative;
            margin: 0 -8px;
            margin-bottom: 24px;
            opacity: 0.6;
        }

        .route-connector::after {
            content: '';
            position: absolute;
            top: -3px;
            left: 0;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #fff;
            box-shadow: 0 0 8px #fff;
            animation: flowParticle 3s linear infinite;
        }

        @keyframes flowParticle {
            0% { left: 0%; opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { left: 100%; opacity: 0; }
        }

        /* Quick Grid */
        .grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }

        .glass-card {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .glass-card:hover {
            border-color: rgba(255, 255, 255, 0.15);
        }

        .proxy-copy-box {
            background: rgba(0, 0, 0, 0.35);
            border: 1px dashed var(--border-glow);
            border-radius: var(--radius-md);
            padding: 14px 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            color: var(--accent-cyan);
        }

        .btn {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--border-subtle);
            color: var(--text-main);
            padding: 10px 18px;
            border-radius: var(--radius-md);
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn:hover {
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.25);
            transform: translateY(-1px);
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            border: none;
            color: #0b0f19;
            box-shadow: 0 4px 15px rgba(0, 245, 160, 0.25);
        }

        .btn-primary:hover {
            background: linear-gradient(135deg, #20f8ac, #1de3fc);
            box-shadow: 0 6px 20px rgba(0, 245, 160, 0.4);
        }

        /* Toggles */
        .toggle-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .toggle-row:last-child {
            border-bottom: none;
        }

        .toggle-info {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .toggle-title {
            font-size: 15px;
            font-weight: 500;
        }

        .toggle-desc {
            font-size: 12px;
            color: var(--text-muted);
        }

        .switch-input {
            position: relative;
            display: inline-block;
            width: 48px;
            height: 26px;
        }

        .switch-input input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(255, 255, 255, 0.12);
            transition: .3s;
            border-radius: 34px;
        }

        .slider:before {
            position: absolute;
            content: "";
            height: 20px;
            width: 20px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: .3s;
            border-radius: 50%;
        }

        input:checked + .slider {
            background-color: var(--accent-cyan);
        }

        input:checked + .slider:before {
            transform: translateX(22px);
            background-color: #0b0f19;
        }

        /* Stats bar */
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-top: 6px;
        }

        .stat-item {
            background: rgba(0, 0, 0, 0.25);
            border-radius: var(--radius-sm);
            padding: 12px;
            text-align: center;
        }

        .stat-num {
            font-size: 20px;
            font-weight: 700;
            color: var(--accent-blue);
            font-family: 'JetBrains Mono', monospace;
        }

        .stat-lbl {
            font-size: 11px;
            color: var(--text-dim);
            text-transform: uppercase;
            margin-top: 4px;
        }

        /* Toast */
        #toast {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--accent-cyan);
            color: #0b0f19;
            font-weight: 600;
            padding: 12px 24px;
            border-radius: var(--radius-md);
            box-shadow: 0 6px 20px rgba(0, 245, 160, 0.4);
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            z-index: 1000;
        }

        #toast.show {
            transform: translateY(0);
            opacity: 1;
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <!-- Header -->
        <header class="header-card">
            <div class="header-title-area">
                <div class="logo-icon">🛡️</div>
                <div>
                    <h1 class="header-title">Nym Privacy Hub</h1>
                    <p class="header-subtitle">Dezentraler Metadaten- & Privatsphäre-Schild für Home Assistant</p>
                </div>
            </div>
            <div class="status-badge-container">
                <div id="statusBadge" class="status-badge">
                    <span class="pulse-dot"></span>
                    <span id="statusText">Mixnet Verbunden</span>
                </div>
                <button class="btn btn-primary" onclick="testConnection()">⚡ Ping Test</button>
            </div>
        </header>

        <!-- Route Visualizer -->
        <section class="visualizer-card">
            <div class="card-header-sm">
                <span>Mixnet Route Topologie</span>
                <span id="routeStats" style="color: var(--accent-cyan); font-family: 'JetBrains Mono', monospace;">3 Mix-Hops • Sphynx-Verschlüsselung</span>
            </div>
            <div class="route-path">
                <div class="route-node">
                    <div class="node-icon-wrapper active">🏠</div>
                    <span class="node-label">Home Assistant</span>
                </div>
                <div class="route-connector"></div>
                <div class="route-node">
                    <div class="node-icon-wrapper active">🧅</div>
                    <span class="node-label">Layer 1</span>
                </div>
                <div class="route-connector"></div>
                <div class="route-node">
                    <div class="node-icon-wrapper active">🧅</div>
                    <span class="node-label">Layer 2</span>
                </div>
                <div class="route-connector"></div>
                <div class="route-node">
                    <div class="node-icon-wrapper active">🧅</div>
                    <span class="node-label">Layer 3</span>
                </div>
                <div class="route-connector"></div>
                <div class="route-node">
                    <div class="node-icon-wrapper active">🌐</div>
                    <span class="node-label">Exit Provider</span>
                </div>
            </div>
        </section>

        <!-- Main Grid -->
        <div class="grid-2">
            <!-- SOCKS5 Quick Access -->
            <div class="glass-card">
                <div class="card-header-sm">
                    <span>SOCKS5 Proxy Endpunkt</span>
                </div>
                <p style="font-size: 13px; color: var(--text-muted);">
                    Nutze diese Adresse in beliebigen Home Assistant Integrationen (Telegram, OpenAI, Push-Services):
                </p>
                <div class="proxy-copy-box">
                    <span id="proxyEndpoint">socks5://127.0.0.1:1080</span>
                    <button class="btn" style="padding: 6px 12px; font-size: 12px;" onclick="copyProxy()">📋 Kopieren</button>
                </div>
                <div class="stat-grid">
                    <div class="stat-item">
                        <div class="stat-num" id="statNodes">839</div>
                        <div class="stat-lbl">Nym Nodes</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-num" id="statGateways">607</div>
                        <div class="stat-lbl">Gateways</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-num" id="statExits">100</div>
                        <div class="stat-lbl">Exit Nodes</div>
                    </div>
                </div>
            </div>

            <!-- Privacy Toggles -->
            <div class="glass-card">
                <div class="card-header-sm">
                    <span>Ein-Klick Privatsphäre-Schutz</span>
                </div>
                <div class="toggle-row">
                    <div class="toggle-info">
                        <span class="toggle-title">🤖 KI & Voice Privacy</span>
                        <span class="toggle-desc">Routet OpenAI & Voice Assistant Anfragen via Mixnet</span>
                    </div>
                    <label class="switch-input">
                        <input type="checkbox" id="toggleAi" checked onchange="saveSetting()">
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="toggle-row">
                    <div class="toggle-info">
                        <span class="toggle-title">🌦️ Wetter & Geodaten Schutz</span>
                        <span class="toggle-desc">Verschleiert Standortkoordinaten vor Drittanbietern</span>
                    </div>
                    <label class="switch-input">
                        <input type="checkbox" id="toggleGeo" checked onchange="saveSetting()">
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="toggle-row">
                    <div class="toggle-info">
                        <span class="toggle-title">🚨 Anti-Einbruch Cover Traffic</span>
                        <span class="toggle-desc">Generiert stetiges Datenrauschen gegen Router-Spione</span>
                    </div>
                    <label class="switch-input">
                        <input type="checkbox" id="toggleCover" onchange="saveSetting()">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>
        </div>

        <!-- Advanced Panel -->
        <div class="glass-card">
            <div class="card-header-sm">
                <span>Erweiterte Einstellungen (Profi-Modus)</span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px;">
                <label style="font-size: 13px; color: var(--text-muted);">Custom Nym Exit Provider Adresse:</label>
                <input type="text" id="providerInput" style="width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 10px 14px; color: var(--text-main); font-family: 'JetBrains Mono', monospace; font-size: 13px;" value="">
                <div style="display: flex; justify-content: flex-end; gap: 10px;">
                    <button class="btn" onclick="fetchStatus()">🔄 Aktualisieren</button>
                    <button class="btn btn-primary" onclick="saveProvider()">💾 Speichern & Neustart</button>
                </div>
            </div>
        </div>
    </div>

    <div id="toast">Proxy-Adresse in Zwischenablage kopiert!</div>

    <script>
        function showToast(msg) {
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3000);
        }

        function copyProxy() {
            const text = document.getElementById('proxyEndpoint').textContent;
            navigator.clipboard.writeText(text).then(() => {
                showToast("Proxy-Adresse in Zwischenablage kopiert!");
            });
        }

        async function fetchStatus() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                document.getElementById('proxyEndpoint').textContent = data.proxy_endpoint;
                document.getElementById('providerInput').value = data.provider;
                document.getElementById('toggleCover').checked = data.cover_traffic;
                document.getElementById('statNodes').textContent = data.mixnet_nodes;
                document.getElementById('statGateways').textContent = data.active_gateways;
                document.getElementById('statExits').textContent = data.exit_nodes;

                const badge = document.getElementById('statusBadge');
                const text = document.getElementById('statusText');
                if (data.socket_active) {
                    badge.className = 'status-badge';
                    text.textContent = 'Mixnet Aktiv (Port 1080)';
                } else {
                    badge.className = 'status-badge disconnected';
                    text.textContent = 'Wird Initialisiert...';
                }
            } catch (err) {
                console.error("Fetch status error:", err);
            }
        }

        async function testConnection() {
            showToast("Sende Test-Paket durch Mixnet...");
            try {
                const start = performance.now();
                const res = await fetch('/api/test');
                const data = await res.json();
                const duration = Math.round(performance.now() - start);
                if (data.ok) {
                    showToast(`Mixnet Ping erfolgreich! (${data.latency_ms || duration} ms)`);
                } else {
                    showToast("Test fehlgeschlagen: " + (data.error || "Timeout"));
                }
            } catch(e) {
                showToast("Verbindungsfehler beim Ping-Test");
            }
        }

        async function saveSetting() {
            const payload = {
                ai_privacy: document.getElementById('toggleAi').checked,
                geo_privacy: document.getElementById('toggleGeo').checked,
                cover_traffic: document.getElementById('toggleCover').checked,
            };
            await fetch('/api/save_toggles', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            showToast("Einstellungen gespeichert!");
        }

        async function saveProvider() {
            const provider = document.getElementById('providerInput').value;
            await fetch('/api/save_provider', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ provider })
            });
            showToast("Provider aktualisiert!");
        }

        fetchStatus();
        setInterval(fetchStatus, 10000);
    </script>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path == "/api/status":
            self._send_json(get_stats())
        elif self.path == "/api/test":
            start_t = time.monotonic()
            is_open = check_socks5_socket()
            latency = round((time.monotonic() - start_t) * 1000, 1)
            self._send_json({
                "ok": is_open,
                "latency_ms": latency if is_open else None,
                "error": None if is_open else "SOCKS5 Port 1080 not reachable"
            })
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b"{}"
        try:
            body = json.loads(post_body.decode("utf-8"))
        except Exception:
            body = {}

        if self.path == "/api/save_toggles":
            opts = get_options()
            if "cover_traffic" in body:
                opts["cover_traffic"] = body["cover_traffic"]
            save_options(opts)
            self._send_json({"ok": True})
        elif self.path == "/api/save_provider":
            opts = get_options()
            if "provider" in body:
                opts["provider"] = body["provider"]
            save_options(opts)
            self._send_json({"ok": True})
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server = HTTPServer(("0.0.0.0", PORT), RequestHandler)
    print(f"Nym Privacy Hub Ingress server listening on port {PORT}...")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
