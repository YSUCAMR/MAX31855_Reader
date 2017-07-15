#!/usr/bin/python

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import time


import datetime as dt
import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855
import re as re


# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0

# Uncomment one of the blocks of code below to configure your Pi or BBB to use
# software or hardware SPI.

# Raspberry Pi software SPI configuration.
#CLK = 
#CS  = 
#DO  = 
#sensor = MAX31855.MAX31855(CLK, CS, DO)

# Raspberry Pi hardware SPI configuration.
SPI_PORT   = 0
SPI_DEVICE = 1
sensor = MAX31855.MAX31855(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

##Create file with name ---.txt

with open("/home/pi/Programs/project2b/py_thermocouple/test.txt","r+") as mydata:
        read = mydata.readlines()
        a = str(read)


b = re.match('Time', a)

if b is None:
        
        mydata.write('Time \t Thermocouple Temp (*C \t *F) \t Internal Temperatur\e ( *C \t *F)\n')
        
else:
        mydata.write('\n',file)

mydata.close()

with open("/home/pi/Programs/project2b/py_thermocouple/test.txt","a") as data:

# Loop printing measurements every second.

        while True:

                temp = sensor.readTempC()
                internal = sensor.readInternalC()
                clock = str(dt.datetime.now())

                thermotemp_C = '{0:0.3F}'.format(temp,c_to_f(temp))
                thermotemp_F = '{1:0.3F}'.format(temp,c_to_f(temp))
           
                intertemp_C = '{0:0.3F}'.format(internal, c_to_f(internal))
                intertemp_F = '{1:0.3F}'.format(temp, c_to_f(internal))
                data.write( '{0} \t {1} \t {3} \t {4}'.format(clock,float(thermotemp_C),float(thermotemp_F),float(intertemp_C),float(intertemp_F)))
        


                time.sleep(0.5)


