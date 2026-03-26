"""Base entity for the Visualizer Coffee integration."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class visualizer_coffee(CoordinatorEntity):
    """Base entity for Visualizer Coffee."""

    Default_name = "Visualizer Coffee"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        if not self.coordinator.config_entry:
            return DeviceInfo(
                name=self.Default_name,
                manufacturer="visualizer.coffee",
            )

        return DeviceInfo(
            name=self.coordinator.config_entry.title or self.Default_name,
            manufacturer="visualizer.coffee",
            identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
        )
