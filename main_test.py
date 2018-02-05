import json

from alarmclock import alarm as a
from dev_tools import clock_actions
import time


def main():
    # this main is for testing on a normal ubuntu system
    # hard coded defines
    pathToConfigs = "./config.json"

    # get current time from wifi
    config = json.load(open(pathToConfigs, "r"))

    # create instance of sunrise which will be launched by alarm at the correct time
    # read maximum intensity

    s = clock_actions.StringPrinter("rise sun!", config)

    # set alarm
    alarm = a.Alarm(s, config)

    while True:
        alarm.spin_once()
        time.sleep(1.)
    print("done")


if __name__ == '__main__':
    main()
