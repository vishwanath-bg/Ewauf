__author__ = 'Chinmayee P S'

from Library.Parser.SSH_Command_Parser import SSH_Parser
from Library.Parser.ConfigParser import Config_Parser
from Library.Utils.Logger import Logger
from pathlib import Path
import requests

class ServerUtils:
    """
    This script is for starting/stopping/verifying the status of the service installed via both docker and aws.
    These libraries are helpful for interacting with the services.

    class ServerUtils:
            def docker_start_service
            def docker_stop_service
            def docker_restart_service
            def docker_verify_service_status
            def start_service
            def stop_service
            def restart_service
            def verify_service_status

    """

    def __init__(self):
        self.ssh = SSH_Parser()
        self.data = Config_Parser()
        self.creds = self.data.get_item(Path(__file__).parent.parent.parent / 'Config/Config.ini', "REDMINE")
        self.logger = Logger()

    def docker_start_service(self, *service_name):
        """
            This function starts the services installed using docker
            :param service_name : This parameter is the service name to be started
        """

        try:
            for service in service_name:
                res=self.docker_verify_service_status(service)
                if res and res != None:
                    self.logger.log_info(f"{service} service is already running\n")
                    return True
                elif res == None:
                    return False
                else:
                    self.logger.log_info(f"{service} service is curently not running..")
                    self.logger.log_info(f"Starting the {service} service...\n")
                    command = f'sudo docker start {service}'
                    stdin, stdout, stderr = self.ssh.client.exec_command(command)
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(f'Problem occurred while running COMMAND :: {command}  \nError message: {error}\n')
                        return False
                    else: 
                        self.logger.log_info(f'\n---- command execution completed ----\n')
                        self.logger.log_info(f"{service} service successfully Started...\n")
                        return True

        except Exception as e:
            self.logger.log_error(f"Error occurred while starting the service : {e}\n")
            return False

    def docker_stop_service(self, *service_name):
        """
            This function stops the services installed using docker
            :param service_name : This parameter is the service name to be stopped
        """

        try:
            for service in service_name:
                res=self.docker_verify_service_status(service)
                if not res and res!= None:
                    self.logger.log_info(f"{service} service has already stopped\n")
                    return True
                elif res == None:
                    return False
                else:
                    self.logger.log_info(f"{service} service is curently running..")
                    self.logger.log_info(f"Stopping the {service} service...\n")
                    command = f"sudo docker stop {service}"
                    stdin, stdout, stderr = self.ssh.client.exec_command(command
                        )
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(f'Problem occurred while running COMMAND :: {command}  \nError message: {error}\n')
                        return False
                    else: 
                        self.logger.log_info(f'\n---- command execution completed ----\n')
                        self.logger.log_info(f"{service} service successfully stopped...\n")
                        return True
                        
                
        except Exception as e:
            self.logger.log_error(f"Error occurred while stopping the service : {e}\n")
            return False
    def docker_restart_service(self, *service_name):
        """
            This function restarts the services installed using docker
            :param service_name : This parameter is the service name to be restarted
        """

        try:
            if self.ssh.connect_to_server():
                for service in service_name:
                    command = f"sudo docker restart {service}"
                    stdin, stdout, stderr = self.ssh.client.exec_command(command
                        )
                    error = stderr.read().decode()
                    if error:
                            self.logger.log_error(f'Problem occurred while running COMMAND :: {command}  \nError message: {error}\n')
                            return False
                    else: 
                        self.logger.log_info(f'---- command execution completed ----\n')
                        self.logger.log_info(f"{service_name} service successfully restarted...\n")
                        return True
            else:
                return False

        except Exception as e:
            self.logger.log_error(f"Error occurred while restarting the service : {e}\n")
            return False

    def docker_verify_service_status(self, service_name):
        """
            This function verifies the status of the service(running or stopped) installed using docker
            :param service_name: This parameter is the service name whose status is to be checked
            :return: True if the service is running else False, None if service doesn't exist
        """

        try:
            if self.ssh.connect_to_server():
                command = f"sudo docker ps -a | grep -w {service_name}"
                self.logger.log_info(f"Checking the {service_name} service status...\n")
                stdin, stdout, stderr = self.ssh.client.exec_command(command
                    )
                result = stdout.read().decode()
                error = stderr.read().decode()
                if len(result) == 0:
                    self.logger.log_error(f"Service {service_name} doesnt exist\n")
                    return None
                else:
                    if error:
                            self.logger.log_error(f'Problem occurred while running COMMAND :: {command}  \nError message: {error}\n')
                    else: 
                        if 'Up' in result:
                            return True
                        elif 'Exited' in result:
                            return False
            else:
                return False

        except Exception as e:
            self.logger.log_error(f"Error occurred while verifying the service : {e}\n")
            return False 


    def start_service(self, *service_name):
        """
            This function starts the service
            :param service_name : This parameter is the service name to be started
        """
        try:
            for service in service_name:
                res=self.verify_service_status(service)
                if res and res != None:
                    self.logger.log_info(f"{service} service is already running\n")
                    return True
                elif res == None:
                    return False
                else:
                    self.logger.log_info(f"{service} service is curently not running..")
                    self.logger.log_info(f"Starting the {service} service...\n")
                    command = f'sudo systemctl start {service}'
                    stdin, stdout, stderr = self.ssh.client.exec_command(command)
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(f'Problem occurred while running COMMAND :: {command}  \nError message: {error}\n')
                        return False
                    else: 
                        self.logger.log_info(f'---- command execution completed ----\n')
                        self.logger.log_info(f"{service} service successfully Started...\n")
                        return True

        except Exception as e:
            self.logger.log_error(f"Error occurred while starting the service : {e}\n")
            return False


    
    def stop_service(self, *service_name):
        """
            This function stops the service
            :param service_name : This parameter is the service name to be stopped
        """ 
        try:
            for service in service_name:
                res=self.verify_service_status(service)
                if not res and res!=None:
                    self.logger.log_info(f"{service} service has already stopped\n")
                    return True
                elif res == None:
                    pass
                else:
                    self.logger.log_info(f"{service} service is curently running..")
                    self.logger.log_info(f"Stopping the {service} service...\n")
                    command =  f"sudo systemctl stop {service}"
                    stdin, stdout, stderr = self.ssh.client.exec_command(command
                    )
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(f'Problem occurred while running COMMAND :: {command} \nError message: {error}\n')
                        return False
                    else: 
                        self.logger.log_info(f'---- command execution completed ----\n')
                        self.logger.log_info(f"{service} service successfully stopped...\n")
                        return True
                    
        except Exception as e:
            self.logger.log_error(f"Error occurred while stopping the service : {e}\n")
            return False
 
       
    
    def restart_service(self, *service_name):
        """
            This function restarts the service
            :param service_name : This parameter is the service name to be restarted
        """

        try:
            if self.ssh.connect_to_server():
                for service in service_name:
                    command = f"sudo systemctl restart {service}"
                    stdin, stdout, stderr = self.ssh.client.exec_command(command
                        )
                    error = stderr.read().decode()
                    if error:
                        self.logger.log_error(f'Problem occurred while running COMMAND :: {command} \nError message: {error}\n')
                        return False
                    else: 
                        self.logger.log_info(f'---- command execution completed ----\n')
                        self.logger.log_info(f"{service_name} service successfully restarted...\n")
                        return True
            else:
                return False

        except Exception as e:
            self.logger.log_error(f"Error occurred while restarting the service : {e}\n")
            return False


    def verify_service_status(self, service_name):
        """
            This function verifies the status of the service(running or stopped)
            :param service_name: This parameter is the service name whose status is to be checked
            :return: True if the service is running else False, None if service doesn't exist
        """

        try:
            if self.ssh.connect_to_server():
                self.logger.log_info(f"Checking the {service_name} service status...\n")
                stdin, stdout, stderr = self.ssh.client.exec_command(
                    f"sudo systemctl status {service_name}")
                result = stdout.readlines()
                error = stderr.read().decode()
                if error:
                    self.logger.log_error(f'{error}\nPlease provide existing service\n')
                    return None
                else:
                    for lines in result:  
                        if "Active: inactive" in lines:
                            return False
                        elif "Active: active" in lines:
                            return True
            else:
                return False

        except Exception as e:
            self.logger.log_error(f"Error occurred while verifying the service : {e}\n")
            return False
    

    def check_service_status(self):
        """
            This function verifies the status of the service(running or stopped) using api
            :return: True if the service is running else False
        """
        try:
            response = requests.get(f"{self.creds['url']}")
            if response.status_code == 200:
                return True
        except Exception as e:
            return False

