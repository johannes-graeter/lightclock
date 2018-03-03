from machine import Pin, I2C
import mcp9808
import utime as time

from alarmclock.with_config import WithConfig


class TemperatureSensor(WithConfig):

    def __init__(self, config):
        # init config setter
        config_attributes = [
            'sdl_pin',
            'sda_pin',
            'verbose'
        ]
        super(TemperatureSensor, self).__init__(config_attributes, config)

        self.i2c = I2C(scl=Pin(self.config['sdl_pin']['value']), sda=Pin(self.config['sda_pin']['value']), freq=10000)
        try:
            self.mcp = mcp9808.MCP9808(i2c=self.i2c)
            self.mcp.set_resolution(mcp9808.T_RES_MAX)
            self.is_functional = True
        except Exception:
            self.is_functional = False
            print("Failed to initialize temperature sensor! Broken connection?")

        self.logfile = open("temp_log.csv", "w")
        self.logfile.write("#time,temp\n")

    def __del__(self):
        self.logfile.close()


class TemperatureLogger(TemperatureSensor):

    def process_once(self, dt):
        if self.mcp:
            try:
                temp, frac = self.mcp.get_temp_int()

                if self.config['verbose']['value']:
                    print ("Temperature is: {:d}.{:d}".format(temp, frac))

                self.logfile.write("{:d},{:d}.{:d}\n".format(time.time(), temp, frac))
            except Exception:
                self.is_functional = False

        if not self.is_functional:
            if self.config['verbose']['value']:
                print ("Temperature reading failed!")

            self.logfile.write("{:d},NA\n".format(time.time()))
