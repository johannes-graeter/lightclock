import machine

from alarmclock.with_config import WithConfig


class Fan(WithConfig):

    OFF = 0
    ON = 1

    def __init__(self, config, action):
        # init config setter
        config_attributes = [
            'fan_pin'
        ]
        super(Fan, self).__init__(config_attributes, config)

        self.action = action
        self.fan_pin = machine.Pin(self.config['fan_pin']['value'], machine.Pin.OUT)

    def process_once(self, dt=None):
        self.fan_pin.value(self.action)
