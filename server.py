import os
from db_controller import DBController
from pathlib import Path


class Server:
    def __init__(self, client):
        self.client_user = None
        self.client = client
        self.db_controller = DBController()
        self.current_path = '.'

    def get_command(self, command):
        command_parts = command.split()
        match command_parts[0]:
            case 'signup':
                if len(command_parts) != 5:
                    self.send_message_to_client('wrong command')
                    return
                if self.db_controller.user_signup(username=command_parts[1], password=command_parts[2],
                                                  name=command_parts[3], family=command_parts[4]):
                    self.send_info_to_client('user created')
                    os.mkdir(f'./{command_parts[1]}')
                else:
                    self.send_error_to_client('username exists')

            case 'signin':
                if len(command_parts) != 3:
                    self.send_error_to_client('wrong command')
                    return
                if self.db_controller.user_signin(username=command_parts[1], password=command_parts[2]):
                    self.client_user = command_parts[1]
                    self.current_path = f'./{self.client_user}'
                    os.chdir(self.current_path)
                    self.send_info_to_client('signed in successfully')
                    self.send_info_to_client(f'currently in path {self.current_path}')
                else:
                    self.send_error_to_client('incorrect username or password')

            case 'signout':
                if len(command_parts) != 1:
                    self.send_error_to_client('wrong command')
                if self.client_user:
                    self.client_user = None
                    self.send_info_to_client('signed out successfully')
                else:
                    self.send_error_to_client('you are not signed in')

            case 'mkdir':
                if len(command_parts) != 2:
                    self.send_error_to_client('wrong command')
                elif self.client_user:
                    current_path = f'./{self.client_user}'
                    path = command_parts[1]
                    folder_names = path.split('/')

                    flag = False
                    for folder_name in folder_names:
                        current_path += f'/{folder_name}'
                        try:
                            os.mkdir(current_path)
                            flag = True
                        except:
                            continue

                    if (flag):
                        self.send_info_to_client('directory created successfully')
                    else:
                        self.send_info_to_client('directory already exists')

            case 'touch':
                if len(command_parts) != 2:
                    self.send_error_to_client('wrong command')
                elif self.client_user:
                    current_path = f'./{self.client_user}'
                    path = command_parts[1]
                    folder_names = path.split('/')[:-1]

                    flag = False
                    for folder_name in folder_names:
                        current_path += f'/{folder_name}'
                        try:
                            os.mkdir(current_path)
                            flag = True
                        except:
                            continue

                    file_name = path.split('/')[-1]
                    Path(f'{current_path}/{file_name}').touch()

                    self.send_info_to_client('file touched')

                else:
                    self.send_error_to_client('you are not signed in')

            case 'cd':
                if len(command_parts) != 2:
                    self.send_error_to_client('wrong command')
                elif self.client_user:
                    try:
                        path = command_parts[1]
                        os.chdir(path)
                    except:
                        self.send_error_to_client('not possible')
                else:
                    self.send_error_to_client('you are not signed in')

            case 'ls': 
                if len(command_parts) > 2:
                    self.send_error_to_client('wrong command')
                elif self.client_user:
                    os.system(command)
                else:
                    self.send_error_to_client('you are not signed in')

            case other:
                self.send_error_to_client('wrong command')

    def send_message_to_client(self, message):
        self.client.get_message(message)

    def send_error_to_client(self, error):
        self.send_message_to_client('ERROR: ' + error)

    def send_info_to_client(self, info):
        self.send_message_to_client('INFO: ' + info)
