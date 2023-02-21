import ctypes
import os
import sys


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def change_dns(dns):
    os.system(f'netsh interface ip set dns name="Wi-Fi" static {dns}')


if __name__ == "__main__":
    if is_admin():
        change_dns("192.168.127.12")
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
