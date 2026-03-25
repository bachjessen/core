"""Application credentials platform for the Visualizer Coffee integration."""

from homeassistant.components.application_credentials import AuthorizationServer
from homeassistant.core import HomeAssistant

from .const import OAUTH2_AUTHORIZE, OAUTH2_TOKEN


async def async_get_authorization_server(hass: HomeAssistant) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )


# TODO when i get PKCE support enabled by the developer of visualizer.coffee, add the following to the returned AuthorizationServer:
# from homeassistant.core import HomeAssistant
# from homeassistant.helpers.config_entry_oauth2_flow import AbstractOAuth2Implementation, LocalOAuth2ImplementationWithPkce
# from homeassistant.components.application_credentials import AuthImplementation, ClientCredential

# from .const import OAUTH2_AUTHORIZE, OAUTH2_TOKEN

# async def async_get_auth_implementation(
#     hass: HomeAssistant, auth_domain: str, credential: ClientCredential
# ) -> AbstractOAuth2Implementation:
#     """Return auth implementation for a custom auth implementation."""
#     return LocalOAuth2ImplementationWithPkce(
#         hass,
#         auth_domain,
#         credential.client_id,
#         authorize_url=OAUTH2_AUTHORIZE,
#         token_url=OAUTH2_TOKEN,
#         client_secret=credential.client_secret, # optional `""` is default
#         code_verifier_length=128 # optional
#     )
