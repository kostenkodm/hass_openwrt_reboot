DOMAIN = "openwrt_reboot"

async def async_setup(hass, config):
    """Set up the OpenWrt Reboot component."""
    return True

async def async_setup_entry(hass, config_entry):
    """Set up OpenWrt Reboot from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = config_entry.data

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "button")
    )
    return True

async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(config_entry, "button")
    hass.data[DOMAIN].pop(config_entry.entry_id)
    return True
