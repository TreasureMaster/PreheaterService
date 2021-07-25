"""Файл конфигурационных настроек менеджера."""

from exceptions.exceptions import FNModuleInvalidModeException


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

    # ПАПКИ, определенные в системе:
    # Путь к папке, где хранятся все архивы модулей
    __modularlist_folder = 'modules'
    # Базовый путь папки модуля (корневая папка, куда распаковывается вся структура выбранного модуля)
    __workmodule_folder = 'module'
    # Основная папка, где хранятся файлы редактируемого модуля
    __base_editablemodule_folder = 'editable'
    # Распакованный путь:
    # Название подпапки с данными
    __data_subfolder = 'data'
    # Название подпапки с документацией
    __docs_subfolder = 'docs'
    # ФАЙЛЫ, определенные в системе:
    # Изображение отопителя
    __image_filename = 'image.jpg'
    # Описание отопителя
    __description_filename = 'readme.txt'
    # Файл конфигурации отопителя
    __config_filename = 'config.bin'

    # Поддерживаемые режимы работы модуля
    __REQUIRED_WORKMODES = {
        'work',
        'edit'
    }
    # Формирование путей к рабочим папкам
    __REQUIRED_PATHS = {
        'work': {
            'main': __workmodule_folder,
            'data': f"{__workmodule_folder}/{__data_subfolder}",
            'docs': f"{__workmodule_folder}/{__docs_subfolder}"
        },
        'edit': {
            'root': __base_editablemodule_folder,
            'main': f"{__base_editablemodule_folder}/{__workmodule_folder}",
            'data': f"{__base_editablemodule_folder}/{__workmodule_folder}/{__data_subfolder}",
            'docs': f"{__base_editablemodule_folder}/{__workmodule_folder}/{__docs_subfolder}"
        }
    }
    # Имена файлов
    __REQUIRED_FILES = {
        'image': __image_filename,
        'config': __config_filename,
        'description': __description_filename
    }

# ----------------------------- Данные менеджера ----------------------------- #
    def getManagerName(self) -> str:
        return self.__mainname

    def getVersion(self) -> str:
        return self.__version__

    def getFullVersion(self) -> str:
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
    def getModulesPath(self) -> str:
        return self.__modularlist_folder

# --------------------------- Универсальные функции -------------------------- #
    def isSupportedModes(self, mode: str) -> bool:
        """Проверяет вяляется ли режим работы модуля допустимым в данном менеджере."""
        mode = mode.lower()
        if mode in FNConfig.__REQUIRED_WORKMODES:
            return True
        else:
            raise FNModuleInvalidModeException(mode)

    def getPath(self, mode: str, path: str) -> str:
        """Возвращает относительный путь к папке.
        
        mode - режим модуля (работа/редактирование)
        path - название требуемой подпапки (например, data или docs)
        """
        if self.isSupportedModes(mode):
            return FNConfig.__REQUIRED_PATHS[mode][path]
        

    def getDatafile(self, mode: str, filename: str) -> str:
        """Возвращет относительный путь к файлу.
        
        mode - режим модуля (работа/редактирование)
        filename - требуемый файл (например, image.jpg, config.bin, readme.txt)
        """
        if self.isSupportedModes(mode):
            return f"{FNConfig.__REQUIRED_PATHS[mode]['data']}/{FNConfig.__REQUIRED_FILES[filename]}"


if __name__ == '__main__':
    cfg = FNConfig()
    for key in cfg.getMainKeys():
        print(key)
    for key in cfg.getCompatibleKeys():
        print(key)
    for key in cfg.getAllKeys():
        print(key)