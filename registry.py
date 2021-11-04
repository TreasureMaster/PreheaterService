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
    # 7) listbox - отображение списка модулей
    # 8) send_frame - фрейм окна модуля с данными пакетов отправки
    # 9) current_module_window - текущее рабочее окно модуля
    __values = {
        'work_info_frame': None,
        'save_work_info_frame': None,
        'edit_info_frame': None,
        'main_window': None,
        'list_modules': None,
        'log_frame': None,
        'listbox': None,
        'send_frame': None,
        'current_module_window': None
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
        # print('set Work Info Frame:', frame)
        self.set('work_info_frame', frame)

    # TODO возможно, push и pop можно будет удалить. Вроде бы работает и без них нормально
    # (вводились для решения проблемы с инфо-модулем главного окна и рабочего окна модуля)
    def pushWorkInfoFrame(self, frame):
        """Добавить информационный фрейм окна рабочего модуля и сделать его активным."""
        # print('push Work Info Frame:', frame)
        self.set('save_work_info_frame', self.getWorkInfoFrame())
        self.set('work_info_frame', frame)

    def getSaveWorkInfoFrame(self):
        """Получить информационный фрейм главного окна менеджера (неактивный в данный момент)."""
        return self.get('save_work_info_frame')

    def popWorkInfoFrame(self):
        """Извлечь информационный фрейм окна модуля и сделать активным информационный фрейм главного окна менеджера."""
        # print('pop Work Info Frame:', end=' ')
        self.set('work_info_frame', self.getSaveWorkInfoFrame())
        self.set('save_work_info_frame', None)
        # print(self.getWorkInfoFrame())
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

    # СВОЙСТВО: фрейм с информацией об отправке пакетов (окно модуля)
    def getSendingFrame(self):
        return self.get('send_frame')

    def setSendingFrame(self, send_frame):
        self.set('send_frame', send_frame)

    # СВОЙСТВО: Текущее рабочее окно модуля
    def getCurrentModuleWindow(self):
        return self.get('current_module_window')

    def setCurrentModuleWindow(self, module_window):
        self.set('current_module_window', module_window)

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


# ---------------------- Данные выбора в рабочем модуле ---------------------- #
class DeviceRegistry(Registry):
    """Реестр данных выбора в рабочем окне модуля.
    Например, пульт, тип соединения."""
    # статические приватные свойства
    # 1) remote_control - выбранный пульт
    # 2) connection_port - COM-порт для соединения
    # 3) python_module - модуль Python, загружаемый из архива рабочего модуля устройства
    # 4) current_connection - объект текущего соединения с ШИНОЙ (LIN или других - CAN, Bluetooth)
    # 5) lin_revision - версия шины LIN (классическая LIN 1.x или расширенная LIN 2.x)
    # 6) device_protocol - объект текущего соединение с УСТРОЙСТВОМ (без учета его типа)
    __values = {
        'remote_control': None,
        'connection_port': None,
        'python_module': None,
        'current_connection': None,
        'lin_revision': None,
        'device_protocol': None,
        'disconnect_event': None
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
        with DeviceRegistry.__lock:
            if not DeviceRegistry.__instance:
                DeviceRegistry.__instance = DeviceRegistry()
        return DeviceRegistry.__instance

    # нельзя напрямую изменять свойства
    @protected
    def get(self, key):
        return self.__values[key]

    @protected
    def set(self, key, value):
        self.__values[key] = value

    # СВОЙСТВО: выбранный пульт для работы с модулем (строка)
    def getCurrentRemoteControl(self):
        """Получить название текущего выбранного пульта."""
        return self.get('remote_control')

    def setCurrentRemoteControl(self, rmc: str):
        """Установить название текущего выбранного пульта."""
        self.set('remote_control', rmc)

    # СВОЙСТВО: выбранный COM-порт для работы с модулем (строка)
    def getCurrentComPort(self):
        """Получить название текущего выбранного COM-порта."""
        return self.get('remote_control')

    def setCurrentComPort(self, port: str):
        """Установить название текущего выбранного COM-порта."""
        self.set('remote_control', port)

    # СВОЙСТВО: выбранный тип работы с контрольной суммой в зависимости от версии LIN
    def getLINRevision(self) -> int:
        """Получить вариант работы с CRC."""
        revision = self.get('lin_revision')
        return revision if revision is not None else 0

    def setLINRevision(self, revision: int):
        """Установить вариант работы с CRC."""
        self.set('lin_revision', revision)

    # СВОЙСТВО: загруженный модуль Python
    def getPythonModule(self):
        """Получить загруженный из архива модуль."""
        return self.get('python_module')

    def setPythonModule(self, mod):
        """Установить загруженный из архива модуль."""
        self.set('python_module', mod)

    # СВОЙСТВО: объект соединения с шиной (LIN или другие)
    def getCurrentConnection(self):
        """Получить вид соединения с шиной."""
        return self.get('current_connection')

    def setCurrentConnection(self, conn):
        """Сохранить вид соединения с шиной."""
        self.set('current_connection', conn)

    # СВОЙСТВО: объект конкретного соединения устройства со всеми командами (из архива модуля)
    def getDeviceProtocol(self):
        """Получить текущее соединение с устройством."""
        return self.get('device_protocol')

    def setDeviceProtocol(self, device):
        """Сохранить текущее соединение с устройством."""
        self.set('device_protocol', device)

    # СВОЙСТВО: Флаг отключения прямого управления (непрерывной отправки пакетов)
    def is_DisconnectEvent(self):
        """Событие отключения произошло ?"""
        return self.get('disconnect_event')

    def setDisconnectEvent(self, event):
        """Установить флаг события отключения."""
        self.set('disconnect_event', event)


# -------------------------- Данные пакета отправки -------------------------- #
class PackageRegistry(Registry):
    """Реестр пакета отправки данных в блок и доп.условий отправки."""
    # статические приватные свойства
    # 1) 0xB0 - байт 0x01 пакета отправки
    # 2) 0xB1 - байт 0x01 пакета отправки
    # 3) extended - тип пакета - короткий или длинный
    __values = {
        '0xB0': 0x00,
        '0xB1': 0x00,
        'extended': False,
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
        with PackageRegistry.__lock:
            if not PackageRegistry.__instance:
                PackageRegistry.__instance = PackageRegistry()
        return PackageRegistry.__instance

    # нельзя напрямую изменять свойства
    @protected
    def get(self, key):
        return self.__values[key]

    @protected
    def set(self, key, value):
        self.__values[key] = value

    # СВОЙСТВО: байт пакета 0xB0
    # def get0xB0(self):
    #     """Получить байт 0xB0."""
    #     return self.get('0xB0')

    def set0xB0(self, b0: str):
        """Установить байт 0xB0."""
        self.set('0xB0', b0)

    # СВОЙСТВО: байт пакета 0xB1
    # def get0xB1(self):
    #     """Получить байт 0xB1."""
    #     return self.get('0xB1')

    def set0xB1(self, b1: str):
        """Установить байт 0xB1."""
        self.set('0xB1', b1)

    # СВОЙСТВО: Тип пакета - короткий или расширенный (длинный)
    def getPackageType(self):
        """Получить тип пакета - короткий или длинный."""
        return self.get('extended')

    def setPackageType(self, package_type: str):
        """Установить тип пакета - короткий или длинный."""
        self.set('extended', package_type)

    # СВОЙСТВО: Пакет для отправки (собирается здесь, поэтому доступно только свойство get)
    def getPackage(self):
        """Получить пакет для отправки."""
        package = [
            self.get('0xB0'),
            self.get('0xB1')
        ]
        if self.get('extended'):
            package += [0x00]*6

        return package


if __name__ == '__main__':
    package = PackageRegistry.instance()
    print(package.getPackage())
    package.setPackageType(True)
    print(package.getPackage())
# ---------------------------------------------------------------------------- #
    # print('Создать объект напрямую невозможно:')
    # try:
    #     app = AppRegistry('test value')
    # except Exception as exc:
    #     print('ERROR (test passed):', exc)
    # print('При обращении к реестру получаем один и тот же объект:')
    # app = AppRegistry.instance()
    # print(app)
    # app2 = AppRegistry.instance()
    # print(app2)
    # print('Получить значение напрямую:')
    # try:
    #     print(app.get('value'))
    # except Exception as exc:
    #     print('ERROR (test passed):', exc)
    # print('Установить значение напрямую:')
    # try:
    #     app.set('value', 'direct access')
    # except Exception as exc:
    #     print('ERROR (test passed):', exc)
    # print('Установить значение с помощью разрешенного доступа и проверить:')
    # app.setValue('allowed access')
    # print(app.getValue())
    # print('Проверяем вторую ссылку на объект реестра:')
    # print(app2.getValue())
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