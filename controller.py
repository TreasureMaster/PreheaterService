from accessify import private

from registry import AppRegistry
from modulehelper import ModuleHelper


class Controller:

    __instance = None
    __moduleHelper = None

    @private
    def __init__(self):
        pass

    @staticmethod
    def run():
        print(AppRegistry.instance().getRunPath())
        Controller.__instance = Controller()
        Controller.__instance.init()

    def init(self):
        self.__moduleHelper = ModuleHelper.instance()
        self.__moduleHelper.init()
        # На данном этапе должен быть загружен список модулей либо ошибка
        # TODO должны быть извлечены имена модулей, т.е. должны быть раскрыты архивы всех модулей и извлечены конфигурации
        # Это должно быть сделано в ModuleHelper.init()


if __name__ == '__main__':
    Controller.run()