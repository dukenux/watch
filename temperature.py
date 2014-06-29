#!/usr/bin/python
# -*- coding: utf8 -*-
import time
import os
import smbus
import sys

class temperature():

    def __init__(self):
	self.bus=smbus.SMBus(2)

    def getTemp(self):
        try:
              temp=self.bus.read_word_data(72,0)
        except Exception as ex5:
              try:
                   temp=self.bus.read_word_data(73,0)
              except Exception as ex6:
                   try:
                       temp=self.bus.read_word_data(74,0)
                   except Exception as ex7:
                       try:
                            temp=self.bus.read_word_data(75,0)
                       except Exception as ex27: 
                            return 99
#swap MSB and LSB
        msb=(temp&0xFF)<<8
        lsb=(temp>>8)&0xF0
# keep only the 12 most significant bits
        hextemp=(msb+lsb)>>4
# special case for negative temperature
# compute the twos complement
        neg=False
        if (hextemp&0x0800==0x0800):
            hextemp=(~hextemp)&0xFFF
            hextemp+=1
            neg=True
        tempdec=hextemp*0.0625
        if neg:
            tempdec*=-1
        return tempdec


