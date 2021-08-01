import os, glob, shutil
import zipfile, tarfile

from threading import Lock
from accessify import private
from distutils.dir_util import copy_tree

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

from registry import AppRegistry, WidgetsRegistry, ModListRegistry, ConfigRegistry
from applogger import AppLogger
from base.fnmodule import FNModule
from base.encryption import decode_xml

from tests import timethis


class ModuleHelper:
    """Загружает модуль."""
    # статические приватные свойства
    __REQUIRED_MODULESPATH = ConfigRegistry.instance().getManagerConfig().getModulesPath()
    __instance = None
    # __registry = None
    __lock = Lock()
    # TODO внести все пути в config.py
    __REQUIRED_CONFIG = ConfigRegistry.instance().getManagerConfig().getDatafile('work', 'config')

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
    # @timethis
    def init(self):
        # logger = AppLogger.instance()
        
        # self.logger.info('Start ModuleHandler init')
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
        directory = ModuleHelper.__REQUIRED_MODULESPATH
        if not os.path.isdir(directory):
            # self.logger.error('Стандартная папка с модулями не найдена.')
            # Стандартная папка не найдена, ищем вручную
            if askyesno('Поиск модулей', 'Стандартная папка с модулями не найдена.\nХотите указать, где она находиться?'):
                directory = askdirectory(initialdir=os.getcwd())
            else:
                # Если папку не выбирают, предлагаем выбрать отдельный модуль
                # self.logger.error('Не выбрана папка или модуль для работы.')
                showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
                self.getSingleModule()
                # Выходим, когда выбран отдельный модуль
                if fakeroot is not None:
                    fakeroot.deiconify()
                    fakeroot.destroy()
                return
        # На данный момент у нас есть директория с модулями (если не вышли при выборе отдельного модуля)
        if not directory:
            # self.logger.error('Не выбрана папка или модуль для работы.')
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
                    cfg = self.getConfigFNMFile(link)
                    if cfg is not None:
                        mod = FNModule(link, cfg)
                    ModListRegistry.instance().addModule(mod.getName(), mod)
            else:
                # self.logger.error('Не выбрана папка или модуль для работы.')
                showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
        else:
            # self.logger.error('Не выбрана папка или модуль для работы.')
            showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')

    def getModuleDirectory(self, directory):
        """Сканирует указанную папку и ищет в ней модули (файлы с раширением fnm)."""
        modules = list(map(os.path.abspath, glob.glob(f'{directory}/*.fnm')))
        if modules:
            for link in modules:
                cfg = self.getConfigFNMFile(link)
                if cfg is not None:
                    mod = FNModule(link, cfg)
                    ModListRegistry.instance().addModule(mod.getName(), mod)
        else:
            # self.logger.error('В указанной папке модули отсутствуют.')
            showerror('Выбор модулей', 'В указанной папке файлы модулей не обнаружены.')

    def getConfigFNMFile(self, fnm):
        # 1) проверить расширение файла
        if os.path.splitext(fnm)[1] != '.fnm':
            # self.logger.error('Ошибочное расширение модуля')
            return
        # 2) проверить возможность чтения файла
        # TODO возможно просто нужно его попробовать загрузить и обработать в try-except
        if not os.path.exists(fnm):
            # self.logger.error(f'Файл {fnm} не существует.')
            return
        # Пробуем возвратить текст из xml
        return self.getXMLfromZip(fnm)

    # @timethis
    def getXMLfromZip(self, fnm):
        # 3) проверить является ли файл архивом zip
        # 4) проверить все ли обязательные файлы в архиве
        # 5) если все нормально, считать требуемые файлы
        try:
            with zipfile.ZipFile(fnm) as myzip:
                # zipfile использует байтовый режим, поэтому не нужно указывать 'b'
                with myzip.open(ModuleHelper.__REQUIRED_CONFIG, 'r') as myfile:
            # with tarfile.open(fnm) as myfile:
            #         prep = myfile.getmember('module/data/config.bin')
            #         prep = myfile.extractfile(prep)
                    # print(prep)
                        cfg = decode_xml(
                            raw_data = myfile.read(),
                            fnm = fnm,
                            keys = ConfigRegistry.instance().getManagerConfig().getAllKeys()
                        )
        except Exception as msg:
            # self.logger.error('Ошибка при распаковке файла: ' + str(msg))
            return
        return cfg

    def createFNMFile(self, where: str) -> str:
        """Создание архива файлов модуля и перемещение его в папку со всеми модулями."""
        manager_cfg = ConfigRegistry.instance().getManagerConfig()
        save_path = os.path.join(
            AppRegistry.instance().getRunPath(),
            manager_cfg.getModulesPath(),
            AppRegistry.instance().getEditableModule().getName() + '.fnm'
        )
        os.chdir(where)
        with zipfile.ZipFile(save_path, 'w') as myzip:
            myzip.write(manager_cfg.getPath('work', 'main'))
            myzip.write(manager_cfg.getPath('work', 'data'))
            myzip.write(manager_cfg.getPath('work', 'docs'))
            for file in os.listdir(os.path.join(os.getcwd(), manager_cfg.getPath('work', 'data'))):
                myzip.write(os.path.join(manager_cfg.getPath('work', 'data'), file))
            for file in os.listdir(os.path.join(os.getcwd(), manager_cfg.getPath('work', 'docs'))):
                myzip.write(os.path.join(manager_cfg.getPath('work', 'docs'), file))
        os.chdir(AppRegistry.instance().getRunPath())
        # Возвращает путь сохранения для регистрации в списке модулей нового модуля
        return save_path

if __name__ == '__main__':
    pass