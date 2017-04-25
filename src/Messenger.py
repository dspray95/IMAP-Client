import email
import Tkinter as tk

class Messenger(tk.Frame):
    """
    widgets here get sent to a holder frame in inbox_frame before being added to the grid layout
    this is done to keep alignment with all the messenger objects, while still keeping the benefit of having this class
    separate from it's inbox_frame
    """
    def __init__(self, master, message, clean_message, row, inbox, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.master = master
        self.inbox = inbox
        if row < 99:
            self.build_messenger(clean_message, row)
        self.message = message
        self.message_view_widgets = list
        self.message_view = tk.Frame(self.controller)

    def build_messenger(self, clean_message, row):
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

    def get_body(self):
        msgRaw = email.message_from_string(self)

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
        body = msgRaw.get_payload()


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
        self.lbl_subject.grid(column=0, row=0, padx=5, sticky=tk.N)
        lbl_message_subject.grid(column=1, row=0, sticky=tk.W)
        lbl_sender.grid(column=0, row=1, padx=5, sticky=tk.N)
        lbl_message_sender.grid(column=1, row =1, sticky=tk.W)
        lbl_body.grid(column=0, row=2, padx=5, sticky=tk.N)
        lbl_message_body.grid(column=1, row=2, sticky=tk.W)
        self.inbox.push_message_view(self.message_view)

    def hide_message_view(self):
        self.message_view.grid_remove()



class MessengerDud(Messenger):
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


