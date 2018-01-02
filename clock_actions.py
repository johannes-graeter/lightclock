class StringPrinter:
    """
    Dummy action for testing which prints the string given

    Args:
        s (str): string to print

    Attributes:
        s (str): string to print

    """

    def __init__(self, s):
        self.s = s
        # rise time
        self.sunriseTimeSec = 60. * 30.

    def set_config(self, config_file):
        """
        :param config_file: json file with config params
        :return:
        """
        func_mapping = {
            'max_intensity_percent': self.set_max_intensity_percent,
            'sunrise_time_sec': self.set_sunrise_time,
            'led_number': self.set_led_num
        }

        # apply functions that are both in config_file and func_mapping
        for param in config_file:
            if param['name'] in func_mapping:
                func_mapping[param['name']](param['value'])

    def set_led_num(self, num):
        print('set led num {}'.format(num))

    def set_sunrise_time(self, time):
        print('sunrise time {} sec'.format(time))

    def set_max_intensity_percent(self, inten):
        print('set max intensity to {} percent'.format(inten))

    def process(self):
        print(self.s)

    def process_once(self, dt):
        print(self.s)
        print("time difference=", dt)



