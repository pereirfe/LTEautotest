#!/usr/bin/python
#+---------------------------------------------------------------------------------------------------------------------+
#| setCMW500.py: This file pretends to call a XML file passing as parameter and run                                    |
#|               all the SCPI commands inside the file on the CMW500.                                                  |
#|                                                                                                                     |
#| Author: Bruno Villas Boas                                                                                           |
#| Usage: setCMW500.py -i <xml_file> [-o <equipment_name>]                                                             |
#|   example: python setCMW500.py -i configurationFiles\eBSP_GSM_GPRS_v1.xml -o TCPIP0::CMW50050-144593::inst0::INSTR  |
#+---------------------------------------------------------------------------------------------------------------------+
from xml.dom.minidom import parse
import sys, getopt, visa, time, xml.dom.minidom
sys.path.insert(0, '/supportFiles')
from prettytable import PrettyTable

def main(argv):
    version = 0.1
    #####################################################################
    ### Get argument file ###############################################
    #####################################################################
    try:
        myopts, args = getopt.getopt(argv,"i:")
    except getopt.GetoptError as e:
        print (str(e))
        print("Usage: %s -i input_file [-e equipment_name]" % sys.argv[0])
        sys.exit(2)

    for o, a in myopts:
        if o == '-i':
            ifile=a
        elif o == '-e':
            equipment=a

    if 'ifile' not in locals():
        print("Usage: %s -i input_file [-e equipment_name]" % sys.argv[0])
        sys.exit(2)

    # Header
    print "\n"
    printList = PrettyTable(["CMW500 configuration"])
    printList.padding_width = 1 # One space between column edges and contents (default)
	
    printList.add_row(["Version %2f" % version])
    #####################################################################
    ### Import XML File #################################################
    #####################################################################

    # Load argument xml file
    printList.add_row(["Loading %s" % ifile])
    DOMTree = xml.dom.minidom.parse(ifile)
    commands = DOMTree.documentElement
    if commands.hasAttribute("network"):
        printList.add_row(["Network used : %s" % commands.getAttribute("network")])
    else:
        print printList
        print "The configuration file doesn't have the 'network' configuration attribute."
        sys.exit(2)

    #####################################################################
    ### Instrument Handle ###############################################
    #####################################################################
    # instrument connection
    rm = visa.ResourceManager()
    if 'equipment' not in locals():
        equipment = "TCPIP0::CMW50050-144593::inst0::INSTR"

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
    print "-----------      Configuring Network       -----------"
    print "------------------------------------------------------"
    try:
        for command in commands.getElementsByTagName('command'):
            print "\t-> %s" % (command.firstChild.data)
            cmw.write(command.firstChild.data)
            queryReturn = cmw.query('SYST:ERR:ALL?')
            if "No error" not in queryReturn:
                errorList.append(queryReturn)
            print "\t<- %s" % queryReturn
    except:
        print("Cannot send the command <%s> to the equipment" % command.firstChild.data)
        cmw.close()
        sys.exit(2)
    cmw.close()


    print "------------------------------------------------------\n"
    if len(errorList) != 0:
        print "The parameters configured return the following error(s):"
        for err in errorList:
            print "Error:\t%s" % err


    #####################################################################
    ### Wait until device connect to NW #################################
    #####################################################################

if __name__ == "__main__":
   main(sys.argv[1:])