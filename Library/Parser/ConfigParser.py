__author__ = 'Roshanzameer M'


from configparser import ConfigParser
from Library.Utils.Logger import Logger


class Config_Parser:
    def __init__(self) -> None:
         self.logger = Logger()

    def get_item(self, file_path, section):
        """
            This method will take file & section reading config file and return the dictionary
            :param file_path: specify the file path
            :param section: specify the config file section
            :return: returns dicti object of config sections, which include items
        """
        try:
            config = ConfigParser()
            config.read(file_path)
            d = {}
            for sections in config.sections():
                d[sections] = {}
                for key, value in config.items(sections):
                    d[sections][key] = value
            return d[section.upper()]
        except KeyError as error:
                self.logger.log_error(f"{error}:Section Not Found\n")
