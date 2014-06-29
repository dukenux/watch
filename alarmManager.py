#!/usr/bin/python
import time
from datetime import datetime
import A20_GPIO as GPIO

MAX_BIP = 1
# GPIO libre
# PIN3_7, PIN3_8, PIN3_17, PIN3_39
# PIN3_7 -> relais alarme

def getAlarmCounter():
        try:
                f=open('/run/shm/alarmCnt.txt','r')
                cnt=f.read()
                f.close()
                return int(cnt)
        except Exception as ex5:
                return 0

def updateAlarmCounter():
    alarmCnt=getAlarmCounter()+1
    try:
        f=open('/run/shm/alarmCnt.txt','w+')
        f.write(str(alarmCnt))
        f.close()
    except Exception, e7:
        print "Erreur : %s" % e7

def updateLog():
    try:
        f=open('/run/shm/alarmLog.txt','a+')
        f.write(datetime.now().strftime("%H:%M")+'\n')
        f.close()
    except Exception, e8:
        print "Erreur : %s" % e8

def updateAlarmFlag():
    try:
        f=open('/run/shm/alarmFlag.txt','w+')
        f.write("1")
        f.close()
    except Exception, e11:
        print "Erreur : %s" % e11

def bipbip():
            for i in range(0,MAX_BIP):
                GPIO.output(GPIO.PIN3_7, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(GPIO.PIN3_7, GPIO.LOW)
                time.sleep(0.1)

GPIO.init()
GPIO.setcfg(GPIO.PIN3_7, GPIO.OUTPUT)
updateAlarmFlag()
updateAlarmCounter()
updateLog()
bipbip()
GPIO.cleanup()


