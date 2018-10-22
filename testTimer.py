from threading import Timer
i = 0
def oneSecondInterrupt():
    print "This is one second Timer interrupt \n"
    tOne = Timer(1.0,oneSecondInterrupt)
    tOne.start()
def fiveSecondInterrupt():
    print "This is five second Timer interrupt \n"
    i = i + 1
    while i < 5:
        print i
    tFive = Timer(5.0,fiveSecondInterrupt)
    tFive.start()
def halfSecondInterrupt():
    print "This is half second Timer interrupt \n"
    tHalfOne = Timer(0.5,halfSecondInterrupt)
    tHalfOne.start()

tOne = Timer(1.0,oneSecondInterrupt)
tHalfOne = Timer(0.5,halfSecondInterrupt)
tFive = Timer(5.0,fiveSecondInterrupt)
tHalfOne.start()
tOne.start()
tFive.start()

