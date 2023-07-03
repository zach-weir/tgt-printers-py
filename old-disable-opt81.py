#!/opt/homebrew/bin/python3
import sys
import telnetlib
import socket

# Enter the printer IP address space then the hostname item to get
#print ("device.unique_id")
#print ("device.product_name")
#print ("odometer.total_print_length")

#can also try port 6101
serverPort = 9100
BUFFER_SIZE = 1024
TCP_PORT = serverPort

#ipAndHost = input("Enter the store number: ")
ipAndHost = sys.argv[1] + "rtr_v29.target.com" 
ipAndHostList = list(map(str, ipAndHost.split()))
print(ipAndHostList)

reportLine = sys.argv[1]
storeNameAndPRT0 = sys.argv[1] + "prt0"
#print (reportLine)

try:
	addr = socket.gethostbyname(ipAndHostList[0])
	print (addr)
	
	baseAddrList = addr.split('.')
	baseAddr3Octet = baseAddrList[0] + "." + baseAddrList[1] + "." + baseAddrList[2]

	countInDNS = 0
	countQuoteFound = 0
	countQuote0QuoteFound = 0
	strToDisplay = sys.argv[1]
	
	
	
	for x in range(129, 255):
		strToDisplay = sys.argv[1]
		xAddress = baseAddr3Octet + "." + str(x)
		#print (xAddress)
		shouldTryQueryZebra = False
		try:
			name = socket.gethostbyaddr (xAddress)
			#print (name)
			#filter on prt05 or j unconfigured Zebra printers only
			if str(name).lower().find("prt") > 0:
				#print (name)
				strToDisplay += ", " + str(name)
				shouldTryQueryZebra = True
				countInDNS += 1
			if str(name).lower().find("j") > 0:
				#print (name)
				strToDisplay += ", " + str(name)
				shouldTryQueryZebra = True
				countInDNS += 1
				
			if (shouldTryQueryZebra):
				#print ("Trying")
				TCP_IP = xAddress
				
				# Configure this string to the printer
				stringToRetrieve = "! U1 getvar \"device.unique_id\"\r\n"
				MESSAGE = stringToRetrieve.encode('utf-8')
				#print (stringToRetrieve)
				
				try:
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.connect((TCP_IP, TCP_PORT))
					s.send(MESSAGE)
					data = s.recv(BUFFER_SIZE)
					s.close()
				
					#print ("received data: " + str(data, 'utf-8'))
					strToDisplay += ", serial: " + str(data, 'utf-8')
				except:
					pass
				
				strQuote0Quote = "\"TA"
				#strQuote0Quote = "\"TAZKJ"
				#strQuote0Quote = "\"TAQLJ"
				strQuote = "\""
				if strToDisplay.find(strQuote) > 0:
					countQuoteFound += 1
					if strToDisplay.find(strQuote0Quote) > 0:
						countQuote0QuoteFound += 1

						#appl.name
						stringToRetrieve = "! U1 getvar \"appl.name\"\r\n"
						MESSAGE = stringToRetrieve.encode('utf-8')
						try:
							s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							s.connect((TCP_IP, TCP_PORT))
							s.send(MESSAGE)
							data = s.recv(BUFFER_SIZE)
							s.close()
							strToDisplay += ", appl.name: " + str(data, 'utf-8')
						except:
							pass

						#Get Firmwre
						stringToRetrieve = "! U1 getvar \"appl.version\"\r\n"
						MESSAGE = stringToRetrieve.encode('utf-8')
						try:
							s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							s.connect((TCP_IP, TCP_PORT))
							s.send(MESSAGE)
							data = s.recv(BUFFER_SIZE)
							s.close()
							strToDisplay += ", apl.version: " + str(data, 'utf-8')
						except:
							pass
						
						#print ("It either QLN320 or ZQ620.  Ask if it's in ZPL, then change it to ZPL*")
						stringToRetrieve = "! U1 getvar \"apl.enable\"\r\n"
						#stringToRetrieve = "! U1 setvar \"device.cpcl_synchronous_mode\" \"off\"\r\n! U1 setvar \"device.reset\" \"now\"\r\n"
						#stringToRetrieve = "! U1 setvar \"file.rename\" \"CONFIG.SYS CONFIG.TXT\"\r\n! U1 setvar \"media.type\" \"label\"\r\n! U1 setvar \"device.languages\" \"hybrid_xml_zpl\"\r\n! U1 setvar \"apl.enable\" \"none\"\r\n! U1 setvar \"device.reset\" \"now\"\r\n";

						MESSAGE = stringToRetrieve.encode('utf-8')
						
						try:
							s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							s.connect((TCP_IP, TCP_PORT))
							s.send(MESSAGE)
							data = s.recv(BUFFER_SIZE)
							s.close()
							strToDisplay += ", apl.enable: " + str(data, 'utf-8')
							#strQuote0Quote = "\"none"

							#if strToDisplay.find(strQuote0Quote) > 0: #print ("Printer is in ZPL or ZPL*.  Ask another question if in journal or label")
							stringToRetrieve = "! U1 getvar \"media.type\"\r\n"
							#stringToRetrieve = "! U1 setvar \"file.rename\" \"CONFIG.SYS CONFIG.TXT\"\r\n! U1 setvar \"media.type\" \"label\"\r\n! U1 setvar \"device.languages\" \"hybrid_xml_zpl\"\r\n! U1 setvar \"apl.enable\" \"none\"\r\n! U1 setvar \"device.reset\" \"now\"\r\n";
							#stringToRetrieve = "! U1 setvar \"file.rename\" \"CONFIG.SYS CONFIG.TXT\"\r\n! U1 setvar \"media.type\" \"label\"\r\n! U1 setvar \"device.languages\" \"hybrid_xml_zpl\"\r\n! U1 setvar \"apl.enable\" \"none\"\r\n! U1 setvar \"media.tof\" \"36\"\r\n! U1 setvar \"media.feed_length\" \"2030\"\r\n! U1 setvar \"media.sense_mode\" \"bar\"\r\n! U1 setvar \"zpl.data_timeout_in_seconds\" \"30\"\r\n! U1 setvar \"label.x_move\" \"0\"\r\n! U1 setvar \"label.y_move\" \"0\"\r\n! U1 setvar \"device.reset\" \"now\"\r\n";

							MESSAGE = stringToRetrieve.encode('utf-8')
						
							try:
								s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
								s.connect((TCP_IP, TCP_PORT))
								s.send(MESSAGE)
								data = s.recv(BUFFER_SIZE)
								s.close()
								strToDisplay += ", media.type: " + str(data, 'utf-8')
								
								strQuote0Quote = "\"none"
								if strToDisplay.find(strQuote0Quote) > 0:
									strQuote0Quote = "\"journal"
									if strToDisplay.find(strQuote0Quote) > 0:
										print ("Printer is in ZPL not ZPL*.  Tell it to be ZPL*")
										stringToRetrieve = "! U1 setvar \"file.rename\" \"CONFIG.SYS CONFIG.TXT\"\r\n! U1 setvar \"media.type\" \"label\"\r\n! U1 setvar \"device.languages\" \"hybrid_xml_zpl\"\r\n! U1 setvar \"apl.enable\" \"none\"\r\n! U1 setvar \"media.tof\" \"36\"\r\n! U1 setvar \"media.feed_length\" \"2030\"\r\n! U1 setvar \"media.sense_mode\" \"bar\"\r\n! U1 setvar \"zpl.data_timeout_in_seconds\" \"30\"\r\n! U1 setvar \"label.x_move\" \"0\"\r\n! U1 setvar \"label.y_move\" \"0\"\r\n! U1 setvar \"device.reset\" \"now\"\r\n";
										
										MESSAGE = stringToRetrieve.encode('utf-8')
						
										try:
											s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
											s.connect((TCP_IP, TCP_PORT))
											s.send(MESSAGE)
											#data = s.recv(BUFFER_SIZE)
											s.close()
										except:
											pass
								
								strQuote0Quote = "\"pdf"
								if strToDisplay.find(strQuote0Quote) > 0:
									strQuote0Quote = "\"label"
									if strToDisplay.find(strQuote0Quote) > 0:
										print ("Printer is in PDF* not ZPL*.  Tell it to be ZPL*")
										stringToRetrieve = "! U1 setvar \"file.rename\" \"CONFIG.SYS CONFIG.TXT\"\r\n! U1 setvar \"media.type\" \"label\"\r\n! U1 setvar \"device.languages\" \"hybrid_xml_zpl\"\r\n! U1 setvar \"apl.enable\" \"none\"\r\n! U1 setvar \"media.tof\" \"36\"\r\n! U1 setvar \"media.feed_length\" \"2030\"\r\n! U1 setvar \"media.sense_mode\" \"bar\"\r\n! U1 setvar \"zpl.data_timeout_in_seconds\" \"30\"\r\n! U1 setvar \"label.x_move\" \"0\"\r\n! U1 setvar \"label.y_move\" \"0\"\r\n! U1 setvar \"device.reset\" \"now\"\r\n";
										
										MESSAGE = stringToRetrieve.encode('utf-8')
						
										try:
											s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
											s.connect((TCP_IP, TCP_PORT))
											s.send(MESSAGE)
											#data = s.recv(BUFFER_SIZE)
											s.close()
										except:
											pass
											
								strQuote0Quote = "\"apl-o"
								if strToDisplay.find(strQuote0Quote) > 0:
									strQuote0Quote = "\"label"
									if strToDisplay.find(strQuote0Quote) > 0:
										print ("Printer is in EZPRINT not ZPL*.  Tell it to be ZPL*")
										stringToRetrieve = "! U1 setvar \"file.rename\" \"CONFIG.SYS CONFIG.TXT\"\r\n! U1 setvar \"media.type\" \"label\"\r\n! U1 setvar \"device.languages\" \"hybrid_xml_zpl\"\r\n! U1 setvar \"apl.enable\" \"none\"\r\n! U1 setvar \"media.tof\" \"36\"\r\n! U1 setvar \"media.feed_length\" \"2030\"\r\n! U1 setvar \"media.sense_mode\" \"bar\"\r\n! U1 setvar \"zpl.data_timeout_in_seconds\" \"30\"\r\n! U1 setvar \"label.x_move\" \"0\"\r\n! U1 setvar \"label.y_move\" \"0\"\r\n! U1 setvar \"device.reset\" \"now\"\r\n";
										
										MESSAGE = stringToRetrieve.encode('utf-8')
						
										try:
											s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
											s.connect((TCP_IP, TCP_PORT))
											s.send(MESSAGE)
											#data = s.recv(BUFFER_SIZE)
											s.close()
										except:
											pass
							except:
								pass	
						except:
							pass
							
						#Get Cradle Override status
						stringToRetrieve = "! U1 getvar \"internal_wired.auto_switchover\"\r\n"
						MESSAGE = stringToRetrieve.encode('utf-8')
						
						try:
							s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							s.connect((TCP_IP, TCP_PORT))
							s.send(MESSAGE)
							data = s.recv(BUFFER_SIZE)
							s.close()
							strToDisplay += ", internal_wired.auto_switchover: " + str(data, 'utf-8')
							strQuote0Quote = "\"on"

							if strToDisplay.find(strQuote0Quote) > 0: 
								print ("Cradle ethernet override ON.  Sending the OFF switch.")
								stringToRetrieve = "! U1 setvar \"internal_wired.auto_switchover\" \"off\"\r\n! U1 setvar \"device.reset\" \"now\"\r\n"
						
								MESSAGE = stringToRetrieve.encode('utf-8')
						
								try:
									s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
									s.connect((TCP_IP, TCP_PORT))
									s.send(MESSAGE)
									#data = s.recv(BUFFER_SIZE)
									s.close()
								except:
									pass
						except:
							pass

						#ip.dhcp.option81
						stringToRetrieve = "! U1 getvar \"ip.dhcp.option81\"\r\n"
						MESSAGE = stringToRetrieve.encode('utf-8')
						
						try:
							s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							s.connect((TCP_IP, TCP_PORT))
							s.send(MESSAGE)
							data = s.recv(BUFFER_SIZE)
							s.close()
							strToDisplay += ", ip.dhcp.option81: " + str(data, 'utf-8')
							strQuote0Quote = "\"on"

							if strToDisplay.find(strQuote0Quote) > 0: 
								print ("ip.dhcp.option81 ON.  Sending the OFF switch, but not yet")
								stringToRetrieve = "! U1 setvar \"ip.dhcp.option81\" \"off\"\r\n! U1 setvar \"device.reset\" \"now\"\r\n"
								print (stringToRetrieve)

								MESSAGE = stringToRetrieve.encode('utf-8')
						
								# try:
								# 	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
								# 	s.connect((TCP_IP, TCP_PORT))
								# 	s.send(MESSAGE)
								# 	#data = s.recv(BUFFER_SIZE)
								# 	s.close()
								# except:
								# 	pass
						except:
							pass

						#Get TOF Override status
						stringToRetrieve = "! U1 getvar \"media.tof\"\r\n"
						MESSAGE = stringToRetrieve.encode('utf-8')
						
						try:
							s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							s.connect((TCP_IP, TCP_PORT))
							s.send(MESSAGE)
							data = s.recv(BUFFER_SIZE)
							s.close()
							strToDisplay += ", media.tof: " + str(data, 'utf-8')
							#strQuote0Quote = "\""
							#act on it later here

						except:
							pass
						
						#Get WLAN MAC
						stringToRetrieve = "! U1 getvar \"wlan.mac_addr\"\r\n"
						MESSAGE = stringToRetrieve.encode('utf-8')
						
						try:
							s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							s.connect((TCP_IP, TCP_PORT))
							s.send(MESSAGE)
							data = s.recv(BUFFER_SIZE)
							s.close()
							strToDisplay += ", wlan.mac_addr: " + str(data, 'utf-8')
							#strQuote0Quote = "\""
							#act on it later here

						except:
							pass
						
						#Get more stuff here
						
						#Get ezpl.print_width
						stringToRetrieve = "! U1 getvar \"media.width_sense.enable\"\r\n"
						MESSAGE = stringToRetrieve.encode('utf-8')
						
						try:
							s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							s.connect((TCP_IP, TCP_PORT))
							s.send(MESSAGE)
							data = s.recv(BUFFER_SIZE)
							s.close()
							strToDisplay += ", media.width_sense.enable: " + str(data, 'utf-8')
							#strQuote0Quote = "\""
							#act on it later here

						except:
							pass

						printWidth = 0
						#Get ezpl.print_width
						stringToRetrieve = "! U1 getvar \"ezpl.print_width\"\r\n"
						MESSAGE = stringToRetrieve.encode('utf-8')
						
						try:
							s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							s.connect((TCP_IP, TCP_PORT))
							s.send(MESSAGE)
							data = s.recv(BUFFER_SIZE)
							printWidth = int(str(data, 'utf-8').strip("\""))
							s.close()
							strToDisplay += ", ezpl.print_width: " + str(data, 'utf-8')
							#strQuote0Quote = "\""
							#act on it later here

						except:
							pass

						#device.friendly_name
						stringToRetrieve = "! U1 getvar \"device.friendly_name\"\r\n"
						MESSAGE = stringToRetrieve.encode('utf-8')
						
						try:
							s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							s.connect((TCP_IP, TCP_PORT))
							s.send(MESSAGE)
							data = s.recv(BUFFER_SIZE)
							hostLength = len(str(data, 'utf-8'))
							s.close()
							strToDisplay += ", device.friendly_name: " + str(data, 'utf-8')
							#strQuote0Quote = "\""
							#act on it later here

						except:
							pass

				#strToDisplay += ", " + sys.argv[1]
				#Check if TXXXXPRT0 is in the hostname
				if strToDisplay.upper().find(storeNameAndPRT0.upper()) > 0:
					strToDisplay += ", hostname_" + storeNameAndPRT0
				else:
					strToDisplay += ", check_hostname"


				if str(strToDisplay).lower().find("taqlj") > 0:
					strToDisplay += ",Is_QLN320_TAQLJ"
				elif str(strToDisplay).lower().find("taqlc") > 0:
					strToDisplay += ",Is_QLN320_TAQLC"
				elif str(strToDisplay).lower().find("tazkj") > 0:
					strToDisplay += ",Is_ZQ620_TAZKJ"
				elif str(strToDisplay).lower().find("tazkc") > 0:
					strToDisplay += ",Is_ZQ620_TAZKC"
				elif str(strToDisplay).lower().find("tazkn") > 0:
					strToDisplay += ",Is_ZQ620_TAZKN"
				elif str(strToDisplay).lower().find("xxzln") > 0:
					strToDisplay += ",Is_ZQ620_XXZLN"
				else:
					if str(strToDisplay).lower().find("prt01") > 0:
						strToDisplay += ",Is_QLN320"
					if str(strToDisplay).lower().find("prt02") > 0:
						strToDisplay += ",Is_ZQ620"

				print (strToDisplay)
			#To get all VLAN11 uncomment below
			#print (strToDisplay)
		except:
			pass
			
	#print (countQuoteFound)
	#print (countQuote0QuoteFound)
	reportLine += ", InDNS, " + str(countInDNS) + ", Responses, " + str(countQuoteFound)
	if (countQuote0QuoteFound != 0):
		reportLine += ", HIP_network"
	print (reportLine)
except:
	pass
	





#