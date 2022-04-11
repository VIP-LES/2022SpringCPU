# SPDX-FileCopyrightText: 2021 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
import adafruit_ltr390

f = open('//home/pi/Desktop/spring 22/ltr390test/data/ltr390.csv', 'w')

i2c = board.I2C()
ltr = adafruit_ltr390.LTR390(i2c)


count = 0
while (count < 15):
    time.sleep(0.5)
    print("UV:", ltr.uvs, "\t\tAmbient Light:", ltr.light)
    print("UVI:", ltr.uvi, "\t\tLux:", ltr.lux)
    f.write(str(time.ctime()) + "\tUV: " + str(ltr.uvs) + "\tUVI: " + str(ltr.uvi) + "\tAmbient Light: " + str(ltr.light) + "\tLux: " + str(ltr.lux) + "\n")    
    count += 1
    
f.close()