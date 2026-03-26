"""Example integration using DataUpdateCoordinator."""

import asyncio
from datetime import timedelta
import logging

from visualizer_coffee.exceptions import (
    VisualizerAuthError,
    VisualizerError,
    VisualizerRateLimitError,
)

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)


class VisualizerCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass, config_entry, client):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Visualizer.coffee coordinator",
            config_entry=config_entry,
            update_interval=timedelta(seconds=30),
            always_update=False,
        )
        self.client = client

    async def _async_update_data(self):
        """Fetch all data from the API."""
        try:
            async with asyncio.timeout(10):
                # 1. Fetch the Shots
                shots_response = await self.client.get_shots(items=1)
                count = (
                    shots_response.paging.count
                    if shots_response.paging.count is not None
                    else 0
                )

                # 2. Fetch the Account Info
                me_response = await self.client.get_me()

                # 3. Package EVERYTHING into a dictionary
                return {"total_shots": count, "account_name": me_response.name}

        except VisualizerAuthError as err:
            raise ConfigEntryAuthFailed from err
        except VisualizerRateLimitError as err:
            raise UpdateFailed(retry_after=60) from err
        except VisualizerError as err:
            raise UpdateFailed(f"Visualizer API error: {err}") from err
