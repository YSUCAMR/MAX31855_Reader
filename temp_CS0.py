#!/usr/bin/python

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import time
import re
import datetime as dt
import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855
import numpy as np
from datetimestats import mean

# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0

# Raspberry Pi hardware SPI configuration.
SPI_PORT   = 0
SPI_DEVICE = 0
sensor = MAX31855.MAX31855(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


 ##Delete existing and create new file **WARNING LOSS OF DATA**
#infile = open("/home/pi/evan/programs/pythermocouple/pi3n6/cs0data.txt","w+")

 ##Append data to this file **DOES NOT LOSE EXISTING DATA**
infile = open("/home/pi/evan/programs/pythermocouple/pi3n6/cs0data.txt","a")

 ##Loop printing measurements and storing data.        
        
i = 0
alldata = np.zeros((3,4))# Empty array 10 data points in one tenth of a second
alldata[:] = np.NAN
times = []
timeout = time.time() +3600*2.5 #60*10   # 4 hours from now --> time to take less datapoints

while time.time() < timeout:

        temp = sensor.readTempC()
        internal = sensor.readInternalC()
        now = dt.datetime.now()
        
        thermotemp_C = '{0:0.3F}'.format(temp)
        thermotemp_F = '{0:0.3F}'.format(c_to_f(temp))
        
        intertemp_C = '{0:0.3F}'.format(internal)
        intertemp_F = '{0:0.3F}'.format(c_to_f(internal))

        if i < 3:

                
                alldata[i, 0] = thermotemp_C
                alldata[i, 1] = thermotemp_F 
                alldata[i, 2] = intertemp_C
                alldata[i, 3] = intertemp_F
                times.append(now)
                i += 1
                
        else:
                
                i = 0
                average = mean(times[:])
                a = '{0}\t{1}\t{2}\t{3}\t{4}\n'.format( average, np.nanmean(alldata[:,0]),np.nanmean(alldata[:,1]),
                                                      np.nanmean(alldata[:,2]),np.nanmean(alldata[:,3]))
                #print a
                times = []
                alldata = np.zeros((3,4))
                #alldata[:] = np.NAN
                infile.write(a)
                
        time.sleep(.05)


i = 0
alldata = np.zeros((15,4)) ## Empty array for all data points in one second --> Data is now average of 100 points
alldata[:] = np.NAN


while True:

        temp = sensor.readTempC()
        internal = sensor.readInternalC()
        now = dt.datetime.now()

        thermotemp_C = '{0:0.3F}'.format(temp)
        thermotemp_F = '{0:0.3F}'.format(c_to_f(temp))

        intertemp_C = '{0:0.3F}'.format(internal)
        intertemp_F = '{0:0.3F}'.format(c_to_f(internal))

        if i < 15:

                
                alldata[i, 0] = thermotemp_C
                alldata[i, 1] = thermotemp_F
                alldata[i, 2] = intertemp_C
                alldata[i, 3] = intertemp_F
                times.append(now)
                i += 1

        else:

                i = 0
                time.sleep(0.85)
                average = mean(times[:])
                a = '{0}\t{1}\t{2}\t{3}\t{4}\n'.format( average, np.nanmean(alldata[:,0]),np.nanmean(alldata[:,1]),
                                                        np.nanmean(alldata[:,2]),np.nanmean(alldata[:,3]))
                #print a
                times = []
                alldata = np.zeros((100,4))
                alldata[:] = np.NAN
                infile.write(a)

        time.sleep(0.05)
