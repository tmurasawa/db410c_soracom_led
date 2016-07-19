#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from gpio_96boards import GPIO
import paho.mqtt.client as mqtt
	
# GPIO_A is D_A on Mezzanine
GPIO_A = GPIO.gpio_id('GPIO_A')
pins = (
    (GPIO_A, 'out'),
)

def on_connect(client, userdata, rc):
  print("Connected with result code " + str(rc))
	#if you use Scalenics WITHOUT SORACOM,comment out below..
  #client.subscribe("<DEVICE_TOKEN>/<DEVICE_ID>/subscribe")
	#if you use Scalenics WITH SORACOM,comment out below..
  client.subscribe(topic)

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


print "-- Get metadata from SORACOM..."


import json
import requests

metadata=requests.get('http://metadata.soracom.io/v1/subscriber').json()
#print metadata
imsi=metadata["imsi"]
print "imsi:%s" %imsi

device_token=requests.get('http://metadata.soracom.io/v1/userdata').text
print "device_token:%s" %device_token

topic = device_token + "/" + imsi + "/subscribe"
print "MQTT topic:%s" %topic

if __name__ == '__main__':

 client = mqtt.Client()
 client.on_connect = on_connect
 client.on_disconnect = on_disconnect
 client.on_publish = on_publish
 client.on_message = on_message

 ## if you use Scalenics WITHOUT SORACOM,comment out below..
 #client.username_pw_set("<SCALENICS_ID>","<DEVICE_TOKEN>")
 #client.connect("api.scalenics.io", 1883, 10)
 ## if you use Scalenics WITH SORACOM,comment out below..
 client.connect("beam.soracom.io", 1883, 10)
 client.loop_forever()





