from with_config import WithConfig


class StringPrinter(WithConfig):
    """
    Dummy action for testing which prints the string given

    Args:
        s (str): string to print

    Attributes:
        s (str): string to print

    """

    def __init__(self, s, config):
        config_attributes = [
            'max_intensity_percent',
            'sunrise_time_sec',
            'led_pin'
        ]
        super().__init__(config_attributes, config)

        self.s = s

        self.sunriseTimeSec = 1.

    def process(self):
        print(self.s)
        print("config", self.config)

    def process_once(self, dt):
        print(self.s)
        print("time difference=", dt)
        print("config", self.config)
