import math
from alarmclock.with_config import WithConfig

try:
    import machine
    import utime as time
except:
    print("using ubuntu testing version")


class Sunrise(WithConfig):
    """interface class to do a sunrise with specified intensity profile
        Args:

        Attributes:
            intensityProfile (functor): Defines an intensity to a given point in time
                                        This can be overloaded and thus used in a strategy pattern.
            maxIntensityPercent (int): maximum intensity of the light in percent, maximum value is 100
            sunriseTimeSec (float): total time sunrise lasts in seconds
            ledNum (int): number of the pin which controls the led, notice needs to be bound to ground, so when oin is low LED is on(as for Pin 0 on HUZZAH ESP8266 FEATHER)
            delayMs (float): delay in milliseconds after each intensity modification
    """

    def __init__(self, config):
        # init config setter
        config_attributes = [
            'max_intensity_percent',
            'sunrise_time_sec',
            'led_pin'
        ]
        super(Sunrise, self).__init__(config_attributes, config)

        # default profile is linear
        self.intensityProfile = lambda x: 50 + x / float(self.config['sunrise_time_sec']['value']) * 205

        # led delay in millisec
        self.delayMs = 1

    def get_max_intensity_percent(self):
        return min(float(self.config['max_intensity_percent']['value']), 100)

    def set_intensity_profile(self, func):
        """setter for the intensity profile function
            you can use this in a strategy pattern-like manner or just overload the profile such as in SunriseExp to make interface easier
        """
        self.intensityProfile = func

    def pre_action(self, dt):
        led = machine.PWM(machine.Pin(self.config['led_pin']['value'], machine.Pin.OUT), freq=20000)
        led.duty(0)

    def main_action(self, dt):
        # print("start sunrise")
        # select led
        led = machine.PWM(machine.Pin(self.config['led_pin']['value'], machine.Pin.OUT), freq=20000)

        # intensity from profile ->strategy pattern
        intensity = int(self.intensityProfile(dt))
        # get valid range of intensity
        intensity = max(intensity, 0)
        intensity = min(intensity, self.get_max_intensity_percent())

        # set intensity with bandwidth modulation pulsing, max duty val is 1023, led for pin 0 is on when pin.value()==0
        led.duty(int(intensity * 1023 / 100))

    def post_action(self, dt):
        led = machine.PWM(machine.Pin(self.config['led_pin']['value'], machine.Pin.OUT), freq=20000)
        led.duty(0)

class SunriseExp(Sunrise):
    """overload intensity Profile
        Args:
            same as Sunrise
        Attributes:
            multiplier (float): multiplier for exponential func
            dt (float): time delay in sec for exponential func
    """

    def __init__(self, config):
        # call parent constructor
        super(SunriseExp, self).__init__(config)

        self.a = 100.
        self.b = 1.5
        self.c = self.a

        self.intensityProfile = lambda x: min(
            self.a * math.exp(self.b / float(self.config['sunrise_time_sec']['value']) * x) - self.c,
            self.get_max_intensity_percent())

    def set_exp_vars(self, a, b):
        self.a = a
        self.b = b
        self.c = self.a
