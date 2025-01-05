import logging
import paramiko
import io
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers import storage
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_REBOOT_COMMAND = "reboot"
RESTART_WIFI_COMMAND = "wifi down radio0 && wifi up radio0"
RESTART_VPRDNS_COMMAND = "vprdns"

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up buttons for OpenWrt integration."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    auth_method = config_entry.data.get("auth_method")

    if auth_method == "private_key":
        storage_path = storage.Store(1, f"{DOMAIN}_{config['host']}_key")
        key_data = await storage_path.async_load()
        private_key = key_data["key"] if key_data else None
        if not private_key:
            _LOGGER.error("Private key not found in storage.")
            return
    else:
        private_key = None

    async_add_entities([
        OpenWrtRebootButton(config["host"], config["username"], config.get("password"), private_key, config_entry.entry_id),
        OpenWrtWiFiRestartButton(config["host"], config["username"], config.get("password"), private_key, config_entry.entry_id),
        OpenWrtVprDnsRestartButton(config["host"], config["username"], config.get("password"), private_key, config_entry.entry_id),
    ])

class OpenWrtButtonBase(ButtonEntity):
    """Base class for OpenWrt buttons."""

    def __init__(self, host, username, password, private_key, entry_id):
        self._host = host
        self._username = username
        self._password = password
        self._private_key = private_key
        self._entry_id = entry_id

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name="OpenWrt Router",
            manufacturer="OpenWrt",
            model="Custom Integration",
        )

    async def _execute_command(self, command):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self._private_key:
                private_key_obj = paramiko.RSAKey.from_private_key(io.StringIO(self._private_key))
                client.connect(self._host, username=self._username, pkey=private_key_obj)
            else:
                client.connect(self._host, username=self._username, password=self._password)

            stdin, stdout, stderr = client.exec_command(command)
            _LOGGER.info(f"Command '{command}' executed successfully on the router.")
            client.close()
        except Exception as e:
            _LOGGER.error(f"Failed to execute command '{command}': {e}")

class OpenWrtRebootButton(OpenWrtButtonBase):
    @property
    def name(self):
        return "OpenWrt Reboot Router"

    @property
    def unique_id(self):
        return f"openwrt_reboot_{self._host}"

    async def async_press(self):
        await self._execute_command(DEFAULT_REBOOT_COMMAND)

class OpenWrtWiFiRestartButton(OpenWrtButtonBase):
    @property
    def name(self):
        return "OpenWrt Restart Wi-Fi (radio0)"

    @property
    def unique_id(self):
        return f"openwrt_wifi_restart_{self._host}"

    async def async_press(self):
        await self._execute_command(RESTART_WIFI_COMMAND)

class OpenWrtVprDnsRestartButton(OpenWrtButtonBase):
    @property
    def name(self):
        return "OpenWrt Restart VPR DNS"

    @property
    def unique_id(self):
        return f"openwrt_vprdns_restart_{self._host}"

    async def async_press(self):
        await self._execute_command(RESTART_VPRDNS_COMMAND)
