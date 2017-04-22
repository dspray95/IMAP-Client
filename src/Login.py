###### IMAP EMAIL CLIENT - NETWORKS ASSIGNMENT 1 - Login ######

from imapclient import IMAPClient
import imaplib

HOST = "elwood.yorkdc.net"
SSL = False

"""
## AttemptLogin ###
Attempt Login requires conn(IMAPClient)
Attempt login will gather user input for password and username, and try to login to conn

TODO: Secure login and connection
"""

HOST = "elwood.yorkdc.net"
SSL = False

def GetNewHost():
    HOST = raw_input()
    return HOST

def AttemptLogin():
    ## Setup connection to Elwood ##

    print "Creating connection..."
    try:
        conn = IMAPClient(HOST, ssl=SSL)
        print "Connection success\n"
    except imaplib.IMAP4.error:
        print "Connection failed"

    print "Welcome to Elwood"
    print "LOGIN\n"

    #  username = raw_input("Please Enter your username: ")
    #  password = raw_input("Now enter your password: ")
    ########TODO Change back to softcode
    conn.login("david.spray", "PUDU79X8")
    return conn

