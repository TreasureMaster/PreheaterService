"""Файл конфигурационных настроек менеджера."""


class FNConfig:
    # ------------------------- Базовые данные настройки ------------------------- #
    # Название менеджера (название программы, может измениться в будущем)
    __mainname = 'FN-Service'
    # Версия менеджера (major.minor.micro)
    __version__ = '0.2.0'
    # Базовые ключи менеджера, введенные именно для этого менеджера
    __main_keys = [
        b'kF-4g(kl{[s</!!~',
        b'sjioGY29<<!"n_=k',
        b'YRod48&:*fst^%@j'
    ]
    # Совместимые ключи менеджеров, с версиями которых может работать данный менеджер
    __compatible_keys = []
    # Базовый путь папки модуля
    __required_mainfolder = 'module'
    # Название подпапки с данными
    __required_datafolder = 'data'
    # Путь к папке с данными
    __required_datapath = f"{__required_mainfolder}/{__required_datafolder}"
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

    def getMainPath(self):
        return self.__required_mainfolder

    def getDataPath(self):
        return self.__required_datapath



if __name__ == '__main__':
    cfg = FNConfig()
    for key in cfg.getMainKeys():
        print(key)
    for key in cfg.getCompatibleKeys():
        print(key)
    for key in cfg.getAllKeys():
        print(key)