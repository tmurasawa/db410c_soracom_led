#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from gpio_96boards import GPIO
import paho.mqtt.client as mqtt

GPIO_A = GPIO.gpio_id('GPIO_A')
pins = (
    (GPIO_A, 'out'),
)

def on_connect(client, userdata, rc):
  print("Connected with result code " + str(rc))
  client.subscribe("16755F158AC56C21BBEDB8E019A4517E/440103072674825/subscribe")

def on_disconnect(client, userdata, rc):
  if rc != 0:
     print("Unexpected disconnection.")

def on_publish(client, userdata, mid):
  print("publish: {0}".format(mid))

def on_message(client, userdata, msg):
  print(msg.topic + ' ' + str(msg.payload))
  if msg.payload == "led:on":
    print "led:on!!"
    with GPIO(pins) as gpio:
      led_on(gpio)

  if msg.payload == "led:off":
    print "led:off!!"
    with GPIO(pins) as gpio:
      led_off(gpio)


def led_on(gpio):
        gpio.digital_write(GPIO_A, GPIO.HIGH)

def led_off(gpio):
        gpio.digital_write(GPIO_A, GPIO.LOW)


print "- Init.."


import json
import requests

#device_token=requests.get('http://metadata.soracom.io/v1/userdata').text
#print device_token

if __name__ == '__main__':

 client = mqtt.Client()
 client.on_connect = on_connect
 client.on_disconnect = on_disconnect
 client.on_publish = on_publish
 client.on_message = on_message

 client.username_pw_set("SC000014","16755F158AC56C21BBEDB8E019A4517E")
 #client.connect("beam.soracom.io", 1883, 10)
 client.connect("api.scalenics.io", 1883, 10)
 client.loop_forever()





