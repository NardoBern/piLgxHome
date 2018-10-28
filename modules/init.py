#### Modulo di init software ####
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

def initSystem(enable):
    if enable:
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
