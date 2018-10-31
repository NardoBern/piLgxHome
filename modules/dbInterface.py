#### Modulo contenente le funzioni di interfaccia verso il database ####

def numbersToDay(dayOfWeek):
    switcher = {
        0: "lunedi",
        1: "martedi",
        2: "mercoledi",
        3: "giovedi",
        4: "venerdi",
        5: "sabato",
        6: "domenica",
    }
    return switcher.get(dayOfWeek, lambda: "Giorno non valido")

## Funzione di controllo se presenti nuovi comandi ##
def checkForNewCommands(databaseObj):
    #######################################
    #### TEST E LETTURA COMANDI DA HMI ####
    #######################################
    print 'CONTROLLO SE CI SONO NUOVI COMANDI DA HMI'
    readData = databaseObj.lettura_dato_multiplo('update','NEED_UPDATE')
    update = []
    test_nuovo_comando = 0
    test_nuovo_configurazione = 0
    test_salva_trend = 0
    for row in readData:
        update.append(row[0])
    test_nuovo_comando = update[0]
    test_nuovo_configurazione = update[1]
    test_salva_trend = update[2]
    print 'TEST NUOVO COMANDO: ', test_nuovo_comando
    print 'TEST NUOVO CONFIGURAZIONE: ', test_nuovo_configurazione
    print 'TEST SALVA TREND: ', test_salva_trend
    return update

## Funzione di lettura dati riscaldamento automatico ##
def readAutoHeatData(databaseObj,dayOfWeek,HeatZone):
    print "Funzione di lettura dati riscaldamento automatico del giorno: " + numbersToDay(dayOfWeek)
    #####################################################
    #### LETTURA DATI RISCALDAMENTO BAGNO AUTOMATICO ####
    #####################################################
    nuovi_dati = databaseObj.lettura_dato_multiplo(HeatZone,numbersToDay(dayOfWeek))
    #### TOBEDONE: definire una classe riscaldamento ####
    autoHeatData = []
    for row in nuovi_dati:
        autoHeatData.append(row[0])
    print autoHeatData
    return autoHeatData

## Funzione di lettura dati automatico / manuale riscaldamento ##
def readAutoManHeat(databaseObj):
    nuovi_stati = databaseObj.lettura_dato_multiplo('stati_riscaldamento','AUTOMATICO')
    stati = []
    for row in nuovi_stati:
        stati.append(row[0])
    print "Automatico riscaldamento bagno: " + str(stati[0])
    print "Automatico riscaldamento notte: " + str(stati[1])
    print "Automatico riscaldamento giorno: " + str(stati[2])
    return stati

## Funzione di lettura comandi manuali ##
def readHeatManCmd(databaseObj):
    comandi_manuali = databaseObj.lettura_dato_multiplo('comandiManuali_riscaldamento','COMANDO')
    comandi = []
    for row in comandi_manuali:
        comandi.append(row[0])
    return comandi
        
## Funzione di lettura contatori manuali ##        
def readHeatManTimer(databaseObj):
    setContatoriManuali = databaseObj.lettura_dato_multiplo('comandiManuali_riscaldamento','CONTATORE')
    contatori = []
    for row in setContatoriManuali:
        contatori.append(row[0])
    return contatori

## Funzione di lettura comandi manuali luci da HMI ##
def readManHmiLampCmds(databaseObj):
    print 'Leggo i comandi manuali per le luci da HMI...'
    nuovi_comandi = databaseObj.lettura_dato_multiplo('comandi_luci','COMANDO')
    comandi = []
    for row in nuovi_comandi:
        comandi.append(row[0])
    return comandi

## Funzione di scrittura modalita riscaldamento ##
def writeHeatModalState(databaseObj,zonaBagno,zonaNotte,zonaGiorno):
    print 'RISCALDAMENTO BAGNO'
    print 'AGGIORNAMENTO DATASTORE @ RISCALDAMENTO BAGNO -- MODALITA'
    databaseObj.scrittura_singola_db('stati_riscaldamento','AUTOMATICO','bagno',zonaBagno)
    print 'RISCALDAMENTO NOTTE'
    print 'AGGIORNAMENTO DATASTORE @ RISCALDAMENTO NOTTE -- MODALITA'        
    databaseObj.scrittura_singola_db('stati_riscaldamento','AUTOMATICO','notte',zonaNotte)
    print 'RISCALDAMENTO GIORNO'
    print 'AGGIORNAMENTO DATASTORE @ RISCALDAMENTO GIORNO -- MODALITA'
    databaseObj.scrittura_singola_db('stati_riscaldamento','AUTOMATICO','giorno',zonaGiorno)
    #databaseObj.salva_dati()

## Funzione di scrittura stato riscaldamento ##
def writeHeatState(databaseObj,zonaBagno,zonaNotte,zonaGiorno):
    print 'RISCALDAMENTO BAGNO'
    print 'AGGIORNAMENTO DATASTORE @ RISCALDAMENTO BAGNO -- STATO'
    databaseObj.scrittura_singola_db('stati_riscaldamento','STATO','bagno',zonaBagno)
    print 'RISCALDAMENTO NOTTE'
    print 'AGGIORNAMENTO DATASTORE @ RISCALDAMENTO NOTTE -- STATO'
    databaseObj.scrittura_singola_db('stati_riscaldamento','STATO','notte',zonaNotte)
    print 'RISCALDAMENTO GIORNO'
    print 'AGGIORNAMENTO DATASTORE @ RISCALDAMENTO GIORNO -- STATO'        
    databaseObj.scrittura_singola_db('stati_riscaldamento','STATO','giorno',zonaGiorno)
    #databaseObj.salva_dati()

## Funzione di scrittura time-out riscaldamento ##
def writeHeatTimeOut(databaseObj,zonaBagno,zonaNotte,zonaGiorno):
    print 'RISCALDAMENTO BAGNO'
    print 'AGGIORNAMENTO DATASTORE @ RISCALDAMENTO BAGNO -- TIMEOUT'
    databaseObj.scrittura_singola_db('stati_riscaldamento','CONTATORE_MANUALE','bagno',zonaBagno)
    print 'RISCALDAMENTO NOTTE'
    print 'AGGIORNAMENTO DATASTORE @ RISCALDAMENTO NOTTE -- TIMEOUT'
    databaseObj.scrittura_singola_db('stati_riscaldamento','CONTATORE_MANUALE','notte',zonaNotte)
    print 'RISCALDAMENTO GIORNO'
    print 'AGGIORNAMENTO DATASTORE @ RISCALDAMENTO GIORNO -- TIMEOUT'
    databaseObj.scrittura_singola_db('stati_riscaldamento','CONTATORE_MANUALE','giorno',zonaGiorno)
    #databaseObj.salva_dati()

## Funzione di salvataggio dati sul database
def saveModify(databaseObj):
    print 'Salvo i dati sul database...'
    databaseObj.salva_dati()

def writeLampState(databaseObj,veranda,cantina,cucina,sala,ingresso,corridoio,antibagno,bagno,salaLibreria,cameraLetto,fuoriDavanti):
    print 'AGGIORNAMENTO DATASTORE @ LUCE SALA -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','STATO','luce_sala',sala)
    print 'AGGIORNAMENTO DATASTORE @ LUCE CORRIDOIO -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','STATO','luce_corridoio',corridoio)
    print 'AGGIORNAMENTO DATASTORE @ LUCE INGRESSO -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','STATO','luce_ingresso',ingresso)
    print 'AGGIORNAMENTO DATASTORE @ LUCE BAGNO -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','STATO','luce_bagno',bagno)
    print 'AGGIORNAMENTO DATASTORE @ LUCE VERANDA -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','STATO','luce_veranda',veranda)
    print 'AGGIORNAMENTO DATASTORE @ LUCE CUCINA -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','STATO','luce_cucina',cucina)
    print 'AGGIORNAMENTO DATASTORE @ LUCE ANTIBAGNO -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','STATO','luce_antibagno',antibagno)
    print 'AGGIORNAMENTO DATASTORE @ LUCE SALA LIBRERIA -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','STATO','luce_sala_libreria',salaLibreria)
    print 'AGGIORNAMENTO DATASTORE @ LUCE CAMERA LETTO -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','STATO','luce_camera_letto',cameraLetto)
    print 'AGGIORNAMENTO DATASTORE @ LUCE FUORI DAVANTI -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','STATO','luce_fuori_davanti',fuoriDavanti)

def writeLampModalState(databaseObj,veranda,cantina,cucina,sala,ingresso,corridoio,antibagno,bagno,salaLibreria,cameraLetto,fuoriDavanti):
    print 'AGGIORNAMENTO DATASTORE @ LUCE SALA -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','AUTOMATICO','luce_sala',sala)
    print 'AGGIORNAMENTO DATASTORE @ LUCE CORRIDOIO -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','AUTOMATICO','luce_corridoio',corridoio)
    print 'AGGIORNAMENTO DATASTORE @ LUCE INGRESSO -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','AUTOMATICO','luce_ingresso',ingresso)
    print 'AGGIORNAMENTO DATASTORE @ LUCE BAGNO -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','AUTOMATICO','luce_bagno',bagno)
    print 'AGGIORNAMENTO DATASTORE @ LUCE VERANDA -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','AUTOMATICO','luce_veranda',veranda)
    print 'AGGIORNAMENTO DATASTORE @ LUCE CUCINA -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','AUTOMATICO','luce_cucina',cucina)
    print 'AGGIORNAMENTO DATASTORE @ LUCE ANTIBAGNO -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','AUTOMATICO','luce_antibagno',antibagno)        
    print 'AGGIORNAMENTO DATASTORE @ LUCE SALA LIBRERIA -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','AUTOMATICO','luce_sala_libreria',salaLibreria)
    print 'AGGIORNAMENTO DATASTORE @ LUCE CAMERA LETTO -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','AUTOMATICO','luce_camera_letto',cameraLetto)
    print 'AGGIORNAMENTO DATASTORE @ LUCE FUORI DAVANTI -- STATO'
    databaseObj.scrittura_singola_db('punti_luce','AUTOMATICO','luce_fuori_davanti',fuoriDavanti)
    