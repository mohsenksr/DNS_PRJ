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
                command_parts.append(self.encode(command_parts[1]))
                command = " ".join(command_parts)

            if command.split()[0] == 'signin' and len(command.split()) == 3:
                self.password = command.split()[2]
                command = get_hashed_command(command=command, index_to_hash=2)

                command_parts = command.split()
                command_parts.append(self.encode(command_parts[1]))
                command = " ".join(command_parts)

            if any([command.split()[0] == 'mkdir', command.split()[0] == 'touch', command.split()[0] == 'cd',
                    command.split()[0] == 'read', command.split()[0] == 'ls']) and len(command.split()) == 2:
                command_parts = command.split()
                new_directory_parts = []
                for part in command_parts[-1].split('/'):
                    if part == '..' or part == '.':
                        new_directory_parts.append(part)
                    else:
                        new_directory_parts.append(self.encode(part))

                command_parts[1] = "/".join(new_directory_parts)
                command = " ".join(command_parts)

            if any([command.split()[0] == 'rm', command.split()[0] == 'mv']) and \
                    (len(command.split()) == 2 or len(command.split()) == 3):
                command_parts = command.split()
                new_directory_parts = []

                for part in command_parts[-1].split('/'):
                    if part == '..' or part == '.':
                        new_directory_parts.append(part)
                    else:
                        new_directory_parts.append(self.encode(part))

                command_parts[-1] = "/".join(new_directory_parts)
                command = " ".join(command_parts)

            if command.split()[0] == 'edit' and len(command.split()) > 2:
                command_parts = command.split()
                new_directory_parts = []
                for part in command_parts[1].split('/'):
                    if part == '..' or part == '.':
                        new_directory_parts.append(part)
                    else:
                        new_directory_parts.append(self.encode(part))

                command_parts[1] = "/".join(new_directory_parts)

                text = " ".join(command_parts[2:])
                encoded_text = self.encode(text)
                command = 'edit ' + command_parts[1] + ' ' + encoded_text

            self.server.get_command(command)

    def char_to_num(self, c):
        return ord(c) - self.min_char

    def num_to_char(self, num):
        return chr(num + self.min_char)

    def sum(self, a, b):
        result = ""
        for i in range(len(a)):
         #   print("add1: ", a[i], self.char_to_num(a[i]), b[i % len(b)], self.char_to_num(b[i % len(b)]))
         #   print("add2: ", ((self.char_to_num(a[i]) + self.char_to_num(b[i % len(b)])) % self.chr_size), self.num_to_char((self.char_to_num(a[i]) + self.char_to_num(b[i % len(b)])) % self.chr_size))
            result += self.num_to_char((self.char_to_num(a[i]) + self.char_to_num(b[i % len(b)])) % self.chr_size)
        return result

    def sub(self, a, b):
        result = ""
        for i in range(len(a)):
         #   print("sub: ", ord(a[i]), ord(b[i % len(b)]))
            result += self.num_to_char((self.char_to_num(a[i]) - self.char_to_num(b[i % len(b)]) + self.chr_size) % self.chr_size)
        return result

    def encode(self, plain_text):
        return self.sum(plain_text, self.password)

    def decode(self, encoded_text):
        return self.sub(encoded_text, self.password)

    def get_message(self, message):
        words = message.split()

        if words[0] == 'file:':
            print(self.decode(' '.join(words[1:])))
        else:
            print(message)

    def get_address(self, address):
        dir_names = address.split('/')
        for i in range(len(dir_names)):
            dir_names[i] = self.decode(dir_names[i])
        address = '/'.join(dir_names)

        print(f'{dir_names[0]}({dir_names[0]}): {address}>')


def get_hashed_command(command, index_to_hash):
    command_parts = command.split()
    command_parts[index_to_hash] = sha256(command_parts[index_to_hash].encode('utf-8')).hexdigest()
    return " ".join(command_parts)
