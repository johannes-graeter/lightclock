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

    def process(self):
        print(self.s)



