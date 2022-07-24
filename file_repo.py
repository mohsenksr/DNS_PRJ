from distutils.cmd import Command
from genericpath import isfile
import os
from db_controller import DBController
from pathlib import Path
import shutil

class FileRepo:
    def __init__(self, server):
        self.server = server
        self.db_controller = DBController()
        self.file_max_length = 1000
        try:
            os.mkdir('all_shared_r')
            os.mkdir('all_shared_rw')
        except:
            pass


    def signup(self, args):
        if self.db_controller.user_signup(username=args[1], password=args[2],
                                                  name=args[3], family=args[4]):
            self.send_message_to_server('user created')
            username = args[1]
            hashed_username = args[5]
            os.mkdir(f'./{hashed_username}')
            os.mkdir(f'./{hashed_username}/shared_r')
            os.mkdir(f'./{hashed_username}/shared_rw')
        else:
            self.send_error_to_server('username exists')

    def signin(self, args):
        if self.db_controller.user_signin(username=args[1], password=args[2]):
            self.send_message_to_server('signed in successfully')
            return True
        else:
            self.send_error_to_server('incorrect username or password')
            return False

    def update(self, username, encoded_username):
            list_r = os.listdir('./all_shared_r')
            for file_r in list_r:
                f = file_r.split('_#_')
                if f[0] == username and file_r.split('_')[-1] != 'key':
                    shutil.copyfile(f'./all_shared_r/{file_r}', f'./{encoded_username}/shared_r/{f[1]}')
                    
                    fd = os.open(f'./all_shared_r/{file_r}_key', os.O_RDONLY)
                    key = os.read(fd, self.file_max_length).decode()
                    os.close(fd)

                    key_file_path = f'./{encoded_username}/shared_r/{f[1]}_key'
                    Path(key_file_path).touch()
                    fd = os.open(key_file_path, os.O_RDWR)
                    os.write(fd, str.encode(key))
                    os.close(fd)

                    os.remove(f'./all_shared_r/{file_r}')
                    os.remove(f'./all_shared_r/{file_r}_key')
            
            list_rw = os.listdir('./all_shared_rw')
            for file_rw in list_rw:
                f = file_rw.split('_#_')
                if f[0] == username and file_rw.split('_')[-1] != 'key':
                    shutil.copyfile(f'./all_shared_rw/{file_rw}', f'./{encoded_username}/shared_rw/{f[1]}')

                    fd = os.open(f'./all_shared_rw/{file_rw}_key', os.O_RDONLY)
                    key = os.read(fd, self.file_max_length).decode()
                    os.close(fd)

                    key_file_path = f'./{encoded_username}/shared_rw/{f[1]}_key'
                    Path(key_file_path).touch()
                    fd = os.open(key_file_path, os.O_RDWR)
                    os.write(fd, str.encode(key))
                    os.close(fd)

                    os.remove(f'./all_shared_rw/{file_rw}')
                    os.remove(f'./all_shared_rw/{file_rw}_key')

            self.send_message_to_server('All shared files updated successfully')


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
        list = os.listdir(path)
        files = ' '.join(list)
        self.send_message_to_server(f'files: {path} {files}')

    def show_files(self, path):
        list = os.listdir(path)
        return list

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
            self.send_message_to_server(f'file: {path} {text}')
        else:
            self.send_error_to_server('not a file')

    def show(self, path):
        if self.isfile(path):
            fd = os.open(path, os.O_RDONLY)
            text = os.read(fd, self.file_max_length).decode()
            os.close(fd)
            return text
        else:
            self.send_error_to_server('not a file')
    
    def edit(self, path, text):
        if 'shared_r' in path.split('/'):
            self.send_error_to_server('not permissible')
            return

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

    def cp_file_r(self, path, key, name):
        if self.isfile(path):
            shutil.copyfile(path, f'./all_shared_r/{name}')
            print(path, f'./all_shared_r/{name}')

            key_file_path = f'./all_shared_r/{name}_key'
            Path(key_file_path).touch()
            fd = os.open(key_file_path, os.O_RDWR)
            os.write(fd, str.encode(key))
            os.close(fd)

            self.send_message_to_server('file shared successfully')
        else:
            self.send_error_to_server('not a file')

    def cp_file_rw(self, path, key, name):
        if self.isfile(path):
            shutil.copyfile(path, f'./all_shared_rw/{name}')
            self.send_message_to_server('file shared successfully')

            key_file_path = f'./all_shared_rw/{name}_key'
            Path(key_file_path).touch()
            fd = os.open(key_file_path, os.O_RDWR)
            os.write(fd, str.encode(key))
            os.close(fd)
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