import ujson as json
import machine
import utime as time


pathToConfigs = "./config.json"

config_file = open(pathToConfigs, "r")
config = json.load(config_file)
config_file.close()


led = machine.PWM(machine.Pin(config['led_pin']['value'], machine.Pin.OUT), freq=20000)

while True:
    led.duty(256)
    time.sleep(1)
    led.duty(768)
    time.sleep(1)

