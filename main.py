import ujson as json

from alarm import Alarm
from clock_actions_micropython import *
import machine
import ntptime
import utime as time

def blink_led(pin_number):
    machine.Pin(pin_number, machine.Pin.OUT).low()
    time.sleep_ms(500)
    machine.Pin(pin_number, machine.Pin.OUT).high()
    time.sleep_ms(500)
    machine.Pin(pin_number, machine.Pin.OUT).low()
    time.sleep_ms(500)

def set_time(utcDelay):
    print("getting ntptime from the internet")
    is_time_set = False
    while not is_time_set:
        try:
            ntptime.settime()
            print("ntp time was set")
            is_time_set = True
        except:
            time.sleep(1)
            print(".", end="")
    tm = time.localtime()
    print("now its ", end="")
    print(tm)
    print("add " + str(utcDelay) + " hour delay to utc")
    # add delay
    tm_sec = time.mktime((tm[0], tm[1], tm[2], tm[3] + utcDelay, tm[4], tm[5], tm[6], tm[7]))
    tm = time.localtime(tm_sec)
    # convert to format for rtc
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    # set real time clock on controller
    machine.RTC().datetime(tm)
    print("current time: ", end="")
    print(time.localtime())

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

# set time from wifi
set_time(utcDelay)

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
machine.PWM(machine.Pin(0,machine.Pin.OUT),freq=20000).duty(1024)

ledNum = 0  # use pin without LED branched to
if "led_number" in config:
    ledNum=config["led_number"]

# create instance of sunrise which will be launched by alarm at the correct time
s = SunriseExp()
s.set_led_num(ledNum)
s.set_max_intensity_percent(maxIntensity)
s.set_sunrise_time(sunriseTimeSec)
s.set_exp_vars(100., 1.5)

# set alarm
alarm = Alarm(s)

if "verbose" in config:
    alarm.set_verbosity(config["verbose"])

alarm.set_sleep_time_spinning_sec(alarmSleepTimeSec)
# don't prepone for debugging
alarm.set_action_prepone_time_min(0.)

alarm.spin()
