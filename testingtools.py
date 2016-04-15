import time

def mountFilename(testname,param,value,extension):
    return '{tn}_{v}_{p}.{e}'.format(tn=testname, p=param, v=value, e=extension)

def runTest(osc,filename):
    print "\n\t -- Running test for %s" % filename
    osc_commandlist = []
    #_ = "MMEM:EXP:DLOG \"external:\\" + filename + "\""
    _ = "INIT:DLOG \"external:\\" + filename + "\""
    osc_commandlist.append("SENS:DLOG:TIME 10")
    osc_commandlist.append(_)
    osc_commandlist.append("SENS:DLOG:TIME?")
    for x in osc_commandlist:
        queryReturn = osc.query(x)
        qr2 = osc.query("*OPC?")
        print "Waiting",
        while "1" not in qr2:
            time.sleep(1)
            print qr2
            qr2 = osc.query("*OPC?")
        qerr = osc.query('SYSTem:ERRor?')
        print "Error:", qerr
        print ""
        print "Command: %s" % x
        print "Return : %s" % queryReturn
        print ""
    print "\t\tDone!"


def addNewTest(cmw_testlist, test, testname, param, value):
    filename = mountFilename(testname, param, value, "dlog") #"csv")
    cmw_testlist[0].append(test)
    cmw_testlist[1].append(filename)

def setTest(cmw, test):
    print "Setting test %s" % test
    qrret = cmw.query(test)
    print "Return : %s" % qrret


def mountTestBattery(cmw_testlist, prefix, posfix, vi, vf, step, testname, param):
    for _ in range(vi,vf,step):
        test  = prefix + str(_) + posfix
        addNewTest(cmw_testlist, test, testname, param, _)
