import visa
import sys
from testingtools import *
import time

cmwByIP = "TCPIP0::172.17.70.226::inst0::INSTR"
oscByIP = "TCPIP0::172.17.60.162::inst0::INSTR"

rm = visa.ResourceManager('@py')

cmw = rm.get_instrument(cmwByIP)
osc = rm.get_instrument(oscByIP)

cmw_testlist = [[],[]]
osc_commandlist = []

i = 0
while i < 6:
    try:
        print("  Trying to reach the OSC - #%i" % i)
        osc.timeout = 500
        queryReturn = osc.query('SYSTem:ERRor?')
        print "Query return: %s" % queryReturn
        break
    except:
        print("\tCannot reach the equipment")
        i+=1
        if i > 5:
            print("\n\tCheck the communication")
            sys.exit(2)

print "\n\t -- OSC OK!"

#Set tests
#addNewTest(cmw_testlist, "CONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26\nCONF:LTE:SIGN:UL:PUSCH:TPC:CLTPower 23\nCONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26", "alternated_prb" ,"distance_prb","1" )

#mountTestBattery(cmw_testlist, "CONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26\nCONF:LTE:SIGN:UL:PMAX ","\nCONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 00,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,00,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26", -20, 20, 5, "alternate_PMAX" ,"dbm")

#T1
#mountTestBattery(cmw_testlist, "CONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26\nCONF:LTE:SIGN:UL:PMAX -30\nCONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 00,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,00,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26\nCONF:LTE:SIGN:CONN:PCC:UDTT:UL:ALL 0,0,0,",",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,0,0,0,0,0,0,0,0,0,0", 26, 100, 5, "T1_alter_tti4_PRBnum" ,"_with_MCS0_QPSK_pmax_-30")

#T7
mountTestBattery(cmw_testlist, "SENSe:LTE:SIGN:RRCState?\nCONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26\nCONF:LTE:SIGN:UL:PMAX ","\nCONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 00,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,00,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26\nCONF:LTE:SIGN:CONN:PCC:UDTT:UL:ALL 0,0,0,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,0,0,0,0,0,0,0,0,0,0", -30, 0, 5, "T7I_BAND28_Bandwidth_20_alter_ptrans_","_with_MCS0_QPSK_100prb_tti4")


#T2


mountTestBattery(cmw_testlist, "SENSe:LTE:SIGN:RRCState?\nCONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26\nCONF:LTE:SIGN:UL:PMAX -30\nCONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 00,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,00,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26\nCONF:LTE:SIGN:CONN:PCC:UDTT:UL:ALL 0,0,",",100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,0,0,0,0,0,0,0,0,0,0", 0, 101, 5, "T2A_BAND7_Bandwidth_20_alter_prb_tti3_","_with_MCS0_QPSK_100prb_tti4_ptransmit_-30")

mountTestBattery(cmw_testlist, "SENSe:LTE:SIGN:RRCState?\nCONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26\nCONF:LTE:SIGN:UL:PMAX -30\nCONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 00,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,00,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26\nCONF:LTE:SIGN:CONN:PCC:UDTT:UL:ALL 0,0,",",100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,QPSK,0,0,0,0,0,0,0,0,0,0", 0, 101, 5, "T2B_BAND7_Bandwidth_20_alter_prb_tti3_","_with_MCS0_QPSK_100prb_tti4_ptransmit_23")



#addNewTest(cmw_testlist, "CONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,00,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26\nCONF:LTE:SIGN:UL:PMAX 23\nCONF:LTE:SIGN:CONN:PCC:UDTT:DL:ALL 00,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,00,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26", "alternated_prb" ,"distance_prb","1" )

# addNewTest(cmw_testlist, "CONF:LTE:SIGN:CONN:PC:UDTT:UL1:ALL 50,0,50,0,50,0,50,0,50,0,0,0,0,0,0,0,0,0,0,00,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26\nCONF:LTE:SIGN:UL:PMAX 20", "alternated_prb" ,"distance_prb","1" )

# addNewTest(cmw_testlist, "CONF:LTE:SIGN:CONN:PCC:UDTT:UL1:ALL 50,0,0,50,0,0,50,0,0,50,0,0,0,0,0,0,0,0,0,0,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26", "alternated_prb","distance_prb","2" )
#End_of_testsetting
#Main Loop
#print cmw_testlist

for i in range(len(cmw_testlist[0])):
    setTest(cmw, cmw_testlist[0][i])
    runTest(osc, cmw_testlist[1][i])
