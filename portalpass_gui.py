import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)


class PortalPassGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PortalPass')
        self.resize(340, 220)
        layout = QVBoxLayout()

        self.ssid_label = QLabel('Wi-Fi SSID:')
        self.ssid_input = QLineEdit()
        self.ssid_input.setPlaceholderText('e.g. Hotel_Guest_WiFi')

        self.mac_label = QLabel('MAC of your already-authorized device:')
        self.mac_input = QLineEdit()
        self.mac_input.setPlaceholderText('e.g. AA:BB:CC:DD:EE:FF')

        self.btn = QPushButton('Connect')
        self.btn.clicked.connect(self.run_portalpass)

        for w in (self.ssid_label, self.ssid_input,
                  self.mac_label, self.mac_input, self.btn):
            layout.addWidget(w)
        self.setLayout(layout)

    def run_portalpass(self):
        ssid = self.ssid_input.text().strip()
        mac = self.mac_input.text().strip()
        if not ssid or not mac:
            QMessageBox.warning(self, 'Missing info',
                                'Enter both the Wi-Fi SSID and the MAC address.')
            return
        # arg-list (not shell=True) so the SSID/MAC can't inject shell commands
        commands = [
            ['nmcli', 'con', 'modify', ssid, 'wifi.cloned-mac-address', mac],
            ['nmcli', 'con', 'modify', ssid, 'ipv4.dns', '8.8.8.8'],
            ['nmcli', 'con', 'modify', ssid, 'ipv4.ignore-auto-dns', 'yes'],
            ['nmcli', 'con', 'down', ssid],
            ['nmcli', 'con', 'up', ssid],
        ]
        for cmd in commands:
            subprocess.run(cmd)
        QMessageBox.information(self, 'Done',
                               'PortalPass applied. Your device should be online.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = PortalPassGUI()
    gui.show()
    sys.exit(app.exec_())
