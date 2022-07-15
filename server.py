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
                    current_path = '.'
                    path = command_parts[1]
                    folder_names = path.split('/')
                    directory_path = self.cd(self.current_path, '/'.join(folder_names))

                    if directory_path == '.':
                        self.send_error_to_client('not permissible')
                    else:   
                        folder_names = directory_path.split('/')

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
                else:
                    self.send_error_to_client('you are not signed in')

            case 'touch':
                if len(command_parts) != 2:
                    self.send_error_to_client('wrong command')
                elif self.client_user:
                    current_path = '.'
                    path = command_parts[1]
                    folder_names = path.split('/')[:-1]
                    directory_path = self.cd(self.current_path, '/'.join(folder_names))

                    if directory_path == '.':
                        self.send_error_to_client('not permissible')
                    else:
                        folder_names = directory_path.split('/')

                        for folder_name in folder_names:
                            current_path += f'/{folder_name}'
                            try:
                                os.mkdir(current_path)
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
                    path = command_parts[1]
                    new_path = self.cd(self.current_path, path)

                    if new_path == '.':
                        self.send_error_to_client('not permissible')
                    elif os.path.isdir(new_path):
                        self.current_path = new_path
                        self.send_info_to_client(f'your\'re in {self.current_path}')
                    else:
                        self.send_error_to_client('no such directory')
                else:
                    self.send_error_to_client('you are not signed in')

            case 'ls': 
                if len(command_parts) > 2:
                    self.send_error_to_client('wrong command')
                elif self.client_user:
                    if len(command_parts) == 1:
                        os.system(f'ls {self.current_path}')
                    else:
                        path = command_parts[1]
                        new_path = self.cd(self.current_path, path)

                        if new_path == '.':
                            self.send_error_to_client('not permissible')
                        elif os.path.isdir(new_path):
                            os.system(f'ls {new_path}')
                        else:
                            self.send_error_to_client('no such directory')
                else:
                    self.send_error_to_client('you are not signed in')

            case other:
                self.send_error_to_client('wrong command')

        if self.client_user:
            self.send_message_to_client(f'{self.client_user}: {self.current_path}')

    def cd(self, current_path, cd_path):
        current_path = current_path.split('/')
        cd_path = cd_path.split('/')

        for dir in cd_path:
            if dir == '.':
                continue
            if dir == '..':
                current_path = current_path[:-1]
                if len(current_path) == 1:
                    return current_path[0]
            else:
                current_path.append(dir)

        new_path = '/'.join(current_path)
        return new_path


    def send_message_to_client(self, message):
        self.client.get_message(message)

    def send_error_to_client(self, error):
        self.send_message_to_client('ERROR: ' + error)

    def send_info_to_client(self, info):
        self.send_message_to_client('INFO: ' + info)
