import subprocess, time, os, requests

# -- API ------------------------------------------------------------- #

class system:
	def __init__(self):
		pass

	def e(self, text, seconds):
		print(text)
		time.sleep(seconds)
		exit(0)

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
			print(f"Creating VPN connection with name '{self.vpn_name}'")
			command = [
				"powershell",
				"-Command",
				f"Add-VpnConnection -Name '{self.vpn_name}' -ServerAddress '{self.server_address}' "
				f"-TunnelType 'L2tp' -L2tpPsk '{self.pre_shared_key}' -AuthenticationMethod 'Pap' "
				"-RememberCredential -Force"
			]
			subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			print(f"VPN connection '{self.vpn_name}' created successfully.")
		except subprocess.CalledProcessError as e:
			print(f"Error creating VPN connection: {e}")

	def check(self):
		try:
			if not self.check_vpn_connection():
				self.create_vpn_connection()
			return True
		except Exception as e:
			return False

	def fix(self):
		subprocess.run("netsh int ip reset && netsh winsock reset", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		print("reboot pc.")
		input()

	def remove_vpn_connection(self):
		try:
			print(f"Removing VPN connection '{self.vpn_name}'")
			command = f"powershell -Command \"Remove-VpnConnection -Name '{self.vpn_name}' -Force\""
			subprocess.run(command, check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			print(f"VPN connection '{self.vpn_name}' removed successfully.")
		except subprocess.CalledProcessError as e:
			print(f"Error removing VPN connection: {e}\n\nRemove by yourself please. Sorry.")

	def connect_vpn(self):
		try:
			print(f"Connecting to VPN '{self.vpn_name}'")
			command = f'rasdial "{self.vpn_name}" "{self.username}" "{self.password}"'
			subprocess.run(command, check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			print(f"Connected to VPN '{self.vpn_name}'.")
			return True
		except subprocess.CalledProcessError as e:
			print(f"Error connecting to VPN: {e}")
			return False
			#print("Fixing ...")
			#self.fix()
			#system().e("reboot pc!!!", 3)

	def disconnect_vpn(self):
		try:
			command = f'rasdial "{self.vpn_name}" /disconnect'
			subprocess.run(command, check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			print(f"Disconnected from VPN '{self.vpn_name}'.")
			return True
		except subprocess.CalledProcessError as e:
			print(f"Error disconnecting from VPN: {e}")
			return False

# -------------------------------------------------------------------- #


system = system()
vpn = EasyVPN()
connection = None

menu = """EasyVPN 1.1 ( t.me/kryyaasoft )

[1] Connect
[2] Disconnect
[3] Delete configuration from system

user-choice : """

def main():
	global connection
	while True:
		system.title(f"Connection: {connection}")
		system.clear()
		user_choice = input(menu)
		try:
			user_choice = int(user_choice)
			if user_choice == 1:
				if vpn.check():
					if vpn.connect_vpn():
						connection = True
						print("Done.")
						time.sleep(2)
					else:
						vpn.fix()
			elif user_choice == 2:
				if vpn.check():
					if vpn.disconnect_vpn():
						connection = False
						print("Done.")
						time.sleep(2)
					else:
						vpn.fix()
			elif user_choice == 3:
				vpn.remove_vpn_connection()
				system.e("Done.", 2)
			else:
				time.sleep(1)
		except Exception as e:
			time.sleep(1)

if __name__ == '__main__':
	main()