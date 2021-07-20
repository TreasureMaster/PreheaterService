import logging
from accessify import private

from registry import AppRegistry
from applogger import AppLogger
from base.modulehelper import ModuleHelper

from views.mainwindow import MainWindow


class Controller:

    __instance = None
    __moduleHelper = None

    @private
    def __init__(self):
        pass

    @staticmethod
    def run():
        # print(AppRegistry.instance().getRunPath())
        Controller.__instance = Controller()
        Controller.__instance.init()
        Controller.__instance.handleView()

    def init(self):
        logger = AppLogger.instance()
        logger.info('Start controller init')
        
        self.__moduleHelper = ModuleHelper.instance()
        self.__moduleHelper.init()
        # logger.error('Test second handler')
        # logger.error('Русский текст')
        # AppLogger.instance().error('Русский текст 2')
        # AppLogger.instance().info('Русский текст 3')
        AppLogger.instance().debugv('Тест пользовательского уровня DEBUGV с новой func')
        for _ in range(20):
            AppLogger.instance().critical('Тест записи уровня выше, чем задан в test.log')
        # logging.debugv('Тест пользовательского уровня DEBUGV')
        # print((logger))
        # import logging
        # print(logging._handlerList)
        # На данном этапе должен быть загружен список модулей либо ошибка
        # TODO [x] должны быть извлечены имена модулей, т.е. должны быть раскрыты архивы всех модулей и извлечены конфигурации

    def handleView(self):
        # Вывод на экран
        MainWindow.instance().startWindow()


if __name__ == '__main__':
    Controller.run()