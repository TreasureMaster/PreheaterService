from __future__ import annotations
from lxml import objectify, etree
from typing import Any

if __name__ != '__main__':
    from .encryption import decode_xml
    from registry import ConfigRegistry


class ModuleConfig:

    __HEADER = {
        'name', 'title',
        'majorrevision', 'minorrevision', 'editrevision',
        'manufacturer', 'releasedate', 'lastupdated',
        'editor'
    }
    __OPTIONS = {'voltage', 'remote', 'fuel', 'extra'}
    __MANAGER = {'mainname', 'major', 'minor', 'micro'}
    __DIGITAL_PROPS = {
        'majorrevision', 'minorrevision', 'editrevision',
        'major', 'minor', 'micro'
    }

    # def __init__(self, filename=None):
    #     if filename:
    #         self.parseXML(filename)

    def __init__(self, cfg: str = None) -> None:
        # cfg_text = None
        # cgf теперь считанный bin, нужно расшифровать
        # if cfg:
        #     cfg_text = decode_xml(cfg)
        # if xml:
        #     self.parseXML(xml)
        if cfg:
            self.root = objectify.XML(cfg)

    # def parseXML(self, xml=None):
    #     """парсинг XML файла."""
        # self.xml_file = filename
        # TODO указать ошибку при отсутствии файла
        # with open(self.xml_file, encoding='utf-8') as f:
        # self.root = objectify.XML(xml)

    def getFromXML(self, filename: str = None) -> ModuleConfig:
        """Получить объект конфигурации из незашифрованного XML файла."""
        # self.xml_file = filename
        # TODO указать ошибку при отсутствии файла
        with open(filename, encoding='utf-8') as f:
            self.root = objectify.XML(f.read())
        return self

    def getFromBIN(self, filename: str = None) -> ModuleConfig:
        """Получить объект конфигурации из зашифрованного XML->BIN файла."""
        # self.xml_file = filename
        # TODO указать ошибку при отсутствии файла
        with open(filename, 'rb') as f:
            cfg = decode_xml(
                raw_data = f.read(),
                fnm = filename,
                keys = ConfigRegistry.instance().getManagerConfig().getAllKeys()
            )
            self.root = objectify.XML(cfg)
        return self

    def toStringXML(self) -> str:
        """Возвращает строковое представление текущей конфигурации XML."""
        # WARNING для шифрования нужно байтовое ???
        # Вначале удаляет все лишние аннотации lxml
        objectify.deannotate(self.root)
        etree.cleanup_namespaces(self.root)
        return etree.tostring(
            self.root,
            encoding='utf-8',
            pretty_print=True,
            # xml_declaration=True
        )#.decode('utf-8')

    def getProperty(self, key: str) -> Any:
        """Возвращает значение свойства, указанного в XML-объекте файла конфигурации."""
        if key in ModuleConfig.__HEADER | ModuleConfig.__OPTIONS | ModuleConfig.__MANAGER:
            try:
                if key in ModuleConfig.__HEADER:
                    return self.root.header[key]
                elif key in ModuleConfig.__MANAGER:
                    return self.root.manager[key]
                elif key in ModuleConfig.__OPTIONS:
                    return list(map(str, self.root.options[key].opvalues))
            except AttributeError:
                if key in ModuleConfig.__HEADER | ModuleConfig.__MANAGER:
                    return self.getUnknownProperty(key)
                else:
                    # TODO пустой список возвращать или нет ???
                    return []

    def getUnknownProperty(self, key: str) -> Any:
        if key in ModuleConfig.__DIGITAL_PROPS:
            return 0
        elif key in {'name', 'mainname'}:
            return 'unknown'
        elif key == 'title':
            return self.getProperty('name')
        elif key == 'lastupdated':
            return self.getProperty('releasedate')
        elif key == 'releasedate':
            # TODO неизвестно, что возвращать, если нет даты выпуска
            return 0
        else:
            return ''

    def setProperty(self, key: str, value: Any) -> None:
        """Присваивает новое значение свойству XML-объекта файла конфигурации."""
        # WARNING пока без options
        if key in ModuleConfig.__HEADER | ModuleConfig.__MANAGER:
            try:
                if key in ModuleConfig.__HEADER:
                    self.root.header[key] = value
                elif key in ModuleConfig.__MANAGER:
                    self.root.manager[key] = value
                # else:
                    # TODO не реализовано
                    # return list(self.root.options[key].opvalues)
                    # return
            except AttributeError:
                return


if __name__ == '__main__':
    with open('tests/xmlfiles/config_binar5s.xml', encoding='utf-8') as fd:
        xmltext = fd.read()
    xml = ModuleConfig(xmltext)
    # xml = ModuleConfig()
    print('имя отопителя:           ', xml.getProperty('name'))
    print('неизвестное свойство:    ', xml.getProperty('aaa'))
    print('вольтаж (список):        ', xml.getProperty('voltage'))
    print('пульты (список):         ', xml.getProperty('remote'))
    print('допы (список, если есть):', xml.getProperty('extra'))
    # print(xml.toStringXML().decode('utf-8'))