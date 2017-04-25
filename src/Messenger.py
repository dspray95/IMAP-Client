import email
import Tkinter as tk
import imaplib

class Messenger(tk.Frame):
    """
    The messenger class is used to send and update attributes of a message to the GUI. 
    
    widgets here get sent to a holder frame in inbox_frame before being added to the grid layout
    this is done to keep alignment with all the messenger objects, while still keeping the benefit of having this class
    separate from it's inbox_frame
    """
    def __init__(self, master, message, clean_message, row, inbox, controller):
        """
        :param master: Master (Usually the inbox's master
        :param message: email message object
        :param clean_message: cleaned email object for putting to strings 
        :param row: the grid.row to which the messenger should be placed
        :param inbox: the inbox which contains the message mobject
        :param controller: The GUI main controller
        """
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.master = master
        self.inbox = inbox
        if row < 99:
            self.build_messenger(clean_message, row)
        self.message_raw = message
        self.message = email.message_from_string(message)
        self.message_view_widgets = list
        self.message_view = tk.Frame(self.controller)

    def build_messenger(self, clean_message, row):
        """
        Builds the widgets for the messenger. Widgets are built to master in order to keep them
        grid aligned
        :param clean_message: cleaned message object for passing to string
        :param row: row to which the message should be inserted
        """
        self.clean_msgid = clean_message[0]
        self.clean_subject = clean_message[1]
        self.clean_flags = clean_message[2]
        self.clean_sender = clean_message[3]
        self.clean_body = clean_message[4]
        self.row = row

        self.grid(column=1, row=self.row, columnspan=5, sticky=tk.W + tk.E + tk.N)

        self.button_select = tk.Checkbutton(self.master)
        self.button_select.grid(column=1, row=self.row, padx=5, pady=5, sticky=tk.W+tk.E)
        self.lbl_msgid = tk.Label(self.master,
                                  anchor=tk.W,
                                  text=self.clean_msgid)
        self.lbl_msgid.grid(column=2, row=self.row, padx=20, pady=0, sticky=tk.W+tk.E)
        self.lbl_subject = tk.Label(self.master,
                                    anchor=tk.W,
                                    text=self.clean_subject)
        self.lbl_subject.grid(column=3, row=self.row, padx=20, pady=0, sticky=tk.W+tk.E)
        self.lbl_sender = tk.Label(self.master,
                                   anchor=tk.E,
                                   text=self.clean_sender)
        self.lbl_sender.grid(column=4, row=self.row, padx=20, columnspan = 1, pady=0, sticky=tk.E+tk.W)

        self.btn_read = tk.Button(self.master,
                                  anchor="e",
                                  command=lambda : self.get_viewbox(self.message),
                                  padx=5,
                                  pady=0,
                                  text="view")
        self.btn_read.grid(column=5, row=self.row, padx=0, pady=0, sticky=tk.E)

        self.btn_delete = tk.Button(self.master,
                                    anchor="e",
                                    command=lambda : self.delete_message(),
                                    padx=5,
                                    pady=0,
                                    text="delete")
        self.btn_delete.grid(column=6, row=self.row, padx=0, pady=0, sticky=tk.E)

    def get_viewbox(self, message):
        """
        Here we build the message to be viewed once the view button has been clicked.
        We gather the email's details before sending them to a widget, then we add any
        extra widgets (close, copy, move, delete etc.) and grid them into a frame
        :param message: Message to parse
        :return: viewbox: Frame
        """
        msgRaw = message
        subject = email.utils.parseaddr(msgRaw['Subject'])
        sender = email.utils.parseaddr(msgRaw['From'])
        if msgRaw.is_multipart():
            body = msgRaw.get_payload(0).get_payload()
            # for part in msgRaw.get_payload():
            #     body = body + part.get_payload()
            #     print part.get_payload()
        else:
            body = msgRaw.get_payload(decode = True)


        self.lbl_subject = tk.Label(self.message_view,
                               anchor=tk.W,
                               text = "Subject")
        lbl_message_subject = tk.Label(self.message_view,
                                       anchor=tk.W,
                                       text=subject)
        lbl_sender = tk.Label(self.message_view,
                              anchor=tk.W,
                              text = "From")
        lbl_message_sender = tk.Label(self.message_view,
                                      anchor=tk.W,
                                      text = sender)
        lbl_body = tk.Label(self.message_view,
                            anchor=tk.W,
                            text="Body")
        lbl_message_body = tk.Label(self.message_view,
                                    anchor=tk.W,
                                    text=body)
        btn_back = tk.Button(self.message_view,
                                  anchor="e",
                                  command=lambda : self.hide_message_view(),
                                  padx=5,
                                  pady=0,
                                  text="back")
        self.lbl_subject.grid(column=0, row=0, padx=5, sticky=tk.N)
        lbl_message_subject.grid(column=1, row=0, sticky=tk.W)
        lbl_sender.grid(column=0, row=1, padx=5, sticky=tk.N)
        lbl_message_sender.grid(column=1, row =1, sticky=tk.W)
        lbl_body.grid(column=0, row=2, padx=5, sticky=tk.N)
        lbl_message_body.grid(column=1, row=2, sticky=tk.W)
        btn_back.grid(column = 1, row = 3, sticky=tk.E)
        self.inbox.push_message_view(self.message_view)

    def hide_message_view(self):
        """
        Removes this object from the master grid view
        :return: 
        """
        self.message_view.grid_remove()
        self.inbox.hide_message_view(self.message_view)

    def get_message(self):
        return self.message

    def delete_message(self):
        """
        Goes through the process of first deleting the message from the main gui controllers
        conn(IMAPClient) then removing the dud entries from the Inbox and its GUI.
        :return: 
        """
        conn = self.controller.controller.get_conn()
        folder = self.inbox.get_folder()
        conn.select_folder(folder)
        messages = conn.search(['NOT', 'DELETED'])
        response = conn.fetch(messages, ['RFC822', 'BODY[TEXT]', 'FLAGS'])
        # Find the deleted message and delete
        for msgid, data in response.iteritems():
            if msgid == self.clean_msgid:
                conn.delete_messages(msgid)
                print "deleted message"
        self.hide_message_view()
        self.inbox.purge_messages()
        # except imaplib.IMAP4.error:
        #     print "Could not delete"
        #     raise ReferenceError("Could not delete")

class MessengerDud(Messenger):
    """
    Used in setting the headers for the inbox window
    """
    def __init__(self, master, message, clean_message, row, inbox, controller):
        Messenger.__init__(self, master, message, clean_message, row, inbox, controller)
        self.message_view_widgets = list()
        if row == 99:  # TODO: hacky
            self.master = master
            self.clean_msgid = clean_message[0]
            self.clean_subject = clean_message[1]
            self.clean_flags = clean_message[2]
            self.clean_sender = clean_message[3]
            self.clean_body = clean_message[4]
            self.row = 0

            self.grid(column=1, row=self.row, columnspan=5, sticky=tk.W + tk.E + tk.N)

            self.button_select = tk.Checkbutton(self.master)
            self.button_select.grid(column=1, row=self.row, padx=5, pady=5, sticky=tk.W)
            self.lbl_msgid = tk.Label(self.master,
                                      anchor=tk.W,
                                      text=self.clean_msgid)
            self.lbl_msgid.grid(column=2, row=self.row, padx=20, pady=0, sticky=tk.W + tk.E)
            self.lbl_subject = tk.Label(self.master,
                                        anchor=tk.W,
                                        text=self.clean_subject)
            self.lbl_subject.grid(column=3, row=self.row, padx=20, pady=0, sticky=tk.W + tk.E)
            self.lbl_sender = tk.Label(self.master,
                                       anchor=tk.W,
                                       text=self.clean_sender)
            self.lbl_sender.grid(column=4, row=self.row, padx=20, columnspan=1, pady=0, sticky=tk.W)

            self.lbl_read = tk.Label(self.master,
                                      anchor=tk.W,
                                      text="view")
            self.lbl_read.grid(column=5, row=self.row, padx=0, pady=0, sticky=tk.W)


