import pexpect
import time

class BluetoothCtl:
    def __init__(self):
        self.child = pexpect.spawn("bluetoothctl", encoding='utf-8')
        self.child.expect("#")

    def send_command(self, command, timeout=2):
        self.child.sendline(command)
        self.child.expect("#", timeout=timeout)
        return self.child.before

    def power_on(self):
        self.send_command("power on")

    def power_off(self):
        self.send_command("power off")

    def scan_on(self):
        self.send_command("scan on")

    def scan_off(self):
        self.send_command("scan off")

    def connect(self, mac_address):
        print(f"Connecting to {mac_address}")
        self.send_command(f"connect {mac_address}", timeout=5)

    def disconnect(self, mac_address):
        print(f"Disconnecting from {mac_address}")
        self.send_command(f"disconnect {mac_address}")

    def pair(self, mac_address):
        print(f"Pairing with {mac_address}")
        self.send_command(f"pair {mac_address}", timeout=5)

    def remove(self, mac_address):
        print(f"Removing {mac_address}")
        self.send_command(f"remove {mac_address}")

    def list_devices(self):
        return self.send_command("devices")

    def find_device_by_name(self, target_name, timeout=3):
        devices = self.list_devices()
        for line in devices.split('\n'):
            if target_name in line:
                mac_address = line.split()[1]
                print(f"Found known device {target_name} with MAC address: {mac_address}")
                return mac_address

        print(f"{target_name} not found among known devices. Scanning for new devices...")
        self.scan_on()
        time.sleep(timeout)
        self.scan_off()
        devices = self.list_devices()
        for line in devices.split('\n'):
            if target_name in line:
                mac_address = line.split()[1]
                print(f"Found new device {target_name} with MAC address: {mac_address}")
                return mac_address
        return None

    def check_connection(self, mac_address):
        info_output = self.send_command(f"info {mac_address}")
        return "Connected: yes" in info_output

def main():
    target_name = "Multi Role"
    bt = BluetoothCtl()
    bt.power_on()
    time.sleep(1)

    while True:
        print("Checking for known devices...")
        mac_address = bt.find_device_by_name(target_name)
        if mac_address:
            connected = False
            while not connected:
                print(f"Attempting to connect to {mac_address}")
                bt.connect(mac_address)
                time.sleep(1)  # Reduced wait time for faster attempts

                print(f"Attempting to pair with {mac_address}")
                bt.pair(mac_address)
                time.sleep(1)  # Reduced wait time for faster attempts

                if bt.check_connection(mac_address):
                    print(f"Successfully paired with {target_name} ({mac_address})")
                    connected = True
                else:
                    print(f"Pairing failed with {mac_address}. Retrying...")
                    bt.remove(mac_address)
                    time.sleep(1)  # Reduced wait time before retrying
        else:
            print(f"{target_name} not found. Retrying...")

        time.sleep(1)  # Reduced poll interval for faster retry

    bt.power_off()

if __name__ == "__main__":
    main()
