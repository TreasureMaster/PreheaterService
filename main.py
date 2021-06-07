from tkinter import *
from tkinter.ttk import *

from connectionframe import ConnectionFrame


root = Tk()
root.title('FN-Service')

# все окно
mainframe = Frame(root)
mainframe.pack(expand=YES, fill=BOTH)

connectionframe = ConnectionFrame(mainframe)



if __name__ == '__main__':
    root.mainloop()