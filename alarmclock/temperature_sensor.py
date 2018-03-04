from machine import Pin, I2C
import mcp9808
import utime as time

from alarmclock.with_config import WithConfig


class TemperatureSensor(WithConfig):

    def __init__(self, config, extra_config_attributes=None):
        # init config setter
        config_attributes = [
            'sdl_pin',
            'sda_pin',
            'verbose'
        ]
        if extra_config_attributes:
            config_attributes += extra_config_attributes

        super(TemperatureSensor, self).__init__(config_attributes, config)

        self.i2c = I2C(scl=Pin(self.config['sdl_pin']['value']), sda=Pin(self.config['sda_pin']['value']), freq=10000)
        try:
            self.mcp = mcp9808.MCP9808(i2c=self.i2c)
            self.mcp.set_resolution(mcp9808.T_RES_MAX)
            self.is_functional = True
        except Exception:
            self.is_functional = False
            print("Failed to initialize temperature sensor! Broken connection?")

    def measure_temp(self):
        if self.mcp:
            try:
                temp, frac = self.mcp.get_temp_int()

                if self.config['verbose']['value']:
                    print ("Temperature is: {:d}.{:d}".format(temp, frac))

                return temp, frac

            except Exception:
                if self.config['verbose']['value']:
                    print ("Temperature reading failed!")

                self.is_functional = False


class TemperatureLogger(TemperatureSensor):

    def __init__(self, config):
        config_attributes = [
            'temp_log_file'
        ]
        super(TemperatureLogger, self).__init__(config, extra_config_attributes=config_attributes)

        logfile = open(self.config['temp_log_file']['value'], "w")
        logfile.write("#time,temp\n")
        logfile.close()

    def main_action(self, dt):
        temp, frac = self.measure_temp()


        logfile = open(self.config['temp_log_file']['value'], "a")

        if not self.is_functional:
            logfile.write("{:d},NA\n".format(time.time()))
        else:
            logfile.write("{:d},{:d}.{:d}\n".format(time.time(), temp, frac))

        logfile.close()
