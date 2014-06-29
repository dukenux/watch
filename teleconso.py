#!/usr/bin/python
# -*- coding: utf8 -*-
import serial
import time
from datetime import datetime
import subprocess
import os

class teleconso():

    def isInt(self,x):
      try:
        int(x)
        return True
      except ValueError:
        return False

    def getInfo(self):
        noCompteur=tarif=hcJb=hpJb=hcJw=hpJw=hcJr=hpJr=ptec=demain=iInst=""
        try:
            p=subprocess.Popen('ls -l /dev/serial/by-id/ | grep FTDI',shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            results=p.stdout.readlines()
            if len(results)>0:
                posPortComm=results[0].find("ttyUSB")
                if posPortComm>0:
                    portComm=results[0][posPortComm:].replace("\n","")
                    dongle = serial.Serial(port="/dev/"+portComm,baudrate=1200,bytesize=serial.SEVENBITS,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE,rtscts=0,dsrdtr=0,xonxoff=0,timeout=3)
                    try:
                        compteur=10
                        while compteur>0:
                            item=0
                            compteur=compteur-1
                            s = dongle.read(300)
                            position=s.find("ADCO")
                            if position>-1:
                                positionFin=s[position:].find("\r")
                                noCompteur=s[position+5:position+positionFin-2]
                                item+=1
                            position=s.find("OPTARIF")
                            if position>-1:
                                positionFin=s[position:].find("\r")
                                tarif=s[position+8:position+positionFin-2]
                                item+=1
                            position=s.find("BBRHCJB")
                            if position>-1:
                                positionFin=s[position:].find("\r")
                                hcJb=s[position+8:position+positionFin-2]
                                if len(hcJb)!=9: continue
                                if self.isInt(hcJb)==False: continue
                                item+=1
                            position=s.find("BBRHPJB")
                            if position>-1:
                                positionFin=s[position:].find("\r")
                                hpJb=s[position+8:position+positionFin-2]
                                if len(hpJb)!=9: continue
                                if self.isInt(hpJb)==False: continue
                                item+=1
                            position=s.find("BBRHCJW")
                            if position>-1:
                                positionFin=s[position:].find("\r")
                                hcJw=s[position+8:position+positionFin-2]
                                if len(hcJw)!=9: continue
                                if self.isInt(hcJw)==False: continue
                                item+=1
                            position=s.find("BBRHPJW")
                            if position>-1:
                                positionFin=s[position:].find("\r")
                                hpJw=s[position+8:position+positionFin-2]
                                if len(hpJw)!=9: continue
                                if self.isInt(hpJw)==False: continue
                                item+=1
                            position=s.find("BBRHCJR")
                            if position>-1:
                                positionFin=s[position:].find("\r")
                                hcJr=s[position+8:position+positionFin-2]
                                if len(hcJr)!=9: continue
                                if self.isInt(hcJr)==False: continue
                                item+=1
                            position=s.find("BBRHPJR")
                            if position>-1:
                                positionFin=s[position:].find("\r")
                                hpJr=s[position+8:position+positionFin-2]
                                if len(hpJr)!=9: continue
                                if self.isInt(hpJr)==False: continue
                                item+=1
                            position=s.find("PTEC")
                            if position>-1:
                                positionFin=s[position:].find("\r")
                                ptec=s[position+5:position+positionFin-2]
                                item+=1
                            position=s.find("DEMAIN")
                            if position>-1:
                                positionFin=s[position:].find("\r")
                                demain=s[position+7:position+positionFin-2]
                                item+=1
                            position=s.find("IINST")
                            if position>-1:
                                positionFin=s[position:].find("\r")
                                iInst=s[position+6:position+positionFin-2]
                                if self.isInt(iInst)==False:continue
                                item+=1
                            if item>=11: break
                    except Exception, e3:
                        print "Erreur : %s" %e3
                    dongle.flush()
                    dongle.close()
        except Exception, e2:
            print "Erreur connexion teleconso: %s" % e2
        return noCompteur,tarif,hcJb,hpJb,hcJw,hpJw,hcJr,hpJr,ptec,demain,iInst


