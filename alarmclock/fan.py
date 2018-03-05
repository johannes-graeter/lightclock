import machine

from alarmclock.with_config import WithConfig


class Fan(WithConfig):

    def __init__(self, config):
        # init config setter
        config_attributes = [
            'fan_pin'
        ]
        super(Fan, self).__init__(config_attributes, config)

        self.fan_pin = machine.Pin(self.config['fan_pin']['value'], machine.Pin.OUT)


    def pre_action(self, dt=None):
        self.fan_pin.off()

    def main_action(self, dt=None):
        self.fan_pin.on()

    def post_action(self, dt=None):
        self.fan_pin.off()
