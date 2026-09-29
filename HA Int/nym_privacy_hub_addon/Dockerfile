ARG BUILD_FROM
FROM ${BUILD_FROM}

ARG BUILD_ARCH

# Install runtime dependencies via apt
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    jq \
    ca-certificates \
    netcat-openbsd \
    python3 \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Download official Nym SOCKS5 client binary from latest release
RUN set -eux; \
    echo "Downloading Nym SOCKS5 client for ${BUILD_ARCH}..."; \
    NYM_DOWNLOAD_URL="https://github.com/nymtech/nym/releases/download/nym-binaries-v2026.18-essaouria/nym-socks5-client"; \
    curl -sSL -f "${NYM_DOWNLOAD_URL}" -o /usr/local/bin/nym-socks5-client || \
    curl -sSL -f "https://github.com/nymtech/nym/releases/latest/download/nym-socks5-client" -o /usr/local/bin/nym-socks5-client; \
    chmod +x /usr/local/bin/nym-socks5-client

# Prepare data and config directories
RUN mkdir -p /data/.nym /root/.nym && \
    ln -s /data/.nym /root/.nym_data

COPY server.py /usr/local/bin/server.py
RUN chmod +x /usr/local/bin/server.py

COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
