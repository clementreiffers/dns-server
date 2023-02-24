import sys
from threading import Thread

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QMessageBox,
)

from change_dns_address import change_dns
from constants import GOOGLE_DNS, LOCALHOST
from dns_server import launch_dns
from watchdog import launch_watchdog


def create_btn_dns(dns):
    btn = QPushButton(f"change system dns to : {dns}")
    btn.clicked.connect(lambda: change_dns_and_invoke_window(dns))
    return btn


def change_dns_and_invoke_window(dns):
    change_dns(dns)
    msg = QMessageBox()
    msg.setText(f"dns changed to : {dns} !")
    msg.exec()


class Window(QMainWindow):
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Python DNS changing!")
        self.resize(400, 200)

        widget = QWidget(self)

        h_layout = QHBoxLayout()
        widget.setLayout(h_layout)

        h_layout.addWidget(create_btn_dns(GOOGLE_DNS))
        h_layout.addWidget(create_btn_dns(LOCALHOST))

        self.setCentralWidget(widget)


def launch_gui():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    Thread(target=launch_dns).start()
    Thread(target=launch_watchdog).start()
    launch_gui()
