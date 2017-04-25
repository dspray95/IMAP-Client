import imaplib
import email


class FolderManager():

    def set_conn(self, conn):
        """
        grabs the input IMAPClient from the main gui controller and sets up for use.
        initially selects the folder INBOX 
        :param conn: IMAPClient
        :return: 
        """
        self.conn = conn
        self.folders = conn.list_folders()
        self.conn.select_folder("INBOX")  # Initial folder, shouldn't be hardcoded, should be set with list(0)

    def list_folders(self):
        """
        returns a list of folder names for GUI use
        :return: 
        """
        folders = self.conn.list_folders()
        print 'FOLDERS'
        clean_folders = list()  # List of folder names as strings only e.g "Folder1", "Folder2" etc.
        for flags, delimiter, folder_name in folders:
            to_append = '%s' % folder_name
            clean_folders.append(to_append)
        return clean_folders

    def select_folder(self, folderName):
        """
        Returns conn with a selected folder (folderName)
        :param folderName: folder to connect
        :return: conn(IMAPClient)
        """
        folders = self.conn.list_folders()

        folderName = folderName.upper()
        self.conn.close_folder()

        b_folder_found = False

        for flags, delimiter, folder_name in folders:
            if folderName in [folder_name]:
                self.conn.select_folder(folderName)
                print "Folder Set To: ", folderName
                return folderName
        if not b_folder_found:
            raise ReferenceError("Could not select folder")
        print "FOLDER NOT FOUND"
        return self.conn

    def get_messages(self, folder):
        """
        Gathers messages from the selected folder and returns them in a list format
        :param folder: 
        :return: 
        """
        select_info = self.conn.select_folder(folder)

        messages = self.conn.search(['NOT', 'DELETED'])  # This is used when listing the messages and their attributes

        response = self.conn.fetch(messages,['RFC822', 'FLAGS', 'RFC822.SIZE', 'BODY[TEXT]'])
        self.messages_in_folder = list()

        for msgid, data in response.iteritems():  # Iterate through messages and output attributes to console
            msgRaw = email.message_from_string(data['RFC822'])
            self.messages_in_folder.append(data['RFC822'])
        return self.messages_in_folder


    def get_clean_messages(self, folder):
        """
        'Cleans' messages and returns them as a list of strings
        :param folder: 
        :return: 
        """
        messages = self.conn.search(['NOT', 'DELETED'])  # This is used when listing the messages and their attributes

        response = self.conn.fetch(messages, ['RFC822', 'FLAGS', 'RFC822.SIZE', 'BODY[TEXT]'])  # Gather needed attributes

        clean_messages = list()

        for msgid, data in response.iteritems():  # Iterate through messages and output attributes to console
            msgRaw = email.message_from_string(data['RFC822'])
            subject = msgRaw['Subject']
            sender = msgRaw['From']
            msgid = msgid
            flags = data[b'FLAGS']
            body = msgRaw['BODY[TEXT']
            if subject in [None]:
                subject = 'No Subject'
            if sender in [None]:
                sender = 'No Sender'
            if msgid in [None]:
                msgid = "no id"
            if flags in [None]:
                flags = "no flags"
            clean_message = msgid, subject, flags, sender, body
            clean_messages.append(clean_message)
        return clean_messages
