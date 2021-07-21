import copy, os, shutil
from abc import ABC, abstractmethod

from tkinter.messagebox import *
from tkinter.filedialog import *

from registry import AppRegistry, WidgetsRegistry, ModListRegistry, ConfigRegistry
from applogger import AppLogger
from base.modulehelper import ModuleHelper
from views.editwindow import EditWindow


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

class CommandMixin:

    def clearModuleInfo(self):
        WidgetsRegistry.instance().getInfoFrame().updateText()
        WidgetsRegistry.instance().getInfoFrame().clearImage()
        WidgetsRegistry.instance().updateListVar()
        # TODO заменить на путь из Registry
        mainpath = ConfigRegistry.instance().getManagerConfig().getMainPath()
        if os.path.exists(mainpath):
            shutil.rmtree(mainpath)

    def highlightListBox(self):
        listbox = WidgetsRegistry.instance().getModulesListbox()
        for numline in range(listbox.size()):
            if not ModListRegistry.instance().ilocModule(numline).isCompatible():
                listbox.itemconfig(numline, fg='red', selectforeground='red', selectbackground='yellow')


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
    """Вывод информации о выбранном модуле в инфоокне."""
    def __call__(self, event):
        self.execute(event)

    def execute(self, event):
        # print('execute ViewModel')
        if not event.widget.curselection():
            return
        # Текущий модуль
        current_module = ModListRegistry.instance().ilocModule(event.widget.curselection()[0])
        # print('select module form listbox:', current_module)
        
        # print(AppRegistry.instance().getCurrentModule())
        # Распаковка данных в каталог MODULE
        if current_module.unpackData():
            # Текущий модуль сохраняется в реестре только, если распаковывается
            AppRegistry.instance().setCurrentModule(current_module)
            # print(WidgetsRegistry.instance().getInfoFrame())
            WidgetsRegistry.instance().getInfoFrame().updateText()
            WidgetsRegistry.instance().getInfoFrame().updateImage()
            AppLogger.instance().info(f'Распакован модуль {current_module.getName()}.')
            print(WidgetsRegistry.instance().getInfoFrame()._getWorkModule())


class ClearModuleWindow(Command, CommandMixin):
    """Команда очистки окна списка модулей."""
    def execute(self):
        AppRegistry.instance().clearModulesWindow()
        self.clearModuleInfo()
        AppLogger.instance().info('Окно выбора модулей очищено.')



class DeleteModule(Command, CommandMixin):
    """Команда удаления модуля из списка модулей и самого файла модуля."""
    def execute(self):
        cur_mod = AppRegistry.instance().getCurrentModule()
        if askokcancel('Удаление модуля', 'Удалить модуль?\nМодуль {} будет удален из текущей папки.'.format(cur_mod.getTitle())):
            if cur_mod is not None and os.path.exists(cur_mod.link):
                try:
                    os.remove(cur_mod.link)
                    AppLogger.instance().info('Файл модуля был успешно удален.')
                except (FileNotFoundError, LookupError):
                    AppLogger.instance().error('Ошибка удаления файла.')
            else:
                if cur_mod:
                    AppLogger.instance().error('Файл не существует.')
                else:
                    AppLogger.instance().error('Текущий модуль не найден.')
                return
            ModListRegistry.instance().deleteModule(cur_mod.getName())
            AppRegistry.instance().deleteCurrentModule()
            self.clearModuleInfo()
            self.highlightListBox()


class LoadModuleFile(Command, CommandMixin):
    """Команда загрузки отдельного файла модуля."""
    def execute(self):
        AppLogger.instance().info('Загрузка файла модуля.')
        ModuleHelper.instance().getSingleModule()
        self.clearModuleInfo()
        self.highlightListBox()


class LoadModuleDirectory(Command, CommandMixin):
    """Команда загрузки папки с модулями."""
    def execute(self):
        directory = None
        if askyesno('Поиск модулей', 'Стандартная папка с модулями не найдена.\nХотите указать, где она находиться?'):
            directory = askdirectory(initialdir=os.getcwd())
        else:
            # Если папку не выбирают, предлагаем выбрать отдельный модуль
            AppLogger.instance().error('Не выбрана папка или модуль для работы.')
            showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
            return
        if directory:
            AppLogger.instance().info('Выбор папки с модулями.')
            ModuleHelper.instance().getModuleDirectory(directory)
            self.clearModuleInfo()
            self.highlightListBox()
        else:
            AppLogger.instance().error('Не выбрана папка или модуль для работы.')
            showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')


class OpenModule(Command):
    pass
    # Необходимо получить информацию о выбранном модуле
    # Варианты: клик в ListBox, выбран загрузкой как отдельный модуль (выделить в ListBox)
    def execute(self):
        pass


class EditModule(Command):

    def execute(self):
        # TODO вначале проверить, что модуль выбран
        current_module = AppRegistry.instance().getCurrentModule()
        if current_module:
            AppRegistry.instance().setEditableModule(copy.deepcopy(current_module))
            EditWindow()
        else:
            AppLogger.instance().error('Не выбран модуль для редактирования.')
            showerror('Редактирование модуля', 'Вы должны выбрать модуль для редактирования.')


class ViewLog(Command):
    def execute(self):
        # print(AppLogger.get_stream().getvalue())
        logwindow = WidgetsRegistry.instance().getLogFrame()
        for line in AppLogger.get_stream().split('\n'):
            logwindow.insert(
                'end',
                (line + '\n') if line else '',
                # Вроде бы работает и с None, и с ''
                ('error' if 'ERROR]' in line else None)
            )
        # TODO блокировать Lock, пока идет запись?
        # with open('tmplog/stream.log', 'a', encoding='utf-8') as fd:
        #     fd.write('----------------\n')
        #     fd.write(stream.getvalue())

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