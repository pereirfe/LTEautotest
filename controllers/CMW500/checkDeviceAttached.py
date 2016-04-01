#!/usr/bin/python
#+--------------------------------------------------------------------------------------------------+
#| checkDeviceAttached.py: This file pretends to wait until the device attach to                    |
#|                          the network provided by the CMW500.                                     |
#|                                                                                                  |
#| Author: Bruno Villas Boas                                                                        |
#| Usage: checkDeviceAttached.py [-n GSM|WCDMA|LTE] [-t search_duration (s)] [-o <equipment_name>]  |
#|   example: python checkDeviceAttached.py -n LTE -o TCPIP0::CMW50050-144593::inst0::INSTR         |
#+--------------------------------------------------------------------------------------------------+
from xml.dom.minidom import parse
import sys, getopt, visa, time, xml.dom.minidom
sys.path.insert(0, '/supportFiles')
from prettytable import PrettyTable

def main(argv):
    version=0.1
	#####################################################################
    ### Get argument file ###############################################
    #####################################################################
    try:
        opts, args = getopt.getopt(argv,"n:e:t:h")
    except getopt.GetoptError as e:
        print (str(e))
        print("Usage: checkDeviceAttached.py [-n GSM|WCDMA|LTE] [-t search_duration (s)] [-o <equipment_name>]")
        sys.exit(2)

    for o, a in opts:
        if o == '-n':
            network=a
        elif o == '-t':
            search_duration=a
        elif o == '-e':
            equipment=a
        elif o == '-h':
            print("Usage: checkDeviceAttached.py [-n GSM|WCDMA|LTE] [-t search_duration (s)] [-o <equipment_name>]")
            sys.exit(2)

    if 'network' not in locals():
        print("The check will be performed for all networks")
        network = "ALL"
    else:
        if network != "GSM" and network != "WCDMA" and network != "LTE":
            print("Usage: checkDeviceAttached.py [-n GSM|WCDMA|LTE] [-t search_duration (s)] [-o <equipment_name>]")
            sys.exit(2)

    if 'search_duration' not in locals():
        search_duration = 60
    else:
        try:
            search_duration = int(search_duration)
        except:
            print("Usage: checkDeviceAttached.py [-n GSM|WCDMA|LTE] [-t search_duration (s)] [-o <equipment_name>]")
            sys.exit(2)

    # Header
    print "\n"
    printList = PrettyTable([" Check Device Attached"])
    printList.padding_width = 1 # One space between column edges and contents (default)
    printList.add_row(["Version %2f" % version])
    printList.add_row(["Network used: %s" % network])
    printList.add_row(["Search duration: %s" % search_duration])

    #####################################################################
    ### Instrument Handle ###############################################
    #####################################################################
    # instrument connection
    rm = visa.ResourceManager('@py')
    if 'equipment' not in locals():
        equipment = "TCPIP0::CMW50050-144593::inst0::INSTR"
        equipment = "TCPIP0::172.17.70.226::inst0::INSTR"

    printList.add_row(["Equipment used: %s" % equipment])
    print printList

    # connect to the equipment
    i = 1
    while i < 6:
        try:
            print("  Trying to reach the equipment - #%i" % i)
            cmw = rm.open_resource(equipment)
            # set CMW500 timeout to 5 seconds
            cmw.timeout = 5000
            queryReturn = cmw.query('SYST:ERR:ALL?')
            break
        except:
            #print("\tCannot reach the equipment %s" % equipment)
            i+=1
            if i > 5:
                print("\n\t------- Check the communication with your equipment -------")
                sys.exit(2)

    print "\t* Connected to the equipment --- OK\n"

    errorList = [] # Declares an empty list for errors
    print "\t* Equipment Buffer Clean --- OK\n"
    print "------------------------------------------------------"
    print "--------      Check Network Connection       ---------"
    print "------------------------------------------------------"

    try:
        networkCommand = ['FETC:GSM:SIGN:CSW:STAT?','FETC:WCDM:SIGN:CSW:STAT?','FETC:LTE:SIGN:PSW:STAT?']
        startValue = time.time()
        endValue = 1
        while endValue < search_duration:
            if network == "GSM":
                queryReturn = cmw.query(networkCommand[0])
                print "\t-> %s" % networkCommand[0]
            elif network == "WCDMA":
                queryReturn = cmw.query(networkCommand[1])
                print "\t-> %s" % networkCommand[1]
            elif network == "LTE":
                queryReturn = cmw.query(networkCommand[2])
                print "\t-> %s" % networkCommand[2]
            if network != "ALL":
                print "\t<- %s" % queryReturn
            elif network == "ALL":
                for nw in networkCommand:
                    queryReturn = cmw.query(nw)
                    print "\t-> %s" % nw
                    print "\t<- %s" % queryReturn
                    if ("SYNC" in queryReturn or "REG" in queryReturn or "ATT" in queryReturn):
                        break
                    if "ON" in queryReturn:
                        if "GSM" in nw:
                            network = "GSM"
                        elif "WCDM" in nw:
                            network = "WCDMA"
                        elif "LTE" in nw:
                            network = "LTE"
                        print("\t *** Network search changed to %s" % network)
            if ("SYNC" in queryReturn or "REG" in queryReturn or "ATT" in queryReturn):
                print("\t<- Device registered on network")
                cmw.close()
                break
            endValue = time.time() - startValue
    except:
        print("Connection lost ...")
        cmw.close()
        sys.exit(2)
    if ("SYNC" not in queryReturn and "REG" not in queryReturn and "ATT" not in queryReturn):
        print("\t<- ERROR: Device not registered on network: %s" % network)
    print "------------------------------------------------------\n"

if __name__ == "__main__":
   main(sys.argv[1:])
