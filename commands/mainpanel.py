# import typing
from abc import ABC, abstractmethod

from registry import AppRegistry


# NOTE В данной структуре получателем будет являться реестр AppRegistry
# Возможно, потом можно выделить получателя в отдельный класс
# class Receiver:
#     """
#     Классы Получателей содержат некую важную бизнес-логику. Они умеют выполнять
#     все виды операций, связанных с выполнением запроса. Фактически, любой класс
#     может выступать Получателем.
#     """

#     def do_something(self, a: str) -> None:
#         print(f"\nReceiver: Working on ({a}.)", end="")

#     def do_something_else(self, b: str) -> None:
#         print(f"\nReceiver: Also working on ({b}.)", end="")


class Command(ABC):
    """
    Интерфейс Команда объявляет метод для выполнения команд.
    """
    def __call__(self):
        self.execute()

    @abstractmethod
    def execute(self) -> None:
        pass


# NOTE нужна реализация 4 команд для главной панели управления:
# 0) Просмотр модуля (загрузить иинформацию из модуля для просмотра)
# 1) Открыть модуль
# 2) Копировать модуль
# 3) Удалить модуль
# 4) Загрузить модуль с указанием пути (загрузка отдельного модуля, отсутствующего в данной папке)
# -5) Сохранить и Сохранить как нужны ???

class ViewModule(Command):
    def __call__(self, event):
        self.execute(event)

    def execute(self, event):
        print('execute ViewModel')
        widget = event.widget
        selection = widget.curselection()
        picked = widget.get(selection)
        print(picked)


class OpenModule(Command):
    pass
    # Необходимо получить информацию о выбранном модуле
    # Варианты: клик в ListBox, выбран загрузкой как отдельный модуль (выделить в ListBox)
    def execute(self):
        pass

# ---------------------------------------------------------------------------- #

class SimpleCommand(Command):
    """
    Некоторые команды способны выполнять простые операции самостоятельно.
    """

    def __init__(self, payload) -> None:
        self._payload = payload

    # Команда реализует действия самостоятельно
    def execute(self) -> None:
        print(f"SimpleCommand: See, I can do simple things like printing"
              f"({self._payload})")


class ComplexCommand(Command):
    """
    Но есть и команды, которые делегируют более сложные операции другим объектам,
    называемым "получателями".
    """

    def __init__(self, receiver: AppRegistry, a: str, b: str) -> None:
        """
        Сложные команды могут принимать один или несколько объектов-получателей
        вместе с любыми данными о контексте через конструктор.
        """
        self._receiver = receiver
        self._a = a
        self._b = b

    # команда делегирует выполнение получателю
    def execute(self) -> None:
        """
        Команды могут делегировать выполнение любым методам получаетля.
        """
        print("ComplexCommand: Complex stuff should be done by a receiver object", end="")
        self._receiver.do_something(self._a)
        self._receiver.do_something_else(self._b)


class Invoker:
    """
    Отправитель связан с одной или несколькими командами.
    Он отправляет запрос команде.
    """
    _on_start = None
    _on_finish = None
    """
    Инициализация команд.
    """

    # регистрация стартовой команды
    def set_on_start(self, command: Command):
        self._on_start = command

    # регистрация финишной команды
    def set_on_finish(self, command: Command):
        self._on_finish = command

    # исполнение основной команды
    def do_something_important(self) -> None:
        """
        Отправитель не зависит от классов конкретных команд и получателей.
        Отправитель передает запрос получателю косвенно, выполняя команду.
        """

        # вначале выполняется стартовая команда
        print("Invoker: Кто-нибудь хочет, чтобы что-то было сделано до того, как я начну?")
        if isinstance(self._on_start, Command):
            self._on_start.execute()

        # затем выполняется базовая команда
        print("Invoker: ...делаем что-то действительно важное...")

        # в конце выполняется финишная программа
        print("Invoker: Кто-нибудь хочет, чтобы что-то было сделано после того, как я закончу?")
        if isinstance(self._on_finish, Command):
            self._on_finish.execute()


if __name__ == '__main__':
    """
    Клиентский код может параметризовать отправителя любыми командами.
    """
    print('-'*80)
    invoker = Invoker()
    # регистрация просто команды, которая будет исполняться на старте
    invoker.set_on_start(SimpleCommand('Say Hi!'))
    receiver = AppRegistry()
    # регистрация в отправителе комплексной команды (с получателем), которая будет обрабатываться в конце запроса
    invoker.set_on_finish(ComplexCommand(
        receiver, 'Send email', 'Save report'
    ))

    # Что выполняет отправитель при каком-то событии (н-р, нажатии кнопки)
    invoker.do_something_important()
    print('\n' + '-'*80)