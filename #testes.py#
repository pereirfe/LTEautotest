import visa

disp_w_ip = "TCPIP0::172.17.70.226::inst0::INSTR"

rm = visa.ResourceManager('@py')
cwm = rm.get_instrument(disp_w_ip)

command = []

# RB setting
command.append("CONF:LTE:SIGN:CONN:PCC:UDTT:UL1:ALL 50,48,45,39,33,27,21,15,9,3,0,0,3,6,9,12,15,18,21,24,QPSK,QPSK,Q16,Q16,Q64,Q64,Q64,Q64,Q64,Q64,26,26,26,26,26,26,26,26,26,26")

# PUSCH Open Loop Nominal Power
command.append("CONF:LTE:SIGN:UL:OLNPower -10")

# UL Closed Loop
command.append("CONFigure:LTE:SIGN:UL:PUSCh:TPC:SET CLOop")

# Closed  Loop Target Power
command.append("CONF:LTE:SIGN:UL:PUSCH:TPC:CLTPower 50")

for x in command:
    queryReturn = cwm.query(x)
    print "Command: %s" % x
    print "Return : %s" % queryReturn
    print ""

# Falta achar:
# TPC Setup: closed Loop (uplink)
# Connected DRX
# UL Dynamic scheduling
# Uplink power control / Open loop nominal power 
# Cell Bandwidth
# Reset/preset


# Operationg Band 
# RS EPRE
# PUSCH Open loop nominal Power
# PDCCH symbol configuration
# Attenuation  (?)
# PCC
# Scheduling : User def TTI
#

# Closed loop target power:
# CONFigure:LTE:SIGN<i>:UL:PUSCh:TPC:CLTPower
# CONFigure:LTE:SIGN:UL:PUSCh:TPC:SET CLOop
