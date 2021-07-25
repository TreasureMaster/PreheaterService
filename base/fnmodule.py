"""Содержит класс для реализации объекта модуля."""
import os, shutil, zipfile
import time

from typing import Optional

from registry import ConfigRegistry
from applogger import AppLogger
from .moduleconfig import ModuleConfig
from .modulerevision import ModuleRevision


class FNModule:

    # TODO содержит поля:
    # 1) ссылки в папке data на картинку модуля, файл readme и т.п. (может просто ссылку на папку data ?)
    # 2) сами объекты описания и т.п. (ленивая загрузка)
    # 3) словарь конфигурации (должен уметь распарсить xml или т.п. файл)
    def __init__(self, link: str, cfg: Optional[str] = None, mode: str = 'work') -> None:
        """При инициализации здесь хранится только ссылка на файл модуля.
        А также <временно> распакованный и распарсенный config.bin.
        Полностью файлы модуля распаковываются только после выбора модуля.

        link - путь к файлу модуля ('.fnm')
        cfg - считанный и расшифрованный XML-файл конфигурации модуля
        mode - режим работы модуля (пока только работа/редактирование)
        """
        # TODO cfg теперь bin, он уже расшифрован в modulehelper
        # расположение папки data модуля
        self.link = link
        self.__manager_config = ConfigRegistry.instance().getManagerConfig()
        self.setMode(mode)
        self.__config = ModuleConfig(cfg)
        self.__revision = ModuleRevision(self.__config)

    @property
    def revision(self):
        return self.__revision

    @property
    def config(self):
        return self.__config

    def getBaseName(self):
        return self.__config.getProperty('name')

    def getName(self):
        return '{}-{}'.format(
            self.getBaseName(),
            self.getRevision()
        )

    def getTitle(self):
        return '{}  (rev. {})'.format(
            self.__config.getProperty('title'),
            self.getRevision()
        )

    def getBaseRevision(self):
        return self.__revision.getBaseRevision()

    def getEdition(self):
        return self.__revision.getEdition()

    def getRevision(self):
        return self.__revision.getRevision()

    def getManufacturer(self):
        return self.__config.getProperty('manufacturer')

    def getReleaseDate(self):
        return time.strftime('%d %b %Y', time.localtime(self.__config.getProperty('releasedate')))

    def getMakingManager(self):
        return '{}-{}.{}.{}'.format(
            self.__config.getProperty('mainname'),
            self.__config.getProperty('major'),
            self.__config.getProperty('minor'),
            self.__config.getProperty('micro')
        )

    def isCompatible(self):
        current = self.getMakingManager()
        return any([version == current for version in self.__manager_config.getCompatibleVersions()])

    # Распаковать файлы в папку
    def unpackData(self):
        # TODO распаковать в память
        try:
            fnmfile = zipfile.ZipFile(self.link, 'r')
        except Exception as msg:
            # TODO должна быть реализация ошибки извлечения файла
            AppLogger.instance().error(f'Невозможно распаковать архив модуля: {msg}')
            return
        # fnlist = fnmfile.namelist()
        # print('data:', fnlist)

        if os.path.exists(self.__MAINPATH):
            shutil.rmtree(self.__MAINPATH)
        fnmfile.extractall()
        fnmfile.close()
        # просто метка об успехе
        return True

    def checkCurrentData(self):
        """Проверяет соответствие файла конфигурации в папке DATA
        и в случае несоответствия распаковывает данные текущего модуля
        (то есть, если в папке с текущим модулем находяться старые файлы)."""
        if self.getName() != ModuleConfig().getFromBIN(self.__CONFIGFILEPATH).getProperty('name'):
            self.unpackData()

    def getDescription(self, field):
        # проверка соответствия модуля тому, что есть в папке data
        # Пока заглушка - не выполнять проверку, если модуль редактируемый?
        if self.link is not None:
            self.checkCurrentData()
        if field == 'config':
            return self.getConfiguration()
        # Реализация с вычислением пути может пригодиться, если будут использоваться разные папки (для чтения и редактирования копии)
        with open(self.__DESCRIPTIONFILEPATH, encoding='utf-8') as fd:
            desc = fd.read()
        return desc

    def getConfiguration(self) -> str:
        # Создать описание конфигурации
        text = 'Базовый блок: {}\nВерсия: {}\nРедакция: {}\nПроизводитель: {}\nДата выпуска: {}'.format(
            self.getBaseName(),
            self.getBaseRevision(),
            self.getEdition(),
            self.getManufacturer(),
            self.getReleaseDate()
        )
        return text

    def getImageLink(self) -> Optional[str]:
        """Возвращает ссылку на файл изображения подогревателя."""
        return os.path.normpath(os.path.abspath(self.__IMAGEFILEPATH)) if os.path.isfile(self.__IMAGEFILEPATH) else None

    def updateConfigProperty(self, key, value):
        self.__config.setProperty(key, value)

    def __setPaths(self) -> None:
        self.__MAINPATH = self.__manager_config.getPath(self.__mode, 'main')
        # self.__DATAPATH = self.__manager_config.getPath(self.__mode, 'data')
        self.__DESCRIPTIONFILEPATH = self.__manager_config.getDatafile(self.__mode, 'description')
        self.__CONFIGFILEPATH = self.__manager_config.getDatafile(self.__mode, 'config')
        self.__IMAGEFILEPATH = self.__manager_config.getDatafile(self.__mode, 'image')

    def setMode(self, mode: str) -> None:
        """Установить режим работы и рабочие пути для этого модуля."""
        mode = mode.lower()
        if self.__manager_config.isSupportedModes(mode):
            self.__mode = mode
            self.__setPaths()
