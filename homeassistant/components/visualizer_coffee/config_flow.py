"""Config flow for Visualizer Coffee."""

import logging

from homeassistant.config_entries import ConfigFlowResult
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.config_entry_oauth2_flow import (
    LocalOAuth2ImplementationWithPkce,
)

from .const import DOMAIN


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Config flow to handle Visualizer Coffee OAuth2 authentication."""

    DOMAIN = DOMAIN

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle a flow start."""

        # 1. Immediately register the PKCE flow using your generic public ID
        # (There is no form, so we don't care about user_input)
        config_entry_oauth2_flow.async_register_implementation(
            self.hass,
            DOMAIN,
            LocalOAuth2ImplementationWithPkce(
                self.hass,
                DOMAIN,
                # Replace this string with the Client ID you got from Visualizer!
                client_id="R4st1pmO4zNJWC4DRZlHz1oz9ps8UHvgZ4sRgQWb5_k",
                authorize_url="https://visualizer.coffee/oauth/authorize",
                token_url="https://visualizer.coffee/oauth/token",
            ),
        )

        # 2. Instantly push them to the redirect step
        return await self.async_step_pick_implementation()
