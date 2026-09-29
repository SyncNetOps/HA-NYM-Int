"""The Nym Privacy Hub Integration."""
from __future__ import annotations

import logging
import os
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, PLATFORMS
from .coordinator import NymDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Nym Privacy Hub from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = NymDataUpdateCoordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(update_listener))

    frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
    if os.path.exists(frontend_path):
        hass.http.register_static_path(
            "/nym_privacy_hub_frontend",
            frontend_path,
            cache_headers=False,
        )
        _LOGGER.info("Registered Nym Privacy Hub Lovelace Card at /nym_privacy_hub_frontend/nym-privacy-hub-card.js")

    async def async_test_connection_service(call: ServiceCall) -> None:
        """Service to trigger a manual Mixnet connection test."""
        _LOGGER.info("Manuelle Nym Mixnet Verbindungsprüfung ausgelöst...")
        await coordinator.async_request_refresh()

    async def async_send_anonymous_request_service(call: ServiceCall) -> ServiceResponse:
        """Service to send an HTTP request routed via SOCKS5 Mixnet."""
        url = call.data.get("url")
        method = call.data.get("method", "GET").upper()
        if not url:
            raise ValueError("URL parameter ist erforderlich.")
        
        result = await coordinator.send_anonymous_request(url, method)
        return result

    hass.services.async_register(
        DOMAIN, "test_connection", async_test_connection_service
    )
    hass.services.async_register(
        DOMAIN,
        "send_anonymous_request",
        async_send_anonymous_request_service,
        supports_response=SupportsResponse.OPTIONAL,
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)
