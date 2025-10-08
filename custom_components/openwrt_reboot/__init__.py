"""OpenWrt Reboot Integration"""

import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "openwrt_reboot"

PLATFORMS = ["button"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up OpenWrt Reboot integration from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # ✅ Новый API: используем async_forward_entry_setups
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.info("OpenWrt Reboot integration successfully set up for %s", entry.title)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload OpenWrt Reboot config entry."""

    # ✅ Новый API: используем async_unload_platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        _LOGGER.info("OpenWrt Reboot integration unloaded for %s", entry.title)

    return unload_ok
