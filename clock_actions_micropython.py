import math

try:
    import machine
    import utime as time
except:
    print("using ubuntu testing version")


class Sunrise(object):
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

    def __init__(self):
        # max intensity
        self.maxIntensityPercent = 100

        # rise time
        self.sunriseTimeSec = 60. * 30.

        # default profile is linear
        self.intensityProfile = lambda x: 50 + x / self.sunriseTimeSec * 205

        # GPIO number of led
        self.ledNum = 0

        # led delay in millisec
        self.delayMs = 1

    def set_max_intensity_percent(self, maxIntensityPerc):
        self.maxIntensityPercent = min(int(maxIntensityPerc), 100)

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
        # save time at beginning
        beginTime = time.time()

        # run sunrise
        dt = 0.
        while self.sunriseTimeSec - dt > 0.:
            # set new dt
            dt = time.time() - beginTime

            # process one step
            self.process_once(dt)

            # delay a bit
            time.sleep_ms(self.delayMs)

    def process_once(self, dt):
        # print("start sunrise")
        # select led
        led = machine.PWM(machine.Pin(self.ledNum, machine.Pin.OUT), freq=20000)

        # intensity from profile ->strategy pattern
        intensity = int(self.intensityProfile(dt))
        # get valid range of intensity
        intensity = max(intensity, 0)
        intensity = min(intensity, self.maxIntensityPercent)

        # set intensity with bandwidth modulation pulsing, max duty val is 1023, led for pin 0 is on when pin.value()==0
        led.duty(int(intensity*1023/100))


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
                                              self.maxIntensityPercent)

    def set_exp_vars(self, a, b):
        self.a = a
        self.b = b
        self.c = self.a
