"""API for Visualizer Coffee integration bound to Home Assistant OAuth."""

from aiohttp import ClientSession
import visualizer_coffee

from homeassistant.helpers import config_entry_oauth2_flow


class AsyncConfigEntryAuth(visualizer_coffee.AbstractAuth):
    """Provide NEW_NAME authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        websession: ClientSession,
        oauth_session: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        """Initialize NEW_NAME auth."""
        super().__init__(websession)
        self._oauth_session = oauth_session

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        await self._oauth_session.async_ensure_token_valid()

        return self._oauth_session.token["access_token"]
