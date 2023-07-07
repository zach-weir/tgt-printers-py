#   Script:     wireless_disable-opt81.py
#   Version:    v0.1
#   Purpose:    Disable option 81 on wireless printers
#   Updated:    07.02.23
#   Author:     Zach.Weir
#   Email:      zach.weir@target.com

import os
import socket

# INITIAL CONFIG
PRINTER_PORT = 9100 # was serverPort // server port can also be 6101
BUFFER_SIZE = 1024
TCP_PORT = PRINTER_PORT
hostname = f"t{store}rtr_v29.target.com" # was ipAndHost
host_list = list(map(str, hostname.split())) # was ipAndHostList
print(host_list)
report_line = f"T{store}" # was reportLine
printer_host = store + "prt0" # storeNameAndPRT0