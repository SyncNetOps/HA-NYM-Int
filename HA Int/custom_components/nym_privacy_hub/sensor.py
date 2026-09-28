"""Sensor platform for Nym Privacy Hub."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
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
    """Set up Nym Privacy Hub sensors from config entry."""
    coordinator: NymDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            NymMixnetStatusSensor(coordinator, entry),
            NymLatencySensor(coordinator, entry),
            NymProxyEndpointSensor(coordinator, entry),
            NymPacketsSentSensor(coordinator, entry),
            NymCoverTrafficRateSensor(coordinator, entry),
        ]
    )


class NymBaseEntity(CoordinatorEntity[NymDataUpdateCoordinator]):
    """Base entity for Nym Privacy Hub."""

    def __init__(
        self,
        coordinator: NymDataUpdateCoordinator,
        entry: ConfigEntry,
        entity_id_suffix: str,
    ) -> None:
        """Initialize base entity."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_{entity_id_suffix}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Nym Privacy Hub",
            manufacturer="Nym Technologies",
            model="SOCKS5 Mixnet Shield",
            sw_version="1.0.0",
        )


class NymMixnetStatusSensor(NymBaseEntity, SensorEntity):
    """Sensor showing Nym Mixnet connection state."""

    _attr_icon = "mdi:shield-lock"

    def __init__(
        self, coordinator: NymDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, "mixnet_status")
        self._attr_name = "Nym Mixnet Status"

    @property
    def native_value(self) -> str:
        """Return the current status."""
        if self.coordinator.data.get("connected"):
            return "connected"
        return "disconnected"

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        """Return extra attributes."""
        return {
            "proxy_url": self.coordinator.data.get("proxy_url"),
            "last_error": self.coordinator.data.get("error"),
        }


class NymLatencySensor(NymBaseEntity, SensorEntity):
    """Sensor measuring roundtrip latency through Nym Mixnet."""

    _attr_name = "Nym Mixnet Latenz"
    _attr_native_unit_of_measurement = UnitOfTime.MILLISECONDS
    _attr_device_class = SensorDeviceClass.DURATION
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:timer-outline"

    def __init__(
        self, coordinator: NymDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, "latency")

    @property
    def native_value(self) -> float | None:
        """Return the measured latency."""
        return self.coordinator.data.get("latency_ms")


class NymProxyEndpointSensor(NymBaseEntity, SensorEntity):
    """Sensor exposing the SOCKS5 proxy endpoint string."""

    _attr_name = "Nym Proxy Endpunkt"
    _attr_icon = "mdi:lan-connect"

    def __init__(
        self, coordinator: NymDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, "proxy_endpoint")

    @property
    def native_value(self) -> str:
        """Return the proxy endpoint URL."""
        return self.coordinator.data.get("proxy_url", "socks5://127.0.0.1:1080")


class NymPacketsSentSensor(NymBaseEntity, SensorEntity):
    """Sensor showing total packets/requests routed through mixnet."""

    _attr_name = "Nym Anonymisierte Pakete"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_icon = "mdi:package-variant-closed"

    def __init__(
        self, coordinator: NymDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, "packets_sent")

    @property
    def native_value(self) -> int:
        """Return total packets count."""
        return self.coordinator.data.get("packets_sent", 0)


class NymCoverTrafficRateSensor(NymBaseEntity, SensorEntity):
    """Sensor showing cover traffic generation rate."""

    _attr_name = "Nym Cover Traffic Rate"
    _attr_native_unit_of_measurement = "pkt/min"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:waveform"

    def __init__(
        self, coordinator: NymDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, "cover_traffic_rate")

    @property
    def native_value(self) -> int:
        """Return configured cover traffic rate."""
        return self.coordinator.data.get("cover_traffic_rate", 10)
