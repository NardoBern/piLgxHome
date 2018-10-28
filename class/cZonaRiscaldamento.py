### Classe riscaldamento ###
class ZonaRiscaldamento:
    def __init__(self):
        self.stato = False
        self.automatico = False
        self.manCommand = False
        self.manTimeOut = 0
        self.autoSet = []
    