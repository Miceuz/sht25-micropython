# This program is distributed under Apache License Version 2.0
#
# (ɔ) Albertas Mickėnas 2016
# mic@wemakethings.net
# albertas@technariumas.lt
#

import time
from machine import I2C, SPI, Pin
from sht25 import SHT25
from ssd1306 import SSD1306_SPI
import network
from umqtt.simple import MQTTClient

sensor = SHT25(I2C(scl=Pin(5), sda=Pin(4)))
display = SSD1306_SPI(128, 32, SPI(1), Pin(0), Pin(2), Pin(15))


def displayData(temperature, humidity):
	global display
	display.fill(0)
	display.text("Humidity", 0, 0)
	display.text("Temp", 70, 0)
	display.text(str(round(humidity, 2))[0:5] + "%", 8, 12)
	display.text(str(round(temperature, 2))[0:5] + "C", 70, 12)
	display.show()

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

display.fill(0);
display.text("Connecting...", 0, 0)
display.show()
print("Connecting...")

sta_if.connect('TECHNARIUM', '')
while not sta_if.isconnected():
	pass

# try:
c = MQTTClient('myMqttClient', 'mqtt.thingspeak.com', 1883)  # uses unsecure TCP connection
c.connect()
# except:
	# print("Not connected, running offline") 


thingspeakChannelId = '358189'
thingspeakChannelWriteapi = ''
credentials = "channels/{:s}/publish/{:s}".format(thingspeakChannelId, thingspeakChannelWriteapi)  

while True:
	temperature = sensor.getTemperature()
	humidity = sensor.getHumidity()

	print(str(temperature) + ", " + str(humidity))
	displayData(temperature, humidity)
	payload = "field1={:.1f}&field2={:.1f}\n".format(temperature, humidity)
	c.publish(credentials, payload)
	time.sleep(1)