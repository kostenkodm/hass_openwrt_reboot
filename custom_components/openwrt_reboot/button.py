import logging
import paramiko
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_REBOOT_COMMAND = "reboot"
RESTART_WIFI_COMMAND = "/etc/init.d/network restart"
RESTART_VPRDNS_COMMAND = "vprdns"

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the buttons from a config entry."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([
        OpenWrtRebootButton(config["host"], config["username"], config["password"], config_entry.entry_id),
        OpenWrtWiFiRestartButton(config["host"], config["username"], config["password"], config_entry.entry_id),
        OpenWrtVprDnsRestartButton(config["host"], config["username"], config["password"], config_entry.entry_id),
    ])

class OpenWrtButtonBase(ButtonEntity):
    """Base class for OpenWrt buttons."""

    def __init__(self, host, username, password, entry_id):
        self._host = host
        self._username = username
        self._password = password
        self._entry_id = entry_id

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name="OpenWrt Router",
            manufacturer="OpenWrt",
            model="Custom Integration",
        )

class OpenWrtRebootButton(OpenWrtButtonBase):
    """Button to reboot the OpenWrt router."""

    @property
    def name(self):
        return "OpenWrt Reboot Router"

    @property
    def unique_id(self):
        return f"openwrt_reboot_{self._host}"

    async def async_press(self):
        await self._execute_command(DEFAULT_REBOOT_COMMAND)

    async def _execute_command(self, command):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self._host, username=self._username, password=self._password)
            stdin, stdout, stderr = client.exec_command(command)
            _LOGGER.info(f"Command '{command}' executed successfully on the router.")
            client.close()
        except Exception as e:
            _LOGGER.error(f"Failed to execute command '{command}': {e}")

class OpenWrtWiFiRestartButton(OpenWrtButtonBase):
    """Button to restart the Wi-Fi interface on the OpenWrt router."""

    @property
    def name(self):
        return "OpenWrt Restart Wi-Fi (radio0)"

    @property
    def unique_id(self):
        return f"openwrt_wifi_restart_{self._host}"

    async def async_press(self):
        await self._execute_command(RESTART_WIFI_COMMAND)

    async def _execute_command(self, command):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self._host, username=self._username, password=self._password)
            stdin, stdout, stderr = client.exec_command(command)
            _LOGGER.info(f"Command '{command}' executed successfully on the router.")
            client.close()
        except Exception as e:
            _LOGGER.error(f"Failed to execute command '{command}': {e}")

class OpenWrtVprDnsRestartButton(OpenWrtButtonBase):
    """Button to restart the VPR DNS on the OpenWrt router."""

    @property
    def name(self):
        return "OpenWrt Restart VPR DNS"

    @property
    def unique_id(self):
        return f"openwrt_vprdns_restart_{self._host}"

    async def async_press(self):
        await self._execute_command(RESTART_VPRDNS_COMMAND)

    async def _execute_command(self, command):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self._host, username=self._username, password=self._password)
            stdin, stdout, stderr = client.exec_command(command)
            _LOGGER.info(f"Command '{command}' executed successfully on the router.")
            client.close()
        except Exception as e:
            _LOGGER.error(f"Failed to execute command '{command}': {e}")
