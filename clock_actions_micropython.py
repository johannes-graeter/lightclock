import math

try:
    import pyb
    import utime as time
except:
    print("using ubuntu testing version")


class Sunrise(object):
    """interface class to do a sunrise with specified intensity profile
        Args:

        Attributes:
            intensityProfile (functor): Defines an intensity to a given point in time
                                        This can be overloaded and thus used in a strategy pattern.
            maxIntensity (int): maximum intensity of the light, maximum value is 255
            sunriseTimeSec (float): total time sunrise lasts in seconds
            ledNum (int): number of the pin which controls the led
            delayMs (float): delay in milliseconds after each intensity modification
    """

    def __init__(self):
        # max intensity
        self.maxIntensity = 255

        # rise time
        self.sunriseTimeSec = 60. * 30.

        # default profile is linear
        self.intensityProfile = lambda x: 50 + x / self.sunriseTimeSec * 205

        # GPIO number of led
        self.ledNum = 0

        # led delay in millisec
        self.delayMs = 25

    def set_max_intensity(self, maxIntensity):
        self.maxIntensity = min(int(maxIntensity), 255)

    def set_intensity_profile(self, func):
        """setter for the intensity profile function
            you can use this in a strategy pattern-like manner or just overload the profile such as in SunriseExp to make interface easier
        """
        self.intensityProfile = func

    def set_sunrise_time(self, tSec):
        self.sunriseTimeSec = tSec

    def set_led_num(self, num):
        self.ledNum = num

    def process(self):
        # select led
        led = pyb.LED(self.ledNum)

        # save time at beginning
        beginTime = time.time()

        # run sunrise
        dt = 0.
        while self.sunriseTimeSec - dt > 0.:
            # intensity from profile ->strategy pattern
            intensity = int(self.intensityProfile(dt))
            # get valid range of intensity
            intensity = max(intensity, 0)
            intensity = min(intensity, self.maxIntensity)

            # set intensity with pyb pulsing
            led.intensity(intensity)

            # delay a bit
            pyb.delay(self.delayMs)

            # set new dt
            dt = time.time() - beginTime


class SunriseExp(Sunrise):
    """overload intensity Profile
        Args:
            same as Sunrise
        Attributes:
            multiplier (float): multiplier for exponential func
            dt (float): time delay in sec for exponential func
    """

    def __init__(self):
        # call parent constructor
        super(SunriseExp, self).__init__()

        self.a = 100.
        self.b = 1.5
        self.c = self.a

        self.intensityProfile = lambda x: min(self.a * math.exp(self.b / self.sunriseTimeSec * x) - self.c,
                                              self.maxIntensity)

    def set_exp_vars(self, a, b):
        self.a = a
        self.b = b
        self.c = self.a
