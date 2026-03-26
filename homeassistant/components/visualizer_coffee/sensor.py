"""Support for Visualizer Coffee sensors."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import VisualizerConfigEntry
from .entity import visualizer_coffee


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: VisualizerConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Visualizer Coffee sensors from a config entry."""

    # 1. Grab the Broadcaster (Coordinator) from the storage pocket
    coordinator = config_entry.runtime_data

    # 2. Add the sensors and hand them the Broadcaster
    async_add_entities([TotalShotsSensor(coordinator), Identity(coordinator)])


class TotalShotsSensor(visualizer_coffee, SensorEntity):
    """Sensor that displays total shot count."""

    def __init__(self, coordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Total Shots"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_total_shots"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        # Check if the coordinator has fetched data yet
        if not self.coordinator.data:
            return None

        # Safely pull the number from the dictionary
        return self.coordinator.data.get("total_shots")


class Identity(visualizer_coffee, SensorEntity):
    """Sensor that displays name of the user."""

    def __init__(self, coordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Identity"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_identity"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        # Check if the coordinator has fetched data yet
        if not self.coordinator.data:
            return None

        # Safely pull the string from the dictionary
        return self.coordinator.data.get("account_name")
