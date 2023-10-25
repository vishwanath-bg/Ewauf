__author__ = 'Anjana R'


import logging
import os
import inspect
import datetime 


class Logger:
    """
        This class offers a diverse range of log level methods, each designed to facilitate seamless logging experience.
        :param test_case_name: name of the test to be logged
    """
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

    def __init__(self, test_case_name=None,test_id=None):

        try:
            parent_directory = os.path.dirname(os.path.abspath(__file__))
            self.log_directory = os.path.join(parent_directory, "..", "..", f"logs/log_{datetime.date.today().strftime('%d_%m_%Y')}")
            os.makedirs(self.log_directory, exist_ok=True)
            test_name = "TC_Script"
            logging.basicConfig(filename=os.path.join(self.log_directory, f"{test_name}.log"), level=logging.INFO,
                                format=Logger.LOG_FORMAT)
            self.test = test_case_name
            self.test_id = test_id
            if self.test != None:
                self.header_log()
        except Exception as error:
            print("Error occurred..", error)

    def __log_message(self, log, loglevel):
        """
            This method helps in logging the log message with user specified log level
            :params log:log message to be logged
            :param loglevel: specify the logging level
        """
        try:
            logging.log(getattr(logging, loglevel.upper()), log)
        except Exception as error:
            print("Error occurred:", error)

    def header_log(self):
        """
            This method provides the header to the log file and logs the message
        """
        try:
            
            self.__log_message(f"{'#' * 100}", 'info')
            header = f"TEST CASE ID:: {self.test_id} || TEST CASE NAME:: {self.test} || START TIME:: " \
                     f"{datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')}"
            self.__log_message(header, 'info')
            self.__log_message(f"{'#' * 100}", 'info')
        except Exception as error:
            print("Error occurred while adding header into the log:", error)

    def log_info(self, message):
        """
            This method logs the log message with the respective formatted date and step
            :param message: specify name of the Testcase/module name running
        """
        try:
            log_msg = f"{message}"
            self.__log_message(log_msg, 'info')
        except Exception as error:
            print("Error occurred while logging info:", error)

    def log_error(self, error_message):
        """
            This method logs the error messages
            :param: error_message:error message to be logged
        """
        try:
            log_msg = f"{error_message}"
            self.__log_message(log_msg, 'error')
        except Exception as error:
            print("Error occurred while logging error:", error)

    def log_warning(self, warn_message):
        """This method logs the warning messages
        :param warn_message: warning message to be logged"""
        try:
            log_msg = f"{warn_message}"
            self.__log_message(log_msg, 'warning')
        except Exception as error:
            print("Error occurred while logging the warning:", error)

    def log_debug(self, debug_message):
        """This method logs the debug messages
        :param debug_message: debug message to be logged"""
        try:
            log_msg = f"{debug_message}"
            self.__log_message(log_msg, 'debug')
        except Exception as error:
            print("Error occurred while logging debug:", error)

    def log_critical(self, critical_message):
        """This method logs the critical messages
        :param: msg-> critical message to be logged"""
        try:
            log_msg = f"{critical_message}"
            self.__log_message(log_msg, 'critical')
        except Exception as error:
            print("Error occurred while logging critical:", error)
