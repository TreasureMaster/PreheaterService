"""Содержит класс для реализации объекта модуля."""
import os, shutil, zipfile, glob
import datetime, time

from typing import Optional

from registry import ConfigRegistry
from applogger import AppLogger
from .moduleconfig import ModuleConfig
from .modulerevision import ModuleRevision

class FNModule:
    __REQUIRED_MAINPATH = ConfigRegistry.instance().getManagerConfig().getWorkPath()
    __REQUIRED_DATAPATH = ConfigRegistry.instance().getManagerConfig().getWorkDataPath()
    __REQUIRED_DESCRIPTION = ConfigRegistry.instance().getManagerConfig().getWorkDescriptionFilepath()
    __REQUIRED_CONFIG = ConfigRegistry.instance().getManagerConfig().getWorkConfigFilepath()
    __REQUIRED_IMAGE = ConfigRegistry.instance().getManagerConfig().getWorkImageFilepath()

    # TODO содержит поля:
    # 1) ссылки в папке data на картинку модуля, файл readme и т.п. (может просто ссылку на папку data ?)
    # 2) сами объекты описания и т.п. (ленивая загрузка)
    # 3) словарь конфигурации (должен уметь распарсить xml или т.п. файл)
    def __init__(self, link: str, cfg: Optional[str] = None) -> None:
        """При инициализации здесь хранится только ссылка на файл модуля.
        А также <временно> распакованный и распарсенный config.bin.
        Полностью файлы модуля распаковываются только после выбора модуля.
        """
        # TODO cfg теперь bin, он уже расшифрован в modulehelper
        # расположение папки data модуля
        self.link = link
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
        # return self.__config.getProperty('name')
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
        return any([version == current for version in ConfigRegistry.instance().getManagerConfig().getCompatibleVersions()])

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

        if os.path.exists(self.__REQUIRED_MAINPATH):
            shutil.rmtree(self.__REQUIRED_MAINPATH)
        fnmfile.extractall()
        fnmfile.close()
        # просто метка об успехе
        return True

    def checkCurrentData(self):
        """Проверяет соответствие файла конфигурации в папке DATA
        и в случае несоответствия распаковывает данные текущего модуля
        (то есть, если в папке с текущим модулем находяться старые файлы)."""
        path = self.__REQUIRED_CONFIG.format(self.__REQUIRED_DATAPATH)
        # print('path from checkCurrentData:', path)
        if self.getName() != ModuleConfig().getFromBIN(path).getProperty('name'):
            self.unpackData()

    def getDescription(self, field):
        # проверка соответствия модуля тому, что есть в папке data
        # Пока заглушка - не выполнять проверку, если модуль редактируемый?
        if self.link is not None:
            self.checkCurrentData()
        if field == 'config':
            return self.getConfiguration()
        path = self.__REQUIRED_DESCRIPTION.format(self.__REQUIRED_DATAPATH)
        # Реализация с вычислением пути может пригодиться, если будут использоваться разные папки (для чтения и редактирования копии)
        with open(path, encoding='utf-8') as fd:
            desc = fd.read()
        return desc

    def getConfiguration(self):
        # Создать описание конфигурации
        text = 'Базовый блок: {}\nВерсия: {}\nРедакция: {}\nПроизводитель: {}\nДата выпуска: {}'.format(
            self.getBaseName(),
            self.getBaseRevision(),
            self.getEdition(),
            self.getManufacturer(),
            self.getReleaseDate()
        )
        return text

    def getImageLink(self):
        """Возвращает ссылку на файл изображения подогревателя."""
        path = self.__REQUIRED_IMAGE.format(self.__REQUIRED_DATAPATH)
        # link = None
        # path = f'{FNModule.__REQUIRED_PATH}/*.%s'
        # for link in (filter(lambda x: bool(x), [glob.glob(path % ext) for ext in ('jpg', 'png')])):
        #     pass
        return os.path.normpath(os.path.abspath(path)) if os.path.isfile(path) else None

    def updateConfigProperty(self, key, value):
        self.__config.setProperty(key, value)

    def setEditablePaths(self):
        self.__REQUIRED_MAINPATH = ConfigRegistry.instance().getManagerConfig().getEditablePath()
        self.__REQUIRED_DATAPATH = ConfigRegistry.instance().getManagerConfig().getEditableDataPath()
        self.__REQUIRED_DESCRIPTION = ConfigRegistry.instance().getManagerConfig().getEditableDescriptionFilepath()
        self.__REQUIRED_CONFIG = ConfigRegistry.instance().getManagerConfig().getEditableConfigFilepath()
        self.__REQUIRED_IMAGE = ConfigRegistry.instance().getManagerConfig().getEditableImageFilepath()

    def setWorkPaths(self):
        # TODO необходимо убрать дублирование кода (может что-то изменить в config ?)
        self.__REQUIRED_MAINPATH = ConfigRegistry.instance().getManagerConfig().getWorkPath()
        self.__REQUIRED_DATAPATH = ConfigRegistry.instance().getManagerConfig().getWorkDataPath()
        self.__REQUIRED_DESCRIPTION = ConfigRegistry.instance().getManagerConfig().getWorkDescriptionFilepath()
        self.__REQUIRED_CONFIG = ConfigRegistry.instance().getManagerConfig().getWorkConfigFilepath()
        self.__REQUIRED_IMAGE = ConfigRegistry.instance().getManagerConfig().getWorkImageFilepath()