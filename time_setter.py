import ntptime
import machine
import utime as time


class TimeSetter:
    """class to reset time
       Args:
           utc_delay: delay in hours form utc timezone
        Attributes:
            verbose (bool): activate verbose output
            utc_delay (int): time delay from utc (for Berlin: +1)
    """

    def __init__(self):
        self.utcDelay = 1
        self.verbose = False

    def set_config(self, config_file):
        """
        :param config_file: json file with config params
        :return:
        """
        func_mapping = {
            'verbose': self.set_verbose,
            'set_utc_delay': self.set_utc_delay
        }

        # apply functions that are both in config_file and func_mapping
        for param in config_file:
            if param['name'] in func_mapping:
                func_mapping[param['name']](param['value'])

    def set_utc_delay(self, utcDelay):
        self.utcDelay = utcDelay

    def set_verbose(self, verbose):
        self.verbose = verbose

    def process(self):
        if self.verbose:
            print("getting ntptime")
        is_time_set = False
        while not is_time_set:
            try:
                ntptime.settime()
                if self.verbose:
                    print("ntptime was set")
                is_time_set = True
            except:
                time.sleep(1)
                if self.verbose:
                    print(".", end="")

            tm = time.localtime()
            # add delay
            tm_sec = time.mktime((tm[0], tm[1], tm[2], tm[3] + self.utcDelay, tm[4], tm[5], tm[6], tm[7]))
            tm = time.localtime(tm_sec)
            # convert to format for rtc
            tm = tm[0:3] + (0,) + tm[3:6] + (0,)
            # set real time clock on controller
            machine.RTC().datetime(tm)
