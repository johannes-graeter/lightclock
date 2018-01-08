import json

from alarm import Alarm
from clock_actions import *


class TimeSetterDummy:
    def __init__(self):
        pass

    def process(self):
        print("TimeSetterDummy::process called")


def main():
    # this main is for testing on a normal ubuntu system

    # hard coded defines
    pathToConfigs = "./config.json"

    # get current time from wifi
    config = json.load(open(pathToConfigs, "r"))

    # create instance of sunrise which will be launched by alarm at the correct time
    # read maximum intensity

    s = StringPrinter("rise sun!", config)

    # set alarm
    alarm = Alarm(s, TimeSetterDummy(), config)

    alarm.spin()

    print("done")


if __name__ == '__main__':
    main()
