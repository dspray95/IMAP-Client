from Tkinter import Tk, Frame, BOTH
from ttk import Frame, Button, Style, Label


class GUI_Init(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)

        self.master = master

        self.init_ui()

    def init_ui(self):
        self.master.title("IMAP Client")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)

        lbl_header = Label(text = "Choose an interface type")
        lbl_header.place(x=50, y = 20)
        btn_tui = Button(text="Command Line Interface")
        btn_tui.config(command=lambda:choose_ui(self, btn_tui))
        btn_tui.place(x=50, y=50)
        btn_gui = Button(text="Graphical Interface")
        btn_gui.config(command=lambda:choose_ui(self, btn_gui))
        btn_gui.place(x=50, y=90)

def choose_ui(self, btn):
    if btn['text'] in ["Graphical Interface"]:
        root.withdraw()
        import GUI_Main
    else:
        b_GUI = False  # TODO: Link up with Text_Main.py for CLI


root = Tk()
root.geometry("250x150+300+300")
app = GUI_Init(root)
root.mainloop()
