__author__ = 'Chinmayee P S'


import os
import json
import random
import datetime
from pathlib import Path
from Library.Utils.Logger import Logger
from Library.Parser.SSH_Command_Parser import SSH_Parser


class BasicUtils:
    """
        This class library contains all Common Utilities which contains all the function to use all over in project
        def get_random_number
        def verify_json_data
        def get_line_number
        def mac_conv
        def get_file_path
        def bytes_to_bps
        def get_mac_address

    """

    def __init__(self):
        self.f_var = None
        self.file_path = None
        self.converted_value = None
        self.value = None
        self.json_data = None
        self.number = int
        self.string = ""
        self.list = list
        self.dictionary = dict
        self.ssh = SSH_Parser()
        self.logger = Logger()
        self.test_data = {}

    def get_key_value(self, json_file_path, *keys):
        """
            This function will give the key-value which is present in the intput json file
            :param json_file_path: parameter json_file_path required to send the json file location
            :param keys: key from the json data

        """
        try:
            jsonFile = open(json_file_path)
            self.json_data = json.load(jsonFile)
            for key in keys:
                try:
                    value = self.search_key(self.json_data, key)
                    if value:
                        self.logger.log_info(value)
                        return True
                    else:
                        self.logger.log_error('key not found\n')
                        return False
                except Exception as e:
                    self.logger.log_error(f'key not found:{e}\n')
                    return False

        except FileNotFoundError as error:
            self.logger.log_error(f"File is not available:{error}\n")
            return False

    def search_key(self, json_data, key):
        """
            This function will return the key-value which is present in the intput json file
            :param json_file_path: parameter json_file_path required to send the json file location
            :param keys: key from the json data
            :return: value of the key
        """

        for k, v in list(json_data.items()):
            if k == key:
                return json_data[key]
            elif isinstance(v, dict):
                res = self.search_key(v, key)
                if res != None:
                    return res

    def verify_key(self, json_file_path, *keys):
        """
            This function will return true if the provided key is present in the json file
            :param json_file_path: parameter json_file_path required to send the json file location
            :param keys: key from the json data
            :return: True if key is present else False
        """

        try:
            jsonFile = open(json_file_path)
            json_data = json.load(jsonFile)
            for key in keys:
                try:
                    if self.find_key(json_data, key):
                        self.logger.log_info('key found\n')
                        return True
                    else:
                        self.logger.log_warning('key not found\n')
                        return False
                except:
                    self.logger.log_warning('key not found\n')
                    return False

        except FileNotFoundError as error:
            self.logger.log_error(f"File is not available:{error}\n")
            return False

    def find_key(self, json_data, key):
        for k, v in list(json_data.items()):
            if k == key:
                return True
            elif isinstance(v, dict):
                if self.find_key(v, key):
                    return True
        return False

    def get_random_number(self):
        """
            This function generates a random 4-digit number
            :return: return true if executes else false
        """
        self.number = str(random.randint(0, 9999))
        return self.number

    def get_line_number(self, file_path, info):
        """
            This function returns the line number from provided data in file
            :param file_path: parameter required to pass file path
            :param info: parameter required to pass data in file
            :return: return true if executes else false
        """
        try:
            with open(file_path, mode='r') as config_file:
                lines = config_file.readlines()
                self.f_var = 0
                for data in lines:
                    self.f_var += 1
                    if info in data.rstrip():
                        return self.f_var
        except Exception as e:
            self.logger.log_error(f"file doesn't exist:{e}\n")

    def get_mac_address(self):
        """
            This function fetch the mac address of Remote host machine and convert into string
            :return: returns mac address 
        """
        try:
            res = self.ssh.return_stdout("cat /sys/class/net/eth0/address")
            mac_address = str("".join(str(res).split(":")).rstrip())
            return mac_address
        except Exception as error:
            self.logger.log_error(f"MAC Address fetching failed:{error}\n")

    def mac_conv(self, mac_id):
        """
            This function converts the mac address to original format
            :param mac_id: parameter required to pass mac address value
            :return: return true if executes else false
        """
        for i, j in enumerate(mac_id):
            if i % 2 == 0:
                self.string += ":"
            self.string += j
        self.value = self.string[1:]
        return self.value

    def bytes_to_bps(self, bytes, to, bsize=None):
        """
            This function will convert to bytes to kbps, mbps and other conversions
            :param bytes: parameter required to pass bytes value
            :param to: parameter required to pass conversion value
            :param bsize: parameter required the byte size
            :return: return true if executes else false
        """
        conversions = {'kb': 1, 'mb': 2, 'gb': 3, 'tb': 4, 'pb': 5, 'eb': 6}
        for i in range(conversions[to]):
            if bsize is None:
                bsize = 1000000
            self.converted_value = bytes / bsize
        return self.converted_value

    def testrun_data(self, tc_id, tc_name, tc_result, tc_remarks="", tc_runtime="", tc_timestamp="", log_file_path=''):
        """
            This method will create a json file having test data
            :param tc_id: Testcase ID need to pass
            :param tc_name: Testcase Name need to pass
            :param tc_result: Testcase Result need to pass
            :param tc_remarks: Testcase Remarks need to pass
            :param tc_log_path: Testcase log path need to pass  
        """
        try:
            with open(f"{Path(__file__).parent.parent.parent / 'logs' / tc_id}.json", "w") as file:
                json.dump({tc_id: {"tc_id": tc_id, "tc_name": tc_name, "result": tc_result, "remarks": tc_remarks,
                                   "tc_run_time": tc_runtime, "tc_timestamp": tc_timestamp, 'log': log_file_path}},
                          file, indent=4)

        except FileNotFoundError as e:
            self.logger.log_error(f"Error occured due to file not found: {e}")

    def Log_parse(self, test_id):
        """
            This method will return the latest string to be found in the log
            if it finds the match else returns empty string 
            :param test_id: Testcase ID as a string data to search
        """
        with open(Path(__file__).parent.parent.parent / f"logs/log_{datetime.date.today().strftime('%d_%m_%Y')}/TC_Script.log", 'r') as file:
            res = ""
            f_var = 0
            lines = file.readlines()
            match_lines = f"TEST CASE ID:: {test_id}"
            last_known_match = -1
            last_known_match_len = 0
            for data in lines:
                f_var += 1
                if match_lines in data.rstrip():
                    line_num = f_var - 1
                    match_len = self.validate(line_num, lines, match_lines)
                    if match_len > 0:
                        last_known_match = line_num
                        last_known_match_len = match_len
            if last_known_match != -1:
                res = self.print_lines(lines, last_known_match, last_known_match + last_known_match_len)
                if res != None:
                    return res
                else:
                    return ""
            else:
                return res

    def validate(self, start_line, lines, match_lines):
        flag = True
        curr_line = start_line
        log_len = len(lines)

        while (curr_line < log_len):
            if match_lines in lines[curr_line].rstrip():
                while curr_line < log_len:
                    curr_line += 1

            else:
                flag = False
                break

        match_lines = 0
        if flag:
            match_lines = curr_line - start_line
        return match_lines

    def print_lines(self, lines, start_line, end_lines):
        while start_line < end_lines:
            if "Error" in lines[start_line] or "ERROR" in lines[start_line]:
                error_index = lines[start_line].find("ERROR")
                return f"{lines[start_line][error_index:]}"
            start_line += 1

    def backup_folders(self, directory_path, backup_days=1):
        self.logger.log_info(f"{'*'*18}Backup Started{'*'*18}")
        current_date = (datetime.datetime.now())
        self.logger.log_info(f"current date: {current_date}\n")
        try:
            if os.path.exists(directory_path) and os.path.isdir(directory_path):
                directories = [(os.path.join(directory_path, d)) for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
                for source_directory in directories:
                    file_creation_time = os.path.getctime(source_directory)
                    file_creation_date = datetime.datetime.fromtimestamp(file_creation_time)
                    days_ago = current_date - file_creation_date
                    parent_directory = Path(__file__).parent.parent.parent
                    backup_directory = os.path.join(parent_directory, "Logs_Backup")
                    os.makedirs(backup_directory, exist_ok=True)
                    destination_directory = f"{backup_directory}/{os.path.basename(source_directory)}"
                    if days_ago.days >= backup_days:
                        self.logger.log_info(f"The file '{os.path.basename(source_directory)}' was created before {backup_days} days.\n")
                        if os.path.exists(source_directory):
                            if not os.path.exists(destination_directory):
                                os.rename(source_directory, destination_directory)
                                self.logger.log_info(f"File creation date: {file_creation_date}")
                                self.logger.log_info(f"Days before: {days_ago}")
                            else:
                                self.logger.log_info(f"Already file backup found: {os.path.basename(source_directory)}")
                        else:
                            self.logger.log_info(f"File not found.. backup failed: {os.path.basename(source_directory)}")
                else:
                    self.logger.log_info(f"Backup up to date...")

            else:
                self.logger.log_error("The specified directory does not exist or is not a directory.")
            self.logger.log_info(f"{'*'*18}Backup Completed{'*'*18}\n")

        except Exception as e:
            self.logger.log_error(f"Error occured due to: {e}")
            self.logger.log_error(f"{'*'*18}Backup Failed{'*'*18}\n")



