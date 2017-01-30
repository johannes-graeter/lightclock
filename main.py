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

# get configs
maxIntensity = 100
sunriseTimeSec = 30. * 60.
alarmSleepTimeSec = 1.0
utcDelay = 0

config = {}
try:
    config = json.load(open(pathToConfigs, "r"))
except:
    print("couldn't read config"+pathToConfigs)
    blink_led(0)
    time.sleep(500)
    blink_led(0)
    time.sleep(500)

try:
    maxIntensity = config["max_intensity_percent"]
    alarmSleepTimeSec = config["alarm_sleep_time_sec"]
    sunriseTimeSec = config["sunrise_time_sec"]
    utcDelay = config["utc_delay"]
except:
    print("not enough configs specified")
    blink_led(2)
    time.sleep(500)
    blink_led(2)
    time.sleep(500)
    blink_led(2)

# ledNum = 15 # use pin without LED branched to it

# do one sunrise to show you are there
s_startup = SunriseExp()
# try it on 0 pin because it has an led
s_startup.set_led_num(0)
s_startup.set_max_intensity_percent(maxIntensity)
s_startup.set_sunrise_time(10.)
s_startup.set_exp_vars(100., 1.5)
s_startup.process()
# print("end of sunrise")

# turn off the led (why doesn't simply putting low() suffice?
machine.PWM(machine.Pin(0,machine.Pin.OUT), freq=20000).duty(1024)

ledNum = 0  # use pin without LED branched to
if "led_number" in config:
    ledNum = config["led_number"]

# create instance of sunrise which will be launched by alarm at the correct time
s = SunriseExp()
s.set_led_num(ledNum)
s.set_max_intensity_percent(maxIntensity)
s.set_sunrise_time(sunriseTimeSec)
s.set_exp_vars(5., 3.5)

# set alarm
timeSetter = TimeSetter(utcDelay)
timeSetter.set_verbose(True)
alarm = Alarm(s, timeSetter)

if "verbose" in config:
    alarm.set_verbosity(config["verbose"])

alarm.set_sleep_time_spinning_sec(alarmSleepTimeSec)
# don't prepone for debugging
alarm.set_action_prepone_time_min(0.)

alarm.spin()
