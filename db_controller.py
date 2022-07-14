import sqlite3


class DBController:
    def __init__(self):
        self.connection = sqlite3.connect('DNS_PRJ.db')
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        create_user_table = """ CREATE TABLE IF NOT EXISTS User (
                            Username CHAR(25) NOT NULL PRIMARY KEY,
                            Password CHAR(25) NOT NULL
                            ); """
        self.cursor.execute(create_user_table)

    def user_signup(self, username, password):
        create_user = f""" INSERT INTO User VALUES ('{username}', '{password}'); """
        try:
            self.cursor.execute(create_user)
            self.connection.commit()
            return True
        except:
            return False

    def user_signin(self, username, password):
        get_user_pass = f""" SELECT * FROM User WHERE Username == '{username}' """
        try:
            result = self.cursor.execute(get_user_pass).fetchall()
            if len(result) == 1 and result[0][1] == password:
                return True
            else:
                return False
        except:
            return False
