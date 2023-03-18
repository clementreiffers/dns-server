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
    change_dns("8.8.8.8")
    exit(0)


class Window(QMainWindow):
    current_dns = GOOGLE_DNS

    def __init__(self):
        super().__init__()

        write_json_file(TMP_STATE, {"dns_choosen": GOOGLE_DNS, "listening": False})

        self.setWindowIcon(QIcon("../images/icon.ico"))
        self.setWindowTitle("Python DNS changing!")
        self.resize(400, 200)

        widget = QWidget(self)

        v_layout = QVBoxLayout()
        widget.setLayout(v_layout)

        self.label_current_dns = QLabel(self)
        # label_current_dns.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label_current_dns.setText(f"current dns : {self.current_dns}")
        self.label_current_dns.setMaximumSize(self.size().width(), 10)
        self.label_current_dns.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        v_layout.addWidget(self.label_current_dns)

        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)

        exit_btn = QPushButton("EXIT")
        exit_btn.clicked.connect(kill_app)
        v_layout.addWidget(exit_btn)

        h_layout.addWidget(self.create_btn_dns(GOOGLE_DNS))
        h_layout.addWidget(self.create_btn_dns(LOCALHOST))

        self.setCentralWidget(widget)

    def create_btn_dns(self, dns):
        btn = QPushButton(f"change system dns to : {dns}")
        btn.clicked.connect(lambda: self.change_dns_and_invoke_window(dns))
        return btn

    def change_dns_and_invoke_window(self, dns):
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
