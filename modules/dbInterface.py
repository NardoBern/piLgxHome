#### Modulo contenente le funzioni di interfaccia verso il database ####
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

## Funzione di lettura dati riscaldamento automatico ##
def readAutoHeatData(databaseObj,dayOfWeek):
    print "Funzione di lettura dati riscaldamento automatico del giorno: " + numbersToDay(dayOfWeek)
    #####################################################
    #### LETTURA DATI RISCALDAMENTO BAGNO AUTOMATICO ####
    #####################################################
    nuovi_dati = databaseObj.lettura_dato_multiplo('automatico_riscaldamentoBagno',numbersToDay(dayOfWeek))
    #### TOBEDONE: definire una classe riscaldamento ####
    riscaldamentoBagno_ricettaAttuale = []
    for row in nuovi_dati:
        riscaldamentoBagno_ricettaAttuale.append(row[0])
    print riscaldamentoBagno_ricettaAttuale
