import json

from alarm import Alarm
from clock_actions import *


def main():
    # this main is for testing on a normal ubuntu system

    # hard coded defines
    pathToConfigs = "./config.json"

    # get current time from wifi

    # get configs
    maxIntensity = 100
    sleepTimeSec = 60.

    config = {}
    try:
        config = json.load(open(pathToConfigs, "r"))
    except:
        print("blink onboard LED")

    try:
        maxIntensity = config["max_intensity_percent"]
        sleepTimeSec = config["alarm_sleep_time_sec"]
    except:
        print("blink twice")

    print("maxIntensityPercent " + str(maxIntensity))
    print("sleepTimeSec " + str(sleepTimeSec))

    # create instance of sunrise which will be launched by alarm at the correct time
    # read maximum intensity

    s = StringPrinter("rise sun!")

    # set alarm
    alarm = Alarm(s)
    alarm.set_sleep_time_spinning_sec(sleepTimeSec)

    alarm.spin()


if __name__ == '__main__':
    main()
