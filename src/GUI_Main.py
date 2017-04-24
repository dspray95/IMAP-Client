import Tkinter as tk
from ConnectionHandler import ConnectionManager, ConnectionManagerException
from FolderHandler import FolderManager
from Messenger import Messenger
import sys
from ttk import Frame, Button, Style

class EmptyFrame(tk.Frame):
    """An abstract base class for the frames that sit inside PythonGUI.

    Args:
      master (tk.Frame): The parent widget.
      controller (HolderFrame): The controlling Tk object.

    Attributes:
      controller (HolderFrame): The controlling Tk object.

    """

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the frame."""



class LoginFrame(EmptyFrame):
    def create_widgets(self):
        """Creating the login interface"""
        self.lbl_title = tk.Label(self, text="Sign In")
        self.lbl_title.grid(column=0,row=0,columnspan=2, padx=20, pady=20, sticky=tk.W+tk.E)
        self.lbl_address = tk.Label(self, text="Server: ")
        self.lbl_address.grid(column=0, row=1)
        self.ent_address = tk.Entry(self)
        self.ent_address.insert(0, "elwood.yorkdc.net")
        self.ent_address.grid(column=1, row=1, padx=20)

        self.lbl_username = tk.Label(self, text="Username: ")
        self.lbl_username.grid(column=0, row=2)
        self.ent_username = tk.Entry(self)
        self.ent_username.insert(0, "david.spray")
        self.ent_username.grid(column=1, row=2, padx=20)

        self.lbl_password = tk.Label(self, text="Password: ")
        self.lbl_password.grid(column=0, row=3)
        self.ent_password = tk.Entry(self)
        self.ent_password.insert(0, "PUDU79X8")
        self.ent_password.grid(column=1, row=3, padx=20)

        self.btn_login = tk.Button(self,
                                    anchor=tk.W,
                                    command=lambda: self.controller.try_connection(self.ent_address.get(),
                                                                                   self.ent_password.get(),
                                                                                   self.ent_username.get()),
                                    padx=5,
                                    pady=5,
                                    text="Login")
        self.btn_login.grid(column=0,row=5, padx=20, pady=20, sticky=tk.W+tk.E)
        self.btn_exit = tk.Button(self,
                                    anchor=tk.W,
                                    command=lambda: self.controller.show_frame(LoginFrame),
                                    padx=5,
                                    pady=5,
                                    text="Exit")
        self.btn_exit.grid(column=1,row=5, padx=20, pady=20, sticky=tk.W + tk.E)


class FolderFrame(EmptyFrame):

    def __init__(self, master, controller):
        EmptyFrame.__init__(self, master, controller)
        self.folders = list()
        self.inbox_frame = InboxFrame(self, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=8)
        self.inbox_frame.grid(column=1, row=0, padx=0, pady=0, sticky = tk.W+tk.E, )
        self.configure(bg = "blue")

    def set_folders(self, filing_cabinet):
        self.filing_cabinet = filing_cabinet
        self.folders = filing_cabinet.list_folders()

    def create_widgets(self):
        """Create the base widgets for the frame."""

    def populate_folders(self):
        buttons = list()
        self.buttons_frame = tk.Frame(self)
        i = 0
        for folder in self.folders:
            print "creating button for ", folder
            buttons.append(tk.Button(self.buttons_frame,
                                        anchor="w",
                                        command=lambda folder=folder: self.inbox_frame.setup_messages(folder),
                                        padx=5,
                                        pady=0,
                                        text=folder))
            buttons[i].pack(fill=tk.BOTH, expand=1)
            i = i+1
            # buttons[i].grid(column = 0, row = i, sticky=tk.W+tk.E)
            # i = i + 1
        self.buttons_frame.grid(column = 0, row = 0, sticky=tk.W+tk.E)

    def setup_messages(self, folder):
        self.inbox_frame.update_inbox(folder)

class InboxFrame(EmptyFrame):

    def __init__(self, master, controller):
        EmptyFrame.__init__(self, master, controller)
        self.messengers = list()

    def update_inbox(self, folder):
        self.configure(bg = "blue")
        self.folder = folder
        fetched_messages = self.controller.get_messages(self.folder)
        print "fetched messages"
        clean_messages = self.controller.get_clean_messages(self.folder)

        print "Fetched", len(fetched_messages)
        print "Cleaned", len(clean_messages)
        self.messengers = list()

        i = 0
        for message in fetched_messages:
            self.messengers.append(Messenger(self.master, message, clean_messages[i], i))
            i = i + 1

        x = 0
        # for messenger in self.messengers:
        #     messenger.grid(column=1, row = x)
        #     x = x + 1

    def empty_inbox(self):
        for message in self.messengers:
            message.destroy()

    def setup_messages(self, folder):
        self.empty_inbox()
        self.update_inbox(folder)


class HolderFrame(tk.Tk):
    """The main window of the GUI.

    Attributes:
      container (tk.Frame): The frame container for the sub-frames.
      frames (dict of tk.Frame): The available sub-frames.

    """

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Python GUI")
        self.init_holder()
        self.resizable(0, 0)
        self.connector = ConnectionManager()
        self.filing_cabinet = FolderManager()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(bg = "red")

    def init_holder(self):
        self.frames = {}
        for f in (LoginFrame, FolderFrame, InboxFrame): # Classes to include
            frame = f(self, self)
            frame.grid(row=0, column=0, sticky=tk.NW+tk.SE)
            self.frames[f] = frame
        self.show_frame(LoginFrame)

    def show_frame(self, frame):
        self.frames[frame].tkraise()
        if frame in [FolderFrame]:
            self.minsize(width=800, height=600)
        if frame in [LoginFrame]:
            self.minsize(width=300, height=220)

    def try_connection(self, server, password, username):
        print server, password, username
        b_connected = False
        b_logged_in = False
        try:
            self.conn = self.connector.connect(server)
            b_connected = True;
        except ConnectionManagerException:
            print "connect failed"

        if b_connected:
            try:
                self.conn = self.connector.login(username, password)
                self.filing_cabinet.set_conn(self.connector.conn)
                b_logged_in = True
            except ConnectionManagerException:
                print "Login Failed"  # TODO: Relay this to user through GUI

        if b_logged_in:
            self.frames[FolderFrame].set_folders(self.filing_cabinet)
            self.frames[FolderFrame].populate_folders()
            self.show_frame(FolderFrame)
            return

    def choose_folder(self, folder):
        print "choosing folder ", folder
        self.conn = self.filing_cabinet.select_folder(folder)
        print folder

    def get_messages(self, folder):
        messages = self.filing_cabinet.get_messages(folder)
        return messages

    def get_clean_messages(self, folder):
        clean_messages = self.filing_cabinet.get_clean_messages(folder)
        return clean_messages

app = HolderFrame()
app.mainloop()
app.protocol("WM_DELETE_WINDOW", sys.exit())
exit()