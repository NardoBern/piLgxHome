site.addsitedir(sys.path[0]+'/lib')
from eip import PLC
import datetime
from threading import Timer
test = PLC()
test.IPAddress = "192.168.2.15"
test.Micro800 = True

now = datetime.datetime.now()
hour = now.hour
minute = now.minute
second = now.second
day = now.day
month = now.month
year = now.year
weekDay = datetime.datetime.today().weekday()
#value = test.Read("o_xBool")
#print value
#a = 0
#i = 0
#b = 500
#test.Write("i_TimerValue",b)
#test.Write("CLOCK_1S",True)
def updateData():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    test.Write("i_stData.iSec",second)
    test.Write("i_stData.iMin",minute)
    test.Write("i_stData.iOra",hour)
    iHmiWdCounter = test.Read("o_stSystemVar.iHmiWdCounter")
    iHmiWdCounter = iHmiWdCounter + 1
    test.Write("i_stHmiSystemVar.iWatchDog",iHmiWdCounter)
    if iHmiWdCounter > 500:
        iHmiWdCounter = 0
    t = Timer(1.0,updateData)
    t.start()
t = Timer(1.0,updateData)
t.start()

