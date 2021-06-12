import os, glob, shutil
import zipfile
from threading import Lock
from accessify import private

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

from registry import AppRegistry
from modulecore.fnmodule import FNModule


class ModuleHelper:
    """Загружает модуль."""
    # статические приватные свойства
    __path = 'modules'
    __instance = None
    # __registry = None
    __lock = Lock()
    __REQUIRED_FILES = [
        'config.xml'
    ]

    # создать объект напрямую невозможно
    @private
    def __init__(self):
        pass
        self.errorlist = []

    # только так можно получить объект реестра
    @staticmethod
    def instance():
        with ModuleHelper.__lock:
            if not ModuleHelper.__instance:
                ModuleHelper.__instance = ModuleHelper()
        return ModuleHelper.__instance

    # инициализация (поиск и загрузка модуля)
    def init(self):
        # if AppRegistry.instance().getListModules() is None:
        # TODO в любом случае сканируем ?
        self.__getListModules()
        # print(AppRegistry.instance().getListModules())
        # FAKE проверка работы с модулем
        # self.checkFNMFile(AppRegistry.instance().getListModules()[0])
        mod = (AppRegistry.instance().getModule('binar5s'))
        print(mod.getTitle())
        print('errors:', self.errorlist)

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
                    if fnm:
                        for link in fnm:
                            # ERROR: нужно извлечь из zip файлы. Где это делать?
                            mod = FNModule(link, self.getConfigFNMFile(link))
                            AppRegistry.instance().addModule(mod.getName(), mod)
                    else:
                        showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
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
                for link in modules:
                    mod = FNModule(link, self.getConfigFNMFile(link))
                    AppRegistry.instance().addModule(mod.getName(), mod)
            else:
                showerror('Выбор модулей', 'В указанной папке файлы модулей не обнаружены.')


    # def askModulePath(self):
    #     return askopenfilenames(initialdir=os.getcwd(), filetypes=(('fnm files', '*.fnm'),))

    def getConfigFNMFile(self, fnm):
        # 1) проверить расширение файла
        if os.path.splitext(fnm)[1] != '.fnm':
            self.errorlist.append('Ошибочное расширение модуля')
            return
        # 2) проверить возможность чтения файла
        # TODO возможно просто нужно его попробовать загрузить и обработать в try-except
        if not os.path.exists(fnm):
            self.errorlist.append('Файл не существует')
            return
        # 3) проверить является ли файл архивом zip
        # TODO распаковать в память
        # try:
        #     fnmfile = zipfile.ZipFile(fnm, 'r')
        # except Exception as msg:
        #     self.errorlist.append(msg)
        #     return
        # fnlist = fnmfile.namelist()
        # print('data:', fnlist)

        # if os.path.exists('data'):
        #     shutil.rmtree('data')
        # fnmfile.extractall()
        # fnmfile.close()
        try:
            with zipfile.ZipFile(fnm) as myzip:
                with myzip.open('data/config.xml') as myfile:
                    xml = myfile.read()
        except Exception as msg:
            self.errorlist.append(msg)
            return
        # 4) проверить все ли обязательные файлы в архиве
        # if 'config.xml' not in [os.path.basename(f) for f in fnlist]:
        #     self.errorlist.append('Конфигурационный файл отсуствует. Невозможно загрузить модуль.')
        #     return
        # 5) если все нормально, считать требуемые файлы
        # TODO может быть получить объект ModuleConfig или файлоподобный объект config.xml 
        # тогда нужно изменить ModuleConfig для получения файла ???
        # return True
        # Пробуем возвратить текст из xml
        return xml

if __name__ == '__main__':
    pass