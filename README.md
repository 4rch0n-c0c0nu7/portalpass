# PortalPass

Clone-and-connect for headless devices on captive-portal Wi-Fi.

Some Wi-Fi networks (hotels, airports, cafes) put a **captive portal** — a
"click to accept the terms" web page — in front of the connection. Headless or
browserless devices (a Raspberry Pi, an IoT gadget, a game console) can't
display that page, so they never get online even when you're an authorized user.

PortalPass works around that by setting the device's Wi-Fi MAC to the MAC of a
device you've **already** authenticated on the portal, so the network treats
your headless device as the one that already accepted the terms.

## Usage

GUI:

```bash
python3 portalpass_gui.py
```

CLI:

```bash
./portalpass.sh
```

Enter the network's SSID and the MAC address of your already-authorized device.

## Intended use

Use it only when **all** of these are true:

- It's **your own** device whose MAC you're cloning.
- You're an **authorized user** of the network and have **accepted its terms**
  on your primary device.
- You're not evading a paywall or per-device charge you haven't paid, and not
  impersonating anyone else's device.

Don't use it on networks you aren't authorized on, or to pose as hardware that
isn't yours. You are responsible for complying with each network's terms of
service and your local laws.

## Requirements

- Linux with NetworkManager (`nmcli`)
- The GUI needs PyQt5 (`pip install PyQt5`)

## How it works

```
nmcli con modify <SSID> wifi.cloned-mac-address <MAC>   # adopt the authorized MAC
nmcli con modify <SSID> ipv4.dns 8.8.8.8                # use a public resolver
nmcli con modify <SSID> ipv4.ignore-auto-dns yes
nmcli con down <SSID> && nmcli con up <SSID>            # reconnect
```

With the same MAC, only one of the two devices should be on the network at a
time — PortalPass hands your authorized session to the headless device, it
doesn't create an extra one.
