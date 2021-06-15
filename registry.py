import os
from threading import Lock
from abc import ABC, abstractmethod
from accessify import protected, private

from modulemapper import ModuleMapper


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
    # 1) modules - словарь предварительно загруженных из папки модулей
    # 2) run_path - путь запуска программы (будет важно для exe-файла)
    # 3) current_module - текущий, выбранный для работы модуль
    # 4) info_frame - фрейм первого окна с информациоей о модуле
    __values = {
        'value': None,
        'modules': ModuleMapper(),
        'run_path': None,
        'current_module': None,
        'info_frame': None,
        'main_window': None,
        'list_modules': None
    }
    # __modules = collections.OrderedDict()
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

    # СВОЙСТВО: конкретный модуль (получение, добавление, удаление)
    def getModule(self, name):
        return self.instance().get('modules').get(name)

    def ilocModule(self, name):
        return self.instance().get('modules').iloc(name)

    def addModule(self, name, value):
        # TODO: что делать, если ключ есть?
        self.instance().get('modules').update({name: value})

    def deleteModule(self, name):
        self.instance().get('modules').pop(name, None)

    # СВОЙСТВО: работа со словарем модулей
    def getAllModules(self):
        # TODO сделать как итератор, не возвращая сам словарь (иначе можно повредить)
        return self.instance().get('modules')

    def getListModules(self):
        # извлечь как список для Listbox
        return list(map(lambda t: t.getTitle(), self.instance().get('modules').values())) if len(self.instance().get('modules')) > 0 else []

    def clearAllModules(self):
        self.instance().get('modules').clear()

    # TODO Так проверить наличие модулей ?
    def is_emptyModules(self):
        pass

    # СВОЙСТВО: путь запуска программы
    def getRunPath(self):
        if self.instance().get('run_path') is None:
            self.instance().setRunPath()
        return self.instance().get('run_path')

    def setRunPath(self):
        path = os.getcwd()
        # Для exe-файла path = sys.executable
        self.instance().set('run_path', path)

    # СВОЙСТВО: объект текущего модуля, с которым производится работа
    def getCurrentModule(self):
        return self.instance().get('current_module')

    def setCurrentModule(self, value):
        self.instance().set('current_module', value)

    def deleteCurrentModule(self):
        self.instance().set('current_module', None)

    # СВОЙСТВО: фрейм информации о модуле (первое окно)
    def getInfoFrame(self):
        return self.instance().get('info_frame')

    def setInfoFrame(self, frame):
        self.instance().set('info_frame', frame)

    # СВОЙСТВО: существование главного окна
    def getMainWindow(self):
        return self.instance().get('main_window')

    def setMainWindow(self, frame):
        self.instance().set('main_window', frame)

    def existsMainWindow(self):
        if self.instance().get('main_window') is None:
            return False
        return self.instance().get('main_window').exists()

    def clearModulesWindow(self):
        # AppRegistry.__values = {key: (value if key in {'modules', 'run_path'} else None) for key, value in AppRegistry.__values.items()}
        AppRegistry.__values['current_module'] = None
        AppRegistry.__values['modules'] = ModuleMapper()

    # СВОЙСТВО: переменная списка модулей (в Listbox)
    def getListVar(self):
        # TODO метод не нужен ???
        return self.instance().get('list_modules')

    def setListVar(self, var):
        self.instance().set('list_modules', var)

    def updateListVar(self):
        self.instance().get('list_modules').set(self.instance().getListModules())


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