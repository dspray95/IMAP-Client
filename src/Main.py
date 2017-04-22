###### IMAP EMAIL CLIENT - NETWORKS ASSIGNMENT 1 - MAIN ######

## Modules ##
import Login
import Messages
import Folder

## External Libraries
import imapclient
import imaplib
import sys

menuinstruction = "please choose an action... (help for help)"

## Login ##
def LoginMenu():

    bLoggingIn = True

    while bLoggingIn:
        try:
            conn = Login.AttemptLogin()
            bLoggingIn = False
        except imaplib.IMAP4.error:
            print "login failed... \n"
    return conn

## FolderMenu ##
def FolderMenu():
    bChoosingAction = True
    while bChoosingAction:
        Folder.ViewFolders(conn)
        print menuinstruction  # Console instructions for user
        action = raw_input()
        if action in "choose folder":
            try:
                folder_name = Folder.SelectFolder(conn)
                return folder_name
            except ReferenceError:
                print "INVALID FOLDER"
        if action in "create folder":
            Folder.new_folder(conn)
        if action in "delete folder":
            Folder.delete_folder(conn)

    return

def MessageMenu():
    ## Main menu, the user can navigate via console input from here ##
    bInMenu = True
    print "Message Menu"
    while bInMenu:
        print menuinstruction
        action = raw_input()
        if action in ["list"]:
            Messages.ListMessages(conn, folder)
        elif action in ['read']:
            messageToRead = int(input())
            Messages.ReadSingleMessage(conn, messageToRead, folder)
        elif action in ["read all"]:
            Messages.ReadMessages(conn)
        elif action in ["create"]:
            Messages.CreateDraftMessage(conn, folder)
        elif action in ["copy"]:
            Messages.copy_message(conn, folder)
        elif action in ["delete"]:
            Messages.delete_message(conn, folder)
        elif action in ["move"]:
            Messages.move_message(conn, folder)
        elif action in ["set flag"]:
            Messages.ChangeFlags(conn, folder, True)
        elif action in ["remove flag"]:
            Messages.ChangeFlags(conn, folder, False)
        elif action in ["search"]:
            Messages.SearchFolder(conn, folder)
        elif action in ["help"]:
            print ("HELP") # TODO
        elif action in ["folders"]:
            return bInMenu
        elif action in ["logout"]:
            conn.logout()
            sys.exit()
        else:
            print ("INVALID COMMAND")

def AccountLogout():
    print "Logging out..."
    try:
        conn.logout()
        print "Logout Successful"
        global bNavigatingMenus
        bNavigatingMenus = False
    except imaplib.IMAP4.error:
        print "err in logout"

    action = raw_input("Choose an option:\n1. Connect to elwood\n 2. Connect to another address ")
    if action in ["1"]:
        Login.AttemptLogin()
    if action in ["2"]:
        Login.GetNewHost()
        Login.AttemptLogin()

### Running the Application ###

bNavigatingMenus = True

conn = LoginMenu()
while bNavigatingMenus:
    folder = FolderMenu()
    MessageMenu()
    conn.close_folder()