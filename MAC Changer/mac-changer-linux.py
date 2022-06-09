#!/usr/bin/python3
import re
import subprocess
import optparse

def search_mac_address(string):
    return re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', str(string)).group(0)

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac_address", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac_address:
        parser.error("[-] Please specify a new mac address, use --help for more info.")
    return options

def set_new_mac_address(interface, new_mac_address):
    print("[+] Changing MAC address for " + interface + " to " + new_mac_address)
    subprocess.call("ifconfig " + interface + " down", shell=True)
    subprocess.call("ifconfig " + interface + " hw ether " + new_mac_address, shell=True)
    subprocess.call("ifconfig " + interface + " up", shell=True)

def get_mac_address_from_interface(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = search_mac_address(ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result
    else:
        print("[-] Could not read MAC address.")

options = get_arguments()
current_mac_address = get_mac_address_from_interface(options.interface)
print("Current MAC address for interface " + options.interface + " is : " + current_mac_address)

set_new_mac_address(options.interface, options.new_mac_address)

new_mac_address = get_mac_address_from_interface(options.interface)
if new_mac_address == options.new_mac_address:
    print("[+] MAC address was successfully changed to " + new_mac_address + ".")
else:
    print("[-] MAC address did not get changed.")