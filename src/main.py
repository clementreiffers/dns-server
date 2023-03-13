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
from constants import GOOGLE_DNS, LOCALHOST, TMP_STATE
from dns_server import launch_dns
from fs import read_state_dns, set_state_dns_listening, set_state_dns_choosen, write_json_file
from watchdog import launch_watchdog


def create_btn_dns(dns):
    btn = QPushButton(f"change system dns to : {dns}")
    btn.clicked.connect(lambda: change_dns_and_invoke_window(dns))
    return btn


def wait_until_local_dns_is_listening():
    while not read_state_dns()["listening"]:
        pass


def change_dns_and_invoke_window(dns):
    set_state_dns_choosen(dns)
    # wait until the dns is listening
    if dns == LOCALHOST:
        wait_until_local_dns_is_listening()
    change_dns(dns)
    msg = QMessageBox()
    msg.setText(f"dns changed to : {dns} !")
    msg.exec()


def kill_app():
    set_state_dns_listening(False)
    exit(0)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        write_json_file(TMP_STATE, {"dns_choosen": GOOGLE_DNS, "listening": False})

        self.setWindowTitle("Python DNS changing!")
        self.resize(400, 200)

        widget = QWidget(self)

        v_layout = QVBoxLayout()
        widget.setLayout(v_layout)

        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)

        exit_btn = QPushButton("EXIT")
        exit_btn.clicked.connect(kill_app)
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
    change_dns("8.8.8.8")
    launch_gui()
