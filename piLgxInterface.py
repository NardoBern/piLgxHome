import time
import sys
import os
import site
site.addsitedir(sys.path[0]+'/lib')
site.addsitedir(sys.path[0]+'/modules')
site.addsitedir(sys.path[0]+'/class')
from eip import PLC
from system import System
import datetime
from threading import Timer
from db_manager import database_engine
from gestore_orologio import orologio
import writeToPLC
import dbInterface
import cZonaRiscaldamento
import cLamp
import counter
import readFromPLC
import cCheckSums

def applyHmiLampCmds():
    print 'Chiamata alla funzione applyHmiLampCmds...'
    writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceAntiBagnoHmiCmds.xManCmd",luceAntibagno.manHmiCmd)
    writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceBagnoHmiCmds.xManCmd",luceBagno.manHmiCmd)
    writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceCantinaHmiCmds.xManCmd",luceCantina.manHmiCmd)
    writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceCorridoioHmiCmds.xManCmd",luceCorridoio.manHmiCmd)
    writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceCucinaHmiCmds.xManCmd",luceCucina.manHmiCmd)
    writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceFuoriDavantiHmiCmds.xManCmd",luceFuoriDavanti.manHmiCmd)
    writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceIngressoHmiCmds.xManCmd",luceIngresso.manHmiCmd)
    writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceCameraLettoHmiCmds.xManCmd",luceLetto.manHmiCmd)
    writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceSalaHmiCmds.xManCmd",luceSala.manHmiCmd)
    print "Luce Sala Libreria = True..."
    writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceSalaLibreriaHmiCmds.xManCmd",luceSalaLibreria.manHmiCmd)
    writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceVerandaHmiCmds.xManCmd",luceVeranda.manHmiCmd)

def applyHmiLampModal():
    print 'Chiamata alla funzione applyHmiLampModal...'
    writeToPLC.writeLampModalToPLC(lgxPLC,"i_stLuceAntiBagnoHmiCmds.iModeSel",luceAntibagno.automatico)
    writeToPLC.writeLampModalToPLC(lgxPLC,"i_stLuceBagnoHmiCmds.iModeSel",luceBagno.automatico)
    writeToPLC.writeLampModalToPLC(lgxPLC,"i_stLuceCantinaHmiCmds.iModeSel",luceCantina.automatico)
    writeToPLC.writeLampModalToPLC(lgxPLC,"i_stLuceCorridoioHmiCmds.iModeSel",luceCorridoio.automatico)
    writeToPLC.writeLampModalToPLC(lgxPLC,"i_stLuceCucinaHmiCmds.iModeSel",luceCucina.automatico)
    writeToPLC.writeLampModalToPLC(lgxPLC,"i_stLuceFuoriDavantiHmiCmds.iModeSel",luceFuoriDavanti.automatico)
    writeToPLC.writeLampModalToPLC(lgxPLC,"i_stLuceIngressoHmiCmds.iModeSel",luceIngresso.automatico)
    writeToPLC.writeLampModalToPLC(lgxPLC,"i_stLuceCameraLettoHmiCmds.iModeSel",luceLetto.automatico)
    writeToPLC.writeLampModalToPLC(lgxPLC,"i_stLuceSalaHmiCmds.iModeSel",luceSala.automatico)
    writeToPLC.writeLampModalToPLC(lgxPLC,"i_stLuceSalaLibreriaHmiCmds.iModeSel",luceSalaLibreria.automatico)
    writeToPLC.writeLampModalToPLC(lgxPLC,"i_stLuceVerandaHmiCmds.iModeSel",luceVeranda.automatico)

def readAndApplyCommands():
    #### Chiamata alla funzione di lettura dei dati di riscaldamento automatico ####
    riscaldamentoBagno.autoSet = dbInterface.readAutoHeatData(data_commands,system.giornoSettimana,'automatico_riscaldamentoBagno')
    riscaldamentoGiorno.autoSet = dbInterface.readAutoHeatData(data_commands,system.giornoSettimana,'automatico_riscaldamentoGiorno')
    riscaldamentoNotte.autoSet = dbInterface.readAutoHeatData(data_commands,system.giornoSettimana,'automatico_riscaldamentoNotte')
    #### Chiamata alla funzione di scrittura dei dati di riscaldamento automatico nel plc ####
    writeToPLC.writeAutoHeatDataToPLC(lgxPLC,riscaldamentoBagno.autoSet,riscaldamentoGiorno.autoSet,riscaldamentoNotte.autoSet)
    #### Chiamata alla funzione di lettura degli stati Auto/Man del riscaldamento ####
    stati = []
    stati = dbInterface.readAutoManHeat(data_commands)
    riscaldamentoBagno.automatico = stati[0]
    riscaldamentoNotte.automatico = stati[1]
    riscaldamentoGiorno.automatico = stati[2]
    #### Chiamata alla funzione di scrittura degli stati auto/man nel plc ###
    writeToPLC.writeAutoManToPLC(lgxPLC,riscaldamentoBagno.automatico,riscaldamentoGiorno.automatico,riscaldamentoNotte.automatico)
    #### Chiamata alla funzione di lettura dei comandi manuali riscaldamento ####
    comandi = []
    comandi = dbInterface.readHeatManCmd(data_commands)
    riscaldamentoBagno.manCommand = comandi[0]
    riscaldamentoNotte.manCommand = comandi[1]
    riscaldamentoGiorno.manCommand = comandi[2]
    #### Chiamata alla funzione di scrittura dei comandi manuali riscaldamento nel PLC ####
    writeToPLC.writeManHeatCmdToPLC(lgxPLC,riscaldamentoBagno.manCommand,riscaldamentoGiorno.manCommand,riscaldamentoNotte.manCommand)
    #### Chiamata alla funzione di lettura dei time-out riscaldamento manuale ####
    timeOut = []
    timeOut = dbInterface.readHeatManTimer(data_commands)
    print timeOut
    riscaldamentoBagno.manTimeOut = timeOut[0] * 60 * 1000
    riscaldamentoNotte.manTimeOut = timeOut[1] * 60 * 1000
    riscaldamentoGiorno.manTimeOut = timeOut[2] * 60 * 1000
    #### Chiamata alla funzione di scrittura dei time-out manuali riscaldamento nel PLC ####
    writeToPLC.writeManHeatTimerToPLC(lgxPLC,riscaldamentoBagno.manTimeOut,riscaldamentoGiorno.manTimeOut,riscaldamentoNotte.manTimeOut)
    #### Chiamata alla funzione di lettura comandi manuali luci da HMI ####
    comandiLuce = []
    comandiLuce = dbInterface.readManHmiLampCmds(data_commands)
    luceVeranda.manHmiCmd = comandiLuce[0]
    luceCucina.manHmiCmd = comandiLuce[1]
    luceAntibagno.manHmiCmd = comandiLuce[2]
    luceSalaLibreria.manHmiCmd = comandiLuce[3]
    print "Comando luce sala libreria: " + str( luceSalaLibreria.manHmiCmd )
    luceLetto.manHmiCmd = comandiLuce[4]
    luceCorridoio.manHmiCmd = comandiLuce[5]
    luceSala.manHmiCmd = comandiLuce[6]
    luceIngresso.manHmiCmd = comandiLuce[7]
    luceBagno.manHmiCmd = comandiLuce[8]
    luceFuoriDavanti.manHmiCmd = comandiLuce[9]
    #### Chiamata alla funzione di applicazione dei comandi luce da HMI ####
    applyHmiLampCmds()
    #### Chiamata alla funzione di lettura modalita luci da HMI ####
    modalitaLuce = []
    modalitaLuce = dbInterface.readManHmiLampModalita(data_commands)
    luceVeranda.automatico = modalitaLuce[0]
    luceCucina.automatico = modalitaLuce[1]
    luceAntibagno.automatico = modalitaLuce[2]
    luceSalaLibreria.automatico = modalitaLuce[3]
    luceLetto.automatico = modalitaLuce[4]
    luceCorridoio.automatico = modalitaLuce[5]
    luceSala.automatico = modalitaLuce[6]
    luceIngresso.automatico = modalitaLuce[7]
    luceBagno.automatico = modalitaLuce[8]
    luceFuoriDavanti.automatico = modalitaLuce[9]
    #### Chiamata alla funzione di scrittura delle modalita luci su PLC ####
    applyHmiLampModal()
    #### Chiamata alla funzione di lettura dei time-out automatici ####
    timeOut = []
    timeOut = dbInterface.readLampAutoTimeOut(data_commands)
    luceVeranda.timeOut = timeOut[0] * 1000
    luceCucina.timeOut = timeOut[1] * 1000
    luceAntibagno.timeOut = timeOut[2] * 1000
    luceSalaLibreria.timeOut = timeOut[3] * 1000
    luceLetto.timeOut = timeOut[4] * 1000
    luceCorridoio.timeOut = timeOut[5] * 1000
    luceSala.timeOut = timeOut[6] * 1000
    luceIngresso.timeOut = timeOut[7] * 1000
    luceBagno.timeOut = timeOut[8] * 1000
    luceFuoriDavanti.timeOut = timeOut[9] * 1000
    #### Chiamata alla funzione di scrittura timeOut sul PLC ####
    writeToPLC.writeLampTimeOutToPLC(lgxPLC,timeOut)

def checkForNew():
    update = dbInterface.checkForNewCommands(data_commands)
    test_nuovo_comando = update[0]
    test_nuovo_configurazione = update[1]
    test_salva_trend = update[2]
    if test_nuovo_comando == 1:
        data_commands.scrittura_singola_db('update','NEED_UPDATE','1',0)
        data_commands.salva_dati()
        readAndApplyCommands()

    
    if test_nuovo_configurazione == 1:
        data_commands.scrittura_singola_db('update','NEED_UPDATE','2',0)
        data_commands.salva_dati()
    if test_salva_trend == 1:
        data_commands.scrittura_singola_db('update','NEED_UPDATE','3',0)
        data_commands.salva_dati()

def checkForNewDay():
    if system.giorno != system.giornoOld:
        print "Siamo in un nuovo giorno!! Aggiorno i dati del riscaldamento automatico..."
        #### Chiamata alla funzione di lettura dei dati di riscaldamento automatico ####
        riscaldamentoBagno.autoSet = dbInterface.readAutoHeatData(data_commands,system.giornoSettimana,'automatico_riscaldamentoBagno')
        riscaldamentoGiorno.autoSet = dbInterface.readAutoHeatData(data_commands,system.giornoSettimana,'automatico_riscaldamentoGiorno')
        riscaldamentoNotte.autoSet = dbInterface.readAutoHeatData(data_commands,system.giornoSettimana,'automatico_riscaldamentoNotte')
        #### Chiamata alla funzione di scrittura dei dati di riscaldamento automatico nel plc ####
        writeToPLC.writeAutoHeatDataToPLC(lgxPLC,riscaldamentoBagno.autoSet,riscaldamentoGiorno.autoSet,riscaldamentoNotte.autoSet)
    system.giornoOld = system.giorno

def readDataFromPLC():
    print "Lettura dati riscaldamento..."
    modalita = []
    modalita = readFromPLC.readHeatModalState(lgxPLC)
    stati = []
    stati = readFromPLC.readHeatState(lgxPLC)
    checkSums.riscaldamentoModal = checkSums.calculateCheckSums(modalita)
    print 'CheckSum modalita riscaldamento: ' + str(checkSums.riscaldamentoModal)
    checkSums.riscaldamentoStati = checkSums.calculateCheckSums(stati)
    print 'CheckSum stati riscaldamento: ' + str(checkSums.riscaldamentoStati)
    if checkSums.riscaldamentoModal != checkSums.riscaldamentoModalOld:
        dbInterface.writeHeatModalState(data_store,modalita[0],modalita[1],modalita[2])
        dbInterface.saveModify(data_store)
    checkSums.riscaldamentoModalOld = checkSums.riscaldamentoModal
    if checkSums.riscaldamentoStati != checkSums.riscaldamentoStatiOld:
        dbInterface.writeHeatState(data_store,stati[0],stati[1],stati[2])
        dbInterface.saveModify(data_store)
    checkSums.riscaldamentoStatiOld = checkSums.riscaldamentoStati
    print "Lettura dati luci..."
    stati = []
    stati = readFromPLC.readLampState(lgxPLC)
    checkSums.luciStati = checkSums.calculateCheckSums(stati)
    print 'CheckSum stati luci: ' + str(checkSums.luciStati)
    if checkSums.luciStati != checkSums.luciStatiOld:
        dbInterface.writeLampState(data_store,stati[0],stati[1],stati[2],stati[3],stati[4],stati[5],stati[6],stati[7],stati[8],stati[9],stati[10])
        dbInterface.saveModify(data_store)
    checkSums.luciStatiOld = checkSums.luciStati
    modalita = []
    modalita = readFromPLC.readLampModalState(lgxPLC)
    checkSums.luciModalita = checkSums.calculateCheckSums(modalita)
    print "CheckSum modalita luci: " + str(checkSums.luciModalita)
    if checkSums.luciModalita != checkSums.luciModalitaOld:
        dbInterface.writeLampModalState(data_store,modalita[0],modalita[1],modalita[2],modalita[3],modalita[4],modalita[5],modalita[6],modalita[7],modalita[8],modalita[9],modalita[10])
        dbInterface.saveModify(data_store)
    checkSums.luciModalitaOld = checkSums.luciModalita

def memorizzaEvento(evento):
    systemClock.letturaOrologio()
    timeStamp = systemClock.lettura
    EventDatabase.inserisciEvento(evento,timeStamp)
    EventDatabase.salva_dati()

def oneSecondInterrupt():
    print "Funzione di interrupt ad 1sec."
    secondCounter.counter = secondCounter.counter + 1
    print secondCounter.counter
    writeToPLC.updateWatchDog(lgxPLC,system.updateWatchDog(lgxPLC.Read("o_stSystemVar.iHmiWdCounter")))
    system.updateTime()
    writeToPLC.updateTime(lgxPLC,system.ora,system.minuto,system.secondo)
    if secondCounter.counter > 5:
        print "Funzione di interrupt a 5 sec."
        print "Controllo se vi sono nuovi comandi..."
        secondCounter.counter = 0
        checkForNew()
        checkForNewDay()
        readDataFromPLC()
    tOne = Timer(1.0,oneSecondInterrupt)
    tOne.start()

##########################
#### INIZIALIZZAZIONE ####
##########################
print 'START CICLO DI INIZIALIZZAZIONE'
##############################################
#### INIZIALIZZAZIONE OROLOGIO DI SISTEMA ####
##############################################
try:
    print ("INIZIALIZZAZIONE OROLOGIO DI SISTEMA")
    systemClock = orologio()
    systemClock.inizializzazioneOrologio()
except:
    print "ERRORE NELLA INIZIALIZZAZIONE DELL'OROLOGIO"
#########################################################
#### INIZIALIZZAZIONE CONNESSIONE AL DATABASE ERRORI ####
#########################################################
try:
    print 'CONNESSIONE AL DATABASE DEGLI ERRORI'
    ErrorDatabase = database_engine('/home/pi/db_imp_ele/error_store.db')
except Exception,e:
    print e
#########################################################
#### INIZIALIZZAZIONE CONNESSIONE AL DATABASE EVENTI ####
#########################################################
try:
    print 'CONNESSIONE AL DATABASE DEGLI EVENTI'
    EventDatabase = database_engine('/home/pi/db_imp_ele/event_store.db')
    memorizzaEvento('AVVIO DEL SISTEMA')
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
#### INIZIALIZZAZIONE ZONA RISCALDAMENTO ####
try:
    print 'Inizializzazione zona riscaldamento bagno'
    riscaldamentoBagno = cZonaRiscaldamento.ZonaRiscaldamento()
    print 'Inizializzazione zona riscaldamento giorno'
    riscaldamentoGiorno = cZonaRiscaldamento.ZonaRiscaldamento()
    print 'Inizializzazione zona riscaldamento notte'
    riscaldamentoNotte = cZonaRiscaldamento.ZonaRiscaldamento()
except Exception,e:
    print 'Errore inizializzazione zona riscaldamento bagno'
    print e
#### Inizializzazione contatore secondi ####
try:
    print 'Inizializzazione contatore secondi'
    secondCounter = counter.counter()
    secondCounter.counter = 0
except Exception,e:
    print 'Errore inizializzazione contatore secondi'
    print e
#### Inizializzazione checksums ####
try:
    print 'Inizializzazione CheckSums'
    checkSums = cCheckSums.cChekSums()
except Exception,e:
    print 'Errore inizializzazione checksums'
    print e
#### Inizializzazione punti luce ####
try:
    print 'Inizializzazione punti luce'
    luceVeranda = cLamp.puntoLuce()
    luceCucina = cLamp.puntoLuce()
    luceSala = cLamp.puntoLuce()
    luceIngresso = cLamp.puntoLuce()
    luceCorridoio = cLamp.puntoLuce()
    luceAntibagno = cLamp.puntoLuce()
    luceBagno = cLamp.puntoLuce()
    luceLetto = cLamp.puntoLuce()
    luceSalaLibreria = cLamp.puntoLuce()
    luceFuoriDavanti = cLamp.puntoLuce()
    luceCantina = cLamp.puntoLuce()
except Exception,e:
    print 'Errore inizializzazione punti luce'
    print e
#### FINE CICLO INIZIALIZZAZIONE ####
print 'Fine ciclo inizializzazione...'
#### Lettura ed applicazione dei comandi ####
readAndApplyCommands()

tOne = Timer(1.0,oneSecondInterrupt)
tOne.start()
