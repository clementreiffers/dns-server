import sys
from threading import Thread

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QMessageBox,
    QVBoxLayout,
    QLabel,
)

from change_dns_address import change_dns
from constants import GOOGLE_DNS, LOCALHOST, TMP_STATE
from dns_server import launch_dns
from fs import read_state_dns, set_state_dns_listening, set_state_dns_choosen, write_json_file
from watchdog import launch_watchdog


def wait_until_local_dns_is_listening():
    while not read_state_dns()["listening"]:
        pass


def kill_app():
    set_state_dns_listening(False)
    change_dns(GOOGLE_DNS)
    exit(0)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        with open("stylesheet.css", "r") as f:
            self.style = f.read()
        self.setStyleSheet(self.style)
        self.is_on = False
        self.current_dns = GOOGLE_DNS
        self.objectName = "mainWindow"

        write_json_file(TMP_STATE, {"dns_choosen": self.current_dns, "listening": False})

        self.setWindowIcon(QIcon("../images/icon.ico"))
        self.setWindowTitle("Python DNS changing!")
        self.resize(400, 200)

        widget = QWidget(self)

        v_layout = QVBoxLayout()
        widget.setLayout(v_layout)

        self.label_current_dns = QLabel(self, objectName="currentDns")
        # label_current_dns.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label_current_dns.setText(f"current dns : {self.current_dns}")
        self.label_current_dns.setMaximumSize(self.size().width(), 10)
        self.label_current_dns.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        v_layout.addWidget(self.label_current_dns)

        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)

        exit_btn = QPushButton("EXIT", objectName="exit")
        exit_btn.clicked.connect(kill_app)
        v_layout.addWidget(exit_btn)

        self.on_off_btn = QPushButton("Off", objectName="off")
        self.on_off_btn.clicked.connect(lambda: self.change_dns_and_invoke_window())
        h_layout.addWidget(self.on_off_btn)

        self.setCentralWidget(widget)

    def change_dns_and_invoke_window(self):
        self.is_on = not self.is_on
        if self.is_on:
            dns = self.change_on_off("on", LOCALHOST)
        else:
            dns = self.change_on_off("off", GOOGLE_DNS)

        set_state_dns_choosen(dns)
        self.current_dns = dns
        self.label_current_dns.setText(f"current dns : {self.current_dns}")
        # wait until the dns is listening
        if dns == LOCALHOST:
            wait_until_local_dns_is_listening()
        change_dns(dns)
        msg = QMessageBox()
        msg.setText(f"dns changed to : {dns} !")
        msg.exec()

    def change_on_off(self, btnValue, dns):
        self.on_off_btn.setText(btnValue.capitalize())
        self.on_off_btn.setStyleSheet(
            f"background-color: {'green' if btnValue == 'on' else '#a91515'};"
        )
        # self.on_off_btn.setStyleSheet(self.style)
        return dns

    def closeEvent(self, event):
        kill_app()


def launch_gui():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


def start_daemon(f):
    thread = Thread(target=f)
    thread.daemon = True
    thread.start()


if __name__ == "__main__":
    start_daemon(launch_dns)
    start_daemon(launch_watchdog)
    change_dns("8.8.8.8")
    launch_gui()
