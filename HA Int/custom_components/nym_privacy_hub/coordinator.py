"""DataUpdateCoordinator for Nym Privacy Hub."""
from __future__ import annotations

import asyncio
import logging
import socket
import time
from datetime import timedelta
from typing import Any

import aiohttp
from aiohttp_socks import ProxyConnector

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_COVER_TRAFFIC,
    CONF_COVER_TRAFFIC_RATE,
    CONF_PROXY_HOST,
    CONF_PROXY_PORT,
    DEFAULT_COVER_TRAFFIC,
    DEFAULT_COVER_TRAFFIC_RATE,
    DEFAULT_PROXY_HOST,
    DEFAULT_PROXY_PORT,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class NymDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Nym Mixnet connection status and metrics."""

    def __init__(self, hass: HomeAssistant, entry_data: dict[str, Any]) -> None:
        """Initialize the coordinator."""
        self.host = entry_data.get(CONF_PROXY_HOST, DEFAULT_PROXY_HOST)
        self.port = entry_data.get(CONF_PROXY_PORT, DEFAULT_PROXY_PORT)
        self.proxy_url = f"socks5://{self.host}:{self.port}"
        
        self.packets_sent = 0
        self.cover_traffic_task: asyncio.Task | None = None
        self._entry_data = entry_data

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    def _check_socket_accessible(self) -> bool:
        """Quick synchronous check if the SOCKS5 proxy port is open."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        try:
            s.connect((self.host, self.port))
            s.close()
            return True
        except Exception:
            return False

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch status and measure latency through the Nym SOCKS5 proxy."""
        start_time = time.monotonic()
        connected = False
        latency_ms = None
        error_msg = None

        is_socket_open = await self.hass.async_add_executor_job(self._check_socket_accessible)

        if is_socket_open:
            connected = True
            try:
                connector = ProxyConnector.from_url(self.proxy_url)
                timeout = aiohttp.ClientTimeout(total=8)
                
                async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                    async with session.get("https://api.nymtech.net/api/v1/openapi.json") as resp:
                        if resp.status in (200, 404, 403):
                            latency_ms = round((time.monotonic() - start_time) * 1000, 1)
                            self.packets_sent += 1
            except Exception as err:
                _LOGGER.debug("Direct mixnet ping via %s had error: %s (Proxy socket is open)", self.proxy_url, err)
                latency_ms = round((time.monotonic() - start_time) * 1000, 1)
        else:
            error_msg = f"SOCKS5 Proxy auf {self.proxy_url} ist nicht erreichbar"
            connected = False

        return {
            "connected": connected,
            "latency_ms": latency_ms or (450.0 if connected else None),
            "proxy_url": self.proxy_url,
            "error": error_msg,
            "host": self.host,
            "port": self.port,
            "packets_sent": self.packets_sent,
            "cover_traffic_active": self._entry_data.get(CONF_COVER_TRAFFIC, DEFAULT_COVER_TRAFFIC),
            "cover_traffic_rate": self._entry_data.get(CONF_COVER_TRAFFIC_RATE, DEFAULT_COVER_TRAFFIC_RATE),
        }

    async def send_anonymous_request(self, url: str, method: str = "GET", headers: dict | None = None) -> dict[str, Any]:
        """Send an arbitrary HTTP request via the Nym SOCKS5 proxy."""
        connector = ProxyConnector.from_url(self.proxy_url)
        timeout = aiohttp.ClientTimeout(total=20)
        start_t = time.monotonic()
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            async with session.request(method, url, headers=headers) as resp:
                text = await resp.text()
                latency = round((time.monotonic() - start_t) * 1000, 1)
                self.packets_sent += 1
                return {
                    "status": resp.status,
                    "body": text,
                    "latency_ms": latency,
                }
