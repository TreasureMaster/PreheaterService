"""Содержит класс для реализации объекта модуля."""
import os, shutil, zipfile, glob
import datetime, time

from registry import ConfigRegistry
from applogger import AppLogger
from .moduleconfig import ModuleConfig

class FNModule:
    __REQUIRED_MAINPATH = ConfigRegistry.instance().getManagerConfig().getMainPath()
    __REQUIRED_DATAPATH = ConfigRegistry.instance().getManagerConfig().getDataPath()
    __REQUIRED_DESCRIPTION = ConfigRegistry.instance().getManagerConfig().getDescriptionFullPath()
    __REQUIRED_CONFIG = ConfigRegistry.instance().getManagerConfig().getConfigFullPath()
    __REQUIRED_IMAGE = ConfigRegistry.instance().getManagerConfig().getImageFullPath()

    # TODO содержит поля:
    # 1) ссылки в папке data на картинку модуля, файл readme и т.п. (может просто ссылку на папку data ?)
    # 2) сами объекты описания и т.п. (ленивая загрузка)
    # 3) словарь конфигурации (должен уметь распарсить xml или т.п. файл)
    def __init__(self, link, cfg=None):
        """При инициализации здесь хранится только ссылка на файл модуля.
        А также <временно> распакованный и распарсенный config.bin.
        Полностью файлы модуля распаковываются только после выбора модуля.
        """
        # TODO cfg теперь bin, он уже расшифрован в modulehelper
        # расположение папки data модуля
        self.link = link
        self.config = ModuleConfig(cfg)

    def getName(self):
        # return self.config.getProperty('name')
        return '{}-{}'.format(
            self.config.getProperty('name'),
            self.config.getProperty('revision'),
        )

    def getTitle(self):
        return '{}  (rev. {})'.format(
            self.config.getProperty('title'),
            self.config.getProperty('revision'),
        )

    def getRevision(self):
        return self.config.getProperty('revision')

    def getManufacturer(self):
        return self.config.getProperty('manufacturer')

    def getReleaseDate(self):
        return time.strftime('%d %b %Y', time.localtime(self.config.getProperty('releasedate')))

    def getMakingManager(self):
        return '{}-{}.{}.{}'.format(
            self.config.getProperty('mainname'),
            self.config.getProperty('major'),
            self.config.getProperty('minor'),
            self.config.getProperty('micro')
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

        if os.path.exists(FNModule.__REQUIRED_MAINPATH):
            shutil.rmtree(FNModule.__REQUIRED_MAINPATH)
        fnmfile.extractall()
        fnmfile.close()
        # просто метка об успехе
        return True

    def checkCurrentData(self):
        """Проверяет соответствие файла конфигурации в папке DATA
        и в случае несоответствия распаковывает данные текущего модуля
        (то есть, если в папке с текущим модулем находяться старые файлы)."""
        path = FNModule.__REQUIRED_CONFIG.format(FNModule.__REQUIRED_DATAPATH)
        # print('path from checkCurrentData:', path)
        if self.getName() != ModuleConfig().getFromBIN(path).getProperty('name'):
            self.unpackData()

    def getDescription(self, field):
        # проверка соответствия модуля тому, что есть в папке data
        self.checkCurrentData()
        if field == 'config':
            return self.getConfiguration()
        path = FNModule.__REQUIRED_DESCRIPTION.format(FNModule.__REQUIRED_DATAPATH)
        # Реализация с вычислением пути может пригодиться, если будут использоваться разные папки (для чтения и редактирования копии)
        with open(path, encoding='utf-8') as fd:
            desc = fd.read()
        return desc

    def getConfiguration(self):
        # Создать описание конфигурации
        text = 'Базовый блок: {}\nВерсия: {}\nПроизводитель: {}\nДата выпуска: {}'.format(
            self.getName(),
            self.getRevision(),
            self.getManufacturer(),
            self.getReleaseDate()
        )
        return text

    def getImageLink(self):
        """Возвращает ссылку на файл изображения подогревателя."""
        path = FNModule.__REQUIRED_IMAGE.format(FNModule.__REQUIRED_DATAPATH)
        # link = None
        # path = f'{FNModule.__REQUIRED_PATH}/*.%s'
        # for link in (filter(lambda x: bool(x), [glob.glob(path % ext) for ext in ('jpg', 'png')])):
        #     pass
        return os.path.normpath(os.path.abspath(path)) if os.path.isfile(path) else None