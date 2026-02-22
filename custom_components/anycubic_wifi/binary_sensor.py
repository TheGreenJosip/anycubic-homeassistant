"""Platform for binary sensor integration."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .base_entry_decorator import AnycubicEntityBaseDecorator
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform from config_entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([MonoXPrintingBinarySensor(entry, coordinator)])


class MonoXPrintingBinarySensor(AnycubicEntityBaseDecorator, BinarySensorEntity):
    """Binary sensor that indicates if the printer is currently printing."""

    _attr_device_class = None  # could be "running" but HA doesn't have that device_class

    def __init__(self, entry: ConfigEntry, bridge) -> None:
        """Initialize the binary sensor.
        :param entry: the configuration data.
        :param bridge: the data bridge coordinator.
        """
        super().__init__(entry=entry, bridge=bridge, sensor_generic_name="Printing")

    @property
    def is_on(self) -> bool:
        """Return True if the printer is currently printing."""
        # bridge.data is a MonoXStatus object (or STATUS_OFFLINE)
        status = getattr(self.bridge.data, "status", None)
        return status == "print"
