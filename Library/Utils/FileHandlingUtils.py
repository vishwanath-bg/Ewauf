__author__ = "Vishwanath BG"

from Library.Parser.SSH_Command_Parser import SSH_Parser
from Library.Utils.Logger import Logger
import os
import json
import csv
import yaml


class File_Handling:
    """
        This class library contains all common file handling methods/functions that simplify file handling experience
        class File_Handling
            def read_txt_file
            def verify_logs
            def write_txt_file
            def append_txt_file
            def read_json_file
            def verify_json_file
            def write_json_file
            def append_json_file
            def update_json_file
            def merge_json_file
            def remove_key_from_json
            def verify_yaml_file
            def read_yaml_file
            def write_yaml_file
            def update_yaml_file
            def merge_yaml_file
            def remove_key_from_yaml
            def read_csv_file
            def write_csv_file
            def append_csv_file
            def update_csv_file
            def remove_row_from_csv
            def read_binary_data
            def write_binary_data
            def check_and_grant_permissions
            def file_download
            def upload file
            def dos_to_unix
    """

    def __init__(self):
        self.logger = Logger()
        self.ssh = SSH_Parser()
        self.searchKeys = []

    def read_txt_file(self, file_path):
        """
            This method helps in reading the given file
            :param file_path: specify the file path
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] in (".txt", ".log"):
                print(os.path.splitext(file_path)[1])
                self.check_and_grant_permissions(file_path)
                read_obj = open(file_path, 'r').read()  # reading file
                self.logger.log_info("Reading File....\n")
                self.logger.log_info(read_obj)
            else:
                self.logger.log_error(f"Error: given file '{file}' is not in .txt format\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to file not readable {error}\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while reading the file {error}\n")
        except NotADirectoryError as error:
            self.logger.log_error(f"Error occurred due to file directory not found {error}\n")

    def verify_logs(self, log_file_path, *searchData):
        """
            This function search the data is available in file over the remote host connection machine
            :param log_file_path: parameter required the location of file
            :param searchData: parameter required search data parameters
            :return: return true if executes else false
        """
        try:
            if self.ssh.connect_to_server():
                ftp_client = self.ssh.client.open_sftp()
                remote_file = ftp_client.open(str(log_file_path))
                flag = []
                temp = [line.strip('\n\r') for line in remote_file]
                for search in searchData:
                    for line in temp:
                        if str(search) in line: 
                            self.logger.log_info(f"{search} - FOUND in LOG File in Line:\n")
                            self.logger.log_info(f'{line}\n')
                            flag.append(True)
                            break
                    else:
                        self.logger.log_error(f"{line} - NOT FOUND in LOG File\n")
                        self.logger.log_error(search)
                        flag.append(False)
                if all(flag):
                    return True
                else:
                    return False 
                
        except FileNotFoundError as e:
            self.logger.log_error(f"File not found:{e}\n")
        except OSError as e:
            self.logger.log_error(f"{e}\n")

    def write_txt_file(self, file_path, *content):
        """
            This method helps in writing the file
            :param file_path: specify the file path
            :param content: single or multiple data to be written into the file
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".txt":
                if os.path.exists(file_path):
                    self.check_and_grant_permissions(file_path)
                open(file_path, 'w').writelines(line+"\n" for line in content)
                if open(file_path, "r").read().strip("\n") == "\n".join(content):
                    self.logger.log_info(file, ": File has been updated with given data\n")
                else:
                    self.logger.log_error("Data not written into the file\n")
            else:
                self.logger.log_error(f"Error: given file '{file}' is not in .txt format\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while writing the file: {error}\n")
        except NotADirectoryError as error:
            self.logger.log_error(f"Unable to find the file directory {error}\n")

    def append_txt_file(self, file_path, *content):
        """
            This method to read append data to file
            :param file_path: specify the file path
            :param data: data to be written into the file
        """      
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".txt":
                self.check_and_grant_permissions(file_path)
                previous_data = open(file_path, 'r').read()
                data = ""
                for line in content:
                    data += line + "\n"
                open(file_path, 'a').write(data)
                self.logger.log_info(f"appended given data in file {file}\n") if open(file_path, 'r').read().strip('\n') == previous_data + data.strip('\n') else print(f"data not appended in file {file}\n")
            else:
                self.logger.log_error(f"Error: given file '{file}' is not in .txt format\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while writing the file: {error}\n")
        except NotADirectoryError as error:
            self.logger.log_error(f"Unable to find the file directory: {error}\n")        

    def read_json_file(self, file_path):
        """
            This method helps in reading json file
            :param file_path: specify the file path
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".json":
                self.check_and_grant_permissions(file_path)
                self.logger.log_info(json.load(open(file_path, 'r')))
            else:
                self.logger.log_error(f"Error: given file '{file}' is not in .json format\n")
        except NotADirectoryError as error:
            self.logger.log_error(error)
        except FileNotFoundError as error:
            self.logger.log_error(f"Unable to find the file directory: {error}\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}")
        except json.JSONDecodeError:
            self.logger.log_error(f"Error: Invalid JSON format in file '{file}'\n")
        
    def verify_json_file(self, file_path):
        """
        Verify the JSON data in the file
        :param file_path: specify the file path
        :return: dictionary type of JSON data if valid, otherwise None
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".json":
                with open(file_path, 'r') as file_obj:
                    json_data = json.load(file_obj)
                return json_data
            else:
                self.logger.log_error(f"Error: given file '{file}' is not in .json format\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error: File '{file}' not found. {error}\n")
        except json.JSONDecodeError:
            self.logger.log_error(f"Error: Invalid JSON format in file '{file}'\n")
        return None

    def write_json_file(self, file_path, data):
        """
        This method helps in writing the json file
        :param file_path: specify the file path
        :param data: dictionary type of data to be written into the json file
        """
        
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".json":
                if os.path.exists(file_path):
                    self.check_and_grant_permissions(file_path)
                with open(file_path, 'w') as file_obj:
                    json.dump(data, file_obj, indent=4)

                written_data = self.verify_json_file(file_path)
                if written_data == data:
                    self.logger.log_info(f"JSON data has been written into file : {file}\n")
                else:
                    self.logger.log_error(f"Unable to write data in file : {file}\n")
            else:
                self.logger.log_error(f"Error: Given file '{file}' is not in .json format\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while writing JSON file: {error}\n")
        except json.JSONDecodeError:
            self.logger.log_error(f"Error: Invalid JSON format in file '{file}'\n")    

    def append_json_file(self, file_path, data):
        """
        This method helps in appending JSON data to an existing JSON file
        :param file_path: specify the file path
        :param data: dictionary type of data to be appended to the JSON file
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".json":
                self.check_and_grant_permissions(file_path)
                with open(file_path, 'a') as file_obj:
                    file_obj.write('\n')  # Add a newline character before appending JSON
                    json.dump(data, file_obj, indent=4)
                self.logger.log_info(f"JSON data has been appended to file : {file}\n")
            else:
                self.logger.log_error(f"Error: Given file '{file}' is not in .json format\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while appending JSON file: {error}\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
        
    def update_json_file(self, file_path, new_data):
        """
        This method updates an existing JSON file with new data while preserving the existing data.
        :param file_path: specify the file path
        :param new_data: dictionary type of data to be updated in the JSON file
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".json":
                self.check_and_grant_permissions(file_path)
                with open(file_path, 'r') as file_obj:
                    existing_data = json.load(file_obj)

                # Update existing data with new data
                existing_data.update(new_data)

                with open(file_path, 'w') as file_obj:
                    json.dump(existing_data, file_obj, indent=4)
                self.logger.log_info(f"JSON file '{file}' has been updated.\n")
                return True
            else:
                self.logger.log_error(f"Error: Given file '{file}' is not in .json format\n")
                return False
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
            return False
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while updating JSON file: {error}\n")
            return False
        except ValueError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
            return False
        
    def merge_json_files(self, output_file, *input_files):
        """
        This method merges multiple JSON files into a single JSON file.
        :param output_file: specify the output file path
        :param input_files: multiple input file paths to be merged
        """
        try:
            merged_data = {}
            flag = []
            output_file_name = os.path.basename(output_file)
            for file_path in input_files:
                input_file = os.path.basename(file_path)
                if os.path.splitext(file_path)[1] == ".json":
                    self.check_and_grant_permissions(file_path)
                    with open(file_path, 'r') as file_obj:
                        json_data = json.load(file_obj)
                    
                    merged_data.update(json_data)
                    flag.append(True)    
                else:
                    self.logger.log_error(f"Error: Given file '{input_file}' is not in .json format")
                    flag.append(False)
            if all(flag):
                with open(output_file, 'w') as file_obj:
                    json.dump(merged_data, file_obj, indent=4)
                
                if self.verify_json_file(output_file) == merged_data:
                    self.logger.log_info(f"JSON files have been merged into '{output_file_name}'.\n")
                    return True
                else:
                    self.logger.log_info(f"JSON files have not been merged...!\n")
                    return False
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
            return False
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while reading JSON file: {error}\n")
            return False
        except json.JSONDecodeError:
            self.logger.log_error(f"Error: Invalid JSON format in file '{input_file}'\n")
            return False

    def remove_nested_key(self, json_data, key_to_remove):
        """
        Recursively remove a nested key from JSON data.
        :param json_data: JSON data (dictionary) to process
        :param key_to_remove: The nested key to be removed
        :return: True if key is removed, False otherwise
        """
        for key, value in list(json_data.items()):
            if key == key_to_remove:
                del json_data[key]
                return True
            elif isinstance(value, dict):
                if self.remove_nested_key(value, key_to_remove):
                    return True
        return False

    def remove_key_from_json(self, file_path, *keys_to_remove):
        """
        This method removes a specified key (even if nested) from a JSON file.
        :param file_path: specify the file path
        :param key_to_remove: the key to be removed from the JSON file
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".json":
                self.check_and_grant_permissions(file_path)

                # Read the JSON data from the file
                with open(file_path, 'r') as file_obj:
                    json_data = json.load(file_obj)

                flag = []
                # Remove the nested key from the JS ON data
                for key_to_remove in keys_to_remove:
                    if self.remove_nested_key(json_data, key_to_remove):
                        self.logger.log_info(f"Key '{key_to_remove}' has been removed from JSON file '{file}'")
                        flag.append(True)
                    else:
                        self.logger.log_error(f"Key '{key_to_remove}' not found in JSON file '{file}'")
                        flag.append(False)
                
                if all(flag):
                    # Write the updated JSON data back to the file
                    with open(file_path, 'w') as file_obj:
                        json.dump(json_data, file_obj, indent=4)
                    self.logger.log_info(f"Updated Json File '{file}'.\n")
                    return all(flag)
                else:
                    self.logger.log_error(f"Updating Json File Failed '{file}'.\n")
                    return False
                
            else:
                self.logger.log_error(f"Error: Given file '{file}' is not in .json format\n")
                return False
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
            return False
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while reading JSON file: {error}\n")
            return False
        except json.JSONDecodeError:
            self.logger.log_error(f"Error: Invalid JSON format in file '{file}'\n")
            return False       

    def verify_yaml_file(self, file_path):
        """
        Verify the YAML data in the file
        :param file_path: specify the file path
        :return: dictionary type of YAML data if valid, otherwise None
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".yaml":
                with open(file_path, 'r') as file_obj:
                    yaml_data = yaml.safe_load(file_obj)
                return yaml_data
            else:
                self.logger.log_error(f"Error: Given file '{file}' is not in .yaml format\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error: File '{file}' not found.\n")
        except yaml.YAMLError as error:
            self.logger.log_error(f"Error: Invalid YAML format in file '{file}'\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
        return None       

    def read_yaml_file(self, file_path):
        """
        Read a YAML file and return its contents as a Python data structure
        :param file_path: specify the file path
        :return: dictionary type of YAML data if valid, otherwise None
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".yaml":
                self.check_and_grant_permissions(file_path)
                with open(file_path, 'r') as file_obj:
                    self.logger.log_info(f"{file} data reading....")
                    self.logger.log_info(yaml.safe_load(file_obj),"\n")
            else:
                self.logger.log_error(f"Error: Given file '{file}' is not in .yaml format\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while reading YAML file: {error}\n")
        except yaml.YAMLError as error:
            self.logger.log_error(f"Error: Invalid YAML format in file '{file}'\n")       

    def write_yaml_file(self, file_path, data):
        """
        This method helps in writing the YAML file
        :param file_path: specify the file path
        :param data: dictionary type of data to be written into the YAML file
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".yaml":
                if os.path.exists(file_path):
                    self.check_and_grant_permissions(file_path)
                with open(file_path, 'w') as file_obj:
                    if isinstance(data, dict):
                        yaml.dump(data, file_obj, sort_keys=False)
                    else:
                        self.logger.log_error("Given data is not dictionary")

                written_data = self.verify_yaml_file(file_path)
                if written_data == data:
                    self.logger.log_info(f"YAML data has been written into file '{file}'\n")
                else:
                    self.logger.log_error(f"Unable to write file: {file}\n")
            else:
                self.logger.log_error(f"Error: Given file '{file}' is not in .yaml format\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while writing YAML file: {error}\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")      

    def update_yaml_file(self, file_path, data_dict):
        """
        This method updates an existing YAML file by replacing multiple key-value pairs.
        :param file_path: specify the file path
        :param data_dict: dictionary containing the keys and their respective new data
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".yaml":
                self.check_and_grant_permissions(file_path)
                with open(file_path, 'r') as file_obj:
                    temp = yaml.safe_load(file_obj)
                    if isinstance(temp, list):
                        yaml_data = temp[0]
                    else:
                        yaml_data = temp
                    self.logger.log_error(yaml_data)

                if isinstance(yaml_data, dict):
                    updated = []
                    for key, new_data in data_dict.items():
                        if key in yaml_data:
                            yaml_data[key] = new_data
                            updated.append(True)
                        else:
                            self.logger.log_error(f"Warning: Key '{key}' not found in file '{file}'. Skipping update.")
                            updated.append(False)

                    if all(updated):
                        with open(file_path, 'w') as file_obj:
                            yaml.dump(yaml_data, file_obj, sort_keys=False, default_flow_style=False)
                        self.logger.log_error(f"YAML file '{file}' has been updated.\n")
                    else:
                        self.logger.log_error("No updates were applied to the YAML file.\n")
                else:
                    self.logger.log_error(f"Error: Invalid YAML data structure in file '{file}'.\n")
            else:
                self.logger.log_error(f"Error: Given file '{file}' is not in .yaml format\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while updating YAML file: {error}\n")
        except yaml.YAMLError as error:
            self.logger.log_error(f"Error: Invalid YAML format in file '{file}'.\n{error}\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")

    def merge_yaml_files(self, output_file, *input_files):
        """
        This method merges multiple YAML files into a single YAML file.
        :param output_file: specify the output file path
        :param input_files: multiple input file paths to be merged
        """
        merged_data = {}

        for file_path in input_files:
            if os.path.splitext(file_path)[1] == ".yaml":
                try:
                    self.check_and_grant_permissions(file_path)
                    with open(file_path, 'r') as file_obj:
                        yaml_data = yaml.safe_load(file_obj)

                    merged_data.update(yaml_data)
                except FileNotFoundError as error:
                    self.logger.log_error(f"Error occurred while reading YAML file: {error}")
                except PermissionError as error:
                    self.logger.log_error(f"Error occurred due to {error}")
                except yaml.YAMLError as error:
                    self.logger.log_error(f"Error: Invalid YAML format in file '{file_path}'.\n{error}")
            else:
                self.logger.log_error(f"Given file is not a .yaml format: {os.path.splitext(file_path)}")

            try:
                with open(output_file, 'w') as file_obj:
                    yaml.dump(merged_data, file_obj, sort_keys=False)
                self.logger.log_info(f"YAML files have been merged into '{output_file}'.\n")
            except FileNotFoundError as error:
                self.logger.log_error(f"Error occurred while writing YAML file: {error}\n")
            except PermissionError as error:
                self.logger.log_error(f"Error occurred due to {error}\n")

    def remove_key_from_yaml(self, file_path, *keys_to_remove):
        """
        This method removes specific keys from a YAML file, including nested keys.
        :param file_path: specify the file path
        :param keys_to_remove: keys to be removed from the YAML file
        :return: if it exectes keys_removed list else returns empty list 
        """
        def _remove_keys(data, keys):
            if isinstance(data, dict):
                keys_removed = []
                for key in keys:
                    if key in data:
                        data.pop(key)
                        keys_removed.append(key)
                for value in data.values():
                    keys_removed.extend(_remove_keys(value, keys))
                return keys_removed
            elif isinstance(data, list):
                keys_removed = []
                for item in data:
                    keys_removed.extend(_remove_keys(item, keys))
                return keys_removed
            return []

        if os.path.splitext(file_path)[1] == ".yaml":
            file = os.path.basename(file_path)
            try:
                with open(file_path, 'r') as file_obj:
                    yaml_data = yaml.safe_load(file_obj)

                keys_removed = _remove_keys(yaml_data, keys_to_remove)

                with open(file_path, 'w') as file_obj:
                    yaml.dump(yaml_data, file_obj, sort_keys=False)

                if keys_removed:
                    self.logger.log_info(f"Keys {keys_removed} have been removed from YAML file '{file}'.\n")
                else:
                    self.logger.log_error(f"No keys found for removal in YAML file '{file}'.\n")
            except FileNotFoundError as error:
                self.logger.log_error(f"Error occurred while reading YAML file: {error}\n")
            except yaml.YAMLError as error:
                self.logger.log_error(f"Error: Invalid YAML format in file '{file}'.\n")
        else:
            self.logger.log_error(f"Error: Given file is not a .yaml format: {os.path.splitext(file_path)}\n")

    def read_csv_file(self, file_path):
        """
        Read a CSV file and return its contents as a list of dictionaries
        :param file_path: specify the file path
        """
        try:
            if os.path.splitext(file_path)[1] == ".csv":
                self.check_and_grant_permissions(file_path)
                with open(file_path, 'r') as file_obj:
                    reader = csv.reader(file_obj)
                    for row in reader:
                        self.logger.log_info(" ".join(row))
            else:
                self.logger.log_error(f"Error: Given file is not a .csv format: {os.path.basename(file_path)}\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while reading CSV file: {error}\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")

    def write_csv_file(self, file_path, headers, *data):
        """
        Write data to a CSV file
        :param file_path: specify the file path
        :param headers: list or comma separated string of field names for the CSV header
        :param data: multiple list of values representing the data to write
        """
        try:
            if os.path.splitext(file_path)[1] == ".csv":
                if os.path.exists(file_path):
                    self.check_and_grant_permissions(file_path)
                with open(file_path, 'w', newline='') as file_obj:
                    writer = csv.writer(file_obj)
                    if isinstance(headers, str):
                        headers = headers.split(",")
                    writer.writerow(headers)
                    for row in data:
                        if isinstance(row, str):
                            row = row.split(",")
                        if not len(headers) == len(row):
                            self.logger.log_error(f"{row}Number of values passing not matching with number of headers\n")
                        else:
                            writer.writerow(row)
                    self.logger.log_info(f"CSV data has been written into: {os.path.basename(file_path)}\n")
            else:
                self.logger.log_error(f"Error: Given file is not a .csv format: {os.path.splitext(file_path)}\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while writing CSV file: {error}\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
        

    def append_csv_file(self, file_path, *data):
        """
        Append data to an existing CSV file
        :param file_path: specify the file path
        :param data: list of lists or string separated by comma representing the data to append
        """
        
        try:
            if os.path.splitext(file_path)[1] == ".csv":
                with open(file_path, 'r', newline='') as file_obj:
                    reader = csv.reader(file_obj)
                    header_len = len(list(reader)[0])
                    with open(file_path, 'a', newline='') as file_obj_1:
                        writer = csv.writer(file_obj_1)
                        for row in data:
                            if isinstance(row, str):
                                row = row.split(",")
                            if not header_len == len(row):
                                self.logger.log_error(f"{row}Number of values passing not matching with number of header\ns")
                            else:
                                writer.writerow(row)
                self.logger.log_info(f"Data has been appended to CSV file: {os.path.basename(file_path)}\n")
            else:
                self.logger.log_error(f"Error: Given file is not a .csv format: {os.path.basename(file_path)}\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while appending CSV file: {error}\n")
        
    def update_csv_file(self, file_path, row_index, col_index, updated_values):
        """
        Update specific values in a CSV file using row index and column index.
        If the provided row and column indices are out of bounds, it will add new data to the CSV file.
        :param file_path: specify the file path
        :param row_index: index of the row to update or add new data
        :param col_index: index of the column to update or add new data
        :param updated_values: list of values to update or add to the CSV file
        """
        
        try:
            file = os.path.basename(file_path)
            if isinstance(updated_values, str):
                updated_values = updated_values.split(",")
            if os.path.splitext(file_path)[1] == ".csv":
                self.check_and_grant_permissions(file_path)
                with open(file_path, "r", newline="") as file_obj:
                    reader = csv.reader(file_obj)
                    data = list(reader)

                max_row_index = len(data) - 1
                max_col_index = max(len(row) for row in data) - 1

                if 0 <= row_index <= max_row_index:
                    row = data[row_index]
                    if 0 <= col_index <= max_col_index:
                        for i, value in enumerate(updated_values):
                            if col_index + i <= max_col_index:
                                row[col_index + i] = value
                            else:
                                # Append None values to the row until it reaches the desired column index
                                row.extend([None] * (col_index + i - max_col_index))
                                row[col_index + i] = value
                    else:
                        # Append None values to the row until it reaches the desired column index
                        row.extend([None] * (col_index - max_col_index))
                        for value in updated_values:
                            row.append(value)
                else:
                    # Append new rows with None values until it reaches the desired row index and column index
                    data.extend([[]] * (row_index - max_row_index))
                    new_row = [None] * col_index
                    new_row.extend(updated_values)
                    data.append(new_row)
                with open(file_path, "w", newline="") as file_obj_1:
                    writer = csv.writer(file_obj_1)
                    writer.writerows(data)
                self.logger.log_info(f"Values at (row {row_index}, columns {col_index} to {col_index + len(updated_values) - 1}) have been updated in the CSV file.\n")
            else:
                self.logger.log_error(f"Error: Given file is not a .csv format: {file}\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while updating CSV file: {error}\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
        

    def remove_row_from_csv(self, file_path, row_index):
        """
        Remove a specific row from a CSV file
        :param file_path: specify the file path
        :param row_index: index of the row to remove
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".csv":
                self.check_and_grant_permissions(file_path)
                with open(file_path, "r") as file_obj:
                    reader = csv.reader(file_obj)
                    data = [row for row in reader]
                    if data is not None and 0 <= row_index < len(data):
                        removed_row = data.pop(row_index)
                        with open(file_path, "w", newline="") as file_obj_1:
                            writer = csv.writer(file_obj_1)
                            for row in data:
                                writer.writerow(row)
                            self.logger.log_info(f"Value at (row {row_index} having {removed_row} has been removed from list.\n")
                    else:
                        self.logger.log_error(f"Error: Invalid row index.\n")
            else:
                self.logger.log_error(f"Error: Given file is not a .csv format: {file}\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while updating CSV file: {error}\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
        
    def read_binary_data(self, file_path):
        """
        Read binary data from a file.
        :param file_path: specify the file path
        :return: binary data read from the file
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".bin":
                self.check_and_grant_permissions(file_path)
                with open(file_path, 'rb') as file_obj:
                    binary_data = file_obj.read()
                self.logger.log_info(f"Binary data has been read from: {file}\n")
                self.logger.log_info(binary_data)
            else:
                self.logger.log_error(f"Error: Given file is not a .bin format: {file}\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while reading the file: {error}\n")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")
        

    def write_binary_data(self, file_path, binary_data):
        """
        Write binary data to a file.
        :param file_path: specify the file path
        :param binary_data: binary data to be written to the file
        """
        try:
            file = os.path.basename(file_path)
            if os.path.splitext(file_path)[1] == ".bin":
                self.check_and_grant_permissions(file_path)
                with open(file_path, 'wb') as file_obj:
                    file_obj.write(binary_data)

                self.logger.log_info(f"Binary data has been written into: {file}\n")
            else:
                self.logger.log_error(f"Error: Given file is not a .bin format: {file}\n")
        except FileNotFoundError as error:
            self.logger.log_error(f"Error occurred while writing the file: {error}\m")
        except PermissionError as error:
            self.logger.log_error(f"Error occurred due to {error}\n")

    def check_and_grant_permissions(self, *file_paths):
        """
        This method verifies file permission and grant permission if permission not found
        :param file_paths: specify multiple filepaths which need to verify and grant file permission
        """
        for file_path in file_paths:
            if os.access(file_path, os.R_OK | os.W_OK):
                self.logger.log_info(f"The file {os.path.basename(file_path)} already has read and write permissions\n")
            else:
                os.chmod(file_path, 0o666)
                self.logger.log_error(f"Read and write permissions have been granted for: {os.path.basename(file_path)}\n")

    def file_download(self, remote_file_path, local_file_path, machine=1, client=None):
        """
            This method facilitates file download/getting-file from remote machine to local/host machine
            :param remote_file_path: specify remote/server file path/location
            :param local_file_path: specify local/host path where file should be downloaded
        """
        try:
            client = self.ssh.connect_to_server(machine) if client == None else client

            stdin, stdout, stderr = client.exec_command(f"ls -l {remote_file_path}")

            if not "-rwxrwxrwx" in stdout.read().decode():
                client.exec_command(f"sudo chmod 777 {remote_file_path}")

            status = self.ssh.file_download(remote_file_path, local_file_path, client=client)
            if status:
                if os.path.exists(local_file_path):
                    self.logger.log_info(f" {os.path.basename(remote_file_path)} Downloaded file successfully\n")
                    return True
                else:
                    self.logger.log_error(f"{os.path.basename(remote_file_path)} file not Downloaded\n")
                    return False
            else:
                self.logger.log_error("SFTP Client Failed\n")
                return False
        except Exception as error:
            self.logger.log_error(f"Unable to download the file: {error}\n")
            return False

    def upload_file(self, local_file_path, remote_file_path, machine=1, client=None):
        """
            This method facilitates uploading file from local/host machine to remote machine
            :param local_file_path: specify local/host path where file should be downloaded
            :param remote_file_path: specify remote/server file path/location
        """
        try:
            self.check_and_grant_permissions(local_file_path)
            if client == None:
                status = self.ssh.upload_file(local_file_path, remote_file_path, machine=machine)
                cmd_output = self.ssh.client.exec_command(f"find {remote_file_path}")
            else:
                status = self.ssh.upload_file(local_file_path, remote_file_path, client=client)
                cmd_output = client.exec_command(f"find {remote_file_path}")
            
            if status and cmd_output:
                self.logger.log_info(f"{os.path.basename(local_file_path)} file uploaded successfully\n")
                return True
            else:
                self.logger.log_info(f"{os.path.basename(local_file_path)} file upload failed\n")
                return False
        except Exception as error:
            self.logger.log_error(f"Unable to upload the file: {error}\n")
            return False

    def dos_to_unix(self, remote_file_path, machine=1, client=None):
        """
            This method converts dos file into unix formation
            :param remote_file_path: specify remote/server file path/location
        """
        try:
            client = self.connect_to_server(machine) if client == None else client
            if client:
                client.exec_command("sudo apt install dos2unix")
                client.exec_command(f"sudo dos2unix {remote_file_path}")
            else:
                self.logger.log_error("server unreachable\n")
        except FileNotFoundError as error:
                self.logger.log_error(f"Given file path not found {remote_file_path}\n")
        except Exception as error:
                self.logger.log_error(f"Error occurred due to: {error}\n")