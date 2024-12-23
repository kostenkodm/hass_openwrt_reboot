import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

class OpenWrtRebootConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OpenWrt Reboot."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                # Validate connection (optional)
                await self._test_connection(
                    user_input[CONF_HOST],
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                )
                return self.async_create_entry(title="OpenWrt Reboot", data=user_input)
            except Exception as e:
                _LOGGER.error(f"Connection test failed: {e}")
                errors["base"] = "connection_failed"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    async def _test_connection(self, host, username, password):
        """Test the connection to the router."""
        import paramiko
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        client.close()
