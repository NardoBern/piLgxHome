import datetime
## Classe orologio ##
class orologio:

    def __init__(self):
        self.giorno = 0
        self.mese = 0
        self.anno = 0
        self.ora = 0
        self.minuti = 0
        self.secondi = 0
        self.lettura = datetime.datetime.now()

    def letturaOrologio(self):
        self.lettura = datetime.datetime.now()
        self.giorno = self.lettura.day
        self.mese = self.lettura.month
        self.anno = self.lettura.year
        self.ora = self.lettura.hour
        self.minuti = self.lettura.minute
        self.secondi = self.lettura.second