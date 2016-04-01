#!/usr/bin/python
#+-----------------------------------------------------------------------------------------------------------------------+
#| setN6075B.py: This file pretends to call a XML file passing as parameter and run                                      |
#|               all the SCPI commands inside the file on the N6075B.                                                    |
#|                                                                                                                       |
#| Author: Bruno Villas Boas                                                                                             |
#| Usage: setN6075B.py -i <xml_file> [-o <equipment_name>]                                                               |
#| example: python setN6075B.py -i xmlCommands\psuFiles\eBSP_PSU_On_Default.xml -o TCPIP0::A-N6705B-01480::inst0::INSTR  |
#+-----------------------------------------------------------------------------------------------------------------------+
from xml.dom.minidom import parse
import sys, getopt, visa, time, xml.dom.minidom
sys.path.insert(0, '/supportFiles')
from prettytable import PrettyTable

def main(argv):
    version = 0.1
    # instrument connection
    rm = visa.ResourceManager('@py')
    equipment = "TCPIP0::172.17.60.237::inst0::INSTR"
    osc = rm.get_instrument(equipment)

    # connect to the equipment
    i = 1
    while i < 6:
        try:
            print("  Trying to reach the equipment - #%i" % i)
            # set CMW500 timeout to 5 seconds
            osc.timeout = 5000
            queryReturn = osc.query('SYSTem:ERRor?')
            print "Query return: %s" % queryReturn
            break
        except:
            print("\tCannot reach the equipment %s" % equipment)
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

    #INIT:ELOG (@1,2)    
    osc_commandlist = []
    osc_commandlist.append("MMEM:EXP:DLOG \"external:\\data1.csv\"")
    osc_commandlist.append("SENSe:DLOG:TIME 10")
    osc_commandlist.append("INIT:DLOG (@1)")

    for x in osc_commandlist:
        queryReturn = osc.query(x)
        print "Command: %s" % x
        print "Return : %s" % queryReturn
        print ""

    print "end"

if __name__ == "__main__":
   main(sys.argv[1:])


def mountFilename(testname,param,value,extension):
    """ Mount the filename testname_parameter_value.extension """
    return (testname+"_"+param+"_"+value+"_"+extension)
