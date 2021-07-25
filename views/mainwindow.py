from threading import Lock
from tkinter import *

from accessify import private

# ttk.Frame не имеет background или bg
# from tkinter.ttk import *

# from connectionframe import ConnectionFrame
# from moduleframe import ControlPanelFrame, LogPanelFrame
from views.infomodule import InfoModuleFrame
from .listmodules import ListModulesFrame
from .infomodule import InfoModuleFrame
from widgets.readonlytext import LoggerWindow
from widgets.scrolledwindow import ScrolledWindow
# Здесь размещать подготовку команды?
from commands.maincommands import ViewLog
from registry import WidgetsRegistry
from applogger import AppLogger

class MainWindow:
    __APPTITLE = 'FN-Service'
    __instance = None
    __lock = Lock()

    @private
    def __init__(self):
        self.window = Tk()
        self.window.title(MainWindow.__APPTITLE)
        WidgetsRegistry.instance().setMainWindow(self.window)
        # self.window.geometry('1078x504')
        # все окно
        self.scrollwindow = ScrolledWindow(self.window)
        self.scrollwindow.pack(expand=YES, fill=BOTH)
        self.mainframe = Frame(self.scrollwindow.frame)
        self.mainframe.pack(expand=YES, fill=BOTH)

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
        self.__prepare_commands()
        self.window.mainloop()
 
    def _make_widgets(self):
        Label(self.mainframe, text='Здесь будет меню первого окна').grid(row=0, columnspan=2)

        listmodules = ListModulesFrame(self.mainframe)
        listmodules.grid(padx=10, row=1, column=0, sticky=N)
        self.scrollwindow.bind_widgets(listmodules.getScrollWidgets())
        info = InfoModuleFrame(self.mainframe)
        info.grid(pady=5, row=1, column=1)
        WidgetsRegistry.instance().setWorkInfoFrame(info)
        self.scrollwindow.bind_widgets(info.getScrollWidgets())

        self.log_window = LoggerWindow(self.mainframe, height=5)
        self.log_window.grid(row=3, columnspan=2, sticky=E+W, padx=10, pady=10)
        self.scrollwindow.bind_widgets((self.log_window,))
        WidgetsRegistry.instance().setLogFrame(self.log_window)
        self.log_window.bind('<Map>', self.on_frame_mapped)

    def __prepare_commands(self):
        # WARNING до этого момента не выполняется запись логов в stream
        AppLogger.set_command_stream(ViewLog())

    def on_frame_mapped(self, event):
        """Изменяет размеры окна после упаковки последнего виджета (окна логов)."""
        # print(event.widget.winfo_width())
        # print(event.widget.winfo_height())
        # префикс req - видимые на экране размеры виджета ???
        # self.scrollwindow.update()
        # print(self.scrollwindow.winfo_reqwidth())
        # print(self.scrollwindow.winfo_reqheight())
        self.scrollwindow.canvas.config(
            width=self.mainframe.winfo_width(),
            height=self.mainframe.winfo_height()
        )


# connectionframe = ConnectionFrame(mainframe)
# controlpanel = ControlPanelFrame(mainframe)
# logpanel = LogPanelFrame(mainframe)



if __name__ == '__main__':
    main = MainWindow()
    main.startWindow()