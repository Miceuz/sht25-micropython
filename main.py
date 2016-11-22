# This program is distributed under Apache License Version 2.0
#
# © Albertas Mickenas, 2016
# mic@wemakethings.net
# albertas@technariumas.lt
#

import time
from machine import I2C
from machine import Pin
from sht25 import SHT25

sensor = SHT25(I2C(scl=Pin(5), sda=Pin(4)))

while True:
	print(str(sensor.getTemperature()) + ", " + str(sensor.getHumidity()))
	time.sleep(1)