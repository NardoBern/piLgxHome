#### Classe lampada ####
class puntoLuce:

    def __init__(self):
        self.automatico = False
        self.manHmiCmd  = False
        self.manHmiCmdOld = False
        self.stato = False
        self.timeOut    = 0
