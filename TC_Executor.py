from Scripts.TC_Script import TC_Script
from Library.Utils.Logger import Logger
from pathlib import Path


class TC_Executor:

    def __init__(self):
        self.script = TC_Script()
    
    def execute_test_case(self):
        
        # Test case 1
        self.script.start_redmine_service()

        # Test case 2
        self.script.add_and_verify_redmine_users()

        # Test case 3
        self.script.delete_redmine_user()

        # Test case 4
        self.script.convert_xml_to_excel()

        # Test case 5
        self.script.update_xml_file()
        self.script.install_packages()

        # Test case 6
        self.script.create_redmine_project()

        # Test case 7
        self.script.delete_issue_from_redmine()

        # Test case 8
        self.script.log_verify()

        # Test case 9
        self.script.update_convert_excel_to_xml_file()

        # TEST CASE 10
        self.script.delete_redmine_project()

        #Test case 11
        self.script.create_and_write_excel_sheet()

        #Test case 12:
        self.script.update_merge_json()

         #Test case 13
        self.script.delete_excel_sheet()

        #Test case 14
        self.script.verify_and_remove_json_key()



