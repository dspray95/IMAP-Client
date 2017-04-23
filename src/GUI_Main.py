import Tkinter as tk
from ConnectionManager import ConnectionManager, ConnectionManagerException
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
        raise NotImplementedError


class LoginFrame(EmptyFrame):
    """The application home page.

    Attributes:
      new_button (tk.Button): The button to switch to ExecuteFrame.

    """

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
        self.ent_username.grid(column=1, row=2, padx=20)

        self.lbl_password = tk.Label(self, text="Password: ")
        self.lbl_password.grid(column=0, row=3)
        self.ent_password = tk.Entry(self)
        self.ent_password.grid(column=1, row=3, padx=20)

        self.btn_login = tk.Button(self,
                                    anchor=tk.W,
                                    command=lambda: self.controller.try_connection(self.ent_address.get(),
                                                                                   self.ent_password.get(),
                                                                                   self.ent_username.get(),
                                                                                   self.controller.connector),
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

class InboxFrame(EmptyFrame):
    """The application home page.

    Attributes:
      new_button (tk.Button): The button to switch to ExecuteFrame.

    """

    def create_widgets(self):
        """Create the base widgets for the frame."""
        self.new_button = tk.Button(self,
                                    anchor=tk.W,
                                    command=lambda: self.controller.show_frame(LoginFrame),
                                    padx=5,
                                    pady=5,
                                    text="Exit")
        self.new_button.grid(padx=5, pady=5, sticky=tk.W+tk.E)

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

    def init_holder(self):
        """First setup of the primary holder frame
        This frame controls the others defined here
        """
        #   Frame Container
        # self.container = tk.Frame(self)
        # self.container.grid(row=0, column=0, sticky=tk.W+tk.E)

        #   Frames
        self.frames = {}
        for f in (LoginFrame, InboxFrame): # Classes to include
            frame = f(self, self)
            frame.grid(row=6, column=2, sticky=tk.NW+tk.SE)
            self.frames[f] = frame
        self.show_frame(LoginFrame)

    def show_frame(self, frame):
        self.frames[frame].tkraise()

    def try_connection(self, server, password, username, connector):
        print server, password, username
        b_connected = False
        b_logged_in = False
        try:
            connector.connect(server)
            b_connected = True;
        except ConnectionManagerException:
            print "connect failed"

        if b_connected:
            try:
                connector.login(username, password)
                b_logged_in = True
            except ConnectionManagerException:
                print "Login Failed"  # TODO: Relay this to user through GUI

        if b_logged_in:
            self.show_frame(InboxFrame)
            return

app = HolderFrame()
app.mainloop()
exit()