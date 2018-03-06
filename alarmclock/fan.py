import machine

from alarmclock.with_config import WithConfig


class Fan(WithConfig):

    OFF = 0
    ON = 1

    def __init__(self, config):
        # init config setter
        config_attributes = [
            'fan_pin'
        ]
        super(Fan, self).__init__(config_attributes, config)

        self.fan_pin = machine.Pin(self.config['fan_pin']['value'], machine.Pin.OUT)
        self.state_override = None

    def set_state_override(self, state):
        self.state_override = state
        self.fan_pin.value(self.state_override)

    def reset_state_override(self):
        self.state_override = None


    def pre_action(self, dt=None):
        if self.state_override != None:
            self.fan_pin.value(self.state_override)
        else:
            self.fan_pin.off()

    def main_action(self, dt=None):
        if self.state_override != None:
            self.fan_pin.value(self.state_override)
        else:
            self.fan_pin.on()

    def post_action(self, dt=None):
        if self.state_override != None:
            self.fan_pin.value(self.state_override)
        else:
            self.fan_pin.off()
