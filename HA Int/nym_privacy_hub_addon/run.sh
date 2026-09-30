#!/usr/bin/env bashio
# ==============================================================================
# Nym Privacy Hub Add-on for Home Assistant
# Starts the SOCKS5 mixnet proxy and the Ingress Web Dashboard
# ==============================================================================

CLIENT_ID="ha_nym_client"
DEFAULT_PROVIDER="Entztfv6Uaz2hpYHQJ6JKoaCTpDL5dja18SuQWVJAmmx.Cvhn9rBJw5Ay9wgHcbgCnVg89MPSV5s2muPV2YF1BXYu@Fo4f4SQLdoyoGkFae5TpVhRVoXCF8UiypLVGtGjujVPf"

bashio::log.info "Starte Nym Privacy Hub Add-on..."

# Ensure persistent data directory and symlink
mkdir -p /data/.nym
rm -rf /root/.nym
ln -s /data/.nym /root/.nym

# Safely extract configuration with direct JSON fallback
PROVIDER=""
USE_REPLY_SURBS="true"
COVER_TRAFFIC="false"
PASSPHRASE=""
LOG_LEVEL="info"

if [ -f /data/options.json ]; then
    PROVIDER=$(jq -r '.provider // empty' /data/options.json 2>/dev/null || true)
    USE_REPLY_SURBS=$(jq -r '.use_reply_surbs // "true"' /data/options.json 2>/dev/null || true)
    COVER_TRAFFIC=$(jq -r '.cover_traffic // "false"' /data/options.json 2>/dev/null || true)
    PASSPHRASE=$(jq -r '.passphrase // empty' /data/options.json 2>/dev/null || true)
    LOG_LEVEL=$(jq -r '.log_level // "info"' /data/options.json 2>/dev/null || true)
fi

# Fallback to bashio if jq didn't find value
if [ -z "${PROVIDER}" ] || [ "${PROVIDER}" = "null" ]; then
    if bashio::config.has_value 'provider' 2>/dev/null; then
        PROVIDER=$(bashio::config 'provider' 2>/dev/null || true)
    fi
fi

# Final fallback to standard reliable exit provider
if [ -z "${PROVIDER}" ] || [ "${PROVIDER}" = "null" ]; then
    bashio::log.warning "Kein Provider konfiguriert - verwende Standard Nym Exit Provider."
    PROVIDER="${DEFAULT_PROVIDER}"
fi

export RUST_LOG="${LOG_LEVEL:-info}"

bashio::log.info "Provider: ${PROVIDER}"
bashio::log.info "SURBs aktiv: ${USE_REPLY_SURBS}"
bashio::log.info "Cover Traffic: ${COVER_TRAFFIC}"
if [ -n "${PASSPHRASE}" ] && [ "${PASSPHRASE}" != "null" ]; then
    bashio::log.info "Passphrase: [GESCHÜTZT] (Passphrase-Verschlüsselung aktiv)"
else
    bashio::log.info "Passphrase: Keine (Automatisch generierte Mixnet-Schlüssel)"
fi

# Start Ingress Dashboard in background
python3 /usr/local/bin/server.py &
INGRESS_PID=$!
bashio::log.info "Ingress Dashboard gestartet (PID: ${INGRESS_PID}, Port: 8099)"

NYM_CLIENT_DIR="/root/.nym/socks5-clients/${CLIENT_ID}"
CONFIG_TOML="${NYM_CLIENT_DIR}/config/config.toml"

# Safe provider for client init (requires valid @ address)
INIT_PROVIDER="${PROVIDER}"
if [[ "${INIT_PROVIDER}" == rotate_* ]] || [[ "${INIT_PROVIDER}" != *"@"* ]]; then
    INIT_PROVIDER="${DEFAULT_PROVIDER}"
fi

# Initialize the client if not already configured
if [ ! -f "${CONFIG_TOML}" ]; then
    bashio::log.info "Initialisiere Nym SOCKS5 Client (${CLIENT_ID}). Krypto-Schlüssel werden generiert..."
    
    SURB_OPT=""
    if [ "${USE_REPLY_SURBS}" = "true" ]; then
        SURB_OPT="--use-reply-surbs true"
    fi

    nym-socks5-client init \
        --id "${CLIENT_ID}" \
        --provider "${INIT_PROVIDER}" \
        ${SURB_OPT} || {
            bashio::log.warning "Init mit Zusatzoptionen fehlgeschlagen, versuche Basis-Init..."
            nym-socks5-client init --id "${CLIENT_ID}" --provider "${INIT_PROVIDER}"
        }
    
    bashio::log.info "Nym Client erfolgreich initialisiert!"
else
    bashio::log.info "Bestehende Nym-Schlüsselkonfiguration gefunden unter ${CONFIG_TOML}."
fi

# Patch config.toml if missing credential_requests_database schema field
python3 - <<EOF
import os

config_path = "${CONFIG_TOML}"
if os.path.exists(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    lines = content.splitlines()
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        if line.strip() == "[storage_paths]":
            if "credential_requests_database" not in content:
                db_path = "/root/.nym/socks5-clients/${CLIENT_ID}/data/credentials_database.db"
                new_lines.append(f'credential_requests_database = "{db_path}"')
                modified = True
    
    if modified:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines) + "\n")
        print("[INFO] TOML Schema-Patch für credential_requests_database erfolgreich angewendet.")
EOF

bashio::log.info "Starte SOCKS5 Proxy auf 0.0.0.0:1080..."

# Graceful shutdown handler to preserve SURB database & crypto keys
_cleanup() {
    bashio::log.info "Empfange Beendigungssignal (Graceful Shutdown) - Sichere SURB-Datenbanken & Krypto-Status..."
    if [ -n "${NYM_PID}" ] && kill -0 "${NYM_PID}" 2>/dev/null; then
        bashio::log.info "Sende SIGTERM an Nym SOCKS5 Client (PID ${NYM_PID})..."
        kill -TERM "${NYM_PID}" 2>/dev/null || true
        wait "${NYM_PID}" 2>/dev/null || true
    fi
    if [ -n "${INGRESS_PID}" ] && kill -0 "${INGRESS_PID}" 2>/dev/null; then
        kill -TERM "${INGRESS_PID}" 2>/dev/null || true
    fi
    bashio::log.info "Nym Privacy Hub sauber beendet. Alle Datenbanken intakt gesichert."
    exit 0
}

trap _cleanup SIGTERM SIGINT SIGQUIT

# Start SOCKS5 client in background and wait for clean termination
nym-socks5-client run \
    --id "${CLIENT_ID}" \
    --host 0.0.0.0 \
    --port 1080 &
NYM_PID=$!

wait "${NYM_PID}"
