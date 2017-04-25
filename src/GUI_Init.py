from Tkinter import Tk, Frame, BOTH
from ttk import Frame, Button, Style, Label


class GUI_Init(Frame):
    '''
    This class will assertain whether the user whats to use a GUI or a CLI, then run whichever they chose
    '''
    def __init__(self, master):
        Frame.__init__(self, master)

        self.master = master

        self.init_ui()

    def init_ui(self):
        self.master.title("IMAP Client")
        self.style = Style()
        self.style.theme_use("default")
        self.grid(column = 0, row = 0)
        self.master.grid_columnconfigure(0, weight=1)
        lbl_header = Label(self, text = "Choose an interface type")
        lbl_header.grid(column = 0, row = 0, columnspan = 2)
        btn_tui = Button(self, text="CLI")
        btn_tui.config(command=lambda:choose_ui(self, btn_tui))
        btn_tui.grid(column = 0, row = 1)
        btn_gui = Button(self, text="GUI")
        btn_gui.config(command=lambda:choose_ui(self, btn_gui))
        btn_gui.grid(column = 1, row = 1)

def choose_ui(self, btn):
    if btn['text'] in ["GUI"]:
        root.destroy()
        import GUI_Main
    else:
        root.withdraw()
        import textbased.Text_Main


root = Tk()
root.geometry("250x150+300+300")
app = GUI_Init(root)
root.mainloop()
