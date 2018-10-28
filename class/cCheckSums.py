class cChekSums:
    
    ## Metodo di inizializzazione ##
    def __init__(self):
        self.riscaldamentoStati = 0
        self.riscaldamentoStatiOld = 0
        self.riscaldamentoModal = 0
        self.riscaldamentoModalOld = 0
        self.riscaldamentoTimeOut = 0
        self.riscaldamentoTimeOutOld
    
    ## Funzione di calcolo del checkSum ##
    def calculateCheckSums(self,data):
        if isinstance(data,(list,)):
            a = 1
            b = 0
            for num in data:
                a = a + num
                b = b + a
            return b * 65536 + a
        elif isinstance(data,(int,)):
            return data

