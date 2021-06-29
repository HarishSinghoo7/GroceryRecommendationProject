import configparser


class ConfigReader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('ecommerce/config/config.ini')

    def get_config(self):
        """
        Description: Returning the config parameters
        :return: dictionary of config parameters
        """
        return self.config