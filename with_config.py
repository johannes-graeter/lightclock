class WithConfig:
    """class that triggers an action at a given time
        Args:
            func_mapping: dict with mapping from names in config to setter functions to set the variables
        Attributes:
            func_mapping (dict): see args
    """

    def __init__(self, func_mapping):
        self.func_mapping = func_mapping

    def set_config(self, config_file):
        """
        :param config_file: json file with config params
        :return:
        """
        # func_mapping={
        #     'alarm_sleep_time_sec': self.set_sleep_time_spinning_sec,
        #     'verbose': self.set_verbosity
        # }

        # apply functions that are both in config_file and func_mapping
        for param in config_file:
            if param['name'] in self.func_mapping:
                self.func_mapping[param['name']](param['value'])
