#!/usr/bin/env bashio
# ==============================================================================
# Nym Privacy Hub Add-on for Home Assistant
# Starts the SOCKS5 mixnet proxy and the Ingress Web Dashboard
# ==============================================================================

CLIENT_ID="ha_nym_client"
NYM_DIR="/data/.nym/socks5-clients/${CLIENT_ID}"

bashio::log.info "Starte Nym Privacy Hub Add-on..."

# Read configuration options
PROVIDER=$(bashio::config 'provider')
USE_REPLY_SURBS=$(bashio::config 'use_reply_surbs')
COVER_TRAFFIC=$(bashio::config 'cover_traffic')
LOG_LEVEL=$(bashio::config 'log_level')

export RUST_LOG="${LOG_LEVEL:-info}"

bashio::log.info "Provider: ${PROVIDER}"
bashio::log.info "SURBs aktiv: ${USE_REPLY_SURBS}"
bashio::log.info "Cover Traffic: ${COVER_TRAFFIC}"

# Start Ingress Dashboard in background
python3 /usr/local/bin/server.py &
INGRESS_PID=$!
bashio::log.info "Ingress Dashboard gestartet (PID: ${INGRESS_PID}, Port: 8099)"

# Create data directory structure if needed
mkdir -p /data/.nym

# Initialize the client if not already configured
if [ ! -d "${NYM_DIR}" ]; then
    bashio::log.info "Initialisiere Nym SOCKS5 Client (${CLIENT_ID}). Krypto-Schlüssel werden generiert..."
    
    SURB_FLAG=""
    if [ "${USE_REPLY_SURBS}" = "true" ]; then
        SURB_FLAG="--use-reply-surbs true"
    else
        SURB_FLAG="--use-reply-surbs false"
    fi

    nym-socks5-client init \
        --id "${CLIENT_ID}" \
        --custom-mixnet "/data/.nym" \
        --provider "${PROVIDER}" \
        ${SURB_FLAG} || {
            bashio::log.warning "Initialisierung mit spezifischem Pfad fehlgeschlagen, versuche Standard-Init..."
            nym-socks5-client init --id "${CLIENT_ID}" --provider "${PROVIDER}"
        }
    
    bashio::log.info "Nym Client erfolgreich initialisiert!"
else
    bashio::log.info "Bestehende Nym-Schlüsselkonfiguration gefunden."
fi

bashio::log.info "Starte SOCKS5 Proxy auf 0.0.0.0:1080..."

# Start SOCKS5 client
exec nym-socks5-client run \
    --id "${CLIENT_ID}" \
    --host 0.0.0.0 \
    --port 1080
