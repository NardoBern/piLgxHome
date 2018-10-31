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

## Funzione di lettura degli stati delle luci ##
def readLampState(PlcConnection):
    state = [0,0,0,0,0,0,0,0,0,0,0]
    state[0] = PlcConnection.Read("o_stLuceVerandaFdbk.xLampState")
    state[1] = PlcConnection.Read("o_stLuceCantinaFdbk.xLampState")
    state[2] = PlcConnection.Read("o_stLuceCucinaFdbk.xLampState")
    state[3] = PlcConnection.Read("o_stLuceSalaFdbk.xLampState")
    state[4] = PlcConnection.Read("o_stLuceIngressoFdbk.xLampState")
    state[5] = PlcConnection.Read("o_stLuceCorridoioFdbk.xLampState")
    state[6] = PlcConnection.Read("o_stLuceAntibagnoFdbk.xLampState")
    state[7] = PlcConnection.Read("o_stLuceBagnoFdbk.xLampState")
    state[8] = PlcConnection.Read("o_stLuceSalaLibreriaFdbk.xLampState")
    state[9] = PlcConnection.Read("o_stLuceCameraLettoFdbk.xLampState")
    state[10] = PlcConnection.Read("o_stLuceFuoriDavantiFdbk.xLampState")
    print "Gli stati delle luci sono: " + str(state)
    return state

def readLampModalState(PlcConnection):
    modalState = [0,0,0,0,0,0,0,0,0,0,0]
    modalState[0] = PlcConnection.Read("o_stLuceVerandaFdbk.iMode")
    modalState[1] = PlcConnection.Read("o_stLuceCantinaFdbk.iMode")
    modalState[2] = PlcConnection.Read("o_stLuceCucinaFdbk.iMode")
    modalState[3] = PlcConnection.Read("o_stLuceSalaFdbk.iMode")
    modalState[4] = PlcConnection.Read("o_stLuceIngressoFdbk.iMode")
    modalState[5] = PlcConnection.Read("o_stLuceCorridoioFdbk.iMode")
    modalState[6] = PlcConnection.Read("o_stLuceAntibagnoFdbk.iMode")
    modalState[7] = PlcConnection.Read("o_stLuceBagnoFdbk.iMode")
    modalState[8] = PlcConnection.Read("o_stLuceSalaLibreriaFdbk.iMode")
    modalState[9] = PlcConnection.Read("o_stLuceCameraLettoFdbk.iMode")
    modalState[10] = PlcConnection.Read("o_stLuceFuoriDavantiFdbk.iMode")
    print "Le modalita delle luci sono: " + str(modalState)
    return modalState
