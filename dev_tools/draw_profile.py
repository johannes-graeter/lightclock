import numpy as np

from clock_actions_micropython import *
from profile_printer import *


def main():
    sunriseTime = 20. * 60.
    s = SunriseExp()
    s.set_sunrise_time(sunriseTime)
    s.set_exp_vars(5., 3.5)

    p = ProfilePlotter()

    p.process(np.linspace(0, sunriseTime, 200), s.intensityProfile)


if __name__ == '__main__':
    main()
