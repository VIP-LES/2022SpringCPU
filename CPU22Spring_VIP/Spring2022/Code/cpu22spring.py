import time
import board
import busio
import adafruit_ms8607
from adafruit_ms8607 import MS8607
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ltr390
import adafruit_tsl2591
import RPi.GPIO as GPIO

# LED status sensor
led_pin = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

# initialize i2c
i2c = board.I2C()
ms = MS8607(i2c)                    # pressure temperature humidity (MS8607)
ltr = adafruit_ltr390.LTR390(i2c)   # ambient light/lux/uv (LTR390)
tsl = adafruit_tsl2591.TSL2591(i2c) # visible light/infrared

# initialize analog
i2cBusio = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2cBusio)
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

ads2 = ADS.ADS1015(i2cBusio, address=0x49)
chan4 = AnalogIn(ads2, ADS.P0)

# initialize time
initialTime = time.time()


try:
    while True:
        f = open('//home/pi/Spring 2022 Data/CPUSpring2022Data.csv', 'a')        

        GPIO.output(led_pin, GPIO.HIGH)  # turn on LED
        elapsedTime = time.time() - initialTime  # calculate time from launch
        
        string = "Time: {time: <10.5f} Pressure: {pressure: <10.5f} Temperature: {temp: <10.5f}  Humidity: {humidity: <10.5f}"  \
                    "UV: {uv: <10.5f}  UVI: {uvi: <10.5f}  Ambient Light: {light: <10.5f}  Lux: {lux: <10.5f} Infrared Light: {infrared: <10.5f}" \
                    "Visible Light: {visible: <15.5f} Full Spectrum (IR + vis): {spectrum: <15.5f} CO2: {co2: <10.5f} UVB: {uvb: <10.5f}" \
                    "O3 Gas: {o3g: <10.5f} O3 Reference: {o3r: <10.5f} O3 Temperature: {o3t: <10.5f} \n"
        f.write(string.format(time = elapsedTime, pressure = ms.pressure, temp = ms.temperature, humidity = ms.relative_humidity,
                              uv = ltr.uvs, uvi = ltr.uvi, light = ltr.light, lux = ltr.lux, infrared = tsl.infrared,
                              visible = tsl.visible, spectrum = tsl.full_spectrum, co2 = chan0.voltage, uvb = chan1.voltage,
                              o3g = chan2.voltage, o3r = chan3.voltage, o3t = chan4.voltage))

        f.close()

        time.sleep(.2)

        GPIO.output(led_pin, GPIO.LOW)   # turn off LED
        time.sleep(.2)

finally:
    GPIO.cleanup()
        





