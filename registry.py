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
    __values = {}
    __instance = None

    # создать объект напрямую невозможно
    @private
    def __init__(self):
        pass

    # только так можно получить объект реестра
    @staticmethod
    def instance():
        if not AppRegistry.__instance:
            AppRegistry.__instance = AppRegistry()
        return AppRegistry.__instance

    # нельзя напрямую изменять свойства
    @protected
    def get(self, key):
        return self.__values[key]

    @protected
    def set(self, key, value):
        self.__values[key] = value

    # доступ к свойствам только именованный и контролируемый
    def getValue(self):
        return self.get('value')

    def setValue(self, value):
        self.__values['value'] = value


if __name__ == '__main__':
    print('Создать объект напрямую невозможно:')
    try:
        app = AppRegistry('test value')
    except Exception as exc:
        print('ERROR:', exc)
    print('При обращении к реестру получаем один и тот же объект:')
    app = AppRegistry.instance()
    print(app)
    app2 = AppRegistry.instance()
    print(app2)
    print('Получить значение напрямую:')
    try:
        print(app.get('value'))
    except Exception as exc:
        print('ERROR:', exc)
    print('Установить значение напрямую:')
    try:
        app.set('value', 'direct access')
    except Exception as exc:
        print('ERROR:', exc)
    print('Установить значение с помощью разрешенного доступа и проверить:')
    app.setValue('allowed access')
    print(app.getValue())
    print('Проверяем вторую ссылку на объект реестра:')
    print(app2.getValue())
