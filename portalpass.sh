#!/bin/bash
# PortalPass -- connect a headless device to captive-portal Wi-Fi by reusing the
# MAC of a device you have already authorized on that portal. See README.md.

read -p "Enter the exact Wi-Fi SSID: " SSID
read -p "Enter the MAC of your already-authorized device (e.g. AA:BB:CC:DD:EE:FF): " MAC

echo "Configuring $SSID..."
nmcli con modify "$SSID" wifi.cloned-mac-address "$MAC"
nmcli con modify "$SSID" ipv4.dns "8.8.8.8"
nmcli con modify "$SSID" ipv4.ignore-auto-dns yes

echo "Restarting the connection..."
nmcli con down "$SSID"
nmcli con up "$SSID"

echo "Testing connectivity..."
ping -c 4 google.com
