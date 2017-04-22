###### IMAP EMAIL CLIENT - NETWORKS ASSIGNMENT 1 - INBOX ######

# External Librares
import email
import imaplib

divider = "--------------------------------------------------"  # Divider used in cleaning up text interface

"""
## ListMessages ##
ListMessages requires conn(IMAPClient) and folder(STRING)
ListMessages will display the number messages, and the number of unread messages, in 'folder'
ListMessages will then display each message with Subject, From Address, msgid, bytes, and flags
"""
def ListMessages(conn, folder):
    select_info = conn.select_folder(folder)

    print divider
    print folder
    print('%d messages' % select_info['EXISTS'])  # Prints the number of messages that exist

    messages = conn.search(['NOT', 'DELETED'])  # This is used when listing the messages and their attributes
    unseen = conn.search([u'UNSEEN'])  # Narrow the search to the unseen messages

    print('%d unread messages' % len(unseen))  # Print the number of unseen messages
    print divider
    print 'Messages:'

    response = conn.fetch(messages, ['RFC822', 'FLAGS', 'RFC822.SIZE', 'BODY[TEXT]'])  # Gather needed attributes

    for msgid, data in response.iteritems():  # Iterate through messages and output attributes to console
        msgRaw = email.message_from_string(data['RFC822'])
        subject = "Subject:", email.utils.parseaddr(msgRaw['Subject'])
        sender = "From: ", email.utils.parseaddr(msgRaw['From'])
        print subject, sender
        print('   ID %d: %d bytes, flags=%s' % (msgid,
                                                data[b'RFC822.SIZE'],
                                                data[b'FLAGS']))
    print divider

"""
## ReadMessages ##
Requires conn(IMAPClient)
Reads every message currently in 'conn' selected folder
"""
def ReadMessages(conn):
    messages = conn.search(['NOT', 'DELETED'])
    response = conn.fetch(messages, ['RFC822', 'BODY[TEXT]'])

    for msgid, data in response.iteritems():
        msgRaw = email.message_from_string(data['RFC822'])
        PrintMessage(msgRaw)

"""
## ReadSingleMessage ##
Requires conn(IMAPClient, idToRead(int), folder(Folder)
Finds the undeleted message by the msgid number, then prints to the console
"""
def ReadSingleMessage(conn, idToRead, folder):
    conn.select_folder(folder)
    messages = conn.search(['NOT', 'DELETED'])
    response = conn.fetch(messages, ['RFC822', 'BODY[TEXT]'])

    bMessageFound = False
    for msgid, data in response.iteritems():
        if msgid == idToRead:
            print 'Reading message ', msgid, '...'
            msgRaw = email.message_from_string(data['RFC822'])
            PrintMessage(msgRaw)
            bMessageFound = True
            break
    if not bMessageFound:
        print "Could not find message ID", idToRead, " in ", folder

"""
## CreateMessage ##
Requires conn(IMAPClient), folder(Folder)
CreateMessage will create a message containing a subject and a body, and store the message in the
'folder' variable
"""
def CreateDraftMessage(conn, folder):
    msg = email.message.Message()
    msg['Subject'] = raw_input("subject: ")
    msg.set_payload(raw_input("body: "))
    conn.append(folder, str(msg))


"""
#SetMessageFlags
Requires conn(IMAPClient), folder(Folder), idToRead(int)
"""
def ChangeFlags(conn, folder, setting):

    idToRead = int(input("Email id (int) : "))
    flag = raw_input("Flag name (without backspaces):")

    conn.select_folder(folder)
    messages = conn.search(['NOT', 'DELETED'])
    response = conn.fetch(messages, ['RFC822', 'BODY[TEXT]', 'FLAGS'])

    for msgid, data in response.iteritems():
        if msgid == idToRead:
            flag = "\\" + flag
            try:
                if setting:
                    print 'Setting flag: ', flag, ' for ', msgid, '...'
                    conn.add_flags(msgid, [flag])
                else:
                    print 'Removing flag: ', flag, ' for ', msgid, '...'
                    conn.remove_flags(msgid, [flag])
            except:
                print "Could not set flag (flags should be a single word string only eg. flagged)"


"""
## Search ##
"""
def SearchFolder(conn, folder):

    query = raw_input('Search: ')

    conn.select_folder(folder)
    messages = conn.search([u'SUBJECT', query, b'NOT', b'DELETED'])
    messages = messages + conn.search([u'FROM', query, b'NOT', b'DELETED'])
    response = conn.fetch(messages, ['RFC822', 'FLAGS', 'RFC822.SIZE', 'BODY[TEXT]'])  # Gather needed attributes

    for msgid, data in response.iteritems():  # Iterate through messages and output attributes to console
        msgRaw = email.message_from_string(data['RFC822'])
        subject = "Subject:", email.utils.parseaddr(msgRaw['Subject'])
        sender = "From: ", email.utils.parseaddr(msgRaw['From'])
        print subject, sender
        print('   ID %d: %d bytes, flags=%s' % (msgid,
                                                data[b'RFC822.SIZE'],
                                                data[b'FLAGS']))


def copy_message(conn, folder, message=0, destination="", only_copy=True):
    if only_copy:
        message = int(input("Email id (int) : "))
        destination = raw_input("Destination folder: ")
        destination = destination.upper()

    conn.select_folder(folder)
    messages = conn.search(['NOT', 'DELETED'])
    response = conn.fetch(messages, ['RFC822', 'BODY[TEXT]', 'FLAGS'])

    for msgid, data in response.iteritems():
        if msgid == message:
            try:
                conn.copy(msgid, destination)
                if only_copy:
                    print "Message copied to ", destination
            except imaplib.IMAP4.error:
                print "Could not copy"
                raise ReferenceError("Could not copy")


def delete_message(conn, folder, only_delete=True):
    if only_delete:
        message = int(input("Email id (int) : "))

    conn.select_folder(folder)
    messages = conn.search(['NOT', 'DELETED'])
    response = conn.fetch(messages, ['RFC822', 'BODY[TEXT]', 'FLAGS'])

    for msgid, data in response.iteritems():
        if msgid == message:
            try:
                conn.delete_messages(msgid)
                if only_delete:
                    print "Message deleted"
            except imaplib.IMAP4.error:
                print "Could not copy"
                raise ReferenceError("Could not copy")

def move_message(conn, folder):
    message = int(input("Email id (int) : "))
    destination = raw_input("Destination folder: ")
    destination = destination.upper()

    b_file_copied = False
    try:
        copy_message(conn, folder, message, destination, False)
        b_file_copied = True
    except ReferenceError as inst:
        print "Could not move file"
        print inst.args
    if b_file_copied:
        try:
            conn.select_folder(folder)
            conn.delete_messages(message)
        except imaplib.IMAP4.error:
            print "Could not delete old file"


"""
## PrintMessage ##
Pint Message requires msgRaw(Message) 
Print Message outputs the Subject, To/From Address, and Body of msgRaw
"""
def PrintMessage(msgRaw):
    print divider
    print "Subject:", email.utils.parseaddr(msgRaw['Subject'])
    print "To: ", email.utils.parseaddr(msgRaw['to'])
    print "From: ", email.utils.parseaddr(msgRaw['From'])
    print "\nBody: \n", msgRaw.get_payload()
    print divider
