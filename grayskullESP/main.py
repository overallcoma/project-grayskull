from wifi_manager import WifiManager
from mqtt import mqtt_send_loop

wm = WifiManager()
if not wm.is_connected():
    wm.connect()
if wm.is_connected():
    print("Wifi is connected")

mqtt_send_loop()

