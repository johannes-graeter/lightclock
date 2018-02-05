import gc
import machine
import network
import ujson as json
import utime as time

gc.collect()
print('loading alarm clock, free memory = ', gc.mem_free())

from alarm import Alarm
from clock_actions_micropython import *
from time_setter import TimeSetter

gc.collect()
print('loading webapp, free memory = ', gc.mem_free())


def blink_led(pin_number):
    machine.Pin(pin_number, machine.Pin.OUT).on()
    time.sleep_ms(500)
    machine.Pin(pin_number, machine.Pin.OUT).off()
    time.sleep_ms(500)
    machine.Pin(pin_number, machine.Pin.OUT).on()
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
time.sleep_ms(1000)

# turn off the led (why doesn't simply putting low() suffice?
machine.PWM(machine.Pin(0, machine.Pin.OUT), freq=20000).duty(1024)

# create instance of sunrise which will be launched by alarm at the correct time
s = SunriseExp(config)
s.set_exp_vars(5., 3.5)

# time zone manager
timeSetter = TimeSetter(config)

# set alarm
alarm = Alarm(s, config)

# don't prepone for debugging
alarm.set_action_prepone_time_min(0.)

gc.collect()
print('free memory = ', gc.mem_free())

# set ntp-time
timeSetter.process()

tim = machine.Timer(-1)


def spin_and_collect(timer):
    alarm.spin_once()
    gc.collect()

tim.init(period=config['period_alarm_ms']['value'], mode=machine.Timer.PERIODIC, callback=spin_and_collect)

# set ntptime
tim.init(period=config['period_get_ntp_time_ms']['value'], mode=machine.Timer.PERIODIC,
         callback=lambda t: timeSetter.process())

while True:
    pass
