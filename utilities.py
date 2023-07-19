#   Script:     utility.py
#   Version:    v0.1.1
#   Purpose:    Disable option 81 on wireless printers
#   Updated:    07.17.23
#   Author:     Zach.Weir
#   Email:      zach.weir@target.com

import os
import subprocess
import socket


def get_printer_model(printer_message, printer_ip):
    string_to_send = printer_message
    MESSAGE = string_to_send.encode('utf-8')

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((printer_ip, TCP_PORT))
        s.send(MESSAGE)
        data = s.recv(BUFFER_SIZE)
        data = str(data, 'utf-8').lower()
        s.close()
    except:
        pass


def ping_host(host):
    # get OS name
    operating_system = os.name

    if operating_system == "nt":
        print("Windows")
        ping = subprocess.call(['ping', '-n', '1', host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
    else:
        print("Mac")
        ping = subprocess.call(['ping', '-c', '1', host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
    return ping


def validate_printer_model(data):
    if "zq620" in data:
        printer_model = "ZQ620"
    elif "qln320" in data:
        printer_model = "QLN320"
    elif "zq620 plus" in data:
        printer_model = "ZQ620 Plus"
    elif "zq630" in data:
        printer_model = "ZQ630"
    elif "zd621" in data:
        printer_model = "ZD621"
    elif "zt410" in data:
        printer_model = "ZT410"
    elif "zt411" in data:
        printer_model = "ZT411"
    else:
        printer_model = "UNKNOWN"
    return printer_model


SERVER_PORT = 9100
BUFFER_SIZE = 1024
TCP_PORT = SERVER_PORT

# COMMANDS
disable_ethernet_switch = "! U1 setvar \"internal_wired.auto_switchover\" \"off\"\r\n"
disable_opt81 = "! U1 setvar \"ip.dhcp.option81\" \"off\"\r\n"
reset = "! U1 setvar \"device.reset\" \"now\"\r\n"