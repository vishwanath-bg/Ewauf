__author__ = 'Chinmayee P S'

from Library.Parser.SSH_Command_Parser import SSH_Parser
from Library.Parser.ConfigParser import Config_Parser
from Library.Utils.ServerUtils import ServerUtils
from Library.Utils.Logger import Logger
from pathlib import Path
import requests
import re


class RedmineUserUtils:
    """
    This script is redmine specific 
    These libraries are helpful for interacting with redmine users.

    class RedmineUserUtils:
            def docker_redmine_add_users 
            def docker_redmine_delete_users 
            def docker_redmine_get_users 
            def docker_redmine_get_project_names
            def docker_redmine_get_project_identifiers
            def docker_redmine_get_projects 
            def docker_redmine_get_project_identifier_by_project_name
            def docker_redmine_add_project 
            def docker_redmine_delete_project
            def docker_redmine_delete_project_by_project_identifier
            def docker_redmine_get_issues_by_project_identifier
            def docker_redmine_get_issue_by_issue_id
            def docker_redmine_delete_issue

            def create_redmine_user  
            def get_user_id_by_username 
            def delete_redmine_user_by_username 
            def delete_redmine_user_by_userid 
            def get_redmine_users 
            def update_redmine_user 
            def get_user_data_by_id 
            def get_redmine_projects 
            def get_redmine_project_by_id 
            def create_redmine_project 
            def get_redmine_project_identifiers
            def get_project_identifier_by_project_name
            def delete_redmine_project
            def delete_redmine_project_by_project_identifier 
            def get_redmine_issues_by_project_id
            def get_redmine_issues
            def get_redmine_issue_by_id    
            def delete_redmine_issue      

    """

    def __init__(self):
        self.ssh = SSH_Parser()
        self.data = Config_Parser()
        self.service = ServerUtils()
        self.creds = self.data.get_item(
            Path(__file__).parent.parent.parent / 'Config/Config.ini', "REDMINE")
        self.logger = Logger()

    def docker_redmine_add_users(self, service_name, username, password, firstname, lastname, mail):
        """
            This function adds a new user in redmine, installed using docker
            :param service_name: This parameter is the service name of redmine
            :param username : This parameter is the name of the user to be created
            :param password : This parameter is the password of the user to be created
            :param firstname : This parameter is the firstname of the user to be created
            :param lastname : This parameter is the lastname of the user to be created

        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                self.logger.log_info(f"{service_name} service is running...")
                if self.ssh.connect_to_server():
                    command = f"sudo docker exec {service_name} bundle exec rails runner \"User.create!(login: '{username}', firstname: '{firstname}', lastname: '{lastname}', mail: '{mail}', password: '{password}', password_confirmation: '{password}', admin: false)\""
                    stdin, stdout, stderr = self.ssh.client.exec_command(command
                                                                         )
                    error = stderr.read().decode().splitlines()[:2]
                    if error:
                        self.logger.log_error(
                            f'Problem occurred while running COMMAND : {command}\nError message: {error}\n')
                        return False
                    else:
                        self.logger.log_info(
                            f'---- command execution completed ----\n')
                        if username in self.docker_redmine_verify_users(service_name):
                            self.logger.log_info(
                                f"User: {username} added SUCCESSFULLY\n")
                            return True
                        else:
                            self.logger.log_error(
                                f"Failed to add User: {username}\n")
                            return False
            elif not flag and flag != None:
                self.logger.log_error(
                    f"The {service_name} service is currently not running\nPlease start the service\n")
                return False
        except Exception as e:
            self.logger.log_error(f"Error occured while adding users:{e}\n")
            return False

    def docker_redmine_delete_users(self, service_name, username):
        """
            This function deletes existing user in redmine, installed using docker
            :param service_name : This parameter is the service name of redmine
            :param username : This parameter is the name of the user to be deleted
        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                self.logger.log_info(f"{service_name} service is running...")
                if self.ssh.connect_to_server():
                    command = f"sudo docker exec {service_name} bundle exec rails runner \"User.find_by(login: '{username}')&.destroy\""
                    stdin, stdout, stderr = self.ssh.client.exec_command(command
                                                                         )
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(
                            f'Problem occurred while running COMMAND : {command}\nError message: {error}\n')
                        return False
                    else:
                        self.logger.log_info(
                            f'---- command execution completed ----\n')
                        if username not in self.docker_redmine_verify_users(service_name):
                            self.logger.log_info(
                                f"User: {username} deleted SUCCESSFULLY\n")
                            return True
                        else:
                            self.logger.log_error(
                                f"Failed to delete User: {username}\n")
                            return False

            elif not flag and flag != None:
                self.logger.log_error(
                    f"The {service_name} service is currently not running\nPlease start the service\n")
                return False
        except Exception as e:
            self.logger.log_error(f"Error occured while deleting users:{e}\n")
            return False

    def docker_redmine_verify_users(self, service_name):
        """
            This is an extension function
            This function returns the users of redmine service, installed using docker
            :param service_name : This parameter is the service name of redmine
            :return : returns all users of redmine
        """
        try:
            command = f"sudo docker exec {service_name} bundle exec rails runner 'puts User.pluck(:login)'"
            stdin, stdout, stderr = self.ssh.client.exec_command(command
                                                                 )
            result = stdout.read().decode()
            error = stderr.read().decode()
            if error:
                self.logger.log_error(
                    f'Problem occurred while running command : \nError message: {error}\n')
                return False
            else:
                return result
        except Exception as e:
            self.logger.log_error(f"Error occured while verifying users:{e}\n")
            return False

    def docker_redmine_get_users(self, service_name):
        """
            This function returns the users of redmine service, installed using docker
            :param service_name : This parameter is the service name of redmine
            :return : returns all users of redmine
        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                if self.ssh.connect_to_server():
                    command = f"sudo docker exec {service_name} bundle exec rails runner 'puts User.pluck(:login)'"
                    stdin, stdout, stderr = self.ssh.client.exec_command(
                        command)
                    exit_status = stdout.channel.recv_exit_status()
                    result = stdout.read().decode()
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(
                            f'Problem occurred while running command : \nError message: {error}\n')
                        return False
                    elif exit_status != 0:
                        self.logger.log_error(f'No users found')
                        return None
                    else:
                        self.logger.log_info(
                            f'---- command execution completed ----\n')
                        return result
            elif not flag and flag != None:
                self.logger.log_error(
                    f"The {service_name} service is currently not running\nPlease start the service\n")
                return False

        except Exception as e:
            self.logger.log_error(f"Error occured while fetching users:{e}\n")
            return False

    def docker_redmine_get_project_names(self, service_name):
        """
        This function return list of project names from the Redmine service, installed using Docker
        :param service_name: The name of the Redmine service
        :return: A list of project names if successfull
        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                if self.ssh.connect_to_server():
                    command = f"sudo docker exec {service_name} bundle exec rails runner 'puts Project.pluck(:name)'"
                    stdin, stdout, stderr = self.ssh.client.exec_command(
                        command)
                    exit_status = stdout.channel.recv_exit_status()
                    result = stdout.read().decode()
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(
                            f'Problem occurred while running command:\nError message: {error}\n')
                        return False
                    elif exit_status != 0:
                        self.logger.log_error(f'No projects found\n')
                        return None
                    else:
                        self.logger.log_info(f'Projects fetched SUCCESSFULLY\n')
                        return result
            elif not flag and flag != None:
                self.logger.log_error(
                    f"The {service_name} service is currently not running\nPlease start the service\n")
                return False
        except Exception as e:
            self.logger.log_error(f"Error occured while fetching projects:{e}\n")
            return False
        

    def docker_redmine_get_project_identifiers(self, service_name):
        """
        This function return list of project identifiers from the Redmine service, installed using Docker
        :param service_name: The name of the Redmine service
        :return: A list of project identifiers if successfull
        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                if self.ssh.connect_to_server():
                    command = f"sudo docker exec {service_name} bundle exec rails runner 'puts Project.pluck(:identifier)'"
                    stdin, stdout, stderr = self.ssh.client.exec_command(
                        command)
                    exit_status = stdout.channel.recv_exit_status()
                    result = stdout.read().decode()
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(
                            f'Problem occurred while running command:\nError message: {error}\n')
                        return False
                    elif exit_status != 0:
                        self.logger.log_error(f'No identifiers found\n')
                        return None
                    else:
                        self.logger.log_info(f'Project identifiers fetched SUCCESSFULLY\n')
                        return result
            elif not flag and flag != None:
                self.logger.log_error(
                    f"The {service_name} service is currently not running\nPlease start the service\n")
                return False
        except Exception as e:
            self.logger.log_error(f"Error occured while fetching identifiers:{e}\n")
            return False
        
    def docker_redmine_verify_project_identifiers(self, service_name):
        """
        This is an extension function 
        This function returns list of project identifiers from the Redmine service, installed using Docker
        :param service_name: The name of the Redmine service
        :return: A list of project identifiers if successfull
        """
        try:
        
            command = f"sudo docker exec {service_name} bundle exec rails runner 'puts Project.pluck(:identifier)'"
            stdin, stdout, stderr = self.ssh.client.exec_command(
                command)
            exit_status = stdout.channel.recv_exit_status()
            result = stdout.read().decode()
            error = stderr.read().decode()
            if error:
                self.logger.log_error(
                    f'Problem occurred while running command:\nError message: {error}\n')
                return False
            elif exit_status != 0:
                self.logger.log_error(f'No identifiers found\n')
                return None
            else:
                self.logger.log_info(f'Project identifiers fetched SUCCESSFULLY\n')
                return result
        except Exception as e:
            self.logger.log_error(f"Error occured while fetching identifiers:{e}\n")
            return False

    def docker_redmine_get_projects(self, service_name):
        """
        This function return list of projects from the Redmine service installed using Docker.
        :param service_name: The name of the Redmine service
        :return: A list of dictionaries representing projects
        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                if self.ssh.connect_to_server():
                    command = f"sudo docker exec {service_name} bundle exec rails runner 'projects = Project.all; puts projects.to_json;'"
                    stdin, stdout, stderr = self.ssh.client.exec_command(
                        command)
                    exit_status = stdout.channel.recv_exit_status()
                    result = stdout.read().decode()
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(
                            f'Problem occurred while running command:\nError message: {error}\n')
                        return False
                    elif exit_status != 0:
                        self.logger.log_error(f'No projects found\n')
                        return None
                    else:
                        self.logger.log_info(f'Projects fetched SUCCESSFULLY\n')
                        return result

            elif not flag and flag != None:
                self.logger.log_error(
                    f"The {service_name} service is currently not running\nPlease start the service\n")
                return False

        except Exception as e:
            self.logger.log_error(f"Error occurred while getting projects:{e}\n")
            return False

    def docker_redmine_get_project_identifier_by_project_name(self, service_name, project_name):
        """
        This function is used to get project identifier using project name from the Redmine service, installed using Docker
        :param service_name: The name of the Redmine service
        :param:project_name: Name of the project
        :return: returns project identifier if successful, None otherwise
        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                if self.ssh.connect_to_server():
                    warning_pattern = re.compile(r'^W, .*? WARN .*?: .*?\.$', re.MULTILINE)
                    command = f"sudo docker exec {service_name} bundle exec rails runner 'project = Project.find_by(name: \"{project_name}\");puts project.identifier'"
                    stdin, stdout, stderr = self.ssh.client.exec_command(
                        command)
                    exit_status = stdout.channel.recv_exit_status()
                    result = stdout.read().decode()
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(
                            f'Problem occurred while running command:\nError message: {error}\n')
                        return False
                    elif exit_status != 0:
                        self.logger.log_error(
                            f"No identifier found for project '{project_name}'\n")
                        return None
                    else:
                        result = re.sub(warning_pattern, '', result).lstrip().rstrip()
                        self.logger.log_info(
                            f'---- command execution completed ----\n')
                        return result
            elif not flag and flag != None:
                self.logger.log_error(
                    f"The {service_name} service is currently not running\nPlease start the service\n")
                return False
        except Exception as e:
            self.logger.log_error(
                f"Error occured while fetching project_identifier:{e}\n")
            return False

    def docker_redmine_verify_projects(self, service_name):
        """
        This is an extension method to verify projects in the Redmine service, installed using Docker
        :param service_name: The name of the Redmine service
        :return: A list of project names if successful, None otherwise
        """
        try:

            command = f"sudo docker exec {service_name} bundle exec rails runner 'puts Project.pluck(:name)'"
            stdin, stdout, stderr = self.ssh.client.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()
            result = stdout.read().decode()
            error = stderr.read().decode()
            if error:
                self.logger.log_error(
                    f'Problem occurred while running command:\nError message: {error}\n')
                return False
            elif exit_status != 0:
                self.logger.log_error(f"No projects found\n")
                return None
            else:
                return result

        except Exception as e:
            self.logger.log_error(
                f"Error occured while verifying projects:{e}\n")
            return False

    def docker_redmine_add_project(self, service_name, project_name, project_identifier, project_description):
        """
        This function adds new project to the redmine service,installed using Docker
        :param service_name: The name of the Redmine service
        :param project_name: The name of the new project
        :param project_identifier: The unique identifier for the new project(String only)
        :param project_description: The description of the new project
        :return: True if project creation is successful, False otherwise
        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                if self.ssh.connect_to_server():
                    command = f"sudo docker exec {service_name} bundle exec rails runner 'Project.create(name: \"{project_name}\", identifier: \"{project_identifier}\", description: \"{project_description}\")'"
                    stdin, stdout, stderr = self.ssh.client.exec_command(
                        command)
                    result = stdout.read().decode()
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(
                            f'Problem occurred while running command:\nError message: {error}\n')
                        return False
                    else:
                        self.logger.log_info(
                            f'---- command execution completed ----\n')
                        projects = self.docker_redmine_verify_projects(
                            service_name)
                        if project_name in projects:
                            self.logger.log_info(
                                f"Project : {project_name} SUCCESSFULLY added\n")
                            return True
                        else:
                            self.logger.log_error("Failed to add project,Project already exists \n")
                            return False

            elif not flag and flag != None:
                self.logger.log_error(
                    f"The {service_name} service is currently not running\nPlease start the service\n")
                return False

        except Exception as e:
            self.logger.log_error(
                f"Error occurred while adding the project:{e}\n")
            return False

    def docker_redmine_delete_project(self, service_name, project_name):
        """
        This function delted project in the redmine service,installed using Docker
        :param service_name: The name of the Redmine service
        :param project_name: Name of the project to be deleted

        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:

                if self.ssh.connect_to_server():
                    projects = self.docker_redmine_verify_projects(
                        service_name)
                    if project_name in projects:
                        command = f"sudo docker exec {service_name} bundle exec rails runner 'Project.find_by(name: \"{project_name}\")&.destroy'"
                        stdin, stdout, stderr = self.ssh.client.exec_command(
                            command)
                        result = stdout.read().decode()
                        error = stderr.read().decode()
                        if error:
                            self.logger.log_error(
                                f'Problem occurred while running command:\nError message: {error}\n')
                            return False
                        else:
                            self.logger.log_info(
                                f'---- command execution completed ----\n')
                            projects = self.docker_redmine_verify_projects(
                                service_name)
                            if project_name in projects:
                                self.logger.log_error(
                                    "Failed to delete project\n")
                                return False
                            else:
                                self.logger.log_info(
                                    f"Project : {project_name} SUCCESSFULLY Deleted\n")
                                return True
                    else:
                        self.logger.log_error(
                            f"Project '{project_name}' doesn't exist please provide valid project name\n")
                        return False
            elif not flag and flag != None:
                self.logger.log_error(
                    f"The {service_name} service is currently not running\nPlease start the service\n")
                return False

        except Exception as e:
            self.logger.log_error(
                f"Error occurred while deleting the project:{e}\n")
            return False
        
    
    def docker_redmine_delete_project_by_project_identifier(self, service_name, project_identifier):
        """
        This function deletes a project in the Redmine service installed using Docker.
        :param service_name: The name of the Redmine service
        :param project_identifier: Identifier of the project to be deleted
        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag is not None:
                if self.ssh.connect_to_server():
                    if project_identifier in self.docker_redmine_verify_project_identifiers(
                        service_name):
                        command = f"sudo docker exec {service_name} bundle exec rails runner 'Project.find_by(identifier: \"{project_identifier}\")&.destroy'"
                        stdin, stdout, stderr = self.ssh.client.exec_command(
                            command)
                        result = stdout.read().decode()
                        error = stderr.read().decode()
                        if error:
                            self.logger.log_error(
                                f'Problem occurred while running command:\nError message: {error}\n')
                            return False
                        else:
                            self.logger.log_info(
                                f'---- Command execution completed ----\n')
                            if project_identifier in self.docker_redmine_verify_project_identifiers(service_name):
                                self.logger.log_error(
                                    "Failed to delete project\n")
                                return False
                            else:
                                self.logger.log_info(
                                    f"Project with identifier '{project_identifier}' SUCCESSFULLY Deleted\n")
                                return True
                    else:
                        self.logger.log_error(
                            f"Project with identifier '{project_identifier}' doesn't exist; please provide a valid project identifier\n")
                        return False
            elif not flag and flag is not None:
                self.logger.log_error(
                    f"The {service_name} service is currently not running\nPlease start the service\n")
                return False

        except Exception as e:
            self.logger.log_error(
                f"Error occurred while deleting the project: {e}\n")
            return False

    def docker_redmine_get_issues_by_project_identifier(self, service_name, project_identifier):
        """
        This function returns a list of issues from a project in the Redmine service installed using Docker, based on the project identifier
        :param service_name: The name of the Redmine service
        :param project_identifier: The unique identifier of the project
        :return: A list of dictionaries representing issues, None otherwise
        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                if self.ssh.connect_to_server():
                    command = f"sudo docker exec {service_name} bundle exec rails runner 'project = Project.find_by(identifier: \"{project_identifier}\");issues = project.issues; puts issues.to_json();'"
                    stdin, stdout, stderr = self.ssh.client.exec_command(
                        command)
                    result = stdout.read().decode()
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(
                            f'Failed to get the issues.\nError message: {error}\n')
                        return None
                    else:
                        self.logger.log_info(
                            f'---- Retrieved issues from project "{project_identifier}" ----\n')
                        return result

            elif not flag and flag != None:
                self.logger.log_error(
                    f"The {service_name} service is currently not running\nPlease start the service\n")
                return False
        except Exception as e:
            self.logger.log_error(
                f"Error occurred while fetching the issues:{e}\n")
            return False

    def docker_redmine_get_issue_by_issue_id(self, service_name, issue_id):
        """
        This function returns issue from a project in the Redmine service installed using Docker, based on the issue_id
        :param service_name: The name of the Redmine service
        :param issue_id: The id of the issue
        :return: A string representing issue, None otherwise
        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                if self.ssh.connect_to_server():
                    command = f"sudo docker exec {service_name} bundle exec rails runner 'issue = Issue.find({issue_id}); puts issue.inspect'"
                    stdin, stdout, stderr = self.ssh.client.exec_command(
                        command)
                    result = stdout.read().decode()
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(
                            f'Failed to get the issue.\nError message: {error}\n')
                        return None
                    else:
                        self.logger.log_info(
                            f'---- Retrieved issue from project with issue_id "{issue_id}" ----\n')
                        return result

            elif not flag and flag != None:
                self.logger.log_error(
                    f"The {service_name} service is currently not running\nPlease start the service\n")
                return False
        except Exception as e:
            self.logger.log_error(
                f"Error occurred while fetching the issue:{e}\n")
            return False

    def docker_redmine_delete_issue(self, service_name, issue_id):
        """
        This Function deletes an issue in Redmine, installed using Docker
        :param service_name: The name of the Redmine service
        :param issue_id: The ID of the issue to be deleted
        :return: True if the issue is deleted successfully, False otherwise
        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                if self.ssh.connect_to_server():
                    command = f"sudo docker exec {service_name} bundle exec rails runner 'Issue.find({issue_id}).destroy'"
                    stdin, stdout, stderr = self.ssh.client.exec_command(
                        command)
                    result = stdout.read().decode()
                    error = stderr.read().decode().splitlines()[:2]
                    if error:
                        self.logger.log_error(
                            f'Failed to delete the issue.\nError message: {error}\n')
                        return None
                    else:
                        present_issues = self.get_redmine_issues()
                        for issue in present_issues:
                            if issue['id'] == issue_id:
                                self.logger.log_info(f'Failed to delete issue with issue_id:{issue_id}\n')
                                return False
                        self.logger.log_info(
                        f'issue with issue_id:{issue_id} SUCCESSFULLY deleted\n')
                        return True

            elif not flag and flag != None:
                self.logger.log_error(
                    f"The {service_name} service is currently not running\nPlease start the service\n")
                return False
        except Exception as e:
            self.logger.log_error(
                f"Error occurred while deleting the issue:{e}\n")
            return False

    def create_redmine_user(self, username, password, firstname, lastname, email):
        """
            This function adds a new user in redmine using Redmine API
            :param username : This parameter is the name of the user to be created
            :param password : This parameter is the password of the user to be created
            :param firstname : This parameter is the firstname of the user to be created
            :param lastname : This parameter is the lastname of the user to be created

        """
        try:
            flag = self.service.check_service_status()
            if flag:
                # creds = self.cdata.get_item(Path(__file__).parent.parent.parent / 'Config/Config.ini', "REDMINE")
                url = f"{self.creds['url']}/users.json"
                headers = {'X-Redmine-API-Key': self.creds['api_key']}
                data = {
                    'user': {
                        'login': username,
                        'password': password,
                        'firstname': firstname,
                        'lastname': lastname,
                        'mail': email
                    }
                }

                response = requests.post(url, json=data, headers=headers)

                if response.status_code == 201:
                    users = self.get_redmine_users()
                    if data['user']['login'] in users:
                        self.logger.log_info(
                            f"User '{username}' SUCCESSFULLY created.\n")
                        return True
                    else:
                        self.logger.log_error("Failed to create user\n")
                        return False
                else:
                    self.logger.log_error(
                        f"Failed to create user. Status code: {response.status_code}, Error: {response.text}\n")
                    return False

            elif not flag:
                self.logger.log_error(
                    f"The redmine service is currently not running\nPlease start the service\n")
                return False

        except Exception as e:
            self.logger.log_error(f"Error occurred while creating user:{e}\n")
            return False

    def get_user_id_by_username(self, username):
        """
            This function returns the user_id of the provided username using redmine API
            :Param username : username of the redmine service
            :return : returns user_id of the user
        """
        try:
            url = f"{self.creds['url']}/users.json?name={username}"
            headers = {'X-Redmine-API-Key': self.creds['api_key']}

            response = requests.get(url, headers=headers)
        
            if response.status_code == 200:
                data = response.json()
                if 'users' in data and len(data['users']) > 0:
                    user_id = data['users'][0]['id']
                    self.logger.log_info(
                        f"User_id with {username} fetched SUCCESSFULLY.\n")
                    return user_id
            return None

        except Exception as e:
            self.logger.log_error(f"Error occurred while fetching user_id:{e}\n")
            return False

    def delete_redmine_user_by_username(self, username):
        """
            This function deletes the user data of the provided username using redmine API
            :Param username : username of the redmine user
        """
        try:
            flag = self.service.check_service_status()
            if flag:
                # creds = self.data.get_item(Path(__file__).parent.parent.parent / 'Config/Config.ini', "REDMINE")
                user_id = self.get_user_id_by_username(username)
                if user_id:
                    url = f"{self.creds['url']}/users/{user_id}.json"
                    headers = {'X-Redmine-API-Key': self.creds['api_key']}

                    response = requests.delete(url, headers=headers)

                    if response.status_code == 204:
                        users = self.get_redmine_users()
                        if username in users:
                            self.logger.log_error("Failed to delete user\n")
                            return False
                        else:
                            self.logger.log_info(
                                f"User '{username}' with ID '{user_id}' SUCCESSFULLY deleted.\n")
                            return True
                    else:
                        self.logger.log_error(
                            f"Failed to delete user. Status code: {response.status_code}, Error: user_id not found\n")
                        return False
                     
                else:
                    self.logger.log_error(
                        f"User with username '{username}' not found.\n")
                    return False
            elif not flag:
                self.logger.log_error(
                    f"The redmine service is currently not running\nPlease start the service\n")
                return False

        except Exception as e:
            self.logger.log_error(f"Error occurred while deleting user:{e}\n")
            return False

    def delete_redmine_user_by_userid(self, user_id):
        """
            This function deletes the user data of the provided user_id using redmine API
            :Param user_id : user_id of the redmine user
        """
        try:
            flag = self.service.check_service_status()
            if flag:
                url = f"{self.creds['url']}/users/{user_id}.json"
                headers = {'X-Redmine-API-Key': self.creds['api_key']}

                response = requests.delete(url, headers=headers)

                if response.status_code == 204:
                    self.logger.log_info(
                        f"User with ID '{user_id}' SUCCESSFULLY deleted.\n")
                    return True
                else:
                    self.logger.log_error(
                        f"Failed to delete user. Status code: {response.status_code}, Error: user_id not found\n")
                    return False

            elif not flag:
                self.logger.log_error(
                    f"The redmine service is currently not running\nPlease start the service\n")
                return False

        except Exception as e:
            self.logger.log_error(f"Error occurred while deleting user:{e}\n")
            return False

    def get_redmine_users(self):
        """
            This function returns the users of the redmine service using redmine API
            :return : returns list of redmine users
        """
        try:
            flag = self.service.check_service_status()
            if flag:
                redmine_users = []
                url = f"{self.creds['url']}/users.json"
                headers = {'X-Redmine-API-Key': self.creds['api_key']}

                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    users_data = response.json()
                    users = users_data.get('users', [])
                    for user in users:
                        redmine_users += [user['login']]
                        # print(f"Username: {user['login']}, Name: {user['firstname']} {user['lastname']}, Email: {user['mail']}")
                    self.logger.log_info(f"Users fetched SUCCESSFULLY\n")
                    return redmine_users
                else:
                    self.logger.log_error(
                        f"Failed to get users. Status code: {response.status_code}, Error: {response.text}\n")
                    return False
            elif not flag:
                self.logger.log_error(
                    f"The redmine service is currently not running\nPlease start the service\n")
                return False

        except Exception as e:
            self.logger.log_error(f"Error occurred while fetching users:{e}\n")
            return False

    def update_redmine_user(self, user_id, user_data):
        """
            This function updates the user data of the provided user_id using redmine API
            :Param user_id : user_id of the redmine user
            :user_data : data to be updated in json formmat ex: {'firstname':'user_name'}
        """

        try:
            flag = self.service.check_service_status()
            if flag and flag != None:
                url = f"{self.creds['url']}/users/{user_id}.json"
                headers = {
                    'X-Redmine-API-Key': self.creds['api_key'],
                    'Content-Type': 'application/json'
                }

                response = requests.put(
                    url, headers=headers, json={'user': user_data})

                if response.status_code == 204:
                    update_flag = False
                    user = self.get_user_data_by_id(user_id)
                    for keys, values in user_data.items():
                        if user[keys] == values:
                            update_flag = True
                        else:
                            update_flag = False
                    if update_flag:
                        self.logger.log_info("User data updated SUCCESSFULLY.\n")
                        return True
                    else:
                        self.logger.log_error("Failed to update user\n")
                        return False
                else:
                    self.logger.log_error(
                        f"Failed to update user. Status code: {response.status_code}, Error: {response.text}\n")
                    return False
            elif not flag:
                self.logger.log_error(
                    f"The redmine service is currently not running\nPlease start the service\n")
                return False

        except KeyError as e:
            self.logger.log_error(f"Key not found:{e}\n")
            return False
        except Exception as e:
            self.logger.log_error(f"Error occurred while updating user:{e}\n")
            return False

    def get_user_data_by_id(self, user_id):
        """
        This function fetches specific user data using the user ID from the Redmine API.
        :param user_id: user_id of the redmine user
        :return: A dictionary containing the user data if the user is found, None otherwise.
        """

        try:
            flag = self.service.check_service_status()
            if flag:
                url = f"{self.creds['url']}/users/{user_id}.json"
                headers = {
                    'X-Redmine-API-Key': self.creds['api_key']
                }

                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    user_data = response.json().get('user', {})
                    self.logger.log_info(
                        f"User data with id:{user_id} fetched SUCCESSFULLY\n")
                    return user_data
                elif response.status_code == 404:
                    self.logger.log_error(f"User with ID {user_id} not found.\n")
                    return False
                else:
                    self.logger.log_error(
                        f"Failed to fetch user data. Status code: {response.status_code}, Error: {response.text}\n")
                    return False

            elif not flag:
                self.logger.log_error(
                    "The Redmine service is currently not running\nPlease start the service.\n")
                return False

        except Exception as e:
            self.logger.log_error(
                f"Error occurred while fetching user data:{e}\n")
            return False

    def get_redmine_projects(self):
        """
            This function fetches the existing projects in redmine using redmine API
            :return : returns list of project information
        """
        try:
            flag = self.service.check_service_status()
            if flag:
                url = f"{self.creds['url']}/projects.json"
                headers = {'X-Redmine-API-Key': self.creds['api_key']}

                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    projects_data = response.json().get('projects', [])
                    self.logger.log_info(f"Projects fetched SUCCESSFULLY\n")
                    return projects_data
                else:
                    self.logger.log_error(
                        f"Failed to get projects. Status code: {response.status_code}, Error: {response.text}\n")
                    return False

            elif not flag:
                self.logger.log_error(
                    "The Redmine service is currently not running\nPlease start the service.\n")
                return False

        except Exception as e:
            self.logger.log_error(
                f"Error occurred while fetching projects:{e}\n")
            return False

    def get_redmine_project_by_id(self, project_id):
        """
            This function fetches the project from the provided project_id in redmine using redmine API
            :param project_id : project_id of the project
            :return : returns project information from the provided project_id in dictionary
        """
        try:
            flag = self.service.check_service_status()
            if flag:
                url = f"{self.creds['url']}/projects/{project_id}.json"
                headers = {'X-Redmine-API-Key': self.creds['api_key']}

                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    project = response.json().get('project', {})
                    self.logger.log_info(
                        f"Project with id:{project_id} fetched SUCCESSFULLY\n")
                    return project
                else:
                    self.logger.log_error(
                        f"Failed to get project information. Status code: {response.status_code}, Error: {response.text}\n")
                    return False

            elif not flag:
                self.logger.log_error(
                    "The Redmine service is currently not running\nPlease start the service.\n")
                return False

        except Exception as e:
            self.logger.log_error(f"Error occurred while fetching project:{e}\n")
            return False

    def create_redmine_project(self, project_name, project_identifier, project_description):
        """
        This function Creates a new project in Redmine using redmine API.
        :param project_name: The name of the new project
        :param project_identifier: The unique identifier for the new project
        :param project_description: The description of the new project
        :return: True if project creation is successful, False otherwise
        """
        projects_endpoint = f"{self.creds['url']}/projects.json"
        headers = {'X-Redmine-API-Key': self.creds['api_key']}
        data = {
            'project': {
                'name': project_name,
                'identifier': project_identifier,
                'description': project_description
            }
        }

        try:
            response = requests.post(
                projects_endpoint, headers=headers, json=data)
            response.raise_for_status()
            if response.status_code == 201:
                res = self.get_redmine_projects()
                for i in range(len(res)):
                    if project_name in res[i]['name']:
                        self.logger.log_info(
                            f'Project "{project_name}" created SUCCESSFULLY.\n')
                        return True
                self.logger.log_error(f'Failed to create the project')
                return False
            else:
                self.logger.log_error(
                    f'Failed to create the project.\nError message: {response.json()}\n')
                return False

        except requests.exceptions.RequestException as e:
            self.logger.log_error(
                f"Error occurred while creating the project:{e}\n")
            return False
    
    def get_redmine_project_identifiers(self):
        """
        This function fetches the existing project identifiers in Redmine using the Redmine API.
        :return: Returns a list of project identifiers.
        """
        try:
            flag = self.service.check_service_status()
            if flag:
                url = f"{self.creds['url']}/projects.json"
                headers = {'X-Redmine-API-Key': self.creds['api_key']}

                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    projects_data = response.json().get('projects', [])
                    project_identifiers = [project.get('identifier') for project in projects_data]
                    self.logger.log_info("Project Identifiers fetched SUCCESSFULLY\n")
                    return project_identifiers
                else:
                    self.logger.log_error(
                        f"Failed to get project identifiers. Status code: {response.status_code}, Error: {response.text}\n")
                    return False

            elif not flag:
                self.logger.log_error(
                    "The Redmine service is currently not running\nPlease start the service.\n")
                return False

        except Exception as e:
            self.logger.log_error(
                f"Error occurred while fetching project identifiers: {e}\n")
            return False

    def get_project_identifier_by_project_name(self, project_name):
        """
        This function gets the project identifier by its name using redmine API.
        :param project_name: The name of the project
        :return: The project identifier if found, None otherwise
        """
        projects_endpoint = f"{self.creds['url']}/projects.json"
        headers = {'X-Redmine-API-Key': self.creds['api_key']}
        params = {'name': project_name}

        try:
            response = requests.get(
                projects_endpoint, headers=headers, params=params)
            response.raise_for_status()

            if response.status_code == 200:
                projects_data = response.json()['projects']
                if projects_data:
                    self.logger.log_info(
                        f'Project identifier with name "{project_name}" fetched SUCCESSFULLY.\n')
                    # Return the ID of the first matching project
                    return projects_data[0]['identifier']
                else:
                    return False

        except requests.exceptions.RequestException as e:
            self.logger.log_error(
                f"Error occurred while fetching projects:{e}\n")
            return False

    def get_project_id_by_project_name(self, project_name):
        """
        This function gets the project ID by its name in Redmine using the API.
        :param project_name: The name of the project for which you want to get the ID
        :return: The project ID if the project is found, or None if the project is not found or there was an error
        """
        projects_endpoint = f"{self.creds['url']}/projects.json"
        headers = {
            'Content-Type': 'application/json',
            'X-Redmine-API-Key': self.creds['api_key']
        }

        params = {
            'name': project_name
        }

        try:
            response = requests.get(
                projects_endpoint, params=params, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                projects_data = response.json()
                projects = projects_data.get('projects')
                if projects:
                    self.logger.log_info(
                        f'Project_id with name "{project_name}" fetched SUCCESSFULLY.\n')
                    # Assuming there is only one project with the given identifier
                    return projects[0]['id']

            self.logger.log_error(f"Project '{project_name}' not found.\n")
            return None

        except requests.exceptions.RequestException as e:
            self.logger.log_error(
                f"Error occurred while fetching projects:{e}\n")
            return False
        
    def delete_redmine_project(self, project_name):
        """
        This function deletes a project in Redmine using the Redmine API.
        :param project_name: The name of the project to delete
        :return: True if project deletion is successful, False otherwise
        """

        project_endpoint = f"{self.creds['url']}/projects/{project_name}.json"
        headers = {'X-Redmine-API-Key': self.creds['api_key']}

        try:
            response = requests.delete(project_endpoint, headers=headers)
            response.raise_for_status()
            if response.status_code == 204:
                res = self.get_redmine_projects()
                for project in res:
                    if project_name != project['name']:
                        self.logger.log_info(
                            f"Project '{project_name}' has been deleted.\n")
                        return True
                self.logger.log_error(f"Failed to delete the project\n")
                return False
            else:
                self.logger.log_error(
                    f"Failed to delete the project.\nError message: {response.json()}\n")
                return False

        except requests.exceptions.RequestException as e:
            self.logger.log_error(
                f"Error occurred while deleting the project: {e}\n")
            return False

    def delete_redmine_project_by_project_identifier(self, project_identifier):
        """
        This function deletes project in Redmine using redmine API.
        :param project_identifier: The unique identifier of the project to delete
        :return: True if project deletion is successful, False otherwise
        """

        project_endpoint = f"{self.creds['url']}/projects/{project_identifier}.json"
        headers = {'X-Redmine-API-Key': self.creds['api_key']}

        try:
            response = requests.delete(project_endpoint, headers=headers)
            response.raise_for_status()
            if response.status_code == 204:
                res = self.get_redmine_projects()
                for i in range(len(res)):
                    if project_identifier not in res[i]['identifier']:
                        self.logger.log_info(
                            f"Project with identifier '{project_identifier}' has been deleted.\n")
                        return True
                self.logger.log_error(f"Failed to delete the project\n")
                return False
            else:
                self.logger.log_error(
                    f"Failed to delete the project.\nError message: {response.json()}\n")
                return False

        except requests.exceptions.RequestException as e:
            self.logger.log_error(
                f"Error occurred while deleting the project:{e}\n")
            return False

    def get_redmine_issues_by_project_id(self, project_id):
        """
            This function fetches the issues of the project in redmine using redmine API
            :param project_id: id of the project
            :return : returns all the issues in dictionary
        """
        try:
            flag = self.service.check_service_status()
            if flag:
                url = f"{self.creds['url']}/issues.json"
                headers = {'X-Redmine-API-Key': self.creds['api_key']}

                params = {
                    'project_id': project_id
                }

                response = requests.get(url, params=params, headers=headers)

                if response.status_code == 200:
                    issues_data = response.json().get('issues')
                    self.logger.log_info(
                        f'Redmine issues fetched SUCCESSFULLY.\n')
                    return issues_data

                else:
                    self.logger.log_error(
                        f"Failed to get issues. Status code: {response.status_code}, Error: {response.text}\n")
                    return False
            elif not flag:
                self.logger.log_error(
                    "The Redmine service is currently not running\nPlease start the service.\n")
                return False

        except Exception as e:
            self.logger.log_error(
                f"Error occurred while fetching the issues:{e}\n")
            return False
            

    def get_redmine_issues(self):
        """
            This function fetches all the issues in redmine using redmine API
            :return : returns all the issues in list
        """
        try:
            flag = self.service.check_service_status()
            if flag:
                url = f"{self.creds['url']}/issues.json"
                headers = {'X-Redmine-API-Key': self.creds['api_key']}

            
                response = requests.get(url , headers=headers)

                if response.status_code == 200:
                    issues_data = response.json().get('issues')
                    self.logger.log_info(
                        f'Redmine issues fetched SUCCESSFULLY.\n')
                    return issues_data

                else:
                    self.logger.log_error(
                        f"Failed to get issues. Status code: {response.status_code}, Error: {response.text}\n")
                    return False
            elif not flag:
                self.logger.log_error(
                    "The Redmine service is currently not running\nPlease start the service.\n")
                return None

        except Exception as e:
            self.logger.log_error(
                f"Error occurred while fetching the issues:{e}\n")

    def get_redmine_all_issue_id(self):
        """
            This function fetches all the issues in redmine using redmine API
            :return : returns all the issues in list
        """
        list_of_all_issue_id = []
        try:
            flag = self.service.check_service_status()
            if flag:
                url = f"{self.creds['url']}/issues.json"
                headers = {'X-Redmine-API-Key': self.creds['api_key']}

                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    issues_data = response.json().get('issues')
                    self.logger.log_info(
                        f'Redmine issues fetched SUCCESSFULLY.\n')
                    present = issues_data
                    for issue in present:
                        list_of_all_issue_id.append(issue['id'])
                    return list_of_all_issue_id

                else:
                    self.logger.log_error(
                        f"Failed to get issues. Status code: {response.status_code}, Error: {response.text}\n")
                    return False
            elif not flag:
                self.logger.log_error(
                    "The Redmine service is currently not running\nPlease start the service.\n")
                return False

        except Exception as e:
            self.logger.log_error(
                f"Error occurred while fetching the issues:{e}\n")
            return False

    def get_redmine_issue_by_id(self, issue_id):
        """
            This function fetches the specific issue in redmine from the provided issue_id using redmine API
            :param issue_id : issue id of the project
            :return : returns issue information from the provided issue_id in dictionary
        """
        try:
            flag = self.service.check_service_status()
            if flag:
                url = f"{self.creds['url']}/issues/{issue_id}.json"
                headers = {'X-Redmine-API-Key': self.creds['api_key']}

                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    issue_data = response.json().get('issue')
                    self.logger.log_info(
                        f"Issue with ID:{issue_id} fetched SUCCESSFULLY\n")
                    return issue_data
                else:
                    self.logger.log_error(
                        f"Failed to get issue. Status code: {response.status_code}, Error: {response.text}\n")
                    return False
            elif not flag:
                self.logger.log_error(
                    "The Redmine service is currently not running\nPlease start the service.\n")
                return False

        except Exception as e:
            self.logger.log_error(
                f"Error occurred while fetching the issue:{e}\n")
            return False
    
    def get_role_id_by_role_name(self, role_name):
        """
            This methid fetches the specific role if in redmine using redmine API
            :param role_name : role name of the project
            :return : returns role id from the provided role name 
        """
        try:
            flag = self.service.check_service_status()
            if flag:
                url = f"{self.creds['url']}/roles.json"
                headers = {'X-Redmine-API-Key': self.creds['api_key']}
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    role_data = response.json()["roles"]
                    for role in role_data:
                        if role["name"] == role_name:
                            self.logger.log_info(f"Role with name:{role_name} fetched SUCCESSFULLY\n")
                            return role["id"]
                        else:
                            self.logger.log_error(f"{role_name} not found in roles list\n")
                            return False
                else:
                    self.logger.log_error("Given parameter is not valid.")
                    return False
            else:
                self.logger.log_error("The Redmine service is currently not running\nPlease start the service.\n")
                return False

        except Exception as e:
            self.logger.log_error(f"Error occurred while fetching role_id:{e}\n")
            return False

    def delete_redmine_issue(self, issue_id):
        """
        This function deletes an issue in Redmine using the redmine API.
        :param issue_id: The ID of the issue to be deleted
        :return: True if the issue is deleted successfully, False otherwise
        """
        issue_endpoint = f"{self.creds['url']}/issues/{issue_id}.json"
        headers = {'X-Redmine-API-Key': self.creds['api_key']}

        try:
            response = requests.delete(issue_endpoint, headers=headers)
            response.raise_for_status()
            if response.status_code == 204:
                self.logger.log_info(
                    f"Issue with ID:{issue_id} is deleted SUCCESSFULLY.\n")
                return True
            else:
                self.logger.log_error(
                    f"Failed to delete the issue with ID {issue_id}.\nError message: {response.json()}\n")
                return False

        except requests.exceptions.RequestException as e:
            self.logger.log_error(
                f"Error occurred while deleting the issue:{e}\n")
            return False

    def add_member_to_project(self, service_name, project_name, member_name, role_name):
        """
        This method used to add user as member of project
        :param service_name: This parameter is the service name of redmine
        :param project_name:This parameter is the project name in redmine
        :param member_name: This parameter is the user name 
        :param role_name: This parameter is the role for user need to assign
        :return: True if the member is added successfully, False otherwise
        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                user_id = self.get_user_id_by_username(member_name) 
                role_id = self.get_role_id_by_role_name(role_name)
                project_id = self.get_project_id_by_project_name(project_name)
                if not self.verify_project_members(service_name, project_name, member_name):
                    if user_id and role_id and project_id:
                        data = {
                                "membership":{
                                                "user_id": user_id,
                                                "project_id": project_id,
                                                "role_ids": [role_id]
                                            }
                                }
                        url = f"{self.creds['url']}/projects/{project_id}/memberships.json"
                        headers = {'Content-Type': 'application/json','X-Redmine-API-Key': self.creds['api_key']}
                        response = requests.post(url, json=data, headers=headers)
                        if response.status_code == 201:
                            self.logger.log_info(f"{member_name} user is added to {project_name} as a member\n")
                            return True
                        else:
                            self.logger.log_info(f"{member_name} user is not able to add to {project_name} as a member\n")
                            return False
                    else:
                        self.logger.log_error("The given parameters are not valid\n")
                        return False
                else:
                    self.logger.log_info(f"{member_name} already present in Project as member\n")
                    return True
            else:
                self.logger.log_error("The Redmine service is currently not running\nPlease start the service.\n")
                return False   
                        
        except Exception as e:
            self.logger.log_error(f"Error while adding user as a member to the project: {e}\n") 
            return False  
    
    def verify_project_members(self, service_name, project_name, user):
        """
        This method verifies an user is present in project or not in Redmine using the redmine API.
        :param service_name: This parameter is the service name of redmine
        :param project_name: This parameter is the project name in redmine
        :param user: This parameter is the user name 
        :return: True if the user is found in project members list successfully, False otherwise
        """
        try:
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                project_id = self.get_project_id_by_project_name(project_name)
                url = f"{self.creds['url']}/projects/{project_id}/memberships.json"
                headers = {'X-Redmine-API-Key': self.creds['api_key']}
                response = requests.get(url, headers=headers)   
                if response.status_code == 200:
                    for member in response.json()["memberships"]:
                        if (member['user'])['name'] == user or (member['user'])['id'] == user:
                            return (member['user'])['id']
                    else:
                        self.logger.log_error(f"{user} not found\n")
                        return False
                else:
                    self.logger.log_error(f"Unable to fetch members of the project\n")
                    return False
            else:
                self.logger.log_error("The Redmine service is currently not running\nPlease start the service.\n")
                return False
        except Exception as e:
            self.logger.log_error(f"Error occured while fetching user in project:{e}\n")
            return False

    def get_priority_id_by_priority_name(self, priority_name):
        """
        This method returns priority_id by priority_name in Redmine using the redmine API.
        :param priority_name: This parameter is the priority name in Redmine
        :return: True if the priority_name is found returns priority_id, else False
        """
        try:
            url = f"{self.creds['url']}/enumerations/issue_priorities.json"
            headers = {'X-Redmine-API-Key': self.creds['api_key']}
            response = requests.get(url, headers=headers)
            if response.status_code == 200 :
                priority_data = response.json()["issue_priorities"]
                for priority in priority_data:
                    if priority["name"] == priority_name:
                        self.logger.log_info(f"{priority['id']} : '{priority_name}' Successfully retreived status id")
                        return priority["id"]
                else:
                    self.logger.log_error("priority not listed\n")
                    return False
            else:
                self.logger.log_error("Please enter the valid data\n")   
                return False              
        except Exception as e:
            self.logger.log_error(f"error occured while fetching id {e}\n")
            return False

    def get_status_id_by_status_name(self, status_name):
        """
        This method returns status_id by status_name in Redmine using the redmine API.
        :param status_name: This parameter is the status name in Redmine
        :return: True if the status_name is found returns status_id, else False
        """
        try:
            url = f"{self.creds['url']}/issue_statuses.json"
            headers = {'X-Redmine-API-Key': self.creds['api_key']}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                status_data = response.json()["issue_statuses"]
                for data in status_data: 
                    if data['name'] == status_name:
                        self.logger.log_info(f"{data['id']} : '{status_name}' Successfully retreived status id\n")
                        return data["id"]
                else:
                    self.logger.log_error("status is not listed\n") 
                    return False
            else:
                self.logger.log_error("Please enter the valid data\n")   
                return False       
        except Exception as e:
            self.logger.log_error(f"error occured while fetching id {e}\n")
            return False

    def get_tracker_id_by_tracker_name(self, tracker_name):
        """
        This method returns tracker_id by tracker_name in Redmine using the redmine API.
        :param tracker_name: This parameter is the tracker name in Redmine
        :return: True if the tracker_name is found returns tracker_id, else False
        """
        try:
            url = f"{self.creds['url']}/trackers.json"
            headers = {'X-Redmine-API-Key': self.creds['api_key']}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                tracker_data = response.json()["trackers"]
                for tracker in tracker_data:
                    if tracker["name"] == tracker_name:
                        self.logger.log_info(f"{tracker['id']} : {tracker['name']} Successfully retrieved tracker id")
                        return tracker["id"]
                else:
                    self.logger.log_error(f"{tracker_name} not listed..\n")
                    return False   
            else:
                self.logger.log_error("Please enter the valid data\n")   
                return False     
        except Exception as e:
            self.logger.log_error(f"Error occurred while fetching user_id:{e}\n")
            return False
    
    def add_issue_to_redmine_project(self, service_name, project_name, tracker_name, subject, description, status, priority, assignee, role_name=None):
        """
        This method will add issue in project
        :param service_name: This parameter is the service name in redmine
        :param project_name: This parameter is the project name in redmine
        :param tracker_name: This parameter is the tracker name in redmine
        :param subject: This parameter is the subject of the issue in redmine
        :param descripton: This parameter is for brief description of the issue in redmine
        :param status: This parameter is the status of the issue in redmine
        :param priority: This parameter is the priority of the issue in remine
        :param assignee: This parameter is used to assign a member to issue in redmine
        :param role_name: This parameter by default None, assign issue to user who is not in project need to mention role os the user
        :return: True if the issue is created successfully, False otherwise
        """
        try: 
            flag = self.service.docker_verify_service_status(service_name)
            if flag and flag != None:
                project_id = self.get_project_id_by_project_name(project_name)
                user_id = self.get_user_id_by_username(assignee)
                tracker_id = self.get_tracker_id_by_tracker_name(tracker_name)
                status_id = self.get_status_id_by_status_name(status)
                priority_id = self.get_priority_id_by_priority_name(priority)
                if project_id and user_id and tracker_id and status_id and priority_id:
                    if user_id == self.verify_project_members(service_name, project_name, assignee):
                        issue_data = {"issue": 
                                    {
                                    "project_id": project_id,
                                    "tracker_id": tracker_id,
                                    "subject": subject,
                                    "description": description,
                                    "status_id": status_id,
                                    "priority_id": priority_id,
                                    "assigned_to_id": user_id
                                    }
                                }
                        
                        url = f"{self.creds['url']}/issues.json"
                        headers = {'Content-Type': 'application/json','X-Redmine-API-Key': self.creds['api_key']}
                        response = requests.post(url, json=issue_data, headers=headers)
                        if response.status_code == 201:
                            self.logger.log_info(f"Issue Created Successfully\n")
                            return True
                        else:
                            self.logger.log_error(f"Failed to create a issue\n")
                            return False
                    else:
                        self.logger.log_warning(f"{assignee} Not a member of project can't assign to issue\n")
                        if role_name != None:
                            if self.add_member_to_project(service_name, project_name, assignee, role_name):
                                if self.add_issue_to_redmine_project(self, service_name, project_name, tracker_name, subject, description, status, priority, assignee):
                                    return True
                                else:
                                    self.logger.log_error("Failed to add issue to {project_name}")
                                    return False
                            else:
                                self.logger.log_error("Failed to add user {assignee}")
                                return False                            
                        else:
                            self.logger.log_error("Role is missing\n")
                else:
                    self.logger.log_error("given parameters are not valid\n")
                    return False
            else:
                self.logger.log_error("The Redmine service is currently not running\nPlease start the service.\n")
                return False
        except requests.exceptions.RequestException as e:
            self.logger.log_error(f"Error occurred while creating the issue:{e}\n")
            return False


