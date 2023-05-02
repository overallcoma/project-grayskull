from wifi_manager import WifiManager
import time


time.sleep(3)

try:
    wm = WifiManager()
    wm.connect()
    
except Exception as e:
    print(e)