import json

from alarm import Alarm
from clock_actions import *

def main():
    # this main is for testing on a normal ubuntu system

    # hard coded defines
    pathToConfigs = "./config.json"

    # get current time from wifi

    # get configs
    maxIntensity = 255
    sleepTimeSec = 60.

    config = {}
    try:
        config = json.load(open(pathToConfigs, "r"))
    except:
        print("blink onboard LED")

    try:
        maxIntensity = config["max_intensity"]
        sleepTimeSec = config["sleep_time_sec"]
    except:
        print("blink twice")

    print("maxIntensity "+str(maxIntensity))
    print("sleepTimeSec "+str(sleepTimeSec))

    # create instance of sunrise which will be launched by alarm at the correct time
    # read maximum intensity

    s = StringPrinter("rise sun!")
    # Sunrise s(maxIntensity)

    # set alarm
    alarm = Alarm(s)
    alarm.set_sleep_time_spinning_sec(sleepTimeSec)

    alarm.spin()


if __name__ == '__main__':
    main()
