import ctypes
import os
import sys


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def change_dns(dns):
    os.system(f'netsh interface ip set dns name="Wi-Fi" static {dns}')


def restart_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


if __name__ == "__main__":
    dns = sys.argv[1]
    if is_admin():
        change_dns(dns)
    else:
        restart_as_admin()
