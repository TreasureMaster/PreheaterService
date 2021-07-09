"""Содержит класс для реализации объекта модуля."""
import os, shutil, zipfile, glob
import datetime, time

from registry import ConfigRegistry
from .moduleconfig import ModuleConfig

class FNModule:
    __REQUIRED_MAINPATH = ConfigRegistry.instance().getManagerConfig().getMainPath()
    __REQUIRED_DATAPATH = ConfigRegistry.instance().getManagerConfig().getDataPath()
    __REQUIRED_DESCRIPTION = '{}/readme.txt'
    __REQUIRED_CONFIG = '{}/config.xml'
    __REQUIRED_IMAGE = '{}/image.jpg'

    # TODO содержит поля:
    # 1) ссылки в папке data на картинку модуля, файл readme и т.п. (может просто ссылку на папку data ?)
    # 2) сами объекты описания и т.п. (ленивая загрузка)
    # 3) словарь конфигурации (должен уметь распарсить xml или т.п. файл)
    def __init__(self, link, cfg=None):
        # cfg теперь bin
        # расположение папки data модуля
        self.link = link
        self.config = ModuleConfig(cfg)

    def getName(self):
        return self.config.getProperty('name')

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

    # Распаковать файлы в папку
    def unpackData(self):
        # TODO распаковать в память
        try:
            fnmfile = zipfile.ZipFile(self.link, 'r')
        except Exception as msg:
            # TODO должна быть реализация ошибки извлечения файла
            # self.errorlist.append(msg)
            return
        fnlist = fnmfile.namelist()
        # print('data:', fnlist)

        if os.path.exists(FNModule.__REQUIRED_MAINPATH):
            shutil.rmtree(FNModule.__REQUIRED_MAINPATH)
        fnmfile.extractall()
        fnmfile.close()

    def checkCurrentData(self):
        """Проверяет соответствие файла конфигурации в папке DATA
        и в случае несоответствия распаковывает данные текущего модуля."""
        path = FNModule.__REQUIRED_CONFIG.format(FNModule.__REQUIRED_DATAPATH)
        # print('path from checkCurrentData:', path)
        if self.getName() != ModuleConfig().getFromXML(path).getProperty('name'):
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