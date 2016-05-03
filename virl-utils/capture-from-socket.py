__author__ = 'Sebastian Rieger'

import os;

ncat_path = "C:\\Users\\Sebastian\\Downloads\\ncat"
wireshark_path = "\"C:\\Program Files\\Wireshark\\Wireshark.exe\""
virl_host = "192.168.0.150"
pcap_port = input("Please enter the port of the live capture: ")

os.system(ncat_path + " " + virl_host + " " + str(pcap_port) + " | " + wireshark_path + " -k -i -")
