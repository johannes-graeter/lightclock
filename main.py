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

# time zone manager
timeSetter = ts.TimeSetter(config)

# fan manager
fanOn = Fan(config, Fan.ON)
fanOff = Fan(config, Fan.OFF)

# set alarm
# TODO set fanOff as postaction, when light shuts down again
if 'fan_pin' in config.keys():
    alarm = a.Alarm([s, fanOn], config, preactions=[fanOff])
else:
    alarm = a.Alarm([s], config)

# don't prepone for debugging
alarm.set_action_prepone_time_min(0.)

gc.collect()
print('set ntp-time, free memory = ', gc.mem_free())

# set ntp-time
timeSetter.process(1000)

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

    del fanOn, fanOff
