"""Файл конфигурационных настроек менеджера."""


class FNConfig:
    # ------------------------- Базовые данные настройки ------------------------- #
    # Название менеджера (название программы, может измениться в будущем)
    __mainname = 'FN-Service'
    # Версия менеджера (major.minor.micro)
    __version__ = '0.2.0'
    # Совместимые версии менеджеров
    __compatible_versions = [
        # '0.1.0'
    ]
    # WARNING Длина ключей РОВНО 16 символов !!!
    # Базовый ключ этой версии менеджера, действующий именно для этого менеджера
    __main_keys = [
        b'kF-4g(kl{[s</!!~'
    ]
    # Совместимые ключи менеджеров, с версиями которых может работать данный менеджер
    __compatible_keys = [
        b'sjioGY29<<!"n_=k',
        b'YRod48&:*fst^%@j'
    ]
    # ПАПКИ, определенные в системе
    # Путь к папке, где хранятся архивы модулей
    __modularlist_folder = 'modules'
    # Базовый путь папки модуля (корневая папка, куда распаковывается вся структура модуля)
    __workmodule_folder = 'module'
    # Основная папка, где хранятся файлы редактируемого модуля
    __base_editablemodule_folder = 'editable'
    # Рабочая папка редактируемого модуля
    __editablemodule_folder = f'{__base_editablemodule_folder}/{__workmodule_folder}'
    # Название подпапки с данными (распаковка данных)
    __data_subfolder = 'data'
    # Название подпапки с документацией
    __docs_subfolder = 'docs'
    # ФАЙЛЫ, определенные в системе
    # Изображение отопителя
    __image_filename = 'image.jpg'
    # Описание отопителя
    __description_filename = 'readme.txt'
    # Файл конфигурации отопителя
    __config_filename = 'config.bin'
    # Путь к папке с данными
    __workmodule_datapath = f"{__workmodule_folder}/{__data_subfolder}"
    # Путь к папке с документацией
    __workmodule_docspath = f"{__workmodule_folder}/{__docs_subfolder}"
    # Путь к папке с редактируемыми данными
    __editablemodule_datapath = f"{__editablemodule_folder}/{__data_subfolder}"
    # TODO изменить эти данные на зашитые названия файлов и формирование названия в вызовах 'get'
    # Полные относительные пути для файлов модуля
    # рисунок
    # __required_image = f"{__workmodule_datapath}/image.jpg"
    # описание
    # __required_description = f"{__workmodule_datapath}/readme.txt"
    # конфигурация
    # __required_config = f"{__workmodule_datapath}/config.bin"
    # Полные относительные пути для файлов редактируемого модуля
    # рисунок
    # __required_editable_image = f"{__editablemodule_datapath}/image.jpg"
    # описание
    # __required_editable_description = f"{__editablemodule_datapath}/readme.txt"
    # конфигурация
    # __required_editable_config = f"{__editablemodule_datapath}/config.bin"
    # ---------------------------------------------------------------------------- #

# ----------------------------- Данные менеджера ----------------------------- #
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

    def getCompatibleVersions(self):
        for version in [self.__version__] + self.__compatible_versions:
            yield '{}-{}'.format(
                self.__mainname,
                version
            )

# --------------------------- Пути рабочего модуля --------------------------- #
    # def getPathsForZip(self):
    #     for path in {self.__data_subfolder, self.__docs_subfolder}:
    #         yield path

    def getModulesPath(self):
        return self.__modularlist_folder

    def getWorkPath(self):
        return self.__workmodule_folder

    def getWorkDataPath(self):
        return self.__workmodule_datapath

    def getWorkDocsPath(self):
        return self.__workmodule_docspath

    def getWorkImageFilepath(self):
        return f"{self.getWorkDataPath()}/{self.__image_filename}"

    def getWorkDescriptionFilepath(self):
        return f"{self.getWorkDataPath()}/{self.__description_filename}"

    def getWorkConfigFilepath(self):
        return f"{self.getWorkDataPath()}/{self.__config_filename}"

# ------------------------ Пути редактируемого модуля ------------------------ #

    def getBaseEditablePath(self):
        return self.__base_editablemodule_folder

    def getEditablePath(self):
        return self.__editablemodule_folder

    def getEditableDataPath(self):
        return self.__editablemodule_datapath

    def getEditableImageFilepath(self):
        return f"{self.getEditableDataPath()}/{self.__image_filename}"

    def getEditableDescriptionFilepath(self):
        return f"{self.getEditableDataPath()}/{self.__description_filename}"

    def getEditableConfigFilepath(self):
        return f"{self.getEditableDataPath()}/{self.__config_filename}"


if __name__ == '__main__':
    cfg = FNConfig()
    for key in cfg.getMainKeys():
        print(key)
    for key in cfg.getCompatibleKeys():
        print(key)
    for key in cfg.getAllKeys():
        print(key)