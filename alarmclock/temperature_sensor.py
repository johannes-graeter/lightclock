from machine import Pin, I2C
import mcp9808
import utime as time
import uos

from alarmclock.with_config import WithConfig
from alarmclock.fan import Fan


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
                self.is_functional = True

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

        if uos.stat('temp_log.csv')[6] > self.config['temp_log_file_max_bytes']['value']:
            logfile = open(self.config['temp_log_file']['value'], "w")
            logfile.write("#time,temp\n")
        else:
            logfile = open(self.config['temp_log_file']['value'], "a")

        if not self.is_functional:
            logfile.write("{:d},NA\n".format(time.time()))
        else:
            logfile.write("{:d},{:d}.{:d}\n".format(time.time(), temp, frac))

        logfile.close()


class TemperatureWatcher(TemperatureSensor):

    def __init__(self, config, led_control, fan_control):
        config_attributes = [
            'shutdown_temp',
            'shutdown_hysteresis'
        ]
        super(TemperatureWatcher, self).__init__(config, extra_config_attributes=config_attributes)

        self.led_control = led_control
        self.fan_control = fan_control
        self.temp = None

    def pre_action(self, dt):
        if self.led_control.duty_override != None:

            self.temp, frac = self.measure_temp()

            if not self.is_functional:
                self._shutdown_led()

            elif self.temp < int(self.config['shutdown_temp']['value']) - int(self.config['shutdown_hysteresis']['value']):
                self._reset_led()

    def main_action(self, dt):
        self.temp, frac = self.measure_temp()

        if not self.is_functional:
            self._shutdown_led()

        elif self.temp >= int(self.config['shutdown_temp']['value']):
            self._shutdown_led()

        # Add hysteresis of 2 degree
        elif self.led_control.duty_override != None \
                and self.temp < int(self.config['shutdown_temp']['value']) - int(self.config['shutdown_hysteresis']['value']):
            self._reset_led()

    def post_action(self, dt):
        self.pre_action(dt)

    def _shutdown_led(self):
        print("WARNING! Danger of overheating! Shutting down the LED...")
        self.led_control.set_duty_override(0)
        self.fan_control.set_state_override(Fan.ON)

    def _reset_led(self):
        print("Overheating in control, resetting LED override")
        self.led_control.reset_duty_override()
        self.fan_control.reset_state_override()
