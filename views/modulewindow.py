from threading import Lock
from accessify import private

from tkinter import *

from registry import WidgetsRegistry
# from applogger import AppLogger

from .infomodule import EditableModuleFrame
# from widgets.readonlytext import ReadonlyScrolledText, LoggerWindow
from widgets import ScrolledWindow, ModuleMenu
# Здесь размещать подготовку команды?


class ModuleWindow:
    __APPTITLE = 'Создание модуля'
    __instance = None
    __lock = Lock()

    # @private
    def __init__(self):
        mainwindow = WidgetsRegistry.instance().getMainWindow()
        self.window = Toplevel(mainwindow)
        self.window.title(ModuleWindow.__APPTITLE)
        # self.window.geometry('1078x504')
        # все окно
        self.sw = ScrolledWindow(self.window)
        self.sw.pack(expand=YES, fill=BOTH)
        self.mainframe = Frame(self.sw.frame)
        self.mainframe.pack(expand=YES, fill=BOTH)
        self.menu = ModuleMenu(self.mainframe)
        self.menu.grid(row=0, column=0, sticky='ew')

        self._make_widgets()
        self.window.focus_set()
        self.window.grab_set()
        self.window.wait_window()

    # @staticmethod
    # def instance():
    #     with EditWindow.__lock:
    #         if not EditWindow.__instance:
    #             EditWindow.__instance = EditWindow()
    #     return EditWindow.__instance

    @staticmethod
    def exists():
        return ModuleWindow.__instance is not None

    def _make_widgets(self):
        Label(self.mainframe, text='Модуль:').grid(row=0, column=1)

        # Левый фрейм с кнопками управления
        buttonsframe = Frame(self.mainframe)
        # listmodules = Label(self.mainframe, text='Заглушка')
        buttonsframe.grid(padx=10, row=1, column=0, sticky=N)
        # self.scrollwindow.bind_widgets(listmodules.getScrollWidgets())
        # WARNING размещено здесь из-за перекрестного импорта
        from commands.maincommands import ReplaceImage, SaveModule
        Button(buttonsframe, text='Изменить изображение', command=ReplaceImage()).grid(sticky=W+E+S+N, pady=2)
        Button(buttonsframe, text='Резерв...', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        Button(buttonsframe, text='Резерв...', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        Button(buttonsframe, text='Резерв...', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        Button(buttonsframe, text='Сохранить', command=SaveModule()).grid(sticky=W+E+S+N, pady=2)
        Button(buttonsframe, text='Отмена', command=self.window.destroy).grid(sticky=W+E+S+N, pady=2)

        info = EditableModuleFrame(self.mainframe)
        info.grid(pady=5, row=1, column=1)
        self.sw.bind_widgets(info.getScrollWidgets())
        WidgetsRegistry.instance().setEditableInfoFrame(info)

        info.bind('<Map>', self.on_frame_mapped)

        print('edit:', info._getWorkModule())

        # self.log_window = LoggerWindow(self.mainframe, height=5)
        # self.log_window.grid(row=3, columnspan=2, sticky=E+W, padx=10, pady=10)
        # self.scrollwindow.bind_widgets((self.log_window,))
        # WidgetsRegistry.instance().setLogFrame(self.log_window)
        # self.log_window.bind('<Map>', self.on_frame_mapped)

    # def editwindow_destroy(self):
    #     # WARNING не помогло
    #     self.sw.off_binds(None)
    #     self.window.destroy()

    # def __prepare_commands(self):
    #     from commands.maincommands import ViewLog
    #     # WARNING до этого момента не выполняется запись логов в stream
    #     AppLogger.set_command_stream(ViewLog())
        # TODO создать и привязать событие обновления
        # self.window.event_add('<<StreamFlush>>', 'None')
        # self.window.bind('<<StreamFlush>>', TestSaveStream(), '%d')

    def on_frame_mapped(self, event):
        """Изменяет размеры окна после упаковки последнего виджета (окна логов)."""
        # print(event.widget.winfo_width())
        # print(event.widget.winfo_height())
        # префикс req - видимые на экране размеры виджета ???
        # self.scrollwindow.update()
        # print(self.scrollwindow.winfo_reqwidth())
        # print(self.scrollwindow.winfo_reqheight())
        self.sw.canvas.config(
            width=self.mainframe.winfo_width(),
            height=self.mainframe.winfo_height()
        )


# connectionframe = ConnectionFrame(mainframe)
# controlpanel = ControlPanelFrame(mainframe)
# logpanel = LogPanelFrame(mainframe)



if __name__ == '__main__':
    main = ModuleWindow()
    main.startWindow()