try:
    import utime as time
    import gc
except:
    import time

from alarmclock.with_config import WithConfig


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
    """

    def __init__(self, action, config):
        # init config setter
        config_attributes = [
            'alarmtime',
            'sunrise_time_sec',
            'verbose'
        ]
        super(Alarm, self).__init__(config_attributes, config)

        # inputs
        # action to trigger
        self.action = action

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

    def get_alarmtime(self):
        """convert alarmtime (format hh:mm:ss, ss optional) into tuple of ints"""
        # split it and convert to int (first to float since seconds can be a float in datetime format)
        return tuple([int(float(x)) for x in self.config['alarmtime']['value'].strip().split(":")])

    def get_expected_time(self, tm):
        """ get time that was read from file corresponding to current year including prepone time"""
        # get expected start time
        wakingTime = self.get_alarmtime()
        try:
            expectedTime = time.mktime((tm[0], tm[1], tm[2], wakingTime[0],
                                        wakingTime[1] - self.actionPreponeTimeMin, 0, tm[6], tm[7]))
        except:
            expectedTime = time.mktime((tm[0], tm[1], tm[2], wakingTime[0],
                                        wakingTime[1] - self.actionPreponeTimeMin, 0, tm[6], tm[7], 0))
        if self.config['verbose']['value']:
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

    def spin_once(self):
        # get start time corresponding to alarmtime
        startTime = self.get_expected_time(time.localtime())
        # current time diff
        dt = time.time() - startTime

        # if the time difference is smaller sunrise time, this means we should adjust the light corresponding to dt
        # otherwise we sleep and get ntp time
        if 0. < dt < float(self.config['sunrise_time_sec']['value']):
            self.action.process_once(dt)
