from matplotlib import pyplot as plt


class ProfilePlotter:
    def __init__(self):
        self.fig = plt.figure()
        plt.xlabel("time in sec")
        plt.ylabel("intensity")

        plt.title("Intensity profile")

        self.plotHandle = plt.plot([0], [0], "-r", label="intensity")
        plt.legend(loc="best")

    def process(self, ts, intensity_profile):
        intens = [intensity_profile(t) for t in ts]
        self.plotHandle = plt.plot(ts, intens, "-r", label="intensity")
        plt.show()
