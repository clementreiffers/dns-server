import ctypes
import os
import sys

from constants import GOOGLE_DNS
from fs import set_state_dns


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def change_dns(dns):
    if dns == GOOGLE_DNS:
        set_state_dns(False)

    print(f"changing dns to {dns}...")
    os.system(f'netsh interface ip set dns name="Wi-Fi" static {dns}')


def restart_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


if __name__ == "__main__":
    dns = sys.argv[1]
    if is_admin():
        change_dns(dns)
    else:
        restart_as_admin()
