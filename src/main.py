import sys
from threading import Thread

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QMessageBox,
    QVBoxLayout,
)

from change_dns_address import change_dns
from constants import GOOGLE_DNS, LOCALHOST
from dns_server import launch_dns
from fs import read_state_dns
from watchdog import launch_watchdog


def create_btn_dns(dns):
    btn = QPushButton(f"change system dns to : {dns}")
    btn.clicked.connect(lambda: change_dns_and_invoke_window(dns))
    return btn


def change_dns_and_invoke_window(dns):
    # wait until the dns is listening
    if dns == LOCALHOST:
        while read_state_dns()["listening"]:
            continue
    change_dns(dns)
    msg = QMessageBox()
    msg.setText(f"dns changed to : {dns} !")
    msg.exec()


class Window(QMainWindow):
    def __init__(self):
        """Initializer."""
        super().__init__()
        self.setWindowTitle("Python DNS changing!")
        self.resize(400, 200)

        widget = QWidget(self)

        v_layout = QVBoxLayout()
        widget.setLayout(v_layout)

        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)

        exit_btn = QPushButton("EXIT")
        exit_btn.clicked.connect(lambda: exit(0))
        v_layout.addWidget(exit_btn)

        h_layout.addWidget(create_btn_dns(GOOGLE_DNS))
        h_layout.addWidget(create_btn_dns(LOCALHOST))

        self.setCentralWidget(widget)


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
    launch_gui()
