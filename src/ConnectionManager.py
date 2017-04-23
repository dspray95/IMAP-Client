from imapclient import IMAPClient
import imaplib


class ConnectionManager():

    def __init__(self):
        self.conn = IMAPClient

    def connect(self, server):
        # Setup connection to Elwood #
        ssl = False
        print "Creating connection..."
        try:
            self.conn = IMAPClient(server, ssl=ssl)
            print "Connection success\n"
        except:
            raise ConnectionManagerException("Connection Failed")

    def login(self, username, password):
        try:
            self.conn.login(username, password)
        except:
            raise ConnectionManagerException("Login Failed")


class ConnectionManagerException(Exception):

    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


