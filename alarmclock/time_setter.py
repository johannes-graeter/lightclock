import ntptime
import machine
import utime as time
from alarmclock.with_config import WithConfig
import gc


class TimeSetter(WithConfig):
    """class to reset time
       Args:
           utc_delay: delay in hours form utc timezone
        Attributes:
            verbose (bool): activate verbose output
            utc_delay (int): time delay from utc (for Berlin: +1)
    """

    def __init__(self, config):
        # init config setter
        config_attributes = [
            'verbose',
            'utc_delay'
        ]
        super(TimeSetter, self).__init__(config_attributes, config)

    def process(self, timeout):
        is_time_set = False
        start_time = time.ticks_ms()

        while not is_time_set and time.ticks_diff(time.ticks_ms(), start_time) < timeout:
            try:
                ntptime.settime()
                if self.config['verbose']['value']:
                    print("ntptime was set")
                is_time_set = True
            except:
                time.sleep(1)
                if self.config['verbose']['value']:
                    print(".", end="")
                continue

            tm = time.localtime()
            # add delay
            tm_sec = time.mktime(
                (tm[0], tm[1], tm[2], tm[3] + self.config['utc_delay']['value'], tm[4], tm[5], tm[6], tm[7]))
            tm = time.localtime(tm_sec)
            # convert to format for rtc
            tm = tm[0:3] + (0,) + tm[3:6] + (0,)
            # set real time clock on controller
            machine.RTC().datetime(tm)

        gc.collect()
