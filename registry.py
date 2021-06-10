import os
from threading import Lock
from abc import ABC, abstractmethod
from accessify import protected, private


class Registry(ABC):
    """
    Объявление интерфейса Реестра.
    """
    @protected
    @abstractmethod
    def get(self, key):
        pass

    @protected
    @abstractmethod
    def set(self, key, value):
        pass


class AppRegistry(Registry):
    """Реестр приложения."""
    # статические приватные свойства
    __values = {
        'value': None,
        'list_modules': None,
        'run_path': None
    }
    __instance = None
    __lock = Lock()

    # создать объект напрямую невозможно
    @private
    def __init__(self):
        pass

    # только так можно получить объект реестра
    @staticmethod
    def instance():
        with AppRegistry.__lock:
            if not AppRegistry.__instance:
                # import time
                # time.sleep(1)
                AppRegistry.__instance = AppRegistry()
                # AppRegistry.__instance.__setRunPath()
        return AppRegistry.__instance

    # нельзя напрямую изменять свойства
    @protected
    def get(self, key):
        return self.__values[key]

    @protected
    def set(self, key, value):
        self.__values[key] = value

    # СВОЙСТВО: тестовое, можно удалить
    def getValue(self):
        return self.instance().get('value')

    def setValue(self, value):
        self.instance().set('value', value)

    # СВОЙСТВО: список модулей
    def getListModules(self):
        return self.instance().get('list_modules')

    def setListModules(self, value):
        self.instance().set('list_modules', value)

    # СВОЙСТВО: путь запуска программы
    def getRunPath(self):
        if self.instance().get('run_path') is None:
            self.instance().setRunPath()
        return self.instance().get('run_path')

    def setRunPath(self):
        path = os.getcwd()
        # Для exe-файла path = sys.executable
        self.instance().set('run_path', path)

    # def getTest(self):
    #     return self.test


if __name__ == '__main__':
    print('Создать объект напрямую невозможно:')
    try:
        app = AppRegistry('test value')
    except Exception as exc:
        print('ERROR (test passed):', exc)
    print('При обращении к реестру получаем один и тот же объект:')
    app = AppRegistry.instance()
    print(app)
    app2 = AppRegistry.instance()
    print(app2)
    print('Получить значение напрямую:')
    try:
        print(app.get('value'))
    except Exception as exc:
        print('ERROR (test passed):', exc)
    print('Установить значение напрямую:')
    try:
        app.set('value', 'direct access')
    except Exception as exc:
        print('ERROR (test passed):', exc)
    print('Установить значение с помощью разрешенного доступа и проверить:')
    app.setValue('allowed access')
    print(app.getValue())
    print('Проверяем вторую ссылку на объект реестра:')
    print(app2.getValue())
# ---------------------------------------------------------------------------- #
    # print('Проверка в потоках:')
    # def test_singleton(value, result, i):
    #     singleton = AppRegistry.instance(value)
    #     # singleton.setValue(value)
    #     # result[i] = singleton.getValue()
    #     result[i] = singleton.getTest()
    # from threading import Thread
    # results = [None]*5
    # process1 = Thread(target=test_singleton, args=('FOO', results, 0))
    # process2 = Thread(target=test_singleton, args=('BAR', results, 1))
    # process3 = Thread(target=test_singleton, args=('BAR1', results, 2))
    # process4 = Thread(target=test_singleton, args=('BAR2', results, 3))
    # process5 = Thread(target=test_singleton, args=('BAR3', results, 4))
    # # print(process1.start())
    # process1.start()
    # process2.start()
    # process3.start()
    # process4.start()
    # process5.start()
    # for t in [process1, process2, process3, process4, process5]:
    #     t.join()
    # print(results)
    # assert results[0] == results[1]
    # print('Тест пройден для старта в потоках.')