class WithConfig:
    """class that triggers an action at a given time
        Args:
            func_mapping: dict with mapping from names in config to setter functions to set the variables
        Attributes:
            func_mapping (dict): see args
    """

    def __init__(self, names, config):
        # check if names are in config
        for n in names:
            if n not in config:
                raise Exception("name "+n+" not defined in config")
        self.config = config
