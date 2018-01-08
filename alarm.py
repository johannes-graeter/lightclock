try:
    import utime as time
    import gc
except:
    import time

from with_config import WithConfig


# try:
#     import machine
# except:
#     pass

class Alarm(WithConfig):
    """class that triggers an action at a given time

        Args:
            action(custom obj with a function process() defined): action that will be performed when the alarm goes off
            time setter(custom obj with a function process() defined): set current system time
        Attributes:
            action (...): action that will be performed when the alarm goes off
            wakingTime (tuple): hour, minutes and seconds of the time to wake up
            sleepTimeSec (int): time in seconds to sleep after each loop while spinning
            actionPreponeTimeMin (int): time in minutes before wakingTime at which action will be triggered
            filename (str): path to file where the alarmtime is saved in the format "%02i:%02i:%02f"%(hour,minutes,seconds)
            timeSetter (...): object with function process, that sets ntp time on machine
    """

    def __init__(self, action, timeSetter):
        # init config setter
        func_mapping = {
            'alarm_sleep_time_sec': self.set_sleep_time_spinning_sec,
            'verbose': self.set_verbosity
        }
        super(Alarm, self).__init__(func_mapping)

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

        # print next waking time to cout
        self.verbose = False

        # object that sets ntptime on controller
        self.timeSetter = timeSetter

        # set the ntp time
        self.timeSetter.process()

    def set_verbosity(self, verbose):
        self.verbose = verbose
        print("set verbosity to ", self.verbose)

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

    def get_expected_time(self, tm):
        """ get time that was read from file corresponding to current year including prepone time"""
        # get expected start time
        try:
            expectedTime = time.mktime((tm[0], tm[1], tm[2], self.wakingTime[0],
                                        self.wakingTime[1] - self.actionPreponeTimeMin, 0, tm[6], tm[7]))
        except:
            expectedTime = time.mktime((tm[0], tm[1], tm[2], self.wakingTime[0],
                                        self.wakingTime[1] - self.actionPreponeTimeMin, 0, tm[6], tm[7], 0))
        if self.verbose:
            print("waking at ", end="")
            print(time.localtime(expectedTime), end=" ")
            print("current time is ", end="")
            print(tm)

        return expectedTime

    def start(self):
        """test if current time is waking time - preponeTime"""
        # get current time
        tm = time.localtime()

        # convert time to seconds, if the time diff is between negative threshold and zero start
        timeDiffSec = self.get_expected_time(tm) - time.mktime(tm)

        return -300. <= timeDiffSec <= 0.

    def spin(self):
        """drop in infinite loop to spin alarm"""
        count = 0
        while True:
            self.spin_once(count == 10)
            gc.collect()
            print("free=", gc.mem_free())
            count += 1

    def spin_once(self, setNtpTime=False):
        # read alarmtime, is saved on class
        self.read_alarmtime()

        # get start time corresponding to alarmtime
        startTime = self.get_expected_time(time.localtime())
        # current time diff
        dt = time.time() - startTime

        # if the time difference is smaller sunrise time, this means we should adjust the light corresponding to dt
        # otherwise we sleep and get ntp time
        if 0. < dt < self.action.sunriseTimeSec:
            self.action.process_once(dt)
        else:
            time.sleep(self.sleepTimeSec)
            # set ntptime
            if setNtpTime:
                self.timeSetter.process()
