"""Содержит класс для реализации объекта модуля."""

from .moduleconfig import ModuleConfig

class FNModule:

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