from distutils.cmd import Command
import os
from db_controller import DBController
from pathlib import Path

class FileRepo:
    def __init__(self, server):
        self.server = server
        self.db_controller = DBController()
        self.file_max_length = 1000

    def signup(self, args):
        if self.db_controller.user_signup(username=args[1], password=args[2],
                                                  name=args[3], family=args[4]):
            self.send_message_to_server('user created')
            username = args[1]
            hashed_username = args[5]
            os.mkdir(f'./{hashed_username}')
        else:
            self.send_error_to_server('username exists')

    def signin(self, args):
        if self.db_controller.user_signin(username=args[1], password=args[2]):
            self.send_message_to_server('signed in successfully')
            return True
        else:
            self.send_error_to_server('incorrect username or password')
            return False

    def mkdir(self, directory_path):
        current_path = '.'
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
            self.send_message_to_server('directory created successfully')
        else:
            self.send_error_to_server('directory already exists')

    def touch(self, folder_names, file_name):
        current_path = '.'
        for folder_name in folder_names:
            current_path += f'/{folder_name}'
            try:
                os.mkdir(current_path)
            except:
                continue

        Path(f'{current_path}/{file_name}').touch()
        self.send_message_to_server('file touched')

    def ls(self, path):
        os.system(f'ls {path}')

    def rm_file(self, path):
        if self.isfile(path):
            os.remove(path)
            self.send_message_to_server('file removed successfully')
        else:
            self.send_error_to_server('no such file')

    def rm_dir(self, path):
        if self.isdir(path):
            os.rmdir(path)
            self.send_message_to_server('directory removed successfully')
        else:
            self.send_error_to_server('no such directory')

    def mv_file(self, source_path, destination_path):
        if self.isfile(destination_path):
            self.send_error_to_server('a file with same name exists in that path')
        else:
            os.replace(source_path, destination_path)
            self.send_message_to_server('file moved successfully')

    def mv_folder(self, source_path, destination_path):
        if self.isdir(destination_path):
            self.send_error_to_server('a directory with same name exists in that path')
        else:
            os.replace(source_path, destination_path)
            self.send_message_to_server('directory moved successfully')

    def read(self, path):
        if self.isfile(path):
            fd = os.open(path, os.O_RDONLY)
            text = os.read(fd, self.file_max_length).decode()
            os.close(fd)
            self.send_message_to_server(text)
        else:
            self.send_error_to_server('not a file')
    
    def edit(self, path, text):
        if self.isfile(path):
            fd = os.open(path, os.O_RDWR)
            os.write(fd, str.encode(' ' * self.file_max_length))
            os.close(fd)
            fd = os.open(path, os.O_RDWR)
            os.write(fd, text)
            os.close(fd)
            self.send_message_to_server('file edited successfully')
        else:
            self.send_error_to_server('not a file')

    def isfile(self, path):
        return os.path.isfile(path)

    def isdir(self, path):
        return os.path.isdir(path)

    def send_message_to_server(self, message):
        self.server.get_message(message)

    def send_error_to_server(self, error):
        self.server.get_error(error)