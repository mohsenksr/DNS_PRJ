from server import Server
from hashlib import sha256
from cryptography.fernet import Fernet


class Client:
    def __init__(self):
        self.server = Server(self)
        self.hash_user_name = None

    def start(self):
        while True:
            command = input()
            if command == 'quit()':
                break

            if command.split()[0] == 'signup' and len(command.split()) == 5:
                command_parts = command.split()
                command_parts[2] = sha256(command_parts[2].encode('utf-8')).hexdigest()
                self.hash_user_name = sha256(command_parts[1].encode('utf-8')).hexdigest()
                command_parts.append(self.hash_user_name)
                command = " ".join(command_parts)

            if command.split()[0] == 'signin' and len(command.split()) == 3:
                command_parts = command.split()
                command_parts[2] = sha256(command_parts[2].encode('utf-8')).hexdigest()
                command = " ".join(command_parts)
            self.server.get_command(command)

    def get_message(self, message):
        print(message)
