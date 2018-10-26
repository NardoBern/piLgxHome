#### Modulo per l'interfacciamento in scrittura verso il PLC ####

def updateTime(PlcConnection,ora,minuti,secondi):
    PlcConnection.Write("i_stData.diSec",secondi)
    PlcConnection.Write("i_stData.diMin",minuti)
    PlcConnection.Write("i_stData.diOra",ora)

