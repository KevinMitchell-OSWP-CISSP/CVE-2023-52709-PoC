#A script that assumes the device is already connected and sends the pairing request, pairing confirm, and pairing random messages in that specific order without further user interaction.
import pexpect
import time

class BluetoothCtl:
    def __init__(self):
        self.child = pexpect.spawn("bluetoothctl", encoding='utf-8')
        self.child.expect("#")

    def send_command(self, command, timeout=5):
        self.child.sendline(command)
        self.child.expect("#", timeout=timeout)
        return self.child.before

    def power_on(self):
        self.send_command("power on")

    def power_off(self):
        self.send_command("power off")

    def send_pairing_request(self, mac_address):
        print(f"Sending Pairing Request to {mac_address}")
        pairing_request_data = (
            "000084008000060001000004100000010000041000000100000410000001000004100000010000041000000100000410"
            "000001000004100000010000041000000100000410000001000004100000010000041000000100000410000001000004"
            "100000010000041000000100000410000001000004100000010000041000000100000410000001000004100000010000"
            "0410000001"
        )
        self.send_command(f"pair {mac_address} {pairing_request_data}", timeout=5)

    def send_pairing_confirm(self, mac_address):
        print(f"Sending Pairing Confirm to {mac_address}")
        pairing_confirm_data = (
            "0000150011000600031d9adfe958dd809adcbd7c227274"
        )
        self.send_command(f"pairing confirm {mac_address} {pairing_confirm_data}", timeout=5)

    def send_pairing_random(self, mac_address):
        print(f"Sending Pairing Random to {mac_address}")
        pairing_random_data = (
            "000015001100060004c0c0c0c0c0c0c0c0c0c0c0c0c0c0"
        )
        self.send_command(f"pairing random {mac_address} {pairing_random_data}", timeout=5)

def main():
    bt = BluetoothCtl()
    bt.power_on()
    time.sleep(1)

    mac_address = input("Enter the MAC address of the device: ")

    def send_sequence():
        bt.send_pairing_request(mac_address)
        time.sleep(2)
        bt.send_pairing_confirm(mac_address)
        time.sleep(2)
        bt.send_pairing_random(mac_address)
        time.sleep(2)
        print("Sequence of pairing messages sent successfully.")

    send_sequence()
    bt.power_off()

if __name__ == "__main__":
    main()
