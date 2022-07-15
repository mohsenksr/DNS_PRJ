from server import Server
from hashlib import sha256
from cryptography.fernet import Fernet
import base64


class Client:
    def __init__(self):
        self.server = Server(self)
        self.key = None

    def start(self):
        while True:
            command = input()
            if command == 'quit()':
                break

            if command.split()[0] == 'signup' and len(command.split()) == 5:
                command = get_hashed_command(command=command, index_to_hash=2)
                command = get_hashed_command(command=command, index_to_hash=3)
                command = get_hashed_command(command=command, index_to_hash=4)

                command_parts = command.split()
                key_base = 'DNS_PRJ_' + command_parts[2]
                self.key = base64.urlsafe_b64encode(((key_base * (32 // len(key_base) + 1))[:32]).encode('utf-8'))
                command_parts.append(self.encode(command_parts[1]))
                command = " ".join(command_parts)

            if command.split()[0] == 'signin' and len(command.split()) == 3:
                command = get_hashed_command(command=command, index_to_hash=2)

                command_parts = command.split()
                key_base = 'DNS_PRJ_' + command_parts[2]
                self.key = base64.urlsafe_b64encode(((key_base * (32 // len(key_base) + 1))[:32]).encode('utf-8'))
                command_parts.append(self.encode(command_parts[1]))
                command = " ".join(command_parts)

            self.server.get_command(command)

    def encode(self, text):
        fernet = Fernet(self.key)
        return fernet.encrypt(text.encode()).decode('utf-8')

    def decode(self, encoded_text):
        fernet = Fernet(self.key)
        return fernet.decrypt(encoded_text.encode('utf-8')).decode()

    def get_message(self, message):
        print(message)


def get_hashed_command(command, index_to_hash):
    command_parts = command.split()
    command_parts[index_to_hash] = sha256(command_parts[index_to_hash].encode('utf-8')).hexdigest()
    return " ".join(command_parts)
