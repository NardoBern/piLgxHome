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
import writeToPLC
import dbInterface
import cZonaRiscaldamento
import cLamp
import counter
import readFromPLC
import cCheckSums

def checkForNewLampCmd():
    print 'Chiamata alla funzione checkForNewLampCmd'
    if luceAntibagno.manHmiCmd != luceAntibagno.manHmiCmdOld:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceAntiBagnoHmiCmds.xManCmd",True)
    else:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceAntiBagnoHmiCmds.xManCmd",False)
    if luceBagno.manHmiCmd != luceBagno.manHmiCmdOld:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceBagnoHmiCmds.xManCmd",True)
    else:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceBagnoHmiCmds.xManCmd",False)
    if luceCantina.manHmiCmd != luceCantina.manHmiCmdOld:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceCantinaHmiCmds.xManCmd",True)
    else:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceCantinaHmiCmds.xManCmd",False)
    if luceCorridoio.manHmiCmd != luceCorridoio.manHmiCmdOld:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceCorridoioHmiCmds.xManCmd",True)
    else:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceCorridoioHmiCmds.xManCmd",False)
    if luceCucina.manHmiCmd != luceCucina.manHmiCmdOld:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceCucinaHmiCmds.xManCmd",True)
    else:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceCucinaHmiCmds.xManCmd",False)
    if luceFuoriDavanti.manHmiCmd != luceFuoriDavanti.manHmiCmdOld:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceFuoriDavantiHmiCmds.xManCmd",True)
    else:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceFuoriDavantiHmiCmds.xManCmd",False)
    if luceIngresso.manHmiCmd != luceIngresso.manHmiCmdOld:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceIngressoHmiCmds.xManCmd",True)
    else:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceIngressoHmiCmds.xManCmd",False)
    if luceLetto.manHmiCmd != luceLetto.manHmiCmdOld:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceCameraLettoHmiCmds.xManCmd",True)
    else:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceCameraLettoHmiCmds.xManCmd",False)
    if luceSala.manHmiCmd != luceSala.manHmiCmdOld:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceSalaHmiCmds.xManCmd",True)
    else:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceSalaHmiCmds.xManCmd",False)
    if luceSalaLibreria.manHmiCmd != luceSalaLibreria.manHmiCmdOld:
        print "Luce Sala Libreria = True..."
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceSalaLibreriaHmiCmds.xManCmd",True)
    else:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceSalaLibreriaHmiCmds.xManCmd",False)
    if luceVeranda.manHmiCmd != luceVeranda.manHmiCmdOld:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceVerandaHmiCmds.xManCmd",True)
    else:
        writeToPLC.writeLampManCmdToPLC(lgxPLC,"i_stLuceVerandaHmiCmds.xManCmd",False)
    luceAntibagno.manHmiCmdOld = luceAntibagno.manHmiCmd
    luceBagno.manHmiCmdOld = luceBagno.manHmiCmd
    luceCantina.manHmiCmdOld = luceCantina.manHmiCmd
    luceCorridoio.manHmiCmdOld = luceCorridoio.manHmiCmd
    luceCucina.manHmiCmdOld = luceCucina.manHmiCmd
    luceFuoriDavanti.manHmiCmdOld = luceFuoriDavanti.manHmiCmd
    luceIngresso.manHmiCmdOld = luceIngresso.manHmiCmd
    luceLetto.manHmiCmdOld = luceLetto.manHmiCmd
    luceSala.manHmiCmdOld = luceSala.manHmiCmd
    luceSalaLibreria.manHmiCmdOld = luceSalaLibreria.manHmiCmd
    luceVeranda.manHmiCmdOld = luceVeranda.manHmiCmd


def checkForNew():
    update = dbInterface.checkForNewCommands(data_commands)
    test_nuovo_comando = update[0]
    test_nuovo_configurazione = update[1]
    test_salva_trend = update[2]
    if test_nuovo_comando == 1:
        data_commands.scrittura_singola_db('update','NEED_UPDATE','1',0)
        data_commands.salva_dati()
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
    #### Chiamata alla funzione di controllo se ho un nuovo comando luce da HMI ####
    checkForNewLampCmd()


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

tOne = Timer(1.0,oneSecondInterrupt)
tOne.start()
