#### Modulo per l'interfacciamento in lettura dal PLC ####

## Funzione di lettura delle modalita ##
def readHeatModalState(PlcConnection):
    modalState = [0,0,0]
    modalState[0] = PlcConnection.Read("o_stHMIZonaBRisc.iMode")
    modalState[1] = PlcConnection.Read("o_stHMIZonaARisc.iMode")
    modalState[2] = PlcConnection.Read("o_stHMIZonaCRisc.iMode")
    print "La modalita riscaldamento sono: " + str(modalState)
    return modalState

## Funzione di lettura degli stati ##
def readHeatState(PlcConnection):
    state = [0,0,0]
    state[0] = PlcConnection.Read("o_stHMIZonaBRisc.iState")
    state[1] = PlcConnection.Read("o_stHMIZonaARisc.iState")
    state[2] = PlcConnection.Read("o_stHMIZonaCRisc.iState")
    print "Gli stati riscaldamento sono: " + str(state)
    return state
