import Tkinter as tk
from ConnectionHandler import ConnectionManager, ConnectionManagerException
from FolderHandler import FolderManager
from Messenger import Messenger, MessengerDud
import sys
from ttk import Frame, Button, Style


class EmptyFrame(tk.Frame):
    '''
    Used as a base for most of the frames in the GUI
    '''
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the frame."""



class LoginFrame(EmptyFrame):
    '''
    Handles connection to server and login
    '''
    def create_widgets(self):
        '''
        Creates the login interface
        :return: 
        '''
        self.lbl_title = tk.Label(self, text="Sign In")
        self.lbl_title.grid(column=0,row=0,columnspan=2, padx=20, pady=20, sticky=tk.W+tk.E)
        self.lbl_address = tk.Label(self, text="Server: ")
        self.lbl_address.grid(column=0, row=1)
        self.ent_address = tk.Entry(self)
        self.ent_address.insert(0, "elwood.yorkdc.net") # Defaults to elwood
        self.ent_address.grid(column=1, row=1, padx=20)

        self.lbl_username = tk.Label(self, text="Username: ")
        self.lbl_username.grid(column=0, row=2)
        self.ent_username = tk.Entry(self)
        self.ent_username.grid(column=1, row=2, padx=20)

        self.lbl_password = tk.Label(self, text="Password: ")
        self.lbl_password.grid(column=0, row=3)
        self.ent_password = tk.Entry(self)
        self.ent_password.grid(column=1, row=3, padx=20)

        # This button will gather up all of the user details and send them to the controller for connection
        self.btn_login = tk.Button(self,
                                    anchor=tk.W,
                                    command=lambda: self.controller.try_connection(self.ent_address.get(),
                                                                                   self.ent_password.get(),
                                                                                   self.ent_username.get()),
                                    padx=5,
                                    pady=5,
                                    text="Login")
        self.btn_login.grid(column=1,row=5, padx=20, pady=20, sticky=tk.W+tk.E)
        self.btn_exit = tk.Button(self,
                                    anchor=tk.W,
                                    padx=5,
                                    pady=5,
                                    text="Exit")  # TODO: Impliment quit here
        self.btn_exit.grid(column=0,row=5, padx=20, pady=20, sticky=tk.W + tk.E)


class FolderFrame(EmptyFrame):
    '''Holds the folder and inbox views'''
    def __init__(self, master, controller):
        EmptyFrame.__init__(self, master, controller)
        self.folders = list()
        self.inboxes = list()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=8)

    def set_folders(self, filing_cabinet):
        '''
        Grab the folders from the filing cabinet and store them here.
        create and populate the inbox_folders
        :param filing_cabinet: (FolderHandler)
        :return: 
        '''
        self.filing_cabinet = filing_cabinet
        self.folders = filing_cabinet.list_folders()
        for folder in self.folders:
            inbox_frame = InboxFrame(self, self.controller, folder)
            inbox_frame.grid(column=1, row=1, padx=0, pady=0, sticky=tk.W + tk.E)
            self.inboxes.append(inbox_frame)

    def populate_folders(self):
        '''
        Grab the folder names from the list of folders and push them to the GUI
        :return: 
        '''
        buttons = list()
        self.buttons_frame = tk.Frame(self)
        self.lbl_title = tk.Label(self.buttons_frame, text="Folders")
        self.lbl_title.pack(fill=tk.BOTH, expand=1)
        self.buttons_frame.grid(column = 0, row = 1, sticky=tk.W+tk.E+tk.N)
        i = 0
        # Create buttons for folders
        for folder in self.folders:
            current_inbox = self.inboxes[i]
            buttons.append(tk.Button(self.buttons_frame,
                                     anchor="w",
                                     command=lambda current_inbox = current_inbox: current_inbox.switch_inboxes(self.inboxes),
                                     padx=5,
                                     pady=0,
                                     text=folder))
            buttons[i].pack(fill=tk.BOTH, expand=1)
            row = i + 1
            # buttons[i].grid(column=0, row=row, padx=0, pady=0, sticky=tk.W+tk.E+tk.N+tk.S)
            self.rowconfigure(row, minsize=30)
            i = i + 1
        # Set a default inbox, currently first alpabetical TODO: User set default
        self.inboxes[0].switch_inboxes(self.inboxes)

    def refresh_inboxes(self):
        '''
        Update ever inbox, currently very intensive due to re-creating widgets.
        TODO: Efficiency
        :return: 
        '''
        for inbox in self.inboxes:
            inbox.update_inbox()

class InboxFrame(EmptyFrame):
    '''
    Manages the list of messengers from the folder variable
    '''
    def __init__(self, master, controller, folder):
        '''
        :param master: Frame 
        :param controller: tk.Tk
        :param folder: String
        '''
        EmptyFrame.__init__(self, master, controller)
        self.folder = folder
        self.controller = controller
        self.messengers = list()
        self.message_container = tk.Frame(self)
        self.update_inbox()
        self.grid_columnconfigure(0, weight=2)
        self.message_views = list()  # TODO: unnecessary memory use, use caching

    def get_folder(self):
        return self.folder

    def update_inbox(self):
        '''
        Uses a FolderHandler to update the current list of messages in this inbox
        Once it has the fetched messages from the FolderHandler, messengers are created
        and then they are pushed to the GUI
        Resource Intensive due to creation of many widgets
        :return: 
        '''
        self.message_container = tk.Frame(self) #reset the message container for population
        fetched_messages = self.controller.get_messages(self.folder)
        clean_messages = self.controller.get_clean_messages(self.folder)

        self.messengers = list()

        i = 0
        clean_message_dud = 1, "Subject", "Flags", "Sender", "Body"
        MessengerDud(self.message_container, "message_dud", clean_message_dud, 99, self, self.controller)
        for message in fetched_messages:
            self.messengers.append(Messenger(self.message_container, message, clean_messages[i], i+1, self, self.master))
            i = i + 1
        for x in range(60):
            self.message_container.columnconfigure(x, weight=1)
        # The message_container holds all of the widgets from each messenger in messengers
        self.message_container.grid(column = 0, row = 1, sticky=tk.W+tk.E+tk.N)

    def switch_inboxes(self, other_inboxes):
        '''
        Simple frame swap, hides any other inbox and shows self
        :param other_inboxes: list of inboxes 
        :return: 
        '''
        for inbox in other_inboxes:
            inbox.grid_remove()
        for messenger in self.messengers:
            messenger.hide_message_view()
        self.grid(column = 1, row = 1, sticky=tk.W+tk.E+tk.N)

    def push_message_view(self, message_view):
        ''''''
        self.grid_remove()
        message_view.grid(column=1,row=1, sticky=tk.W+tk.E+tk.N)

    def hide_message_view(self, message_view):
        '''
        Hides the current message_view object, used when viewing and individual messages, usually called by a
        Messenger
        :param message_view: Frame
        :return: 
        '''
        message_view.grid_remove()
        self.grid()

    def purge_messengers(self):
        for messenger in self.messengers:
            messenger.hide_message_view()
        for message_view in self.message_views:
            self.hide_message_view(message_view)
        self.update_inbox()

class HolderFrame(tk.Tk):
    """The main window of the GUI, controller for most objects
    """

    def __init__(self):
        '''
        Set up the managers and the layout
        '''
        tk.Tk.__init__(self)
        self.title("Python IMAP Manager")
        self.init_holder()
        self.resizable(0, 0)
        self.connector = ConnectionManager()
        self.filing_cabinet = FolderManager()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def init_holder(self):
        '''
        more setup, grab and create frames, and show the login
        :return: 
        '''
        self.frames = {}
        for f in (LoginFrame, FolderFrame): # Classes to include
            frame = f(self, self)
            frame.grid(row=0, column=0, sticky=tk.NW+tk.SE)
            self.frames[f] = frame
        self.show_frame(LoginFrame)

    def show_frame(self, frame):
        '''
        Used when swapping between primary frames
        :param frame: 
        :return: 
        '''
        self.frames[frame].tkraise()
        if frame in [FolderFrame]:
            self.minsize(width=1080, height=600)
        if frame in [LoginFrame]:
            self.minsize(width=300, height=220)

    def try_connection(self, server, password, username):
        '''
        Connects to server via a ConnectionHandler, will then attempt to login if the connection was successful
        :param server: String
        :param password: String
        :param username: String  # Very insecure, need secure login
        :return: 
        '''
        print server, password, username
        b_connected = False
        b_logged_in = False
        # Establish connection through connector
        try:
            self.conn = self.connector.connect(server)
            b_connected = True;
        except ConnectionManagerException:
            print "connect failed"

        #login, and set up the folder management system
        if b_connected:
            try:
                self.conn = self.connector.login(username, password)
                self.filing_cabinet.set_conn(self.connector.conn)
                b_logged_in = True
            except ConnectionManagerException:
                print "Login Failed"  # TODO: Relay this to user through GUI

        # Swap out the login frame for the Folder frame
        if b_logged_in:
            self.frames[FolderFrame].set_folders(self.filing_cabinet)
            self.frames[FolderFrame].populate_folders()
            self.show_frame(FolderFrame)
            return

    # These functions are used when an abstracted class needs access to specific variables from elsewhere
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

    def get_conn(self):
        return self.conn

app = HolderFrame()
app.update()
app.mainloop()
app.protocol("WM_DELETE_WINDOW", sys.exit())
exit()