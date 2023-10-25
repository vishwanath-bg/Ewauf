__author__ = 'Roshanzameer M'


import paramiko
import subprocess
import time
from pathlib import Path
from socket import socket
from Library.Parser.ConfigParser import Config_Parser
from Library.Utils.Logger import Logger


class SSH_Parser:
    """
        This library includes methods that simplify SSH connections, command execution, and shell command operations.
         These methods offer convenient functionality with simpler syntax for working with remote machines over SSH.
    """

    def __init__(self):
        self.client = None
        self.client_stack = []
        self.child_ssh = None
        self.sftp_client = None
        self.ssh_stdout = None
        self.ssh_error = None
        self.sftp = None
        self.data = Config_Parser()
        self.logger = Logger()

    def connect_to_server(self, machine=1):
        """
            This method employs the Paramiko library to establish an SSH connection to the remote machine
            :param machine: specify SSH server/machine number[1, 2, 3 etc] (default=1 will be picked)
            :return: returns SSH client if connected else False
        """
        return_flag = False
        creds = self.data.get_item(Path(__file__).parent.parent.parent / 'Config/Config.ini', f'machine_{machine}')
        try:
            self.logger.log_info(f"Initiating connection to the remote machine located at {creds['ip']}")
            self.client = paramiko.SSHClient()
            private_key = paramiko.RSAKey.from_private_key_file(creds['pkey_path'])
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # add auto-add policy for SSH connection
            if creds['password'] == "pem":
                self.client.connect(hostname=creds['ip'], username=creds['username'], pkey=private_key)
            else:
                self.client.connect(hostname=creds['ip'], username=creds['username'],
                            password=creds['password'], pkey=private_key)
            self.logger.log_info(f"Connected to Remote Machine at {creds['ip']} >>>\n")
            return_flag = self.client

        except TypeError as error:
            self.logger.log_error(f"{error}: Section/Key Not Found\n")
        except paramiko.BadHostKeyException:
            self.logger.log_error(f"BadHostKeyException on {creds['ip']}\n")
        except paramiko.AuthenticationException:
            self.logger.log_error("Authentication failed, please verify your credentials\n")
        except paramiko.SSHException as sshException:
            self.logger.log_error(f"Could not establish SSH connection: {sshException}\n")
        except Exception as error:
            self.logger.log_error(f"Error while connecting to {creds['ip']}: {error}\n")
        except BaseException as error:
            self.logger.log_error(f"Error occurred: {error}\n")
        except socket.timeout:
            self.logger.log_error("Connection timed out\n")
        return return_flag

    def nested_ssh(self, *machines):
        """
            This method helps to establish nested SSH connection to the multiple remote machine(A-> B -> C) manner
            :param machines: specify variable number of machines(numbers) combinations (ex: 2, 3, 1...)
            :return: returns latest/last-machine ssh client/object
        """
        try:
            return_flag = False
            self.logger.log_info(f"Establishing nested SSH connections:")
            # checking if parent & child machines are same and also connection is made to parent machine
            for i, machine in enumerate(machines):
                creds = self.data.get_item(Path(__file__).parent.parent.parent / 'Config/Config.ini', f'machine_{machine}')

                if machines.count(machine) == 1:
                    client = self.connect_to_server(machine)  # Connect to the child machine (B, C, D, ...)
                    self.client_stack.append(client)

                    if i > 0:
                        # Set up the channel for the child machine
                        transport = paramiko.Transport(self.client_stack[i-1].get_transport().open_channel("direct-tcpip", (creds['ip'], 22),
                                                                                ("localhost", 0)))
                        transport.start_client()

                        # Authenticate the tunnel with the child machine private key
                        private_key = paramiko.RSAKey.from_private_key_file(creds['pkey_path'])
                        transport.auth_publickey(creds['username'], private_key)

                        # Create a new client using the child machine's transport
                        self.child_ssh = paramiko.SSHClient()
                        self.child_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        self.child_ssh._transport = transport
                        self.client_stack.append(self.child_ssh)
                return_flag = self.child_ssh
            return return_flag
        except Exception as error:
            self.logger.log_error(f"Error occurred while connecting to the machine: {error}\n")

    def run_command(self, *commands, machine=1, client=None):
        """
            This method facilitates opening new `.Channel` for each command and the requested commands are executed.
            Using SSH client instance if provided else new SSH connection is made.
            :param commands: variable number of commands to be executed (separated by comma)
            :param machine: specify SSH server/machine number[1, 2, 3 etc] (default=1 will be picked)
            :param client: specify existing SSH client, instead of making new SSH session using 'machine'.
            :return: returns the standard output if executed else False is returned
        """
        try:
            output = ''
            flag = True
            self.client = self.connect_to_server(machine) if client == None else client

            if self.client:
                for command in commands:
                    stdin, stdout, stderr = self.client.exec_command(command)
                    self.ssh_stdout = stdout.read().decode()
                    self.ssh_error = stderr.read().decode()
                    self.logger.log_info(self.ssh_stdout.strip())

                    # checking error occurred or not, excluding warnings
                    if 'WARNING:' in self.ssh_error:
                        self.logger.log_info(f'---- Command: "{command}" execution completed ----\n')
                    elif self.ssh_error:
                        self.logger.log_error(f'Problem occurred while running command: "{command}", '
                                                f'Error message: {self.ssh_error}\n')
                        flag = False
                    else:
                        self.logger.log_info(f'---- Command: "{command}" execution completed ----\n')
                    output += self.ssh_stdout.strip()
                self.client.close()
            if flag:
                return output
            else:
                return False
        except Exception as error:
            self.logger.log_error(f'{error}, Exception while executing the command: "{command}" \n')
            self.client.close()
            return False

    def run_commands(self, *commands,  machine=1, client=None):
        """
            This method facilitates opening new `.Channel` & starting an interactive shell session on the SSH server
            and executing multiple commands within a single SSH session/channel.
            :param commands: variable number of commands to be executed (separated by comma)
            :param machine: specify SSH server/machine number[1, 2, 3 etc] (default=1 will be picked)
            :param client: specify existing SSH client, instead of making new SSH session using 'machine'.
            :return: returns the standard output
        """
        try:
            self.client = self.connect_to_server(machine) if client == None else client

            if self.client:
                # Invoke the shell
                ssh_shell = self.client.invoke_shell()
                ssh_shell.recv(1024)  # capturing the shell buffer

                output = ''
                for command in commands:
                    ssh_shell.send(command + "\n")
                    time.sleep(0.5)
                while not ssh_shell.closed and ssh_shell.recv_ready():  # waiting for cmd to execution
                    output += ssh_shell.recv(4096).decode()

                ssh_shell.close()
                self.client.close()
                std_out = ''

                for line in output.splitlines():
                    if '$' not in line:
                        std_out += line.strip()+'\n'
                self.logger.log_info(f"{std_out}\n")
                return std_out
        except Exception as error:
            self.logger.log_error(f'{error}, Exception while executing the command: "{command}" \n')
            self.client.close()
            return False

    def run_shell_command(self, *commands, cmd_output=True):
        """
            This method facilitates the execution of shell commands over the terminal
            :param commands: variable number of commands to be executed (separated by comma)
            :param cmd_output: specify whether the command output should be printed (True/False)
            :return: returns standard out
        """
        try:
            flag = True
            for command in commands:
                self.logger.log_info(f'Executing command: "{command}", Shell: True, Command Output: {cmd_output}')
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           universal_newlines=True, shell=True)
                std_output = process.stdout.read().strip()
                if cmd_output:
                    self.logger.log_info('<<< CMD OUTPUT START >>>')
                    self.logger.log_info(std_output)
                    self.logger.log_info('<<< CMD OUTPUT END >>>')
                return_code = process.wait()
                if return_code:
                    self.logger.log_error(f'Command: "{command}" returned non-zero exit status. '
                                          f'Exit Code: {return_code}\n')
                    flag =  False
                else:
                    self.logger.log_info(f'Command: "{command}" executed successfully. Exit Code: {return_code}\n')
                process.stdout.close()
            if flag:
                return std_output
            else:
                return flag
        except Exception as error:
            self.logger.log_error(f"Error occurred while running shell command: {error}\n")

    def return_stdout(self, command, machine=1, client=None):
        """
            This method helps in executing a single command via SSH connection where standard output will be returned.
            :param command: command to be executed
            :param machine: specify SSH server/machine number[1, 2, 3 etc] (default=1 will be picked)
            :param client: specify existing SSH client, instead of making new SSH session using 'machine'.
            :return: returns stdout of the command executed else False
        """
        try:
            self.client = self.connect_to_server(machine) if client == None else client

            if self.client:
                stdin, stdout, stderr = self.client.exec_command(command)
                self.ssh_stdout = stdout.read().decode()
                self.ssh_error = stderr.read().decode()

                # checking error occurred or not, excluding warnings
                if 'WARNING:' in self.ssh_error:
                    self.logger.log_info(f'---- Command: "{command}" execution completed ----\n')
                elif self.ssh_error:
                    self.logger.log_error(f'Problem occurred while running command: "{command}", '
                                            f'Error message: {self.ssh_error}\n')
                    self.client.close()
                    return False
                else:
                    self.logger.log_info(f'---- Command: "{command}" execution completed ----\n')
                self.client.close()
                return self.ssh_stdout
        except Exception as error:
            self.logger.log_error(f"Error occurred:{error}")
            self.logger.log_error(f"{self.ssh_error}\n")

    def return_output(self, command, machine=1, client=None):
        """
            This method helps in opening new `.Channel` and the requested command is executed.
            :param command: command to be executed
            :param machine: specify SSH server/machine number[1, 2, 3 etc] (default=1 will be picked)
            :param client: specify existing SSH client, instead of making new SSH session using 'machine'.
            :return: returns command's input, output & error streams of objects representing stdin, stdout, and stderr.
        """
        try:
            self.client = self.connect_to_server(machine) if client == None else client
            if self.client:
                paramiko_obj = self.client.exec_command(command)
                return paramiko_obj
            else:
                return False
        except Exception as error:
            self.logger.log_error(f"Error occurred:{error}\n")

    def sudo_access(self, *commands, machine=1, client=None):
        """
            This method helps in executing commands with sudo or superuser access in different SSH sessions.
            :param commands: variable number of commands to be executed
            :param machine: specify SSH server/machine number[1, 2, 3 etc] (default=1 will be picked)
            :param client: specify existing SSH client, instead of making new SSH session using 'machine'.
            :return: returns standard output of the commands executed
        """
        try:
            sudo_commands = (f"sudo {i}" for i in commands)  # appending sudo to each command
            # triggering run using sudo commands
            if client == None:
                output = self.run_command(*tuple(sudo_commands), machine=machine)
            else:
                output = self.run_command(*tuple(sudo_commands), client=client)
            return output
        except Exception as error:
            self.logger.log_error(f"Error occurred while running the command:{error}\n")
            return False

    def get_sftp_client(self, machine=1, client=None):
        """
            This method will create & return the SFTP client from the SSH machine mentioned
            :param machine: specify SSH server/machine number[1, 2, 3 etc] (default=1 will be picked)
            :param client: specify existing SSH client, instead of making new SSH session using 'machine'.
            :return: returns sftp client
        """
        try:
            self.client = self.connect_to_server(machine) if client == None else client
            if self.client:
                return self.client.open_sftp()
            else:
                return False
        except Exception as error:
            self.logger.log_error(f"Error while creating SFTP client: {error}\n")
    
    def get_file_open_client(self, file, permission: str, machine=1, client=None):
        """
            This method will create & return the file open object present in SSH machine mentioned.
            :param file: File path in server machine/instance.
            :param permission: Specify file permission in which file shall be accessed.
            :param machine: specify SSH server/machine number[1, 2, 3 etc] (default=1 will be picked)
            :param client: specify existing SSH client, instead of making new SSH session using 'machine'.
            :return: returns file open sftp client
        """
        try:
            sftp = self.get_sftp_client(machine=machine) if client == None else self.get_sftp_client(client=client)
            open_file_sftp = sftp.open(file, permission)
            return open_file_sftp
        except Exception as error:
            self.logger.log_error(f"Error: {error}\n")

    def upload_file(self, local_file_path, remote_file_path, machine=1, client=None):
        """
            This method facilitates uploading file from local/host machine to remote machine
            :param local_file_path: specify local/host path where file should be downloaded
            :param remote_file_path: specify remote/server file path/location
            :param machine: specify SSH server/machine number[1, 2, 3 etc] (default=1 will be picked)
            :param client: specify existing SSH client, instead of making new SSH session using 'machine'.
        """
        try:
            self.sftp = self.get_sftp_client(machine=machine) if client == None else self.get_sftp_client(client=client)
            if self.sftp:
                self.logger.log_info(f"Uploading the file\n")
                self.sftp.put(local_file_path, remote_file_path)
                return True
            else:
                self.logger.log_error("Connection to SSH server failed\n")
                return False
        except Exception as error:
            self.logger.log_error(f"Error while uploading the file: {error}\n")

    def file_download(self, remote_file_path, local_file_path, machine=1, client=None):
        """
            This method facilitates file download/getting-file from remote machine to local/host machine
            :param remote_file_path: specify remote/server file path/location
            :param local_file_path: specify local/host path where file should be downloaded
            :param machine: specify SSH server/machine number[1, 2, 3 etc] (default=1 will be picked)
            :param client: specify existing SSH client, instead of making new SSH session using 'machine'.
        """
        try:
            self.sftp = self.get_sftp_client(machine=machine) if client == None else self.get_sftp_client(client=client)
            if self.sftp:
                self.logger.log_info(f"Downloading the file\n")
                self.sftp.get(remote_file_path, local_file_path)
                return True
            else:
                self.logger.log_error("Connection to SSH server failed\n")
                return False
        except Exception as error:
            self.logger.log_error(f"Error while downloading the file: {error}\n")
