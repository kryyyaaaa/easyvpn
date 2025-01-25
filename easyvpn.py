import subprocess
import time
import os
import requests
import curses

# -- API ------------------------------------------------------------- #

class System:
    def __init__(self):
        pass

    def e(self, text, seconds):
        print(text)
        time.sleep(seconds)
        exit(0)

    def reboot(self, seconds):
        os.system(f"shutdown /r /t {seconds}")

    def pause(self, text):
        print(text)
        os.system("pause >nul")

    def clear(self):
        os.system('cls')

    def title(self, title):
        os.system(f"title {title}")

class EasyVPN:
    def __init__(self):
        self.vpn_name = "kryyaasoft"
        self.server_address = requests.get("https://github.com/kryyyaaaa/easyvpn/raw/refs/heads/main/server").text.splitlines()[0]
        self.pre_shared_key = "vpn"
        self.username = "vpn"
        self.password = "vpn"

    def check_vpn_connection(self):
        try:
            command = f"powershell -Command \"Get-VpnConnection -Name '{self.vpn_name}'\""
            subprocess.run(command, check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False

    def create_vpn_connection(self):
        try:
            command = [
                "powershell",
                "-Command",
                f"Add-VpnConnection -Name '{self.vpn_name}' -ServerAddress '{self.server_address}' "
                f"-TunnelType 'L2tp' -L2tpPsk '{self.pre_shared_key}' -AuthenticationMethod 'Pap' "
                "-RememberCredential -Force"
            ]
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError as e:
            return False

    def check(self):
        try:
            if not self.check_vpn_connection():
                self.create_vpn_connection()
            return True
        except Exception as e:
            return False

    def fix(self):
        subprocess.run("netsh int ip reset && netsh winsock reset", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "Reboot your PC!"

    def remove_vpn_connection(self):
        try:
            command = f"powershell -Command \"Remove-VpnConnection -Name '{self.vpn_name}' -Force\""
            subprocess.run(command, check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError as e:
            return False

    def connect_vpn(self):
        try:
            command = f'rasdial "{self.vpn_name}" "{self.username}" "{self.password}"'
            subprocess.run(command, check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError as e:
            return False

    def disconnect_vpn(self):
        try:
            command = f'rasdial "{self.vpn_name}" /disconnect'
            subprocess.run(command, check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError as e:
            return False

# -------------------------------------------------------------------- #

system = System()
vpn = EasyVPN()
connection_status = "Disconnected"

def draw_menu(stdscr, selected_row_idx):
    stdscr.clear()
    stdscr.addstr(0, 0, "EasyVPN 1.2 ( t.me/kryyaasoft )")
    options = [
        "Connect",
        "Disconnect",
        "Fix VPN (REBOOT NEEDED)",
        "Delete configuration from system"
    ]

    for idx, option in enumerate(options):
        x = 0
        y = idx + 1
        if idx == selected_row_idx:
            stdscr.addstr(y, x, option, curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, option)

    stdscr.addstr(len(options) + 1, 0, f"Status: {connection_status}")
    stdscr.refresh()

def main(stdscr):
    global connection_status
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.refresh()

    current_row_idx = 0
    draw_menu(stdscr, current_row_idx)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < 3:  # 3 is the last index
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row_idx == 0:  # Connect
                if vpn.check() and vpn.connect_vpn():
                    connection_status = "Connected"
            elif current_row_idx == 1:  # Disconnect
                if vpn.check() and vpn.disconnect_vpn():
                    connection_status = "Disconnected"
            elif current_row_idx == 2:  # Fix VPN
                connection_status = vpn.fix()
                system.reboot(0)
            elif current_row_idx == 3:  # Delete configuration
                if vpn.remove_vpn_connection():
                    connection_status = "Configuration removed"
            draw_menu(stdscr, current_row_idx)
        draw_menu(stdscr, current_row_idx)

if __name__ == '__main__':
    curses.wrapper(main)