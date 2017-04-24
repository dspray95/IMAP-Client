import email
import Tkinter as tk

class Messenger(tk.Frame):

    def get_body(self):
        msgRaw = email.message_from_string(self)
        print msgRaw

    def __init__(self, master, message, clean_message, row, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.master = master
        if row < 99:
            self.build_messenger(clean_message, row)
        self.message = message

    def build_messenger(self, clean_message, row):
        self.clean_msgid = clean_message[0]
        self.clean_subject = clean_message[1]
        self.clean_flags = clean_message[2]
        self.clean_sender = clean_message[3]
        self.clean_body = clean_message[4]
        self.row = row

        self.grid(column=1, row=self.row, columnspan=5, sticky=tk.W + tk.E + tk.N)

        self.button_select = tk.Checkbutton(self)
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
                                  command=lambda : self.view_message(self.message),
                                  padx=5,
                                  pady=0,
                                  text="view")
        self.btn_read.grid(column=5, row=self.row, padx=0, pady=0, sticky=tk.E)

    def view_message(self, message):
        print ""

class MessengerDud(Messenger):
    def __init__(self, master, message, clean_message, row, controller):
        Messenger.__init__(self, master, message, clean_message, row, controller)
        if row == 99:  # TODO: hacky
            self.master = master
            self.clean_msgid = clean_message[0]
            self.clean_subject = clean_message[1]
            self.clean_flags = clean_message[2]
            self.clean_sender = clean_message[3]
            self.clean_body = clean_message[4]
            self.row = 0

            self.grid(column=1, row=self.row, columnspan=5, sticky=tk.W + tk.E + tk.N)

            self.button_select = tk.Checkbutton(self)
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
                                       anchor=tk.E,
                                       text=self.clean_sender)
            self.lbl_sender.grid(column=4, row=self.row, padx=20, columnspan=1, pady=0, sticky=tk.E + tk.W)

            self.btn_read = tk.Button(self.master,
                                      anchor="e",
                                      command=lambda: self.view_message(),
                                      padx=5,
                                      pady=0,
                                      text="view")
            self.btn_read.grid(column=5, row=self.row, padx=0, pady=0, sticky=tk.E)


