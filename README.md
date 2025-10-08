# OpenWrt Reboot Integration for Home Assistant
This custom Home Assistant integration allows you to **reboot your OpenWrt router, restart Wi-Fi, or execute the `vprdns` command** directly from Home Assistant via SSH.

---

## 🧩 Features

- 🔁 Reboot OpenWrt router via SSH
- 📶 Restart Wi-Fi (radio0 or custom interface)
- 🔐 Support for both **password** and **private key** authentication
- 🔍 Zeroconf discovery support
- 🪄 Native Home Assistant button entities

---

## ⚙️ Installation (via HACS)

1. Go to **HACS → Integrations → Custom repositories**
2. Add repository URL:  
   `https://github.com/kostenkodm/hass_openwrt_reboot`
   Type: `Integration`
3. Search for **OpenWrt Reboot** and install it.
4. Restart Home Assistant.
5. Go to **Settings → Devices & Services → Add Integration → OpenWrt Reboot**

---

## 🔑 Authentication

You can choose between:
- **Password authentication**  
- **Private key authentication** (recommended)

If using a private key, ensure it is stored on your Home Assistant host and accessible to the integration.

---

## 🧠 Required components on OpenWrt

Make sure the following packages are installed on your router:

```
opkg update
opkg install openssh-server openssh-client bash coreutils
```

If you use **VPN Policy Routing** and the `vprdns` command, install it too:

```
opkg install vpn-policy-routing
```

Ensure SSH access is enabled and the Home Assistant host is allowed to connect.

---

## 🪄 Available Buttons

- 🖲️ **Reboot Router** — executes `reboot`
- 📡 **Restart Wi-Fi** — executes `wifi down radio0 && wifi up radio0`
- 🌍 **Run vprdns** — executes `vprdns`

---

## 🔧 Configuration Example

Example entity in Home Assistant:

```yaml
type: entities
entities:
  - entity: button.openwrt_reboot_router
  - entity: button.openwrt_restart_wifi
  - entity: button.openwrt_vprdns
```

---

## 🧰 Troubleshooting

If commands fail:
- Verify SSH credentials
- Ensure the router’s IP is reachable
- Check permissions for your SSH key

---

## 🧾 License

MIT License © [kostenkodm](https://github.com/kostenkodm)

---

## 🆕 Changelog

### v1.0.4
- Added `vprdns` custom command
- Added Zeroconf discovery
- Added dual authentication (password/key)
- Added English & Russian translations
