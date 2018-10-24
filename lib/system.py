import datetime
class System:

    ## Metodo init
    def __init__(self):
        self.ora = 0
        self.minuto = 0
        self.secondo = 0
        self.giorno = 0
        self.mese = 0
        self.anno = 0
        self.giornoSettimana = 0
        self.watchDog = 0
    
    ## Metodo aggiornamento watchdog
    def updateWatchDog(self, wdValue):
        self.watchDog = wdValue
        self.watchDog = self.watchDog + 1
        if self.watchDog > 500:
            self.watchDog = 0
        print self.watchDog
        return self.watchDog
    
    ## Metodo aggiornamento data e ora
    def updateTime(self):
        now = datetime.datetime.now()
        self.ora = now.hour
        self.minuto = now.minute
        self.secondo = now.second
        self.giorno = now.day
        self.mese = now.month
        self.anno = now.year
        self.giornoSettimana = datetime.datetime.today().weekday()