from file_repo import FileRepo


class Server:
    def __init__(self, client):
        self.client_user = None
        self.client = client
        self.file_repo = FileRepo(self)
        self.current_path = '.'

    def get_command(self, command):
        command_parts = command.split()

        if len(command_parts) == 0:
            return

        match command_parts[0]:
            case 'signup':
                if len(command_parts) < 6:
                    self.send_message_to_client('wrong command')
                else:
                    self.file_repo.signup(command_parts)

            case 'signin':
                if len(command_parts) < 4:
                    self.send_error_to_client('wrong command')
                else:
                    if (self.file_repo.signin(command_parts)):
                        self.client_user = command_parts[3]
                        self.current_path = f'./{self.client_user}'
                        self.file_repo.update(command_parts[1], self.client_user)

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
                    path = command_parts[1]
                    folder_names = path.split('/')
                    directory_path = self.cd(self.current_path, '/'.join(folder_names))

                    if directory_path == '.':
                        self.send_error_to_client('not permissible')
                    else:   
                        self.file_repo.mkdir(directory_path)
                else:
                    self.send_error_to_client('you are not signed in')

            case 'touch':
                if len(command_parts) != 2:
                    self.send_error_to_client('wrong command')
                elif self.client_user:
                    path = command_parts[1]
                    folder_names = path.split('/')[:-1]
                    directory_path = self.cd(self.current_path, '/'.join(folder_names))

                    if directory_path == '.':
                        self.send_error_to_client('not permissible')
                    else:
                        folder_names = directory_path.split('/')
                        self.file_repo.touch(folder_names, file_name=path.split('/')[-1])
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
                    elif self.file_repo.isdir(new_path):
                        self.current_path = new_path
                    else:
                        self.send_error_to_client('no such directory')
                else:
                    self.send_error_to_client('you are not signed in')

            case 'ls': 
                if len(command_parts) > 2:
                    self.send_error_to_client('wrong command')
                elif self.client_user:
                    if len(command_parts) == 1:
                        self.file_repo.ls(self.current_path)
                    else:
                        path = command_parts[1]
                        new_path = self.cd(self.current_path, path)

                        if new_path == '.':
                            self.send_error_to_client('not permissible')
                        elif self.file_repo.isdir(new_path):
                            self.file_repo.ls(new_path)
                        else:
                            self.send_error_to_client('no such directory')
                else:
                    self.send_error_to_client('you are not signed in')

            case 'rm':
                if len(command_parts) != 2 and len(command_parts) != 3:
                    self.send_error_to_client('wrong command')
                elif self.client_user:
                    if len(command_parts) == 2:
                        path = command_parts[1]
                        new_path = self.cd(self.current_path, path)

                        if new_path == '.':
                            self.send_error_to_client('not permissible')
                        else:
                            self.file_repo.rm_file(new_path)
                    else:
                        if command_parts[1] != '-r':
                            self.send_error_to_client('wrong command')
                        else:
                            path = command_parts[2]
                            new_path = self.cd(self.current_path, path)

                            if new_path == '.':
                                self.send_error_to_client('not permissible')
                            else:
                                self.file_repo.rm_dir(new_path)
                else:
                    self.send_error_to_client('you are not signed in')

            case 'mv':
                if len(command_parts) != 3 and len(command_parts) != 4:
                    self.send_error_to_client('wrong command')
                elif self.client_user:
                    if len(command_parts) == 3:
                        source_path = command_parts[1]
                        destination_path = command_parts[2]

                        source_path = self.cd(self.current_path, source_path)
                        destination_path = self.cd(self.current_path, destination_path)

                        if destination_path == '.':
                            self.send_error_to_client('not permissible')
                        else:
                            self.file_repo.mv_file(source_path, destination_path)

                    else:
                        if command_parts[1] != '-r':
                            self.send_error_to_client('wrong command')
                        else:
                            source_path = command_parts[2]
                            destination_path = command_parts[3]

                            source_path = self.cd(self.current_path, source_path)
                            destination_path = self.cd(self.current_path, destination_path)

                            if destination_path == '.':
                                self.send_error_to_client('not permissible')
                            else:
                                self.file_repo.mv_folder(source_path, destination_path)

                else:
                    self.send_error_to_client('you are not signed in')

            case 'read':
                if len(command_parts) != 2:
                    self.send_error_to_client('wrong command')
                elif self.client_user:
                    path = command_parts[1]
                    path = self.cd(self.current_path, path)
                    self.file_repo.read(path)
                else:
                    self.send_error_to_client('you are not signed in')

            case 'edit':
                if len(command_parts) < 3:
                    self.send_error_to_client('wrong command')
                elif self.client_user:
                    path = command_parts[1]
                    text = str.encode(' '.join(command_parts[2:]))
                    path = self.cd(self.current_path, path)
                    self.file_repo.edit(path, text)
                else:
                    self.send_error_to_client('you are not signed in')

            case 'share':
                if len(command_parts) < 5 or len(command_parts) > 6:
                    self.send_error_to_client('wrong command')
                elif len(command_parts) == 6 and command_parts[3] != '-r' and command_parts[3] != '-rw':
                    self.send_error_to_client('wrong command')
                else:
                    path = self.cd(self.current_path, command_parts[1])
                    
                    if len(command_parts) == 6 and command_parts[3] == '-rw':
                        self.file_repo.cp_file_rw(path, command_parts[-2], command_parts[-1])    
                    else:
                        self.file_repo.cp_file_r(path, command_parts[-2], command_parts[-1])
            
            case other:
                self.send_error_to_client('wrong command')

        if self.client_user:
            self.send_address_to_client(self.current_path[2:])

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

    def get_path(self, path):
        return self.cd(self.current_path, path)

    def read(self, path):
        return self.file_repo.show(path)

    def show_files(self, path):
        return self.file_repo.show_files(path)

    def send_message_to_client(self, message):
        self.client.get_message(message)

    def send_error_to_client(self, error):
        self.send_message_to_client('error: ' + error)

    def send_info_to_client(self, info):
        self.send_message_to_client('info: ' + info)

    def send_address_to_client(self, address):
        self.client.get_address(address)

    def get_message(self, message):
        self.send_message_to_client(message)

    def get_error(self, error):
        self.send_error_to_client(error)
