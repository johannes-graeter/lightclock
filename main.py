import ujson as json

from alarm import Alarm
from clock_actions_micropython import *

# hard coded defines
pathToConfigs = "./config.json"

# get current time from wifi

# get configs
maxIntensity = 255
alarmSleepTimeSec = 60.
sunriseTimeSec = 30. * 60.

config = {}
try:
    config = json.load(open(pathToConfigs, "r"))
except:
    print("blink onboard LED")

try:
    maxIntensity = config["max_intensity"]
    alarmSleepTimeSec = config["alarm_sleep_time_sec"]
    sunriseTimeSec = config["sunrise_time_sec"]
except:
    print("blink twice")

# create instance of sunrise which will be launched by alarm at the correct time
s = SunriseExp()
s.set_max_intensity(maxIntensity)
s.set_sunrise_time(sunriseTimeSec)
s.set_exp_vars(100., 1.5)

# set alarm
alarm = Alarm(s)
alarm.set_sleep_time_spinning_sec(alarmSleepTimeSec)

alarm.spin()
