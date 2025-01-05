import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import storage
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig
from . import DOMAIN

class OpenWrtConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OpenWrt Reboot integration."""

    VERSION = 1

    def __init__(self):
        self._auth_method = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            self._auth_method = user_input["auth_method"]
            return await self.async_step_auth_details()

        data_schema = vol.Schema({
            vol.Required("auth_method", default="password"): vol.In(
                {"password": "Пароль", "private_key": "Приватный ключ"}
            )
        })
        return self.async_show_form(step_id="user", data_schema=data_schema)

    async def async_step_auth_details(self, user_input=None):
        """Handle the step to collect authentication details."""
        if user_input is not None:
            if self._auth_method == "private_key":
                storage_path = self.hass.helpers.storage.Store(1, f"{DOMAIN}_{user_input['host']}_key")
                await storage_path.async_save({"key": user_input["private_key"]})
                del user_input["private_key"]

            return self.async_create_entry(title="OpenWrt Router", data=user_input)

        if self._auth_method == "password":
            data_schema = vol.Schema({
                vol.Required("host"): str,
                vol.Required("username"): str,
                vol.Required("password"): str,
            })
        else:
            data_schema = vol.Schema({
                vol.Required("host"): str,
                vol.Required("username"): str,
                vol.Required("private_key"): str,
            })

        return self.async_show_form(step_id="auth_details", data_schema=data_schema)
