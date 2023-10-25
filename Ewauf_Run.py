from pathlib import Path
import subprocess
import os
import json
from Library.Parser.ConfigParser import Config_Parser
from Library.Utils.Logger import Logger
from Library.Utils.FileHandlingUtils import File_Handling
from jinja2 import Environment, FileSystemLoader
from Library.Utils.BasicUtils import BasicUtils


class Ewauf_Run:
    def __init__(self):
        self.tc = Config_Parser()
        self.list_ = []
        self.creds = self.tc.get_item(Path(__file__).parent / 'Config/dev_config.ini', 'TEST_CASES')
        self.logger = Logger()
        self.utils = BasicUtils()
        self.file = File_Handling()
        self.json_test_data_path = Path(__file__).parent / "json_data_file.json"
        self.souce_directory = Path(__file__).parent / "logs"

    def run_tc(self):
        try:
            self.utils.backup_folders(self.souce_directory)
            if self.creds["tc_all"] != "Yes":
                for TC in self.creds:
                    if self.creds[TC] == "Yes":
                        self.list_ += [TC.upper()]
            else:
                self.list_ += ["TC_ALL"]
            executed_tc = []
            flag = False
            if "TC_ALL" in self.list_:
                for tc in self.creds:
                    executed_tc.append(tc.upper())
                status_code = subprocess.run(['bash', f'./Shell_Executor/{self.list_[-1]}.sh'], check=True)
                file_paths = [f"{Path(__file__).parent / 'logs' / tc_id}.json" for tc_id in executed_tc[:-1]]
                self.file.merge_json_files(self.json_test_data_path, *file_paths)
                for file in file_paths: os.remove(file)
                flag = True

            elif "TC_ALL" not in self.list_:
                for value in self.list_:
                    status_code = subprocess.run(['bash', f'./Shell_Executor/{value}.sh'], check=True)
                    executed_tc.append((value, status_code.returncode))
                file_paths = [f"{Path(__file__).parent / 'logs' / tc_id}.json" for tc_id, status in executed_tc if status == 0]
                self.file.merge_json_files(self.json_test_data_path, *file_paths)
                for file in file_paths: os.remove(file)
                flag = True

            else:
                self.logger.log_error("Something error occured.....")
                flag = False

            if flag:

                data = json.load(open(self.json_test_data_path, "r"))

                total_tc_count = len(data)
                total_pass_count = len([tc_data["result"] for _, tc_data in data.items() if tc_data["result"] == "PASS"])
                total_fail_count = len([tc_data["result"] for _, tc_data in data.items() if tc_data["result"] == "FAIL"])
                total_run_time = round(sum([tc_data["tc_run_time"] for _, tc_data in data.items()]), 2)

                data.update({"TestSuite_Data":
                                 {"total_tc_count": total_tc_count,
                                  "total_pass_count": total_pass_count,
                                  "total_fail_count": total_fail_count,
                                  "total_run_time": total_run_time
                                  }
                             })
                json.dump(data, open(self.json_test_data_path, "w"), indent=4)
            else:
                self.logger.log_error("Unable to update Testsute data to json file")

            f = open('json_data_file.json')
            data = json.load(f)
            total_cases = data['TestSuite_Data']['total_tc_count']
            passed_cases = data['TestSuite_Data']['total_pass_count']
            failed_cases = data['TestSuite_Data']['total_fail_count']
            total_time = data['TestSuite_Data']['total_run_time']
            list_dict_data = []
            for i in data:
                list_dict_data.append(data[i])
            f.close()
            env = Environment(loader=FileSystemLoader('./'))
            template = env.get_template('./report_template.html')
            rendered_template = template.render(test_results=list_dict_data[0:-1], total_test_cases=total_cases,
                                                total_passed=passed_cases, total_failed=failed_cases, total_time=total_time,)
            # Save the rendered HTML to a file
            with open('report.html', 'w') as html_file:
                html_file.write(rendered_template)

        except Exception as e:
            self.logger.log_error(f"Error occured while running testsuite : {e}")


run = Ewauf_Run()
run.run_tc()