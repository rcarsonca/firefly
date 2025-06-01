# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import neopixel
import board
import digitalio
import paho.mqtt.client as mqtt
import logging
from queue import Queue


# intitialize master on/off to off
master = 0

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 32

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.3, auto_write=False, pixel_order=ORDER
)


#################################################################################################
### setup logging
#################################################################################################

logging.basicConfig(
#    level=logging.DEBUG,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

# Set up motion detection
# using input GPIO5 = pi pin 29

pir = digitalio.DigitalInOut(board.D5)
pir.direction = digitalio.Direction.INPUT

#   Yellow shades
#   255,255,[0-51-102-153-204]


# initialize queue for MQTT message arrival
q=Queue()

######################################################################################
###  startup MQTT message subscriber
######################################################################################

def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe("fireflypi/cmd/#",1)


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


# publish state as off
client.publish("fireflypi/state/fireflypi_main","OFF",1,True)

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
        if topic == "fireflypi/cmd/fireflypi_main":
            if payload == "ON":
                client.publish("fireflypi/state/fireflypi_main","ON", qos=1, retain=True)
                master = 1
            else:
                client.publish("fireflypi/state/fireflypi_main","OFF",1,True)
                master = 0
                pixels.fill((0, 0, 0))
                pixels.show()



    if master == 1:

        pir_value = pir.value
        if pir_value:
            #PIR detecting motion
            #repeat the blinking loop x times
            for x in range(0,4):

                pixels.fill((255, 255, 0))
                pixels.show()
                time.sleep(0.1)

                pixels.fill((80, 80, 0))
                pixels.show()
                time.sleep(0.1)

                pixels.fill((200, 200, 0))
                pixels.show()
                time.sleep(0.1)

                pixels.fill((20, 20, 0))
                pixels.show()
                time.sleep(0.1)

        else:
            #PIR not detecting motion
            pixels.fill((0, 0, 0))
            pixels.show()
            time.sleep(0.4)
