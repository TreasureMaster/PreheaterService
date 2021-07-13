from lxml import objectify

from .encryption import decode_xml


class ManagerConfig:

    __HEADER = {'name', 'title', 'revision', 'manufacturer', 'releasedate', 'lastupdated', 'editor'}
    # __OPTIONS = {'voltage', 'remote', 'fuel', 'extra'}
    __MANAGER = {'mainname', 'major', 'minor', 'micro'}

    # def __init__(self, filename=None):
    #     if filename:
    #         self.parseXML(filename)

    def __init__(self, xml=None):
        self.root = None
        if xml:
            self.decodeXML(xml)
        # if xml:
        #     self.root = objectify.XML(xml)

    def decodeXML(self, xml):
        pass
    # def parseXML(self, xml=None):
    #     """парсинг XML файла."""
        # self.xml_file = filename
        # TODO указать ошибку при отсутствии файла
        # with open(self.xml_file, encoding='utf-8') as f:
        # self.root = objectify.XML(xml)

    def getFromXML(self, filename=None):
        """Получить объект конфигурации из XML файла."""
        # self.xml_file = filename
        # TODO указать ошибку при отсутствии файла
        with open(filename, encoding='utf-8') as f:
            self.root = objectify.XML(f.read())
        return self

    def getProperty(self, key):
        if key in ManagerConfig.__MANAGER:
            if key in ManagerConfig.__MANAGER:
                return self.root.manager[key]


if __name__ == '__main__':
    xml = ManagerConfig('data/config_binar.bin')
    # xml = ModuleConfig()
    print(xml.getProperty('mainname'))
    print(xml.getProperty('major'))
    print(xml.getProperty('minor'))
    print(xml.getProperty('micro'))
    # print(xml.getProperty('extra'))