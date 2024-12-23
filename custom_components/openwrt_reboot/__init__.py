import logging

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "openwrt_reboot"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the OpenWrt Reboot integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up the integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "button")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "button")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
