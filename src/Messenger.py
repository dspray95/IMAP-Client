import email
import Tkinter as tk

class Messenger(tk.Frame):
    def get_body(self):
        msgRaw = email.message_from_string(self)
        print msgRaw


    def __init__(self, master, message, clean_message, row):
        tk.Frame.__init__(self, master)
        self.message = message
        self.clean_msgid = clean_message[0]
        self.clean_subject = clean_message[1]
        self.clean_flags = clean_message[2]
        self.clean_sender = clean_message[3]
        self.clean_body = clean_message[4]
        self.row = row

        self.grid(column=1, row=self.row, columnspan=4, sticky = tk.W+tk.E+tk.N)

        self.button_select = tk.Checkbutton(self)
        self.button_select.grid(column=1, row=self.row, padx=5, pady=5, sticky=tk.W)
        self.lbl_msgid = tk.Label(self,
                                  anchor=tk.W,
                                  text = self.clean_msgid)
        self.lbl_msgid.grid(column = 2, row=self.row, padx=20, pady=0, sticky=tk.W)
        self.lbl_subject = tk.Label(self,
                                  anchor=tk.W,
                                  text = self.clean_subject)
        self.lbl_subject.grid(column = 3, row=self.row, padx=20, pady=0, sticky=tk.W)
        self.lbl_sender = tk.Label(self,
                                  anchor=tk.W,
                                  text = self.clean_sender)
        self.lbl_sender.grid(column = 4, row=self.row, padx=20, pady=0, sticky=tk.W)