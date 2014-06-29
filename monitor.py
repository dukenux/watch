#!/usr/bin/python
import struct
import time
import sys
import subprocess
import datetime
import os
import re
import A20_GPIO as GPIO


def getProcessId(processName):
    ps = subprocess.Popen("ps ax -o pid= -o args= ", shell=True, stdout=subprocess.PIPE)
    ps_pid = ps.pid
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    for line in output.split("\n"):
        res = re.findall("(\d+) (.*)", line)
        if res:
            pid = int(res[0][0])
            if processName in res[0][1] and pid != os.getpid() and pid != ps_pid:
                return pid
    return -1

print "Init monitor"
GPIO.init()
GPIO.setcfg(GPIO.PIN3_39, GPIO.INPUT)
GPIO.setcfg(GPIO.PIN3_40, GPIO.INPUT)
screenState=False
motionStatus = True
os.system("echo 1 > /sys/class/gpio/gpio27_pb2/value")
infile_path = "/dev/input/event3"
#long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)
#open file in binary mode
in_file = open(infile_path, "rb")
try:
    event = in_file.read(EVENT_SIZE)
    while event:
        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)
        if type != 0 or code != 0 or value != 0:
            print("Event type %u, code %u, value: %u at %d, %d" % \
                (type, code, value, tv_sec, tv_usec))
            if code==139 and value==1:
                if screenState==False:
                    os.system("echo 0 > /sys/class/gpio/gpio27_pb2/value")
                    print "allumage"
                    screenState=True
                else:
                    os.system("echo 1 > /sys/class/gpio/gpio27_pb2/value")
                    print "extinction"
                    screenState=False
            if code==217 and value==1:
                if motionStatus:
                    pid=getProcessId('/usr/bin/motion')
                    if pid!=-1:
                        subprocess.call('kill -2 '+str(pid),shell=True)
                        print "motion stopped"
                    pid=getProcessId('/opt/mjpg-streamer/mjpg_streamer')
                    if pid!=-1:
                        subprocess.call('kill -2 '+str(pid),shell=True)
                        print "mjpg-streamer stopped"
                    motionStatus=False
                else:
                    os.system('/home/olimex/scripts/watch.sh')
                    print "motion started"
                    motionStatus=True
            if code==114 and value==1:
                print "System halt"
                os.system("halt")
        event = in_file.read(EVENT_SIZE)

finally:
    in_file.close()

