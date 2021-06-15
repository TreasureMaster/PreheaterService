"""Содержит класс для реализации объекта модуля."""
import os, shutil, zipfile, glob

from .moduleconfig import ModuleConfig

class FNModule:
    __REQUIRED_PATH = 'data'
    __REQUIRED_DESCRIPTION = '{}/{}.txt'
    __REQUIRED_CONFIG = '{}/config.xml'

    # TODO содержит поля:
    # 1) ссылки в папке data на картинку модуля, файл readme и т.п. (может просто ссылку на папку data ?)
    # 2) сами объекты описания и т.п. (ленивая загрузка)
    # 3) словарь конфигурации (должен уметь распарсить xml или т.п. файл)
    def __init__(self, link, xml=None):
        # расположение папки data модуля
        self.link = link
        self.config = ModuleConfig(xml)

    def getName(self):
        return self.config.getProperty('name')

    def getTitle(self):
        return self.config.getProperty('title')

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
        print('data:', fnlist)

        if os.path.exists(FNModule.__REQUIRED_PATH):
            shutil.rmtree(FNModule.__REQUIRED_PATH)
        fnmfile.extractall()
        fnmfile.close()

    def checkCurrentData(self):
        """Проверяет соответствие файла конфигурации в папке DATA
        и в случае несоответствия распаковывает данные текущего модуля."""
        path = FNModule.__REQUIRED_CONFIG.format(FNModule.__REQUIRED_PATH)
        # print('path from checkCurrentData:', path)
        if self.getName() != ModuleConfig().getFromXML(path).getProperty('name'):
            self.unpackData()

    def getDescription(self, field):
        # проверка соответствия модуля тому, что есть в папке data
        self.checkCurrentData()
        path = FNModule.__REQUIRED_DESCRIPTION.format(FNModule.__REQUIRED_PATH, field)
        # Реализация с выислением пути может пригодиться, если будут использоваться разные папки (для чтения и редактирования копии)
        with open(
            path,
            encoding='utf-8'
        ) as fd:
            desc = fd.read()
        return desc

    def getImageLink(self):
        """Возвращает ссылку на файл изображения подогревателя."""
        link = None
        path = f'{FNModule.__REQUIRED_PATH}/*.%s'
        for link in (filter(lambda x: bool(x), [glob.glob(path % ext) for ext in ('jpg', 'png')])):
            pass
        return os.path.normpath(link[0]) if link else link