#   Script:     utility.py
#   Version:    v0.1
#   Purpose:    Disable option 81 on wireless printers
#   Updated:    07.02.23
#   Author:     Zach.Weir
#   Email:      zach.weir@target.com

import os
import subprocess

def ping_host(host):
    # get OS name
    operating_system = os.name

    if operating_system == "nt":
        ping = subprocess.call(['ping', '-n', '1', host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        ping = subprocess.call(['ping', '-c', '1', host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
