__author__ = 'Chinmayee P S'


import sys
import os
import subprocess
from pathlib import Path
import configparser
from Library.Utils.Logger import Logger
import os


class SetupInstall:
    """ 
        This script will execute install.sh file and install all the packages necessary to run this framework
        :param self.output : Returns the output of install.sh file
        
    """

    def __init__(self):
        self.output =  None
        self.logger = Logger()

    def package_installer(self):


        try:
            subprocess.run('sudo dos2unix ./install.sh', shell=True, universal_newlines=True, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
            self.output = subprocess.Popen('sudo bash ./install.sh', shell=True, universal_newlines=True, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
            
            output = self.output.stdout.readlines()

            for line in output:
                self.logger.log_info(line)

        except Exception as e:
            self.logger.log_error(f"exception is : {e}\n")


packages_install = SetupInstall()
packages_install.package_installer()
