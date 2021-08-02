from abc import ABC, abstractmethod
from tkinter import *
from tkinter import ttk

from registry import WidgetsRegistry, ConfigRegistry, AppRegistry
from applogger import AppLogger

# from views.infomodule import InfoModuleFrame
from .listmodules import ListModulesFrame
from .infomodule import InfoModuleFrame, EditableModuleFrame
from widgets import LoggerWindow, ScrolledWindow, GUIWidgetConfiguration, ConnectionFrame, ScrolledListboxFrame
# Здесь размещать подготовку команды?
from commands import ViewLog

from appmeta import AbstractSingletonMeta


# --------------------- Абстрактный класс окна приложения -------------------- #

class AppWindow(ABC):
    """Абстрактный класс окна приложения."""

    def __init__(self):
        # WARNING super() в дочерних окнах должна запускаться последней !!!
        # все окно
        self.scrollwindow = ScrolledWindow(self.window)
        self.scrollwindow.pack(expand=YES, fill=BOTH)
        
        self.mainframe = Frame(self.scrollwindow.frame)
        self.mainframe.pack(expand=YES, fill=BOTH)

        self._make_widgets()
        self._prepare_commands()

    @abstractmethod
    def _make_widgets(self):
        """Абстрактный метод создания виджетов окна."""
        ...

    @abstractmethod
    def _prepare_commands(self):
        """Абстрактный метод подключения дополнительных команд (н-р, логирование)."""
        ...

    def on_frame_mapped(self, event):
        """Изменяет размеры окна после упаковки последнего виджета (окна логов)."""
        self.scrollwindow.canvas.config(
            width=self.mainframe.winfo_width(),
            # height=self.mainframe.winfo_height()
            height=min(
                round(self.window.winfo_screenheight() / 2),
                self.mainframe.winfo_height()
            )
        )


# -------------------- Главное окно приложения (менеджер) -------------------- #

class MainWindow(AppWindow, metaclass=AbstractSingletonMeta):
    __APPTITLE = 'FN-Service'

    def __init__(self):
        """Вначале создается окно, затем - виджеты (согласно суперклассу)."""
        self.window = Tk()
        self.window.title(MainWindow.__APPTITLE)
        WidgetsRegistry.instance().setMainWindow(self.window)
        super().__init__()

    @staticmethod
    def instance():
        """Метод оставлен для совместимости с прошлыми версиями."""
        return MainWindow()

    def startWindow(self):
        """Теперь только непосредственно старт."""
        self.window.mainloop()
 
    def _make_widgets(self):
        Label(
            self.mainframe,
            text=f'Версия: {ConfigRegistry.instance().getManagerConfig().getVersion()}'
        ).grid(row=0, column=1, sticky='e', padx=10)# columnspan=2)

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

    def _prepare_commands(self):
        # WARNING до этого момента не выполняется запись логов в stream
        AppLogger.set_command_stream(ViewLog())


# ---------------------------- Окно редактирования --------------------------- #
class EditWindow(AppWindow):
    __APPTITLE = 'Создание модуля'

    def __init__(self):
        # TODO теперь это Python-singleton, можно не сохранять в реестре ?
        self.mainwindow = WidgetsRegistry.instance().getMainWindow()
        self.window = Toplevel(self.mainwindow)
        self.window.title(EditWindow.__APPTITLE)
        super().__init__()

        self.window.focus_set()
        self.window.grab_set()
        self.window.wait_window()

    def _make_widgets(self):
        Label(self.mainframe, text='Здесь будет меню окна редактирования').grid(row=0, columnspan=2)

        # Левый фрейм с кнопками управления
        buttonsframe = Frame(self.mainframe)
        # listmodules = Label(self.mainframe, text='Заглушка')
        buttonsframe.grid(padx=10, row=1, column=0, sticky=N)
        # self.scrollwindow.bind_widgets(listmodules.getScrollWidgets())

        # WARNING размещено здесь из-за перекрестного импорта
        from commands import ReplaceImage, SaveModule

        Button(buttonsframe, text='Изменить изображение', command=ReplaceImage()).grid(sticky=W+E+S+N, pady=2)
        Button(buttonsframe, text='Резерв...', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        Button(buttonsframe, text='Резерв...', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        Button(buttonsframe, text='Резерв...', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        Button(buttonsframe, text='Сохранить', command=SaveModule()).grid(sticky=W+E+S+N, pady=2)
        Button(buttonsframe, text='Отмена', command=self.window.destroy).grid(sticky=W+E+S+N, pady=2)

        info = EditableModuleFrame(self.mainframe)
        info.grid(pady=5, row=1, column=1)
        self.scrollwindow.bind_widgets(info.getScrollWidgets())
        WidgetsRegistry.instance().setEditableInfoFrame(info)

        info.bind('<Map>', self.on_frame_mapped)

        print('edit:', info._getWorkModule())

        # self.log_window = LoggerWindow(self.mainframe, height=5)
        # self.log_window.grid(row=3, columnspan=2, sticky=E+W, padx=10, pady=10)
        # self.scrollwindow.bind_widgets((self.log_window,))
        # WidgetsRegistry.instance().setLogFrame(self.log_window)
        # self.log_window.bind('<Map>', self.on_frame_mapped)

    def _prepare_commands(self):
        pass
    #     from commands.maincommands import ViewLog
    #     # WARNING до этого момента не выполняется запись логов в stream
    #     AppLogger.set_command_stream(ViewLog())
        # TODO создать и привязать событие обновления
        # self.window.event_add('<<StreamFlush>>', 'None')
        # self.window.bind('<<StreamFlush>>', TestSaveStream(), '%d')

from tests import timethis
# --------------------------- Окно работы с модулем -------------------------- #
class ModuleWindow(AppWindow, GUIWidgetConfiguration):
    __APPTITLE = 'Работа с модулем'

    def __init__(self):
        self.mainwindow = WidgetsRegistry.instance().getMainWindow()
        self.window = Toplevel(self.mainwindow)
        self.window.title(ModuleWindow.__APPTITLE)
        self.window.protocol('WM_DELETE_WINDOW', self._quit)
        # self.__current_module = AppRegistry.instance().getCurrentModule()
        super().__init__()

        self.window.focus_set()
        self.window.grab_set()
        self.window.wait_window()

    # @timethis
    def _make_widgets(self):
        self._make_static_widgets()
        self._load_module()

        self.lefttabs = self.module.LeftTabs(self.mainframe, self)
        # ---------------------------------
        
        # Формирование табов
        # nb = ttk.Notebook(self.mainframe)
        # # style = ttk.Style()
        # # style.layout('TNotebook', {'borderwidth': 0})
        
        # # nb.grid(padx=10, row=3, column=0, sticky=N)
        # # ---------------------------------
        # # Первая вкладка с кнопками управления
        # rc_frame = Frame(nb)
        # # listmodules = Label(self.mainframe, text='Заглушка')
        # rc_frame.pack(expand=YES, fill=BOTH)
        # # self.scrollwindow.bind_widgets(listmodules.getScrollWidgets())
        # from widgets import InfoTitleLabel
        # InfoTitleLabel(rc_frame, text='Пульт (прямое управление)').grid(sticky=W+E+S+N, pady=2)
        # # WARNING размещено здесь из-за перекрестного импорта
        # # from commands.maincommands import ReplaceImage, SaveModule
        # Button(rc_frame, text='Выключить', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        # Button(rc_frame, text='Отопление', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        # Button(rc_frame, text='Вентиляция', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        # Button(rc_frame, text='Расширенный запрос', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        # # Button(rc_frame, text='Сохранить', command=SaveModule()).grid(sticky=W+E+S+N, pady=2)
        # Button(rc_frame, text='Отмена', command=self._quit).grid(sticky=W+E+S+N, pady=2)
        # # ------------------------------------
        # # Вторая вкладка с кнопками
        # ignition_frame = Frame(nb)
        # ignition_frame.pack(expand=YES, fill=BOTH)
        # InfoTitleLabel(ignition_frame, text='Розжиг').pack(fill=X, pady=2)
        # listbar = ScrolledListboxFrame(ignition_frame)
        # listbar.pack(pady=10)
        # listbar.add_list([
        #     'Параметры',
        #     'Розжиг',
        #     'Отопление',
        #     'Температура',
        #     'ДН импульс',
        #     'Мониторинг',
        #     'Прошивка'
        # ])
        # listbar.set_command(lambda event: None)
        # listbar.listbox.config(width=30)

        # Button(ignition_frame, text='Save to file', command=lambda: None).pack(fill=X, pady=2)
        # Button(ignition_frame, text='Load from file', command=lambda: None).pack(fill=X, pady=2)
        # Button(ignition_frame, text='AddRow', command=lambda: None).pack(fill=X, pady=2)
        # Button(ignition_frame, text='DelRow', command=lambda: None).pack(fill=X, pady=2)
        # Button(ignition_frame, text='Upload to Block', command=lambda: None).pack(fill=X, pady=2)
        # # Button(ignition_frame, text='Мониторинг', command=lambda: None).pack(fill=X, pady=2)
        # # Button(ignition_frame, text='Прошивка', command=lambda: None).pack(fill=X, pady=2)
        # # Button(rc_frame, text='Сохранить', command=SaveModule()).grid(sticky=W+E+S+N, pady=2)
        # Button(ignition_frame, text='Отмена', command=self._quit).pack(fill=X, pady=2)

        # nb.add(rc_frame, text='Пульт')
        # nb.add(ignition_frame, text='Розжиг')

        # Прикрепление загруженного из модуля виджета
        self.lefttabs.grid(padx=10, row=3, column=0, sticky=N)

        # ------------------------------------
        info = InfoModuleFrame(self.mainframe)
        info.grid(pady=5, row=3, column=1)
        self.scrollwindow.bind_widgets(info.getScrollWidgets())
        WidgetsRegistry.instance().pushWorkInfoFrame(info)

        info.bind('<Map>', self.on_frame_mapped)

        # self.log_window = LoggerWindow(self.mainframe, height=5)
        # self.log_window.grid(row=3, columnspan=2, sticky=E+W, padx=10, pady=10)
        # self.scrollwindow.bind_widgets((self.log_window,))
        # WidgetsRegistry.instance().setLogFrame(self.log_window)
        # self.log_window.bind('<Map>', self.on_frame_mapped)

    def _make_static_widgets(self):
        self.add_underline(self.mainframe, width=2, color='gray').grid(row=0, columnspan=2, sticky='ew')
        self.connection = ConnectionFrame(self.mainframe)
        self.connection.grid(row=1, columnspan=2, sticky='ew')
        self.add_underline(self.mainframe, width=2, color='gray').grid(row=2, columnspan=2, sticky='ew')

    def _quit(self):
        """Собственная обработка выхода."""
        WidgetsRegistry.instance().popWorkInfoFrame()
        WidgetsRegistry.instance().getMainWindow().deiconify()
        self.window.destroy()

    def _load_module(self):
        """Загружает python-module с дополнительными фреймами модуля отопителя"""
        path = ConfigRegistry.instance().getManagerConfig().getDatafile('work', 'code')
        print(path)
        # Загрузка модуля
        import importlib.util
        spec = importlib.util.spec_from_file_location("mod", path)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        print(self.module)
        # Теперь не запускается, а просто загружается
        # Запуск модуля (исполнение встроенного класса)
        # self.lefttabs = self.foo.LeftTabs(self.mainframe, self)

    def _prepare_commands(self):
        pass
    #     from commands.maincommands import ViewLog
    #     # WARNING до этого момента не выполняется запись логов в stream
    #     AppLogger.set_command_stream(ViewLog())
        # TODO создать и привязать событие обновления
        # self.window.event_add('<<StreamFlush>>', 'None')
        # self.window.bind('<<StreamFlush>>', TestSaveStream(), '%d')


if __name__ == '__main__':
    main = MainWindow()
    main.startWindow()