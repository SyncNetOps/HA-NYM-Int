"""Switch platform for Nym Privacy Hub."""
from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_AI_VOICE_PRIVACY,
    CONF_COVER_TRAFFIC,
    CONF_GEO_WEATHER_PRIVACY,
    DEFAULT_AI_VOICE_PRIVACY,
    DEFAULT_COVER_TRAFFIC,
    DEFAULT_GEO_WEATHER_PRIVACY,
    DOMAIN,
)
from .coordinator import NymDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Nym Privacy Hub switches from config entry."""
    coordinator: NymDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            NymAiVoicePrivacySwitch(coordinator, entry),
            NymGeoWeatherPrivacySwitch(coordinator, entry),
            NymCoverTrafficSwitch(coordinator, entry),
        ]
    )


class NymToggleBase(CoordinatorEntity[NymDataUpdateCoordinator], SwitchEntity):
    """Base switch for privacy toggles."""

    def __init__(
        self,
        coordinator: NymDataUpdateCoordinator,
        entry: ConfigEntry,
        key: str,
        name: str,
        icon: str,
        default: bool,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._entry = entry
        self._key = key
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._default = default
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Nym Privacy Hub",
            manufacturer="Nym Technologies",
            model="SOCKS5 Mixnet Shield",
            sw_version="1.0.1",
        )

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._entry.options.get(
            self._key, self._entry.data.get(self._key, self._default)
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn switch on."""
        new_options = dict(self._entry.options)
        new_options[self._key] = True
        self.hass.config_entries.async_update_entry(self._entry, options=new_options)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn switch off."""
        new_options = dict(self._entry.options)
        new_options[self._key] = False
        self.hass.config_entries.async_update_entry(self._entry, options=new_options)
        self.async_write_ha_state()


class NymAiVoicePrivacySwitch(NymToggleBase):
    """Switch for AI & Voice Privacy routing."""

    def __init__(
        self, coordinator: NymDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize switch."""
        super().__init__(
            coordinator,
            entry,
            CONF_AI_VOICE_PRIVACY,
            "KI & Voice Privacy",
            "mdi:account-voice",
            DEFAULT_AI_VOICE_PRIVACY,
        )


class NymGeoWeatherPrivacySwitch(NymToggleBase):
    """Switch for Weather & Geo privacy."""

    def __init__(
        self, coordinator: NymDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize switch."""
        super().__init__(
            coordinator,
            entry,
            CONF_GEO_WEATHER_PRIVACY,
            "Wetter & Geodaten Schutz",
            "mdi:map-marker-radius",
            DEFAULT_GEO_WEATHER_PRIVACY,
        )


class NymCoverTrafficSwitch(NymToggleBase):
    """Switch for Anti-Einbruchs-Schutz / Cover Traffic."""

    def __init__(
        self, coordinator: NymDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize switch."""
        super().__init__(
            coordinator,
            entry,
            CONF_COVER_TRAFFIC,
            "Anti-Einbruchs-Schutz (Cover Traffic)",
            "mdi:shield-account",
            DEFAULT_COVER_TRAFFIC,
        )
