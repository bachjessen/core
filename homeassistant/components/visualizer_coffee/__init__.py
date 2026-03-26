"""The Visualizer Coffee integration."""

from __future__ import annotations

from contextlib import asynccontextmanager

import aiohttp
from visualizer_coffee import VisualizerClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client, config_entry_oauth2_flow
from homeassistant.helpers.config_entry_oauth2_flow import (
    ImplementationUnavailableError,
    LocalOAuth2ImplementationWithPkce,
    OAuth2Session,
    async_get_config_entry_implementation,
)

from . import api
from .const import DOMAIN
from .coordinator import VisualizerCoordinator


class AuthenticatedSessionWrapper:
    """Wraps an aiohttp session to automatically inject OAuth tokens."""

    def __init__(self, session: aiohttp.ClientSession, auth) -> None:
        """Initialize the wrapper."""
        self._session = session
        self._auth = auth

    @asynccontextmanager
    async def request(self, method, url, **kwargs):
        """Intercept the request, add the token, and pass it along."""
        # 1. Ask Home Assistant for the latest valid token
        token = await self._auth.async_get_access_token()

        # 2. Inject the token into the headers
        headers = kwargs.get("headers") or {}
        headers["Authorization"] = f"Bearer {token}"
        kwargs["headers"] = headers

        # 3. Pass the modified request to the REAL session
        async with self._session.request(method, url, **kwargs) as response:
            yield response


_PLATFORMS: list[Platform] = [Platform.SENSOR]

type VisualizerConfigEntry = ConfigEntry[VisualizerCoordinator]


# # TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: VisualizerConfigEntry) -> bool:
    """Set up Visualizer Coffee from a config entry."""
    config_entry_oauth2_flow.async_register_implementation(
        hass,
        DOMAIN,
        LocalOAuth2ImplementationWithPkce(
            hass,
            DOMAIN,
            client_id="R4st1pmO4zNJWC4DRZlHz1oz9ps8UHvgZ4sRgQWb5_k",
            authorize_url="https://visualizer.coffee/oauth/authorize",
            token_url="https://visualizer.coffee/oauth/token",
        ),
    )
    try:
        implementation = await async_get_config_entry_implementation(hass, entry)
    except ImplementationUnavailableError as err:
        raise ConfigEntryNotReady(
            "OAuth2 implementation temporarily unavailable, will retry"
        ) from err

    session = OAuth2Session(hass, entry, implementation)

    api_auth = api.AsyncConfigEntryAuth(
        aiohttp_client.async_get_clientsession(hass), session
    )
    raw_session = aiohttp_client.async_get_clientsession(hass)
    smart_session = AuthenticatedSessionWrapper(raw_session, api_auth)
    client = VisualizerClient(smart_session)

    coordinator = VisualizerCoordinator(hass, entry, client)
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: VisualizerConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
