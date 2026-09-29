"""Config flow for Nym Privacy Hub integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_AI_VOICE_PRIVACY,
    CONF_COVER_TRAFFIC,
    CONF_COVER_TRAFFIC_RATE,
    CONF_CUSTOM_PROVIDER,
    CONF_GEO_WEATHER_PRIVACY,
    CONF_PASSPHRASE,
    CONF_PROXY_HOST,
    CONF_PROXY_PORT,
    DEFAULT_AI_VOICE_PRIVACY,
    DEFAULT_COVER_TRAFFIC,
    DEFAULT_COVER_TRAFFIC_RATE,
    DEFAULT_GEO_WEATHER_PRIVACY,
    DEFAULT_PROXY_HOST,
    DEFAULT_PROXY_PORT,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class NymConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Nym Privacy Hub."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(f"nym_privacy_hub_{user_input[CONF_PROXY_HOST]}_{user_input[CONF_PROXY_PORT]}")
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title=f"Nym Mixnet ({user_input[CONF_PROXY_HOST]}:{user_input[CONF_PROXY_PORT]})",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_PROXY_HOST, default=DEFAULT_PROXY_HOST): cv.string,
                vol.Required(CONF_PROXY_PORT, default=DEFAULT_PROXY_PORT): cv.port,
                vol.Optional(
                    CONF_AI_VOICE_PRIVACY, default=DEFAULT_AI_VOICE_PRIVACY
                ): cv.boolean,
                vol.Optional(
                    CONF_GEO_WEATHER_PRIVACY, default=DEFAULT_GEO_WEATHER_PRIVACY
                ): cv.boolean,
                vol.Optional(
                    CONF_COVER_TRAFFIC, default=DEFAULT_COVER_TRAFFIC
                ): cv.boolean,
                vol.Optional(CONF_PASSPHRASE, default=""): cv.string,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> NymOptionsFlowHandler:
        """Get the options flow for this handler."""
        return NymOptionsFlowHandler(config_entry)


class NymOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Nym Privacy Hub."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        data = self.config_entry.data

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_AI_VOICE_PRIVACY,
                    default=options.get(
                        CONF_AI_VOICE_PRIVACY,
                        data.get(CONF_AI_VOICE_PRIVACY, DEFAULT_AI_VOICE_PRIVACY),
                    ),
                ): cv.boolean,
                vol.Optional(
                    CONF_GEO_WEATHER_PRIVACY,
                    default=options.get(
                        CONF_GEO_WEATHER_PRIVACY,
                        data.get(CONF_GEO_WEATHER_PRIVACY, DEFAULT_GEO_WEATHER_PRIVACY),
                    ),
                ): cv.boolean,
                vol.Optional(
                    CONF_COVER_TRAFFIC,
                    default=options.get(
                        CONF_COVER_TRAFFIC,
                        data.get(CONF_COVER_TRAFFIC, DEFAULT_COVER_TRAFFIC),
                    ),
                ): cv.boolean,
                vol.Optional(
                    CONF_COVER_TRAFFIC_RATE,
                    default=options.get(
                        CONF_COVER_TRAFFIC_RATE, DEFAULT_COVER_TRAFFIC_RATE
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=120)),
                vol.Optional(
                    CONF_CUSTOM_PROVIDER,
                    default=options.get(CONF_CUSTOM_PROVIDER, ""),
                ): cv.string,
                vol.Optional(
                    CONF_PASSPHRASE,
                    default=options.get(CONF_PASSPHRASE, ""),
                ): cv.string,
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
