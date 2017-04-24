from imapclient import IMAPClient
import imaplib


class ConnectionManager():

    def connect(self, server):
        # Setup connection to Elwood #
        ssl = False
        print "Creating connection..."
        try:
            self.conn = IMAPClient(server, ssl=ssl)
            print "Connection success\n"
        except:
            raise ConnectionManagerException("Connection Failed")
        return self.conn

    def login(self, username, password):
        try:
            self.conn.login(username, password)
            print "logged in"#
        except:
            raise ConnectionManagerException("Login Failed")
        return self.conn

class ConnectionManagerException(Exception):

    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


