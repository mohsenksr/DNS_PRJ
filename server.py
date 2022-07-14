from db_controller import DBController


class Server:
    def __init__(self, client):
        self.client_user = None
        self.client = client
        self.db_controller = DBController()

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
                else:
                    self.send_error_to_client('username exists')

            case 'signin':
                if len(command_parts) != 3:
                    self.send_error_to_client('wrong command')
                    return
                if self.db_controller.user_signin(username=command_parts[1], password=command_parts[2]):
                    self.client_user = command_parts[1]
                    self.send_info_to_client('signed in successfully')
                else:
                    self.send_error_to_client('incorrect username or password')

            case 'signout':
                if len(command_parts) != 1:
                    self.send_error_to_client('wrong command')
                if self.client_user:
                    self.client_user = None
                    self.send_info_to_client('signed out successfully')
                else:
                    self.send_error_to_client('you are not sign in')

            case other:
                self.send_error_to_client('wrong command')

    def send_message_to_client(self, message):
        self.client.get_message(message)

    def send_error_to_client(self, error):
        self.send_message_to_client('ERROR: ' + error)

    def send_info_to_client(self, info):
        self.send_message_to_client('INFO: ' + info)
