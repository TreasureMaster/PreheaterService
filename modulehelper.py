import os, glob, shutil
import zipfile
from threading import Lock
from accessify import private

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

from registry import AppRegistry, WidgetsRegistry, ModListRegistry
from applogger import AppLogger
from modulecore.fnmodule import FNModule


class ModuleHelper:
    """Загружает модуль."""
    # статические приватные свойства
    __path = 'modules'
    __instance = None
    # __registry = None
    __lock = Lock()
    __REQUIRED_CONFIG = 'data/config.xml'

    # создать объект напрямую невозможно
    @private
    def __init__(self):
        pass
        self.errorlist = []
        # import logging
        # self.logger = logging.getLogger('app')
        self.logger = AppLogger.instance()

    # только так можно получить объект реестра
    @staticmethod
    def instance():
        with ModuleHelper.__lock:
            if not ModuleHelper.__instance:
                ModuleHelper.__instance = ModuleHelper()
        return ModuleHelper.__instance

    # инициализация (поиск и загрузка модуля)
    def init(self):
        # logger = AppLogger.instance()
        
        self.logger.info('Start ModuleHandler init')
        # TODO в любом случае сканируем ?
        self.__getListModules()
        # print(AppRegistry.instance().getListModules())
        # mod = (AppRegistry.instance().getModule('binar5s'))
        # print(mod.getTitle())
        print('errors:', self.errorlist)

    # получаем список модулей
    def __getListModules(self):
        # Загрузка модулей
        fakeroot = None
        if not WidgetsRegistry.instance().existsMainWindow():
            fakeroot = Tk()
            fakeroot.withdraw()
        # Все должно быть исправлено при использовании exe-файла на соответствующие пути
        directory = ModuleHelper.__path
        if not os.path.isdir(directory):
            self.logger.error('Стандартная папка с модулями не найдена.')
            # Стандартная папка не найдена, ищем вручную
            if askyesno('Поиск модулей', 'Стандартная папка с модулями не найдена.\nХотите указать, где она находиться?'):
                directory = askdirectory(initialdir=os.getcwd())
            else:
                # Если папку не выбирают, предлагаем выбрать отдельный модуль
                self.logger.error('Не выбрана папка или модуль для работы.')
                showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
                self.getSingleModule()
                # Выходим, когда выбран отдельный модуль
                if fakeroot is not None:
                    fakeroot.deiconify()
                    fakeroot.destroy()
                return
        # На данный момент у нас есть директория с модулями (если не вышли при выборе отдельного модуля)
        if not directory:
            self.logger.error('Не выбрана папка или модуль для работы.')
            showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
        else:
            # обработка стандартной папки
            # print('все нормально')
            self.getModuleDirectory(directory)
        if fakeroot is not None:
            fakeroot.deiconify()
            fakeroot.destroy()

    def getSingleModule(self):
        if askokcancel('Выбор модуля', 'Выбрать отдельный модуль?'):
            fnm = askopenfilenames(initialdir=os.getcwd(), filetypes=(('fnm files', '*.fnm'),))
            if fnm:
                for link in fnm:
                    mod = FNModule(link, self.getConfigFNMFile(link))
                    ModListRegistry.instance().addModule(mod.getName(), mod)
            else:
                self.logger.error('Не выбрана папка или модуль для работы.')
                showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
        else:
            self.logger.error('Не выбрана папка или модуль для работы.')
            showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')

    def getModuleDirectory(self, directory):
        modules = list(map(os.path.abspath, glob.glob(f'{directory}/*.fnm')))
        if modules:
            for link in modules:
                mod = FNModule(link, self.getConfigFNMFile(link))
                ModListRegistry.instance().addModule(mod.getName(), mod)
        else:
            self.logger.error('В указанной папке модули отсутствуют.')
            showerror('Выбор модулей', 'В указанной папке файлы модулей не обнаружены.')

    def getConfigFNMFile(self, fnm):
        # 1) проверить расширение файла
        if os.path.splitext(fnm)[1] != '.fnm':
            self.logger.error('Ошибочное расширение модуля')
            return
        # 2) проверить возможность чтения файла
        # TODO возможно просто нужно его попробовать загрузить и обработать в try-except
        if not os.path.exists(fnm):
            self.logger.error(f'Файл {fnm} не существует.')
            return
        # Пробуем возвратить текст из xml
        return self.getXMLfromZip(fnm)

    def getXMLfromZip(self, fnm):
        # 3) проверить является ли файл архивом zip
        # 4) проверить все ли обязательные файлы в архиве
        # 5) если все нормально, считать требуемые файлы
        try:
            with zipfile.ZipFile(fnm) as myzip:
                with myzip.open(ModuleHelper.__REQUIRED_CONFIG) as myfile:
                    xml = myfile.read()
        except Exception as msg:
            self.logger.error('Ошибка при распаковке файла: ' + msg)
            return
        return xml

if __name__ == '__main__':
    pass