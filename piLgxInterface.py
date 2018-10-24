import time
import sys
import os
import site
site.addsitedir(sys.path[0]+'/lib')
from eip import PLC
from system import System
import datetime
from threading import Timer
from db_manager import database_engine

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

def readAutoHeatData(dayOfWeek):
    print "Funzione di lettura dati riscaldamento automatico del giorno: " + numbersToDay(dayOfWeek)
    #####################################################
    #### LETTURA DATI RISCALDAMENTO BAGNO AUTOMATICO ####
    #####################################################
    nuovi_dati = data_commands.lettura_dato_multiplo('automatico_riscaldamentoBagno',numbersToDay(dayOfWeek))
    #### TOBEDONE: definire una classe riscaldamento ####
    riscaldamentoBagno_ricettaAttuale = []
    for row in nuovi_dati:
        riscaldamentoBagno_ricettaAttuale.append(row[0])
    print riscaldamentoBagno_ricettaAttuale

def checkForNew():
    #######################################
    #### TEST E LETTURA COMANDI DA HMI ####
    #######################################
    print 'CONTROLLO SE CI SONO NUOVI COMANDI DA HMI'
    readData = data_commands.lettura_dato_multiplo('update','NEED_UPDATE')
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
    if test_nuovo_comando == 1:
        data_commands.scrittura_singola_db('update','NEED_UPDATE','1',0)
        data_commands.salva_dati()
        #### Chiamata alla funzione di lettura dei dati di riscaldamento automatico ####
        readAutoHeatData(system.giornoSettimana)
    if test_nuovo_configurazione == 1:
        data_commands.scrittura_singola_db('update','NEED_UPDATE','2',0)
        data_commands.salva_dati()
    if test_salva_trend == 1:
        data_commands.scrittura_singola_db('update','NEED_UPDATE','3',0)
        data_commands.salva_dati()

def oneSecondInterrupt():
    print "Funzione di interrupt ad 1sec."
    lgxPLC.Write("i_stHmiSystemVar.iWatchDog",system.updateWatchDog(lgxPLC.Read("o_stSystemVar.iHmiWdCounter")))
    system.updateTime()
    lgxPLC.Write("i_stData.iSec",system.secondo)
    lgxPLC.Write("i_stData.iMin",system.minuto)
    lgxPLC.Write("i_stData.iOra",system.ora)
    tOne = Timer(1.0,oneSecondInterrupt)
    tOne.start()

def fiveSecondInterrupt():
    print "Funzione di interrupt a 5sec."
    print "Controllo se vi sono nuovi comandi..."
    checkForNew()
    print "Fine controllo..."
    tFive = Timer(5.0,fiveSecondInterrupt)
    tFive.start()

##########################
#### INIZIALIZZAZIONE ####
##########################
print 'START CICLO DI INIZIALIZZAZIONE'
#########################################################
#### INIZIALIZZAZIONE CONNESSIONE AL DATABASE ERRORI ####
#########################################################
try:
    print 'CONNESSIONE AL DATABASE DEGLI ERRORI'
    ErrorDatabase = database_engine('/home/pi/db_imp_ele/error_store.db')
except Exception,e:
    print e
#### INIZIALIZZAZIONE SYSTEM ####
try:
    system = System()
except Exception,e:
    print e
#### INIZIALIZZAZIONE PLC CONNECTION ####
try:        
    lgxPLC = PLC()
    lgxPLC.IPAddress = "192.168.2.15"
    lgxPLC.Micro800 = True
except Exception,e:
    print e
#############################################################
#### INIZIALIZZAZIONE CONNESSIONE AL DATABASE DATA_STORE ####
#############################################################
try:
    print 'INIZIALIZZAZIONE CONNESSIONE AL DATABASE DATA_STORE'
    data_store = database_engine('/home/pi/db_imp_ele/data_store.db')
except Exception,e:
    print e
################################################################
#### INIZIALIZZAZIONE CONNESSIONE AL DATABASE DATA_COMMANDS ####
################################################################
try:
    print 'INIZIALIZZAZIONE CONNESSIONE AL DATABASE DATA_COMMANDS'
    data_commands = database_engine('/home/pi/db_imp_ele/data_commands.db')
except Exception,e:
    print 'ERRORE NELLA INIZIALIZZAZIONE DELLA CONNESSIONE AL DATABASE DATA_COMMANDS'
    print e

#### FINE CICLO INIZIALIZZAZIONE ####
print 'Fine ciclo inizializzazione...'

tOne = Timer(1.0,oneSecondInterrupt)
tOne.start()
tFive = Timer(5.0,fiveSecondInterrupt)
tFive.start()
