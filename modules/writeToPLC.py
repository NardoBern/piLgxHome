#### Modulo per l'interfacciamento in scrittura verso il PLC ####

def updateTime(PlcConnection,ora,minuti,secondi):
    PlcConnection.Write("i_stData.diSec",secondi)
    PlcConnection.Write("i_stData.diMin",minuti)
    PlcConnection.Write("i_stData.diOra",ora)

def updateWatchDog(PlcConnection, watchdog):
    PlcConnection.Write("i_stHmiSystemVar.iWatchDog",watchdog)

def writeAutoHeatDataToPLC(PlcConnection,zonaBagno,zonaGiorno,zonaNotte):
    i = 0
    for data in zonaBagno:
        variableName = "i_stZonaBManCmd.axAutoSet[" + str(i) + "]"
        PlcConnection.Write(variableName,data)
        i = i + 1
    i = 0
    for data in zonaGiorno:
        variableName = "i_stZonaCManCmd.axAutoSet[" + str(i) + "]"
        PlcConnection.Write(variableName,data)
        i = i + 1
    i = 0
    for data in zonaNotte:
        variableName = "i_stZonaAManCmd.axAutoSet[" + str(i) + "]"
        PlcConnection.Write(variableName,data)
        i = i + 1

def writeAutoManToPLC(PlcConnection,zonaBagno,zonaGiorno,zonaNotte):
    if zonaBagno:
        modalBagno = 1
    else:
        modalBagno = 0
    if zonaGiorno:
        modalGiorno = 1
    else:
        modalGiorno = 0
    if zonaNotte:
        modalNotte = 1
    else:
        modalNotte = 0
    PlcConnection.Write("i_stZonaBManCmd.iMode",modalBagno)
    print "Modalita giorno: " + str(modalGiorno)
    PlcConnection.Write("i_stZonaCManCmd.iMode",modalGiorno)
    PlcConnection.Write("i_stZonaAManCmd.iMode",modalNotte)

def writeManHeatCmdToPLC(PlcConnection,zonaBagno,zonaGiorno,zonaNotte):
    PlcConnection.Write("i_stZonaAManCmd.xManCmd",zonaNotte)
    PlcConnection.Write("i_stZonaBManCmd.xManCmd",zonaBagno)
    PlcConnection.Write("i_stZonaCManCmd.xManCmd",zonaGiorno)

def writeManHeatTimerToPLC(PlcConnection,zonaBagno,zonaGiorno,zonaNotte):
    PlcConnection.Write("i_stZonaAManCmd.iManTime",zonaNotte)
    PlcConnection.Write("i_stZonaBManCmd.iManTime",zonaBagno)
    PlcConnection.Write("i_stZonaCManCmd.iManTime",zonaGiorno)

def writeLampManCmdToPLC(PlcConnection,tag,value):
    PlcConnection.Write(tag,value)

def writeLampModalToPLC(PlcConnection,tag,value):
    if value == 1:
        PlcConnection.Write(tag,2)
    elif value == 0:
        PlcConnection.Write(tag,0)
    else:
        PlcConnection.Write(tag,1)

def writeLampTimeOutToPLC(PlcConnection,timeOut):
    print 'Chiamata alla funzione di scrittura timeOut luci in automatico...'
    PlcConnection.Write("i_stLuceAntiBagnoHmiCmds.diAutoTime",timeOut[2])
    PlcConnection.Write("i_stLuceBagnoHmiCmds.diAutoTime",timeOut[8])
    PlcConnection.Write("i_stLuceCorridoioHmiCmds.diAutoTime",timeOut[5])
    PlcConnection.Write("i_stLuceCucinaHmiCmds.diAutoTime",timeOut[1])
    PlcConnection.Write("i_stLuceFuoriDavantiHmiCmds.diAutoTime",timeOut[9])
    PlcConnection.Write("i_stLuceIngressoHmiCmds.diAutoTime",timeOut[7])
    PlcConnection.Write("i_stLuceCameraLettoHmiCmds.diAutoTime",timeOut[4])
    PlcConnection.Write("i_stLuceSalaHmiCmds.diAutoTime",timeOut[6])
    PlcConnection.Write("i_stLuceSalaLibreriaHmiCmds.diAutoTime",timeOut[3])
    PlcConnection.Write("i_stLuceVerandaHmiCmds.iModeSel",timeOut[0])

def writeGateCommands(PlcConnection,gateBig,gateSmall):
    print 'Chiamata alla funzione di scrittura comandi cancello grande e piccolo'
    PlcConnection.Write("i_xHMICancGrande",gateBig)
