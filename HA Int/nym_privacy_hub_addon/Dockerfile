ARG BUILD_FROM
FROM ${BUILD_FROM}

ARG BUILD_ARCH
ARG NYM_VERSION="nym-binaries-v2024.1-calypso"

# Install runtime dependencies including Python for Ingress UI
RUN apk add --no-cache \
    curl \
    jq \
    ca-certificates \
    libgcc \
    libssl3 \
    netcat-openbsd \
    python3 \
    bash

# Download appropriate Nym binary based on architecture
RUN set -eux; \
    case "${BUILD_ARCH}" in \
        'amd64') \
            ARCH_NAME="x86_64-unknown-linux-musl"; \
            ;; \
        'aarch64') \
            ARCH_NAME="aarch64-unknown-linux-musl"; \
            ;; \
        'armv7') \
            ARCH_NAME="armv7-unknown-linux-musleabihf"; \
            ;; \
        *) \
            echo "Unsupported architecture: ${BUILD_ARCH}"; \
            exit 1; \
            ;; \
    esac; \
    echo "Downloading Nym SOCKS5 client for ${BUILD_ARCH} (${ARCH_NAME})..."; \
    NYM_DOWNLOAD_URL="https://github.com/nymtech/nym/releases/download/${NYM_VERSION}/nym-socks5-client"; \
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
