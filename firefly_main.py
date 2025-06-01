#encoding:utf-8
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import random
from rpi_ws281x import Adafruit_NeoPixel, Color
import paho.mqtt.client as mqtt
import logging
#commit comment

# LED strip configuration:
LED_COUNT      = 32      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 10    # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# initialize queue for MQTT message arrival
q=Queue()

######################################################################################
###  startup MQTT message subscriber
######################################################################################

def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe("fireflypi/cmd/firefly_main",1)


def on_message(client, userdata, message):
    q.put(message)

#def on_log(client, userdata, paho_log_level, messages):
#    print("paho log: ",message)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"fireflypi")
client.username_pw_set("ha-user", "ha-pass")
broker_address="10.4.24.11"
client.connect_async(broker_address)   #asyn connection in case internet not avail.
client.on_connect = on_connect
client.on_message = on_message
client.enable_logger # enable logging
#client.on_log = on_log
client.loop_start()

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

# Intialize the library (must be called once before other functions).

#################################################################################
### Main Loop
#################################################################################


while True:

#short sleep to avoid high CPU
    time.sleep(0.1)

# check MQTT queue for new cmd messages and act upon them

    while not q.empty():
        logging.debug("MQTT message queue not empty")
        msg = q.get()
        if msg is None:
            continue
        topic = str(msg.topic)
        payload = str(msg.payload.decode("utf-8"))
        logging.debug("new MQTT message decoded")
        logging.debug(topic)
        logging.debug(payload)
        if topic == "fireflypi/cmd/firefly_main":
            if payload == "ON":
                client.publish("fireflypi/state/fireflypi_main","ON", qos=1, retain=True)
                master = 1
            else:
                client.publish("fireflypi/state/fireflypi_main","OFF",1,True)
                master = 0
        
	    
		if master == 1:
	    strip.begin()
	    strip.clear()

	    for i in range(0,strip.numPixels()//4-1):
	    	for y in range(0,strip.numPixels()//8):
			strip.setPixelColor(7+y*8-i, Color(255,255,0))
			strip.setPixelColor(y*8+i, Color(255,255,0))
	    strip.show()
            time.sleep(0.1)

#
	    #turn off
	    strip.clear();
	    strip.show();
	    time.sleep(5)



#random color
#	for x in range(0,5):
#		for i in range(0,strip.numPixels()):
#			strip.setPixelColor(i, Color(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))	
#			strip.show()
#		time.sleep(0.5)
