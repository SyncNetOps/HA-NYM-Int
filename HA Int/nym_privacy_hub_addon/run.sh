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
LOG_LEVEL="info"

if [ -f /data/options.json ]; then
    PROVIDER=$(jq -r '.provider // empty' /data/options.json 2>/dev/null || true)
    USE_REPLY_SURBS=$(jq -r '.use_reply_surbs // "true"' /data/options.json 2>/dev/null || true)
    COVER_TRAFFIC=$(jq -r '.cover_traffic // "false"' /data/options.json 2>/dev/null || true)
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

# Start Ingress Dashboard in background
python3 /usr/local/bin/server.py &
INGRESS_PID=$!
bashio::log.info "Ingress Dashboard gestartet (PID: ${INGRESS_PID}, Port: 8099)"

NYM_CLIENT_DIR="/data/.nym/socks5-clients/${CLIENT_ID}"

# Initialize the client if not already configured
if [ ! -d "${NYM_CLIENT_DIR}" ]; then
    bashio::log.info "Initialisiere Nym SOCKS5 Client (${CLIENT_ID}). Krypto-Schlüssel werden generiert..."
    
    SURB_OPT=""
    if [ "${USE_REPLY_SURBS}" = "true" ]; then
        SURB_OPT="--use-reply-surbs true"
    fi

    nym-socks5-client init \
        --id "${CLIENT_ID}" \
        --provider "${PROVIDER}" \
        ${SURB_OPT} || {
            bashio::log.warning "Init mit Zusatzoptionen fehlgeschlagen, versuche Basis-Init..."
            nym-socks5-client init --id "${CLIENT_ID}" --provider "${PROVIDER}"
        }
    
    bashio::log.info "Nym Client erfolgreich initialisiert!"
else
    bashio::log.info "Bestehende Nym-Schlüsselkonfiguration gefunden unter ${NYM_CLIENT_DIR}."
fi

bashio::log.info "Starte SOCKS5 Proxy auf 0.0.0.0:1080..."

# Start SOCKS5 client
exec nym-socks5-client run \
    --id "${CLIENT_ID}" \
    --host 0.0.0.0 \
    --port 1080
