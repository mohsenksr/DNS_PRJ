from server import Server
from hashlib import sha256
import base64


class Client:
    def __init__(self):
        self.server = Server(self)
        self.password = '-'

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


            self.server.get_command(command)


    def sum(self, a, b):
        result = ""
        for i in range(len(a)):
            result += chr(ord(a[i]) + ord(b[i % len(b)]))
        return result

    def sub(self, a, b):
        result = ""
        for i in range(len(a)):
            result += chr(ord(a[i]) - ord(b[i % len(b)]))
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
