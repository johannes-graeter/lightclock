import gc
import machine
import network
import ujson as json
import utime as time

gc.collect()
print('loading alarm clock, free memory = ', gc.mem_free())

from alarmclock import alarm as a
from alarmclock import clock_actions_micropython as ca
from alarmclock import time_setter as ts
from alarmclock.fan import Fan
from alarmclock.temperature_sensor import TemperatureLogger, TemperatureWatcher

gc.collect()
print('loading webapp, free memory = ', gc.mem_free())

import webapp

gc.collect()
print('setup configs, free memory = ', gc.mem_free())


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
    config_file = open(pathToConfigs, "r")
    config = json.load(config_file)
    config_file.close()
except:
    print("couldn't read config " + pathToConfigs)
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
s = ca.SunriseExp(config)
s.set_exp_vars(5., 3.5)
actions = [s]

# time zone manager
timeSetter = ts.TimeSetter(config)

# fan manager
fan = None
try:
    fan = Fan(config)
    fan.pre_action()
    actions.append(fan)
except:
    print("No Fan loaded!")

# temperature sensor
temp_sensor = None
try:
    temp_sensor = TemperatureLogger(config)
    actions.append(temp_sensor)
except:
    print("No TemperatureLogger loaded!")

# temperature watcher
temp_watcher = None
try:
    temp_watcher = TemperatureWatcher(config, s, fan)
    actions.append(temp_watcher)
except:
    print("No TemperatureWatcher loaded!")


# set alarm
alarm = a.Alarm(actions, config)

# don't prepone for debugging
alarm.set_action_prepone_time_min(0.)

gc.collect()
print('set ntp-time, free memory = ', gc.mem_free())

# set ntp-time
timeSetter.process(5000)

def spin_and_collect(timer):
    alarm.spin_once()
    gc.collect()

gc.collect()
print('create interrupts, free memory = ', gc.mem_free())


try:
    timers = [machine.Timer(0), machine.Timer(1)]
    timers[0].init(period=config['period_alarm_ms']['value'], mode=machine.Timer.PERIODIC, callback=spin_and_collect)

    # set ntptime
    timers[1].init(period=config['period_get_ntp_time_ms']['value'], mode=machine.Timer.PERIODIC,
                   callback=lambda t: timeSetter.process(100))


    gc.collect()

    sta_if = network.WLAN(network.STA_IF)

    if sta_if.isconnected():
        if 'offline_mode' in config.keys():
            del config['offline_mode']
        app = webapp.WebApp(host=sta_if.ifconfig()[0], config=config, debug=config["verbose"]["value"])
    else:
        # TODO add possibility to set the time in the webapp
        ap_if = network.WLAN(network.AP_IF)
        while not ap_if.isconnected():
            print("Not connected to the router, waiting for device connecting to access point")
            time.sleep(1)

        config['offline_mode'] = {'value': True}
        app = webapp.WebApp(host=ap_if.ifconfig()[0], config=config, debug=config["verbose"]["value"])

    gc.collect()
    print('run webapp, free memory = ', gc.mem_free())

    app.run()
except KeyboardInterrupt:
    print("ctrl+c pressed, quitting")
    for tim in timers:
        tim.deinit()

    if sta_if:
        sta_if.active(False)

    if fan:
        fan.post_action()
