from tkinter import *
from tkinter.ttk import *

from connectionframe import ConnectionFrame
from moduleframe import ControlPanelFrame, LogPanelFrame


root = Tk()
root.title('FN-Service')

# все окно
mainframe = Frame(root)
mainframe.pack(expand=YES, fill=BOTH)

connectionframe = ConnectionFrame(mainframe)
controlpanel = ControlPanelFrame(mainframe)
logpanel = LogPanelFrame(mainframe)



if __name__ == '__main__':
    root.mainloop()