from wifi_manager import WifiManager
from common import get_mqtt_cfg
from common import get_network_cfg
import time
from sensor_collect import collect
import machine
import ujson
import binascii
from umqtt.simple import MQTTClient
import network
from mqtt import mqtt_send_loop

wm = WifiManager()
if not wm.is_connected():
    wm.connect()
if wm.is_connected():
    print("Wifi is connected")

mqtt_send_loop()
    
# TESTING CONFIGURATION

print("---Complete---")

