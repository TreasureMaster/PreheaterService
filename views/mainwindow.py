from threading import Lock
from views.infomodule import InfoModuleFrame
from accessify import private

from tkinter import *
from tkinter.ttk import *

# from connectionframe import ConnectionFrame
# from moduleframe import ControlPanelFrame, LogPanelFrame
from .listmodules import ListModulesFrame
from .infomodule import InfoModuleFrame

class MainWindow():
    __APPTITLE = 'FN-Service'
    __instance = None
    __lock = Lock()

    @private
    def __init__(self):
        # self.width = width
        # self.height = height
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

    def startWindow(self):
        self._make_widgets()
        #Тут хочу вызывать методы для создания кнопок, меток и т.д.
        self.window.mainloop()#И потом рисовать
 
    def press(self):
        # self.c.move(self.img, 20, 0)
        pass
 
    def _make_widgets(self):
        Label(self.mainframe, text='Здесь будет меню первого окна').pack()

        ListModulesFrame(self.mainframe).pack(side=LEFT, padx=10, fill=Y)
        InfoModuleFrame(self.mainframe).pack(side=LEFT, expand=YES, fill=BOTH, pady=5)



# connectionframe = ConnectionFrame(mainframe)
# controlpanel = ControlPanelFrame(mainframe)
# logpanel = LogPanelFrame(mainframe)



if __name__ == '__main__':
    main = MainWindow()
    main.startWindow()