# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
from connect_to_router import *

# webrepl stuff
webrepl.start()
gc.collect()

# connect to router, config has fields ssid and password, optional: static_ip
do_connect("./config_wifi.json")
