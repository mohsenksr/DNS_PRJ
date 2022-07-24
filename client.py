from server import Server
from hashlib import sha256
import base64

class Client:
    def __init__(self):
        self.server = Server(self)
        self.password = '-'
        self.chr_size = 127 - 32
        self.min_char = 32

    def start(self):
        while True:
            command = input()
            if command == 'quit()':
                break

            if command.split()[0] == 'signup' and len(command.split()) == 5:
                self.password = command.split()[2]
                command = get_hashed_command(command=command, index_to_hash=2)
                command = get_hashed_command(command=command, index_to_hash=3)
                command = get_hashed_command(command=command, index_to_hash=4)

                command_parts = command.split()
                command_parts.append(self.encode(command_parts[1], self.password))
                command = " ".join(command_parts)

            if command.split()[0] == 'signin' and len(command.split()) == 3:
                self.password = command.split()[2]
                command = get_hashed_command(command=command, index_to_hash=2)

                command_parts = command.split()
                command_parts.append(self.encode(command_parts[1], self.password))
                command = " ".join(command_parts)

            if any([command.split()[0] == 'mkdir', command.split()[0] == 'touch', command.split()[0] == 'cd',
                    command.split()[0] == 'read', command.split()[0] == 'ls']) and len(command.split()) == 2:
                command_parts = command.split()
                new_directory_parts = []
                for part in command_parts[-1].split('/'):
                    if part == '..' or part == '.' or part == 'shared_r' or part == 'shared_rw':
                        new_directory_parts.append(part)
                    else:
                        new_directory_parts.append(self.encode(part, self.password))

                command_parts[1] = "/".join(new_directory_parts)
                command = " ".join(command_parts)

            if any([command.split()[0] == 'rm', command.split()[0] == 'mv']) and \
                    (len(command.split()) == 2 or len(command.split()) == 3):
                command_parts = command.split()
                new_directory_parts = []

                for part in command_parts[-1].split('/'):
                    if part == '..' or part == '.' or part == 'shared_r' or part == 'shared_rw':
                        new_directory_parts.append(part)
                    else:
                        new_directory_parts.append(self.encode(part, self.password))

                command_parts[-1] = "/".join(new_directory_parts)
                command = " ".join(command_parts)

            if command.split()[0] == 'edit' and len(command.split()) > 2:
                command_parts = command.split()
                new_directory_parts = []
                for part in command_parts[1].split('/'):
                    if part == '..' or part == '.' or part == 'shared_r' or part == 'shared_rw':
                        new_directory_parts.append(part)
                    else:
                        new_directory_parts.append(self.encode(part, self.password))

                command_parts[1] = "/".join(new_directory_parts)

                text = " ".join(command_parts[2:])
                encoded_text = self.encode(text, self.encode(self.server.get_path(command_parts[1]), self.password))
                command = 'edit ' + command_parts[1] + ' ' + encoded_text

            if command.split()[0] == 'share' and len(command.split()) >= 3:
                command_parts = command.split()
                new_directory_parts = [] 
                for part in command_parts[1].split('/'):
                    if part == '..' or part == '.' or part == 'shared_r' or part == 'shared_rw':
                        new_directory_parts.append(part)
                    else:
                        new_directory_parts.append(self.encode(part, self.password))

                command_parts[1] = "/".join(new_directory_parts)
                final_path = self.server.get_path(command_parts[1])

                new_key = self.encode(final_path, self.password)
                new_name = command_parts[2] + '_#_' + self.encode(self.decode(new_directory_parts[-1], self.password), new_key)
                
                command_parts.append(new_key)
                command_parts.append(new_name)

                command = " ".join(command_parts)
                print(command)

            if command.split()[0] == 'read' or command.split()[0] == 'edit':
                command_parts = command.split()
                new_directory_parts = command_parts[1].split('/')
                new_directory_parts[-1] = self.decode(new_directory_parts[-1], self.password)
                
                path = self.server.get_path('/'.join(new_directory_parts[:-1]))
                l = self.server.show_files(path)
                
                for word in l:
                    name = '.' 
                    if word.split('_')[-1] == 'key':
                        continue
                    elif f'{word}_key' in l:
                        key = self.server.read(f'{path}/{word}_key')
                        name = self.decode(word, key) 
                    elif word == 'shared_r' or word == 'shared_rw':
                        name = word
                    else:
                        name = self.decode(word, self.password)

                    if name == new_directory_parts[-1]:
                        new_directory_parts[-1] = word

                command_parts[1] = '/'.join(new_directory_parts)
                command = ' '.join(command_parts)

            self.server.get_command(command)

    def char_to_num(self, c):
        return ord(c) - self.min_char

    def num_to_char(self, num):
        return chr(num + self.min_char)

    def sum(self, a, b):
        result = ""
        for i in range(len(a)):
            result += self.num_to_char((self.char_to_num(a[i]) + self.char_to_num(b[i % len(b)])) % self.chr_size)
        return result

    def sub(self, a, b):
        result = ""
        for i in range(len(a)):
            result += self.num_to_char((self.char_to_num(a[i]) - self.char_to_num(b[i % len(b)]) + self.chr_size) % self.chr_size)
        return result

    def encode(self, plain_text, key):
        return self.sum(plain_text, key)

    def decode(self, encoded_text, key):
        return self.sub(encoded_text, key)

    def get_message(self, message):
        words = message.split()

        if words[0] == 'file:':
            path = words[1]
            path_list = path.split('/')
            dir = '/'.join(path_list[:-1])
            name = path_list[-1]
            l = self.server.show_files(dir)

            key = self.encode(path, self.password)
            if f'{name}_key' in l:
                key = self.server.read(f'{dir}/{name}_key')

            print(self.decode(' '.join(words[2:]), key))
        elif words[0] == 'files:':
            path = words[1]
            result = ""
            for word in words[2:]:
                if word.split('_')[-1] == 'key':
                    continue
                elif f'{word}_key' in words:
                    key = self.server.read(f'{path}/{word}_key')
                    result = self.decode(word, key) + ' ' + result
                elif word == 'shared_r' or word == 'shared_rw':
                    result = word + ' ' + result
                else:
                    result = self.decode(word, self.password) + ' ' + result
            print(result)
        else:
            print(message)

    def get_address(self, address):
        dir_names = address.split('/')
        for i in range(len(dir_names)):
            if dir_names[i] != 'shared_r' and dir_names[i] != 'shared_rw':
                dir_names[i] = self.decode(dir_names[i], self.password)
        address = '/'.join(dir_names)

        print(f'{dir_names[0]}({dir_names[0]}): {address}>')


def get_hashed_command(command, index_to_hash):
    command_parts = command.split()
    command_parts[index_to_hash] = sha256(command_parts[index_to_hash].encode('utf-8')).hexdigest()
    return " ".join(command_parts)
