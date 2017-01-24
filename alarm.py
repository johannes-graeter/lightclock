try:
    import utime as time
except:
    import time


class Alarm:
    """class that triggers an action at a given time

        Args:
            action(custom obj with a function process() defined): action that will be performed when the alarm goes off

        Attributes:
            action (...): action that will be performed when the alarm goes off
            wakingTime (tuple): hour, minutes and seconds of the time to wake up
            sleepTimeSec (int): time in seconds to sleep after each loop while spinning
            actionPreponeTimeMin (int): time in minutes before wakingTime at which action will be triggered
            filename (str): path to file where the alarmtime is saved in the format "%02i:%02i:%02f"%(hour,minutes,seconds)
    """

    def __init__(self, action):
        # inputs
        # action to trigger
        self.action = action

        # defaults
        # waking time in hour, minute, second
        self.wakingTime = [13, 30, 00]

        # sleep time while spinning
        self.sleepTimeSec = 60.

        # time in minutes before action should start
        self.actionPreponeTimeMin = 30

        # path to file which shall be read
        self.filename = "./alarmtime.json"

    def set_action_prepone_time_min(self, timeMin):
        self.actionPreponeTimeMin = int(timeMin)

    def set_sleep_time_spinning_sec(self, sleepTimeSec):
        self.sleepTimeSec = sleepTimeSec

    def set_alarmtime_filename(self, filename):
        self.filename = filename

    def read_alarmtime(self):
        """read alarmtime from file"""
        f = open(self.filename, "r")
        a = f.readline()

        # split it and convert to int (first to float since seconds can be a float in datetime format)
        self.wakingTime = tuple([int(float(x)) for x in a.strip().split(":")])

    def start(self):
        """test if current time is waking time - preponeTime"""

        # get current time
        tm = time.localtime()

        # get expected start time
        expectedTime = time.mktime((tm[0], tm[1], tm[2], self.wakingTime[0],
                                    self.wakingTime[1] - self.actionPreponeTimeMin, tm[5], tm[6], tm[7]))
        # print("waking at ", end="")
        # print(time.localtime(expectedTime))

        # convert time to seconds, if the time diff is between negative threshold and zero start
        timeDiffSec = expectedTime - time.mktime(tm)

        return -3. * self.sleepTimeSec <= timeDiffSec <= 0.

    def spin(self):
        """drop in infinite loop to spin alarm"""
        while True:
            self.read_alarmtime()

            if self.start():
                self.action.process()

            time.sleep(self.sleepTimeSec)
