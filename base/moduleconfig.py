from lxml import objectify

from .encryption import decode_xml


class ModuleConfig:

    __HEADER = {
        'name', 'title',
        'majorrevision', 'minorrevision', 'editrevision',
        'manufacturer', 'releasedate', 'lastupdated',
        'editor'
    }
    __OPTIONS = {'voltage', 'remote', 'fuel', 'extra'}
    __MANAGER = {'mainname', 'major', 'minor', 'micro'}

    # def __init__(self, filename=None):
    #     if filename:
    #         self.parseXML(filename)

    def __init__(self, cfg=None):
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

    def getFromXML(self, filename=None):
        """Получить объект конфигурации из незашифрованного XML файла."""
        # self.xml_file = filename
        # TODO указать ошибку при отсутствии файла
        with open(filename, encoding='utf-8') as f:
            self.root = objectify.XML(f.read())
        return self

    def getFromBIN(self, filename=None):
        """Получить объект конфигурации из зашифрованного XML->BIN файла."""
        # self.xml_file = filename
        # TODO указать ошибку при отсутствии файла
        with open(filename, 'rb') as f:
            cfg = decode_xml(f.read(), filename)
            self.root = objectify.XML(cfg)
        return self

    def getProperty(self, key):
        if key in ModuleConfig.__HEADER | ModuleConfig.__OPTIONS | ModuleConfig.__MANAGER:
            try:
                if key in ModuleConfig.__HEADER:
                    return self.root.header[key]
                elif key in ModuleConfig.__MANAGER:
                    return self.root.manager[key]
                else:
                    return list(self.root.options[key].value)
            except AttributeError:
                return

    def setProperty(self, key, value):
        # WARNING пока без options
        if key in ModuleConfig.__HEADER | ModuleConfig.__MANAGER:
            try:
                if key in ModuleConfig.__HEADER:
                    self.root.header[key] = value
                elif key in ModuleConfig.__MANAGER:
                    self.root.manager[key] = value
                # else:
                    # TODO не реализовано
                    # return list(self.root.options[key].value)
                    # return
            except AttributeError:
                return


if __name__ == '__main__':
    xml = ModuleConfig('config_binar.xml')
    # xml = ModuleConfig()
    print(xml.getProperty('name'))
    print(xml.getProperty('aaa'))
    print(xml.getProperty('voltage'))
    print(xml.getProperty('remote'))
    print(xml.getProperty('extra'))