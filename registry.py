from __future__ import annotations

import os
from threading import Lock
from typing import Any
from abc import ABC, abstractmethod
from accessify import protected, private

from modulemapper import ModuleMapper
from config import FNConfig

# ------------------------- Абстрактный класс реестра ------------------------ #

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

# ----------------------------- Реестр приложения ---------------------------- #

class AppRegistry(Registry):
    """Реестр приложения."""
    # статические приватные свойства
    # 1) run_path - путь запуска программы (будет важно для exe-файла)
    # 2) current_module - текущий, выбранный для работы модуль
    # 3) editable_module - редактируемый в данный момент модуль
    __values = {
        'run_path': None,
        'current_module': None,
        'editable_module': None
    }
    __instance = None
    __lock = Lock()

    # создать объект напрямую невозможно
    @private
    def __init__(self) -> None:
        pass

    # только так можно получить объект реестра
    @staticmethod
    def instance() -> AppRegistry:
        with AppRegistry.__lock:
            if not AppRegistry.__instance:
                AppRegistry.__instance = AppRegistry()
        return AppRegistry.__instance

    # Базовые методы set и get (нельзя напрямую изменять свойства)
    @protected
    def get(self, key: str) -> Any:
        return self.__values[key]

    @protected
    def set(self, key: str, value: Any) -> None:
        self.__values[key] = value

    # СВОЙСТВО: путь запуска программы
    def getRunPath(self):
        # WARNING наверное, установка, если None, ошибочна, так как к этому времени может смениться папка
        # if self.get('run_path') is None:
        #     self.setRunPath()
        return self.get('run_path')

    def setRunPath(self) -> None:
        path = os.getcwd()
        # Для exe-файла path = sys.executable
        self.set('run_path', path)

    # СВОЙСТВО: объект текущего модуля, с которым производится работа
    def getCurrentModule(self):
        return self.get('current_module')

    def setCurrentModule(self, value):
        self.set('current_module', value)

    def deleteCurrentModule(self):
        self.set('current_module', None)

    def clearModulesWindow(self):
        # AppRegistry.__values = {key: (value if key in {'modules', 'run_path'} else None) for key, value in AppRegistry.__values.items()}
        self.deleteCurrentModule()
        ModListRegistry.instance().clearAllModules()

    # СВОЙСТВО: объект нового модуля, который будет редактироваться (копия текущего)
    def getEditableModule(self):
        return self.get('editable_module')

    def setEditableModule(self, value):
        self.set('editable_module', value)

    def deleteEditableModule(self):
        self.set('editable_module', None)

# ------------------------------ Реестр модулей ------------------------------ #

class ModListRegistry(Registry):
    """Реестр списка модулей. Это класс-оболочка для словаря сканированых модулей."""
    # статические приватные свойства
    # 1) __modules - словарь предварительно загруженных из папки модулей
    __modules = ModuleMapper()
    __instance = None
    __lock = Lock()

    # создать объект напрямую невозможно
    @private
    def __init__(self) -> None:
        pass

    # только так можно получить объект реестра
    @staticmethod
    def instance() -> ModListRegistry:
        with ModListRegistry.__lock:
            if not ModListRegistry.__instance:
                ModListRegistry.__instance = ModListRegistry()
        return ModListRegistry.__instance

    # нельзя напрямую изменять свойства
    @protected
    def get(self, key: str) -> Any:
        return self.__modules[key]

    @protected
    def set(self, key: str, value: Any) -> None:
        self.__modules[key] = value

    # СВОЙСТВО: конкретный модуль (получение, добавление, удаление)
    def getModule(self, name):
        return self.get(name)

    def ilocModule(self, index):
        return self.__modules.iloc(index)

    def addModule(self, name, value):
        # TODO: что делать, если ключ уже есть, обновить?
        self.__modules.update({name: value})

    def deleteModule(self, name):
        self.__modules.pop(name, None)

    def last_indexModules(self):
        return self.__modules.last_index()

    # WARNING никакой защиты нет (надо продумать, может возвращать копию?)
    # Вроде получение всех модулей нигде не используется...
    # СВОЙСТВО: работа со словарем модулей
    # def getAllModules(self):
    #     # TODO сделать как итератор, не возвращая сам словарь (иначе можно повредить)
    #     return self.instance().get('modules')

    def getListModules(self):
        # извлечь как список названий-ключей для Listbox
        return list(map(lambda t: t.getTitle(), self.__modules.values())) if len(self.__modules) > 0 else []

    def getRevisions(self):
        # извлечь как список редакций модулей для проверки совпадающих
        return list(map(lambda t: t.revision, self.__modules.values())) if len(self.__modules) > 0 else []

    def clearAllModules(self):
        """Очистить список модулей."""
        self.__modules.clear()

    def is_modules(self):
        """Есть ли модули в списке?"""
        return len(self.__modules) > 0

# ------------------------------ Реестр виджетов ----------------------------- #

class WidgetsRegistry(Registry):
    """Реестр виджетов приложения.
    Используется как канал передачи информации между самими виджетами
    и между виджетами и другими объектами."""
    # статические приватные свойства
    # 1) work_info_frame - информационный фрейм первого окна с параметрами модуля (правый)
    # 2) save_work_info_frame - сохранение информационного фрейма первого окна, когда открывается рабочее второе окно
    # 3) main_window - главное окно менеджера (первое окно)
    # 4) list_modules - переменная StringVar списка модулей (левое окно)
    # 5) log_frame - фрейм отображения логов
    # 6) edit_info_frame - информационный фрейм окна редактирования с параметрами модуля (правый)
    __values = {
        'work_info_frame': None,
        'save_work_info_frame': None,
        'edit_info_frame': None,
        'main_window': None,
        'list_modules': None,
        'log_frame': None,
        'listbox': None
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
        with WidgetsRegistry.__lock:
            if not WidgetsRegistry.__instance:
                WidgetsRegistry.__instance = WidgetsRegistry()
        return WidgetsRegistry.__instance

    # нельзя напрямую изменять свойства
    @protected
    def get(self, key):
        return self.__values[key]

    @protected
    def set(self, key, value):
        self.__values[key] = value

    # СВОЙСТВО: правый фрейм информации о модуле (первое окно)
    def getWorkInfoFrame(self):
        """Получить информационный фрейм главного окна менеджера."""
        return self.get('work_info_frame')

    def setWorkInfoFrame(self, frame):
        """Установить информационный фрейм главного окна менеджера."""
        self.set('work_info_frame', frame)

    def pushWorkInfoFrame(self, frame):
        """Добавить информационный фрейм окна рабочего модуля и сделать его активным."""
        self.set('save_work_info_frame', self.getWorkInfoFrame())
        self.set('work_info_frame', frame)

    def getSaveWorkInfoFrame(self):
        """Получить информационный фрейм главного окна менеджера (неактивный в данный момент)."""
        return self.get('save_work_info_frame')

    def popWorkInfoFrame(self):
        """Извлечь информационный фрейм окна модуля и сделать активным информационный фрейм главного окна менеджера."""
        self.set('work_info_frame', self.getSaveWorkInfoFrame())
        self.set('save_work_info_frame', None)
        return self.getWorkInfoFrame()

    # СВОЙСТВО: правый фрейм информации о модуле (окно редактирования модуля)
    def getEditableInfoFrame(self):
        return self.get('edit_info_frame')

    def setEditableInfoFrame(self, frame):
        self.set('edit_info_frame', frame)

    # СВОЙСТВО: существование главного окна
    def getMainWindow(self):
        return self.get('main_window')

    def setMainWindow(self, frame):
        self.set('main_window', frame)

    def existsMainWindow(self):
        if self.get('main_window') is None:
            return False
        return self.get('main_window').exists()

    # Модули не очищаются
    # def clearModulesWindow(self):
    #     AppRegistry.__values['current_module'] = None
    #     AppRegistry.__values['modules'] = ModuleMapper()

    # СВОЙСТВО: переменная списка модулей (в Listbox)
    def getListVar(self):
        return self.instance().get('list_modules')

    def setListVar(self, var):
        self.set('list_modules', var)

    def updateListVar(self):
        self.get('list_modules').set(ModListRegistry.instance().getListModules())

    # СВОЙСТВО: фрейм отображения логов на экране
    def getLogFrame(self):
        return self.get('log_frame')

    def setLogFrame(self, frame):
        self.set('log_frame', frame)

    # СВОЙСТВО: ListBox отображения списка модулей
    def getModulesListbox(self):
        return self.get('listbox')

    def setModulesListbox(self, listbox):
        self.set('listbox', listbox)

# ----------------------- Реестр конфигурации менеджера ---------------------- #

class ConfigRegistry(Registry):
    """Реестр конфигураций (обертка класса конфигурации, н-р, менеджера)."""
    # статические приватные свойства
    # 1) manager - класс конфигурации менеджера
    __values = {
        'manager': None,
    }
    __instance = None
    __lock = Lock()

    # создать объект напрямую невозможно
    @private
    def __init__(self):
        self.__values['manager'] = FNConfig()

    # только так можно получить объект реестра
    @staticmethod
    def instance():
        with ConfigRegistry.__lock:
            if not ConfigRegistry.__instance:
                ConfigRegistry.__instance = ConfigRegistry()
        return ConfigRegistry.__instance

    # нельзя напрямую изменять свойства
    @protected
    def get(self, key):
        return self.__values[key]

    @protected
    def set(self, key, value):
        self.__values[key] = value

    # СВОЙСТВО: объект класс конфигурации менеджера
    def getManagerConfig(self):
        return self.get('manager')

    # TODO возможно следует возвращать некоторые ключи менеджера ?


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