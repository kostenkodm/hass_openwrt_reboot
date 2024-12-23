# OpenWrt Reboot Integration for Home Assistant

This Home Assistant custom integration adds button entities to remotely manage your OpenWrt router. With this integration, you can:

- **Reboot your router** with a single button press.  
- **Restart the Wi-Fi interface** (`radio0`) without rebooting the entire router.  
- Easily configure the integration via Home Assistant’s UI.  

## Features
- **Simple Configuration**: Set up your router’s host, username, and password directly from the Home Assistant interface.  
- **Device Integration**: View and manage buttons directly in the Devices & Services menu.  
- **Secure Commands**: Uses Paramiko to securely execute SSH commands on your OpenWrt router.  

## Requirements
- An OpenWrt router with SSH access enabled.  
- Home Assistant installed and running.  

## Installation
1. Clone or download the repository into your `custom_components` directory.  
2. Restart Home Assistant.  
3. Add the integration via **Settings → Devices & Services → Add Integration → OpenWrt Reboot**.  

## Example Use Cases
- Automate your router’s reboot schedule.  
- Quickly resolve Wi-Fi issues by restarting the interface without disrupting other services.  
