"""Button platform for Nym Privacy Hub."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NymDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Nym Privacy Hub buttons from config entry."""
    coordinator: NymDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            NymReconnectButton(coordinator, entry),
        ]
    )


class NymReconnectButton(CoordinatorEntity[NymDataUpdateCoordinator], ButtonEntity):
    """Button to trigger Mixnet connection re-check and route refresh."""

    _attr_icon = "mdi:refresh-circle"

    def __init__(
        self, coordinator: NymDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = "Nym Verbindung aktualisieren"
        self._attr_unique_id = f"{entry.entry_id}_reconnect"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Nym Privacy Hub",
            manufacturer="Nym Technologies",
            model="SOCKS5 Mixnet Shield",
            sw_version="1.0.0",
        )

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.async_request_refresh()
