#!/usr/bin/env python
# -*- coding: utf8 -*-
import time
from presstemp import *
from temperature import *
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def updateTempPress(tInt,p,tExt):
    try:
        f=open('/run/shm/tempPress.txt','w+')
        f.write(str(tInt)+"\n")
        f.write(str(p)+"\n")
        f.write(str(tExt)+"\n")
        f.close()
    except Exception, e7:
        print "Erreur : %s" % e7
        try:
            f.close()
        except Exception, e40:
            print "Erreur : %s" % e40



plt.rcParams['toolbar'] = 'None'
mngr = plt.get_current_fig_manager()
mngr.window.wm_geometry("100x50+0+0")
mngr.window.title('Pression Temperature')
plt.ion() # set plot to animated
y1data = [1000] * 50
y2data = [20] * 50
y3data = [20] * 50
ax1=plt.subplot(211)
ax2=plt.subplot(212)

line1, = ax1.plot(y1data,label="pression")
ax1.set_ylim([985,1020])
handles1,labels1=ax1.get_legend_handles_labels()
ax1.legend(handles1[::-1],labels1[::-1],loc="upper left")
ax1.axes.get_xaxis().set_visible(False)
ax1.grid(color='#000000', linestyle='-', linewidth=0.5)
ax1.yaxis.tick_right()

line2, = ax2.plot(y2data,label="T int.")
line3, = ax2.plot(y3data,label="T ext.")
ax2.set_ylim([2,40])
handles2,labels2=ax2.get_legend_handles_labels()
ax2.legend(handles2[::-1],labels2[::-1],loc="upper left")
ax2.axes.get_xaxis().set_visible(False)
ax2.grid(color='#000000', linestyle='-', linewidth=0.5)
ax2.yaxis.tick_right()

timetext = ax1.text(1,1,str(datetime.now().hour)+":"+str(datetime.now().minute),transform=ax1.transAxes,size=12,color='red',weight='bold')

# start data collection
pt=presstemp()
t=temperature()
while True:
        timetext.set_text(str(datetime.now().hour)+":"+str(datetime.now().minute))
        data1=pt.getPressure()/100
        data2=pt.getTemperature()
        data3=t.getTemp()
        updateTempPress(data2,data1,data3)
        ymin = float(min(y1data))-5
        ymax = float(max(y1data))+5
        ax1.set_ylim([ymin,ymax])
        y1data.append(data1)
        del y1data[0]
        line1.set_ydata(y1data)  # update the data

        ymin = float(min(y3data))-5
        ymax = float(max(y3data))+5
        ax2.set_ylim([ymin,ymax])
        y2data.append(data2)
        y3data.append(data3)
        del y2data[0]
        del y3data[0]
        line2.set_ydata(y2data)  # update the data
        line3.set_ydata(y3data)  # update the data

        plt.draw() # update the plot
        time.sleep(120)

