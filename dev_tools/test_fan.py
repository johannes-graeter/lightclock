from machine import Pin
import utime as time


pathToConfigs = "./config.json"

config_file = open(pathToConfigs, "r")
config = json.load(config_file)
config_file.close()


pin = Pin(config['fan_pin']['value'], Pin.OUT)

while True:
    pin.on()
    time.sleep(1)
    pin.off()
    time.sleep(1)
