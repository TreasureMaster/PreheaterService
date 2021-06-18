from threading import Lock
from views.infomodule import InfoModuleFrame
from accessify import private

from tkinter import *
from tkinter.ttk import *

# from connectionframe import ConnectionFrame
# from moduleframe import ControlPanelFrame, LogPanelFrame
from .listmodules import ListModulesFrame
from .infomodule import InfoModuleFrame
from widgets.readonlytext import ReadonlyScrolledText

class MainWindow:
    __APPTITLE = 'FN-Service'
    __instance = None
    __lock = Lock()

    @private
    def __init__(self):
        self.window = Tk()
        self.window.title(MainWindow.__APPTITLE)
        # все окно
        self.mainframe = Frame(self.window)
        self.mainframe.pack(expand=YES, fill=BOTH)
        # self.window.geometry(str(width) + 'x' + str(height))    #Размер окна
        self.images = []

    @staticmethod
    def instance():
        with MainWindow.__lock:
            if not MainWindow.__instance:
                MainWindow.__instance = MainWindow()
        return MainWindow.__instance

    @staticmethod
    def exists():
        return MainWindow.__instance is not None

    def startWindow(self):
        self._make_widgets()
        self.window.mainloop()
 
    def press(self):
        # self.c.move(self.img, 20, 0)
        pass
 
    def _make_widgets(self):
        Label(self.mainframe, text='Здесь будет меню первого окна').grid(row=0, columnspan=2)

        ListModulesFrame(self.mainframe).grid(padx=10, row=1, column=0, sticky=N)
        InfoModuleFrame(self.mainframe).grid(pady=5, row=1, column=1)

        ReadonlyScrolledText(self.mainframe, height=5).grid(row=3, columnspan=2, sticky=E+W, padx=10, pady=10)



# connectionframe = ConnectionFrame(mainframe)
# controlpanel = ControlPanelFrame(mainframe)
# logpanel = LogPanelFrame(mainframe)



if __name__ == '__main__':
    main = MainWindow()
    main.startWindow()