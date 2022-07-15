from server import Server


class Client:
    def __init__(self):
        self.server = Server(self)

    def start(self):
        while True:
            command = input()
            if command == 'quit()':
                break
            else:
                self.server.get_command(command)

    def get_message(self, message):
        print(message)
