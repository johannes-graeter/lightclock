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

    def process(self):
        print(self.s)

    def process_once(self, beginTime):
        print(self.s)
        print("start time=", beginTime)



