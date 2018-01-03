import ujson as json

from alarm import Alarm
from clock_actions_micropython import *
import machine
import utime as time
from time_setter import TimeSetter


def blink_led(pin_number):
    machine.Pin(pin_number, machine.Pin.OUT).low()
    time.sleep_ms(500)
    machine.Pin(pin_number, machine.Pin.OUT).high()
    time.sleep_ms(500)
    machine.Pin(pin_number, machine.Pin.OUT).low()
    time.sleep_ms(500)


# hard coded defines
pathToConfigs = "./config.json"

# get config
config = {}
try:
    config = json.load(open(pathToConfigs, "r"))
except:
    print("couldn't read config" + pathToConfigs)
    blink_led(0)
    time.sleep(500)
    blink_led(0)
    time.sleep(500)

# turn on the led to show you are there
machine.PWM(machine.Pin(0, machine.Pin.OUT), freq=20000).duty(1)
# turn off the led (why doesn't simply putting low() suffice?
machine.PWM(machine.Pin(0, machine.Pin.OUT), freq=20000).duty(1024)

# create instance of sunrise which will be launched by alarm at the correct time
s = SunriseExp()
s.set_config(config)
s.set_exp_vars(5., 3.5)

# time zone manager
timeSetter = TimeSetter()
timeSetter.set_config(config)

# set alarm
alarm = Alarm(s, timeSetter)
alarm.set_config(config)

# don't prepone for debugging
alarm.set_action_prepone_time_min(0.)

alarm.spin()
