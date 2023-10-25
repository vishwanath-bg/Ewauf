from Library.Parser.SSH_Command_Parser import SSH_Parser, Path
from Library.Utils.ServerUtils import ServerUtils
from Library.Utils.RedmineUserUtils import RedmineUserUtils
from Library.Parser.XML_Parser import XML_Parser
from Library.Utils.FileHandlingUtils import File_Handling
from Library.Parser.Excel_Parser import Excel_Parser
from Library.Utils.BasicUtils import BasicUtils
import os
import time
import datetime
from pathlib import Path
from Library.Parser.ConfigParser import Config_Parser
import Config.setup_variables as var
from Library.Utils.Logger import Logger


class TC_Script:

    def __init__(self):
        self.ssh = SSH_Parser()
        self.RUtils = RedmineUserUtils()
        self.return_value = False
        self.service = ServerUtils()
        self.user = RedmineUserUtils()
        self.xml = XML_Parser()
        self.file = File_Handling()
        self.excel = Excel_Parser()
        self.data = Config_Parser()
        self.utils = BasicUtils()
        self.file_creds = self.data.get_item(Path(__file__).parent.parent / 'Config/dev_config.ini',"FILE_DATA")
        self.redmine_creds = self.data.get_item(Path(__file__).parent.parent / 'Config/dev_config.ini',"REDMINE_DATA")
        self.machine_creds = self.data.get_item(Path(__file__).parent.parent / 'Config/dev_config.ini',"MACHINE_DATA")
        self.service_name = self.redmine_creds["service_name"]
        self.add_username = self.redmine_creds["add_user_name"]
        self.del_username = self.redmine_creds["del_user_name"]
        self.remote_xml_path = self.file_creds["remote_xml_path"]
        self.local_xml_path  = self.file_creds["local_xml_path"]
        self.output_excel_path = self.file_creds["output_excel_path"]
        self.x_axis = self.file_creds["x_axis"]
        self.y_axis = self.file_creds["y_axis"]
        self.xml_tag = self.file_creds["xml_tag"]
        self.xml_val = self.file_creds["xml_val"]
        self.occurance = self.file_creds["occurance"]
        self.machine_1 = self.machine_creds["machine_1"]
        self.machine_2 = self.machine_creds["machine_2"]
        self.machine_3 = self.machine_creds["machine_3"]
        self.nested_machine = self.machine_creds["nested_machine"]
        self.local_install_path = self.file_creds["local_install_path"]
        self.remote_install_path = self.file_creds["remote_install_path"]
        self.verify_log_path = self.file_creds["verify_log_path"]
        self.local_excel_path = self.file_creds["local_excel_path"]
        self.output_xml_path = self.file_creds["output_xml_path"]
        self.tc9_sheet = self.file_creds["tc9_sheet"]
        self.tc11_sheet = self.file_creds["tc11_sheet"]
        self.remote_json_path = self.file_creds["remote_json_path"]
        self.local_json_path  = self.file_creds["local_json_path"]
        self.output_json_path = self.file_creds["output_json_path"]
        self.input_json_file = self.file_creds["input_json_file"]
        self.remote_json_path2 = self.file_creds["remote_json_path2"]
        self.add_project_name = self.redmine_creds["add_project_name"]
        self.del_project_name = self.redmine_creds["del_project_name"]
        self.project_identifier = self.redmine_creds["project_identifier"]
        self.project_description = self.redmine_creds["project_description"]
        self.del_issue_id = int(self.redmine_creds["del_issue_id"])
        self.project_name = self.redmine_creds["project_name"]
        self.tracker_name = self.redmine_creds["tracker_name"]
        self.subject = self.redmine_creds["subject"]
        self.description = self.redmine_creds["description"]
        self.status = self.redmine_creds["status"]
        self.priority = self.redmine_creds["priority"]
        self.assignee = self.redmine_creds["assignee"]
        self.tc_status = None
        self.remarks = None
        self.log_file_path = str(Path(__file__).parent.parent) + "/logs/log_"+str(datetime.date.today().strftime('%d_%m_%Y'))+"/TC_Script.log"

       
    def start_redmine_service(self):
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger("START REDMINE SERVICE","TC_1")
        if self.service.docker_start_service(self.service_name):
            self.tc_status = "PASS"
            print("TEST CASE TC_1 : PASS")
        else:
            self.tc_status = "FAIL"
            print("TEST CASE TC_1 : FAIL")
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)

        self.remarks = self.utils.Log_parse("TC_1")
        self.utils.testrun_data("TC_1", "START REDMINE SERVICE", self.tc_status, self.remarks, tc_runtime, time_stamp, self.log_file_path)

    def add_and_verify_redmine_users(self):
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger('CREATE AND VERIFY REDMINE USER','TC_2')
        output = self.RUtils.docker_redmine_get_users(self.service_name)
        if output:
            if self.add_username not in output:
                if self.RUtils.docker_redmine_add_users(self.service_name, self.add_username, self.add_username + '@123', self.add_username, 'dummy', self.add_username + '@gmail.com'):
                    print("TEST CASE TC_2 : PASS")
                    self.tc_status = "PASS"
                else:
                    print("TEST CASE TC_2 : FAIL")
                    self.tc_status = "FAIL"
            else:
                if self.user.delete_redmine_user_by_username(self.add_username):
                    if self.RUtils.docker_redmine_add_users(self.service_name, self.add_username, self.add_username + '@123', self.add_username, 'dummy', self.add_username + '@gmail.com'):
                        print("TEST CASE TC_2 : PASS")
                        self.tc_status = "PASS"
                    else:
                        print("TEST CASE TC_2 : FAIL")
                        self.tc_status = "FAIL"
                else:
                        print("TEST CASE TC_2 : FAIL")
                        self.tc_status = "FAIL"
        else:
            print("TEST CASE TC_2 : FAIL")
            self.tc_status = "FAIL"
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)

        remarks = self.utils.Log_parse("TC_2")
        self.utils.testrun_data("TC_2", "CREATE AND VERIFY REDMINE USER", self.tc_status, remarks, tc_runtime, time_stamp,self.log_file_path)

    def delete_redmine_user(self):
        """This method deletes an user from redmine if there exists else it creates the user and then
           deletes it
        """
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger("DELETE REDMINE USER","TC_3")
        output = self.RUtils.docker_redmine_get_users(self.service_name)
        if output:
            if self.del_username in output:
                if self.user.delete_redmine_user_by_username(self.del_username):
                    print("TEST CASE TC_3 : PASS")
                    self.tc_status = "PASS"
                else:
                    print("TEST CASE TC_3 : FAIL")
                    self.tc_status = "FAIL"
            else:
                if self.RUtils.docker_redmine_add_users(self.service_name, self.del_username, self.del_username + '@123',
                                                    self.del_username, 'dummy', self.del_username + '@gmail.com'):
                    if self.user.delete_redmine_user_by_username(self.del_username):
                        print("TEST CASE TC_3 : PASS")
                        self.tc_status = "PASS"
                    else:
                        print("TEST CASE TC_3 : FAIL")
                        self.tc_status = "FAIL"
                else:
                    print("TEST CASE TC_3 : FAIL")
                    self.tc_status = "FAIL"             
        else:
            print("TEST CASE TC_3 : FAIL")
            self.tc_status = "FAIL"
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)

        self.remarks = self.utils.Log_parse("TC_3")
        self.utils.testrun_data("TC_3", "DELETE REDMINE USER", self.tc_status, self.remarks, tc_runtime, time_stamp,self.log_file_path)

    def get_xml_file(self,remote_path,local_path):
        """ This method downloads the xml file from remote redmine server
            :param remote_path : specify remote/server file path/location of redmine
            :param local_file_path: specify local/host path where file should be downloaded
            :return : local path where downloaded xml file has been saved
        """
        if self.file.file_download(remote_path, local_path):
            # self.Log.log_info("The xml file from redmine has been successfully downloaded... ")
            return local_path
        else:
            return False


    def convert_xml_to_excel(self):
        """
            This method helps in converting the Xml file to Excel file
            :param remote_path : specify the path of xml file in the remote machine
            :param local_path: local path where xml file to be saved
            :param output_excel_file : specifies  path where excel file should be placed
            :param x_axis: x-axis to be plotted
            :param y_axis: y-axis to be plotted
        """
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger("PLOTTING GRAPH","TC_4")
        file_path = self.get_xml_file(self.remote_xml_path, Path(__file__).parent.parent / self.local_xml_path)
        if file_path:
            if self.xml.plotgraphfromexcel(self.x_axis, self.y_axis, file_path, Path(__file__).parent.parent / self.output_excel_path):
                print("TEST CASE TC_4 : PASS ")
                self.tc_status = "PASS"
            else:
                print("TEST CASE TC_4 : FAIL")
                self.tc_status = "FAIL"
        else:
            print("TEST CASE TC_4 : FAIL ")
            self.tc_status = "FAIL"
        self.remarks = self.utils.Log_parse("TC_4")
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)
        self.utils.testrun_data("TC_4", "PLOTTING GRAPH", self.tc_status, self.remarks, tc_runtime, time_stamp,self.log_file_path)

    def update_xml_file(self):
        """
            This method will update xml file present in remote machine
            :param local_file_path: specify local/host path where file should be downloaded
            :param remote_file_path: specify remote/server file path/location
            :param machine: specify machine name 
            :param tag_id: specify tag name in xml file
            :param new_value: Specify new value for tag
            :param occurance: Specify which occurance should get change in integer or string numbers
        """
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger("UPDATE XML FILE IN MACHINE-C", "TC_5.1")
        local_file_path = Path(__file__).parent.parent / f'Data_resources/{os.path.basename(self.remote_xml_path)}'
        # Download file from remote machine
        if self.file.file_download(self.remote_xml_path, local_file_path, machine=self.machine_3):

            # Update xml file
            if self.xml.update_tag_values(local_file_path, self.xml_tag, self.xml_val, self.occurance):
                # Upload updated xml file in remote machine
                if self.file.upload_file(local_file_path, self.remote_xml_path, machine=self.machine_3):
                    print("TEST CASE TC_5.1 : PASS")
                    self.tc_status = "PASS"
                else:
                  print("TEST CASE TC_5.1 : FAIL")
                  self.tc_status = "FAIL"
            else:
                print("TEST CASE TC_5.1 : FAIL")
                self.tc_status = "FAIL"
        else:
            print("TEST CASE TC_5.1 : FAIL")
            self.tc_status = "FAIL"
        self.remarks = self.utils.Log_parse("TC_5.1")
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)
        self.utils.testrun_data("TC_5.1", "UPDATE XML FILE IN MACHINE-C", self.tc_status, self.remarks, tc_runtime, time_stamp,self.log_file_path)

    def install_packages(self):
        """
            This method helps in installing system packages on specified machine via SSH connection.
            Can also handle single & nested SSH connections, based on machine counts(1 or [2, 1, 3])
            :param local_path: local host/machine file path
            :param remote_path: remote/server machine file path
            :param machines: specify variable number of machines(numbers) combinations (ex: 2, 3, 1...)
        """
        # check single or nested SSH connection
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger("INSTALL SYSTEM PACKAGES", "TC_5.2")
        machines = ''.join(self.nested_machine) if len(self.nested_machine) == 1 else self.nested_machine.split(',')
        client = self.ssh.nested_ssh(*machines) if len(machines) > 1 else self.ssh.connect_to_server(machines)
        if client:
            # uploading the file
            if self.file.upload_file(self.local_install_path, self.remote_install_path, client=client):
                # converting & running the file
                self.file.dos_to_unix( self.remote_install_path, client=client)
                run_result = self.ssh.sudo_access(f'bash {self.remote_install_path}', client=client)
                if run_result:
                    print("TEST CASE TC_5.2 : PASS")
                    self.tc_status = "PASS"
                else:
                    print("TEST CASE TC_5.2 : FAIL")
                    self.tc_status = "FAIL"
            else:
                print("TEST CASE TC_5.2 : FAIL")
                self.tc_status = "FAIL"
        else:
            print("TEST CASE TC_5.2 : FAIL")
            self.tc_status = "FAIL"
        self.remarks = self.utils.Log_parse("TC_5.2")
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)
        self.utils.testrun_data("TC_5.2", "INSTALL SYSTEM PACKAGES", self.tc_status, self.remarks, tc_runtime, time_stamp,self.log_file_path)


    def create_redmine_project(self):
        """This testcase will create a specified project in the redmine server
        :param service_name: specifies service name to be created
        :param project_name: specifies project name
        :param identifier: specifies project identifier
        :param description: specifies description of project
        """
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger('CREATING PROJECT IN REDMINE','TC_6')
        output = self.RUtils.docker_redmine_get_project_identifiers(self.service_name)
        if output:
            if self.project_identifier in output:
                if self.RUtils.docker_redmine_delete_project_by_project_identifier(self.service_name,self.project_identifier):
                    if self.RUtils.docker_redmine_add_project(self.service_name,self.add_project_name , self.project_identifier, self.project_description):
                        print("TEST CASE TC_6 : PASS")
                        self.tc_status = "PASS"
                    else:
                        print("TEST CASE TC_6 : FAIL")
                        self.tc_status = "FAIL"
                else:
                    print("TEST CASE TC_6 : FAIL")
                    self.tc_status = "FAIL"
            else:
                if self.RUtils.docker_redmine_add_project(self.service_name,self.add_project_name , self.project_identifier, self.project_description):
                    print("TEST CASE TC_6 : PASS")
                    self.tc_status = "PASS"
                else:
                    print("TEST CASE TC_6 : FAIL")
                    self.tc_status = "FAIL"
        else:
            print("TEST CASE TC_6 : FAIL")
            self.tc_status = "FAIL"
        self.remarks = self.utils.Log_parse("TC_6")
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)
        self.utils.testrun_data("TC_6", "CREATING PROJECT IN REDMINE", self.tc_status, self.remarks, tc_runtime, time_stamp,self.log_file_path)


    def delete_issue_from_redmine(self):
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger('DELETE ISSUE IN REDMINE','TC_7')
        output = self.RUtils.get_redmine_all_issue_id()
        if output:
            if self.del_issue_id in output:
                if self.RUtils.docker_redmine_delete_issue(self.service_name, self.del_issue_id):
                    print("TEST CASE TC_7 : PASS")
                    self.tc_status = "PASS"
                else:
                    print("TEST CASE TC_7 : FAIL")
                    self.tc_status = "FAIL"
            else: 
                if self.RUtils.add_issue_to_redmine_project(self.service_name,self.project_name,self.tracker_name,self.subject,self.description, self.status,self.priority,self.assignee):
                    if self.RUtils.docker_redmine_delete_issue(self.service_name, self.del_issue_id):
                        print("TEST CASE TC_7 : PASS")
                        self.tc_status = "PASS"
                    else:
                        print("TEST CASE TC_7 : FAIL")
                        self.tc_status = "FAIL"
                else:
                    print("TEST CASE TC_7 : FAIL")
                    self.tc_status = "FAIL"
        else:
            print("TEST CASE TC_7 : FAIL")
            self.tc_status = "FAIL"
        self.remarks = self.utils.Log_parse("TC_7")
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)
        self.utils.testrun_data("TC_7", "DELETE ISSUE IN REDMINE", self.tc_status, self.remarks, tc_runtime, time_stamp,self.log_file_path)

           
    def log_verify(self):
        """
            This method helps in finding string in log file present or not
            :param file_path : specify  path of log file to be converted
            :param search_data : specifies single string or multiple string to be searched in log file
        """
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger("VERIFY LOGS","TC_8")
        if self.file.verify_logs(self.verify_log_path, var.search_data):
            print("TEST CASE TC_8: PASS")
            self.tc_status = "PASS"
        else:
            print("TEST CASE TC_8 : FAIL")
            self.tc_status = "FAIL"
        self.remarks = self.utils.Log_parse("TC_8")
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)
        self.utils.testrun_data("TC_8", "VERIFY LOGS", self.tc_status, self.remarks, tc_runtime, time_stamp,self.log_file_path)

    def update_convert_excel_to_xml_file(self):
        """
            Testcase for updating Excel file values and converting Excel to XML.
        """
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        machine = self.machine_2
        Logger('UPDATE EXCEL & CONVERT EXCEL TO XML', 'TC_9')
        if machine == None:
            if self.excel.update_excel(self.local_excel_path, self.tc9_sheet, var.cell_values) and self.excel.excel_to_xml(self.local_excel_path, self.tc9_sheet,
                                                                                                   self.output_xml_path):
                print("TEST CASE TC_9 : PASS")
                self.tc_status = "PASS"
            else:
                print("TEST CASE TC_9 : FAIL")
                self.tc_status = "FAIL"
        else:
            local_excel_file = Path(__file__).parent.parent / f'Data_resources/{os.path.basename(self.local_excel_path)}'
            local_xml_file = Path(__file__).parent.parent / f'Data_resources/{os.path.basename(self.output_xml_path)}'

            client = self.ssh.connect_to_server(machine=machine)
            # excel file download, update, conversion & upload
            if client and self.file.file_download(self.local_excel_path, local_excel_file,
                                                  client=client) and self.excel.update_excel(local_excel_file, self.tc9_sheet,
                                                                                             var.cell_values):
                if self.excel.excel_to_xml(local_excel_file, self.tc9_sheet, local_xml_file) and self.file.upload_file(
                        local_xml_file, self.output_xml_path, client=client):
                    print("TEST CASE TC_9 : PASS")
                    self.tc_status = "PASS"
                else:
                    print("TEST CASE TC_9 : FAIL")
                    self.tc_status = "FAIL"
            else:
                print("TEST CASE TC_9 : FAIL")
                self.tc_status = "FAIL"
        self.remarks = self.utils.Log_parse("TC_9")
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)
        self.utils.testrun_data("TC_9", "UPDATE EXCEL & CONVERT EXCEL TO XML", self.tc_status, self.remarks, tc_runtime, time_stamp,self.log_file_path)


    def delete_redmine_project(self):
        """
            This method deletes specified project from the redmine server and verifies it
            :param service: service name to be deleted
            :param project_name: project name of the project to be deleted
        """
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger('DELETE PROJECT IN REDMINE','TC_10')
        output = self.RUtils.docker_redmine_get_project_identifiers(self.service_name)
        if output:
            if self.project_identifier in output:
                if self.RUtils.docker_redmine_delete_project_by_project_identifier(self.service_name,self.project_identifier):
                    print("TEST CASE TC_10 : PASS")
                    self.tc_status = "PASS"
                else:
                    print("TEST CASE TC_10 : FAIL")
                    self.tc_status = "FAIL"
            else:
                if self.RUtils.docker_redmine_add_project(self.service_name, self.del_project_name, self.project_identifier, self.project_description):
                    if self.RUtils.docker_redmine_delete_project_by_project_identifier(self.service_name,self.project_identifier):
                        print("TEST CASE TC_10 : PASS")
                        self.tc_status = "PASS"
                    else:
                        print("TEST CASE TC_10 : FAIL")
                        self.tc_status = "FAIL"
                else:
                    print("TEST CASE TC_10 : FAIL")
                    self.tc_status = "FAIL"
        else:
            print("TEST CASE TC_10 : FAIL")
            self.tc_status = "FAIL"
        self.remarks = self.utils.Log_parse("TC_10")
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)
        self.utils.testrun_data("TC_10", "DELETE PROJECT IN REDMINE", self.tc_status, self.remarks, tc_runtime, time_stamp,self.log_file_path)

    def create_and_write_excel_sheet(self):
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger("CREATE EXCEL SHEET AND WRITE DATA","TC_11")
        machine = self.machine_1
        excel_file = self.ssh.get_file_open_client(self.local_excel_path, 'rb+', machine)

        if excel_file:
            sheets = self.excel.get_sheets(excel_file)
            if sheets:
                if self.tc11_sheet in sheets:
                    if self.excel.delete_sheet(excel_file, self.tc11_sheet) and self.excel.create_sheet(excel_file, self.tc11_sheet):
                        if self.excel.write_file(excel_file, self.tc11_sheet, var.headers, var.excel_data):
                            print("TEST CASE TC_11 : PASS")
                            self.tc_status = "PASS"
                        else:
                            print("TEST CASE TC_11 : FAIL")
                            self.tc_status = "FAIL"
                    else:
                        print("TEST CASE TC_11 : FAIL")
                        self.tc_status = "FAIL"
                else:
                    if self.excel.create_sheet(excel_file, self.tc11_sheet):
                        if self.excel.write_file(excel_file, self.tc11_sheet, var.headers, var.excel_data):
                            print("TEST CASE TC_11 : PASS")
                            self.tc_status = "PASS"
                        else:
                            print("TEST CASE TC_11 : FAIL")
                            self.tc_status = "FAIL"
                    else:
                        print("TEST CASE TC_11 : FAIL")
                        self.tc_status = "FAIL"
            else:
                print("TEST CASE TC_11 : FAIL")
                self.tc_status = "FAIL"
    
        else:
            print("TEST CASE TC_11 : FAIL")
            self.tc_status = "FAIL"
        self.remarks = self.utils.Log_parse("TC_11")
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)
        self.utils.testrun_data("TC_11", "CREATE EXCEL SHEET AND WRITE DATA", self.tc_status, self.remarks, tc_runtime, time_stamp,self.log_file_path)


    def update_merge_json(self):
        """
            This testcase updates an specified json file in the remote machine and merge it with
            existing sample json file in the host machine.
            :param remote_path : path of json file placed in the remote machine
            :param local_path : path of json file in the local machine
        """
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger("MERGE REMOTE JSON TO HOST JSON", "TC_12")
        self.local_json_path = Path(__file__).parent.parent / self.local_json_path
        self.input_json_file = Path(__file__).parent.parent / self.input_json_file
        self.output_json_path = Path(__file__).parent.parent / self.output_json_path

        if self.file.file_download(self.remote_json_path, self.local_json_path):
            if self.file.merge_json_files(self.output_json_path, self.local_json_path, self.input_json_file):
                print("TEST CASE TC_12 : PASS")
                self.tc_status = "PASS"
            else:
               print("TEST CASE TC_12 : FAIL")
               self.tc_status = "FAIL"
        else:
            print("TEST CASE TC_12 : FAIL")
            self.tc_status = "FAIL"
        self.remarks = self.utils.Log_parse("TC_12")
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)
        self.utils.testrun_data("TC_12", "MERGE REMOTE JSON TO HOST JSON", self.tc_status, self.remarks, tc_runtime, time_stamp,self.log_file_path)

    def delete_excel_sheet(self):
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger("DELETE EXCEL SHEET ", "TC_13")
        machine = self.machine_1
        excel_file = self.ssh.get_file_open_client(self.local_excel_path, 'rb+', machine)
        if excel_file:
            sheets = self.excel.get_sheets(excel_file)
            if sheets:
                if self.tc11_sheet in sheets:
                    if self.excel.delete_sheet(excel_file, self.tc11_sheet):
                        print("TEST CASE TC_13 : PASS")
                        self.tc_status = "PASS"
                    else:
                        print("TEST CASE TC_13 : FAIL")
                        self.tc_status = "FAIL"
                else:
                    if self.excel.create_sheet(excel_file, self.tc11_sheet):
                        if self.excel.delete_sheet(excel_file, self.tc11_sheet):
                            print("TEST CASE TC_13 : PASS")
                            self.tc_status = "PASS"
                        else:
                            print("TEST CASE TC_13 : FAIL")
                            self.tc_status = "FAIL"
                    else:      
                        print("TEST CASE TC_13 : FAIL")
                        self.tc_status = "FAIL"
            else:      
                print("TEST CASE TC_13 : FAIL")
                self.tc_status = "FAIL"
        else:
            print("TEST CASE TC_13 : FAIL")
            self.tc_status = "FAIL"
        self.remarks = self.utils.Log_parse("TC_13")
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)
        self.utils.testrun_data("TC_13", "DELETE EXCEL SHEET", self.tc_status, self.remarks, tc_runtime, time_stamp,self.log_file_path)
    
    def verify_and_remove_json_key(self):
        """This method verifies key is present or not and removes specified key from the json file.
            :param file_path: specify  path of log file to be converted
            :param keys_to_remove: specify keys to remove from json file 
        """
        start_time = time.time()
        time_stamp = datetime.datetime.now().strftime('%I:%M:%S%p on %B %d, %Y')
        Logger("VERIFY AND REMOVE JSON KEY","TC_14")
        machine = self.machine_1
        local_file_path = Path(__file__).parent.parent / f'Data_resources/{os.path.basename(self.remote_json_path2)}'
        # Download file from remote machine
        if self.file.file_download(self.remote_json_path2, local_file_path, machine=machine):
            if self.utils.verify_key(local_file_path,var.json_key):
            # Remove key from Json file
                if self.file.remove_key_from_json(local_file_path, var.json_key):
                    # Upload updated xml file in remote machine
                    if self.file.upload_file(local_file_path, self.remote_json_path2, machine=machine):
                        os.remove(local_file_path)
                        # self.file.write_json_file(local_file_path, json_data)
                        # self.file.upload_file(local_file_path, self.remote_json_path2)
                        print("TEST CASE TC_14 : PASS")
                        self.tc_status = "PASS"
                    else:
                        print("TEST CASE TC_14 : FAIL")
                        self.tc_status = "FAIL"
                else:
                    print("TEST CASE TC_14 : FAIL")
                    self.tc_status = "FAIL"
            else:
                if self.file.update_json_file(local_file_path,var.json_data):

                    if self.file.remove_key_from_json(local_file_path, var.json_key):
                        
                        if self.file.upload_file(local_file_path, self.remote_json_path2, machine=machine):
                            os.remove(local_file_path)
                            print("TEST CASE TC_14 : PASS")
                            self.tc_status = "PASS"
                        else:
                            print("TEST CASE TC_14 : FAIL")
                            self.tc_status = "FAIL"
                    else:
                        print("TEST CASE TC_14 : FAIL")
                        self.tc_status = "FAIL"
                else:
                    print("TEST CASE TC_14 : FAIL")
                    self.tc_status = "FAIL"
        else:
            print("TEST CASE TC_14 : FAIL")
            self.tc_status = "FAIL"
        self.remarks = self.utils.Log_parse("TC_14")
        end_time = time.time()
        tc_runtime = round(end_time - start_time, 2)
        self.utils.testrun_data("TC_14", "VERIFY AND REMOVE JSON KEY", self.tc_status, self.remarks, tc_runtime, time_stamp,self.log_file_path)