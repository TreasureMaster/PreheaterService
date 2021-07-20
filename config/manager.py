"""Файл конфигурационных настроек менеджера."""


class FNConfig:
    # ------------------------- Базовые данные настройки ------------------------- #
    # Название менеджера (название программы, может измениться в будущем)
    __mainname = 'FN-Service'
    # Версия менеджера (major.minor.micro)
    __version__ = '0.2.0'
    # Совместимые версии менеджеров
    __compatible_version = []
    # Базовые ключи менеджера, введенные именно для этого менеджера
    __main_keys = [
        b'kF-4g(kl{[s</!!~',
        b'sjioGY29<<!"n_=k',
        b'YRod48&:*fst^%@j'
    ]
    # Совместимые ключи менеджеров, с версиями которых может работать данный менеджер
    __compatible_keys = []
    # Путь к папке, где хранятся архивы модулей
    __required_modulesfolder = 'modules'
    # Базовый путь папки модуля (корневая папка, куда распаковывается вся структура модуля)
    __required_mainfolder = 'module'
    # Название подпапки с данными (распаковка данных)
    __required_datafolder = 'data'
    # Путь к папке с данными
    __required_datapath = f"{__required_mainfolder}/{__required_datafolder}"
    # Полные относительные пути для файлов модуля
    # рисунок
    __required_image = f"{__required_datapath}/image.jpg"
    # описание
    __required_description = f"{__required_datapath}/readme.txt"
    # конфигурация
    __required_config = f"{__required_datapath}/config.bin"
    # ---------------------------------------------------------------------------- #

    def getManagerName(self):
        return self.__mainname

    def getVersion(self):
        return self.__version__

    def getFullVersion(self):
        return self.__mainname + ' ' + self.__version__

    def getMainKeys(self):
        for key in self.__main_keys:
            yield key

    def getCompatibleKeys(self):
        for key in self.__compatible_keys:
            yield key

    def getAllKeys(self):
        for key in self.__main_keys + self.__compatible_keys:
            yield key

    def getModulesPath(self):
        return self.__required_modulesfolder

    def getMainPath(self):
        return self.__required_mainfolder

    def getDataPath(self):
        return self.__required_datapath

    def getImageFullPath(self):
        return self.__required_image

    def getDescriptionFullPath(self):
        return self.__required_description

    def getConfigFullPath(self):
        return self.__required_config



if __name__ == '__main__':
    cfg = FNConfig()
    for key in cfg.getMainKeys():
        print(key)
    for key in cfg.getCompatibleKeys():
        print(key)
    for key in cfg.getAllKeys():
        print(key)