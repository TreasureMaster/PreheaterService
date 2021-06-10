import os, glob
from threading import Lock
from accessify import private

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

from registry import AppRegistry


class ModuleHelper:
    """Загружает модуль."""
    # статические приватные свойства
    __path = 'modules1'
    __instance = None
    # __registry = None
    __lock = Lock()

    # создать объект напрямую невозможно
    @private
    def __init__(self):
        pass

    # только так можно получить объект реестра
    @staticmethod
    def instance():
        with ModuleHelper.__lock:
            if not ModuleHelper.__instance:
                ModuleHelper.__instance = ModuleHelper()
        return ModuleHelper.__instance

    # инициализация (поиск и загрузка модуля)
    def init(self):
        # self.__registry = AppRegistry.instance()
        if AppRegistry.instance().getListModules() is None:
            self.__getListModules()
        print(AppRegistry.instance().getListModules())

    # получаем список модулей
    def __getListModules(self):
        # Загрузка модулей
        # Все должно быть исправлено при использовании exe-файла на соответствующие пути
        directory = ModuleHelper.__path
        if not os.path.isdir(directory):
            # Стандартная папка не найдена, ищем вручную
            if askyesno('Поиск модулей', 'Стандартная папка с модулями не найдена.\nХотите указать, где она находиться?'):
                directory = askdirectory(initialdir=os.getcwd())
            else:
                # Если папку не выбирают, предлагаем выбрать отдельный модуль
                showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
                if askokcancel('Выбор модуля', 'Выбрать отдельный модуль?'):
                    # fnm = self.askModulePath()
                    fnm = askopenfilenames(initialdir=os.getcwd(), filetypes=(('fnm files', '*.fnm'),))
                    AppRegistry.instance().setListModules(fnm) if fnm else showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
                else:
                    showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
                # Выходим, когда выбран отдельный модуль
                return
        # На данный момент у нас есть директория с модулями (если не вышли при выборе отдельного модуля)
        if not directory:
            showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
        else:
            # обработка стандартной папки
            print('все нормально')
            # FAKE нужно сохранять список модулей из папки
            # self.__registry.setListModules(directory)
            # TODO нужно просканировать имеющуюся папку
            modules = list(map(os.path.abspath, glob.glob(f'{directory}/*.fnm')))
            if modules:
                AppRegistry.instance().setListModules(modules)
            else:
                showerror('Выбор модулей', 'В указанной папке файлы модулей не обнаружены.')

    # def askModulePath(self):
    #     return askopenfilenames(initialdir=os.getcwd(), filetypes=(('fnm files', '*.fnm'),))

    def checkFNMFile(self, fnm):
        # 1) проверить расширение файла
        print(os.path.splitext(fnm)[1])
        # 2) проверить возможность чтения файла
        # 3) проверить является ли файл архивом zip
        # 4) проверить все ли обязательные файлы в архиве
        # 5) если все нормально, считать требуемые файлы
        pass

if __name__ == '__main__':
    pass