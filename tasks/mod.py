"""Тестовый модуль, который используется для проработки вида модуля без использования архивов."""

# REVIEW Что расположено в модуле сейчас:
# 1) Команды обработки кнопок модуля
# 2) GUI модуля
# 3) TODO: скрипт связи (команды) для отопителей

from typing import List
from tkinter import *
from widgets.infolabels import InfoTitleLabel
# from tkinter import ttk

from appmeta import AbstractSingletonMeta
from registry import DeviceRegistry, WidgetsRegistry
from widgets import ScrolledListboxFrame, GUIWidgetConfiguration
from views import InfoModuleFrame

# ------------------------------ Команды модуля ------------------------------ #
from commands import Command

class ModuleCommand(Command):

    def __call__(self, parent, scroll=None):
        self.execute(parent, scroll)


class ViewInfo(ModuleCommand):

    # FIXME или нет? Сохранение infomodule не нужно?
    def execute(self, parent, scroll):
        # Необходимо очистить фрейм от дочерних элементов
        # print(len(parent.winfo_children()))
        # print(parent)
        for child in parent.winfo_children():
            # print('---', child)
            # if isinstance(child, Frame):
            #     print(child.winfo_children())
            # if isinstance(child, InfoModuleFrame):
            #     WidgetsRegistry.instance().popWorkInfoFrame()
            if not isinstance(child, InfoTitleLabel):
                child.destroy()
        # print(WidgetsRegistry.instance().getSaveWorkInfoFrame())
        # Основное информационное окно
        info = InfoModuleFrame(parent)
        # info.grid(pady=5, row=1, column=1)
        info.pack()
        scroll.bind_widgets(info.getScrollWidgets())
        # WidgetsRegistry.instance().pushWorkInfoFrame(info)


class DirectControl(ModuleCommand):
    __commands = [
        'Выключить',
        'Отопление',
        'Вентиляция'
    ]

    def execute(self, parent, scroll):
        # Необходимо очистить фрейм от дочерних элементов
        for child in parent.winfo_children():
            # print(child)
            # if isinstance(child, InfoModuleFrame):
                # WidgetsRegistry.instance().popWorkInfoFrame()
            if not isinstance(child, InfoTitleLabel):
                child.destroy()
        # Основное информационное окно
        direct = Frame(parent)
        self.maincommand = IntVar()
        for key, text in enumerate(DirectControl.__commands):
            Radiobutton(
                direct,
                text = text,
                command = self.check_commands,
                variable = self.maincommand,
                value = key
            ).pack(anchor=NW)
        self.maincommand.set(0)

        self.extracommand = IntVar()
        Scale(
            direct,
            label = 'Дополнительно',
            command = self.extra_command,
            variable = self.extracommand,
            from_ = 0, to = 255,
            orient = 'horizontal'
        ).pack()

        self.longanswer = BooleanVar()
        Checkbutton(
            direct,
            text = 'Расширенный запрос',
            variable = self.longanswer,
            command = self.extra_answer
        ).pack()
        # Button(direct, text='Выключить', command=lambda: None).grid(sticky=W+E, pady=2)
        # Button(direct, text='Отопление', command=lambda: None).grid(sticky=W+E, pady=2)
        # Button(direct, text='Вентиляция', command=lambda: None).grid(sticky=W+E, pady=2)
        # Button(direct, text='Расширенный запрос', command=lambda: None).grid(sticky=W+E, pady=2)
        # info.grid(pady=5, row=1, column=1)
        direct.pack()
        # direct.config(
        #     borderwidth=2,
        #     highlightthickness=2,
        #     highlightbackground='gray',
        #     relief=FLAT
        # )
        # scroll.bind_widgets(info.getScrollWidgets())
        # WidgetsRegistry.instance().pushWorkInfoFrame(info)

    def check_commands(self):
        print(self.maincommand.get())

    def extra_command(self, value):
        print(value)

    def extra_answer(self):
        print(self.longanswer.get())


# ------------------------------- Фрейм модуля ------------------------------- #
# class WorkModuleFrame(ttk.Notebook):
class WorkModuleFrame(Frame, GUIWidgetConfiguration):
    # Список для Listbox
    __baselist = (
        'Общее описание',
        'Прямое управление',
        'Обновление ПО',
        'Журнал неисправностей',
        'Состояние узлов блока',
        'Коррекция параметров',
        'График'
    )
    # Команды для listbox
    # TODO нужно унифицировать аргументы, чтобы сделать одинаковый ввод
    __commands_list = [
        ViewInfo(),
        DirectControl()
    ]

    def __init__(self, master=None, root=None, **kwargs):
        # master - к чему крепится фрейм
        super().__init__(master, **kwargs)
        # root - главный виджет (не к которому крепится, а который создан изначально)
        self.root = root
        self._make_widgets()

    def _make_widgets(self):
        # Первая вкладка с кнопками управления
        # rc_frame = Frame(self)
        # rc_frame.pack(expand=YES, fill=BOTH)
        from widgets import InfoTitleLabel
        # InfoTitleLabel(rc_frame, text='Пульт (прямое управление)').grid(sticky=W+E+S+N, pady=2)
        # # WARNING размещено здесь из-за перекрестного импорта
        # # from commands.maincommands import ReplaceImage, SaveModule
        # Button(rc_frame, text='Выключить', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        # Button(rc_frame, text='Отопление', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        # Button(rc_frame, text='Вентиляция', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        # Button(rc_frame, text='Расширенный запрос', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        # # Button(rc_frame, text='Сохранить', command=SaveModule()).grid(sticky=W+E+S+N, pady=2)
        # Button(rc_frame, text='Отмена', command=self.root._quit).grid(sticky=W+E+S+N, pady=2)
        # ------------------------------------
        # Левая часть рабочего окна модуля (listbox выбора функций)
        funcselect_frame = Frame(self)
        # funcselect_frame.pack(side=LEFT, expand=YES, fill=BOTH)
        funcselect_frame.grid(row=0, column=0, sticky=W+N)
        # self.add_border(funcselect_frame, 2)
        InfoTitleLabel(funcselect_frame, text='Управление:').pack(fill=X, pady=2)
        listbar = ScrolledListboxFrame(funcselect_frame)
        listbar.pack(pady=10)
        # listbar.grid(padx=10, row=1, column=0, sticky=N)
        listbar.add_list(WorkModuleFrame.__baselist)
        listbar.set_command(self.__select_commands)
        listbar.listbox.config(width=30)
        listbar.listbox.select_set(0)
        # listbar.listbox.event_generate('<<ListboxSelect>>')

        # Button(funcselect_frame, text='Save to file', command=lambda: None).pack(fill=X, pady=2)
        # Button(funcselect_frame, text='Load from file', command=lambda: None).pack(fill=X, pady=2)
        # Button(funcselect_frame, text='AddRow', command=lambda: None).pack(fill=X, pady=2)
        # Button(funcselect_frame, text='DelRow', command=lambda: None).pack(fill=X, pady=2)
        # Button(funcselect_frame, text='Upload to Block', command=lambda: None).pack(fill=X, pady=2)
        # Button(funcselect_frame, text='Мониторинг', command=lambda: None).pack(fill=X, pady=2)
        # Button(funcselect_frame, text='Прошивка', command=lambda: None).pack(fill=X, pady=2)
        # Button(rc_frame, text='Сохранить', command=SaveModule()).grid(sticky=W+E+S+N, pady=2)
        Button(funcselect_frame, text='Выход', command=self.root._quit).pack(fill=X, pady=2)

        # self.add(rc_frame, text='Пульт')
        # self.add(funcselect_frame, text='Розжиг')

        # Основное информационное окно
        # info = InfoModuleFrame(self)
        # info.grid(pady=5, row=1, column=1)
        # self.scrollwindow.bind_widgets(info.getScrollWidgets())
        # WidgetsRegistry.instance().pushWorkInfoFrame(info)

        # Правая часть рабочего окна модуля (изменяется в зависимости от выбора listbox)
        self.work_frame = Frame(self)
        # work_frame.pack(expand=YES, fill=BOTH)
        self.work_frame.grid(row=0, column=1, sticky=E+W+N+S)
        # self.add_border(work_frame, 2)
        InfoTitleLabel(self.work_frame, text='Здесь будут различные окна работы с модулем').pack(fill=X, pady=2)

        # listbar.listbox.activate(0)
        listbar.listbox.event_generate('<<ListboxSelect>>')

    def __select_commands(self, event):
        # print(event.widget.curselection())
        current = event.widget.curselection()
        if current:
            current = current[0]
        else:
            return
        # print(current)
        print(event.widget.get(current))

        if current in (0, 1):
            WorkModuleFrame.__commands_list[current](self.work_frame, self.root.scrollwindow)
        # elif current == 1:
        #     WorkModuleFrame.__commands_list[1](self.work_frame)

    def view_info(self):
        pass


# ------------------------- Работа с шиной устройства ------------------------ #
# Реализация класса работы модуля с шиной LIN.

'''
Конфигурационные данные протокола LIN.
Версия в виде класса для того, чтобы можно было переписывать константы.
Возможно, нужно будет подгружать их из файла модуля.
'''

# WARNING перенесено сюда для последующего объединения в архиве модуля (требование заказчика)
class BusConfig:
    # ACTIVE_MODE_SLEEP = 0.01
    # loadByte возвращает эхо после каждого получения байта
    # 0х85 - запрос короткого ответа, 0хС4 - запрос длинного ответа
    SHORT_ANSWER = 0x85
    LONG_ANSWER = 0xC4
    # 0x03 - короткая команда, 0x42 - длинная команда
    SHORT_COMMAND = 0x03
    LONG_COMMAND = 0x42

    # Базовая скорость передачи данных
    # BASE_SPEED = 9600

    # Длина команд
    SHORT_CMD_LENGTH = 2
    LONG_CMD_LENGTH = 8
    # Длина ответа
    # TODO скорее всего нужно будет изменить, т.к. первые байты не будут нужны
    SHORT_ANS_LENGTH = 6
    LONG_ANS_LENGTH = 12

    # Пауза (в sec), после которой следует "разбудить" шину LIN
    # LIN_WAKEUP_TIME = 0.145


# Ошибка длины команды
class LINBusCommandLengthError(Exception):
    pass


# Подключение по шине не существует
class LINConnectionLookupError(Exception):
    pass


# LINConfig - просто имплементация констант, которые потом можно заменить внешними
class DeviceProtocol(BusConfig):#, metaclass=AbstractSingletonMeta):

    __device_bus = None

    def __init__(self, connection):
        # pass
        # self.__protocol = connection
        # if baud is None:
        #     baud = self.BASE_SPEED
        # Создает подключение к шине при инициализации
        # TODO в будущем можно сделать создание соединений по разным шинам (пока только LIN)
        # from modulebus import LIN
        # self.__protocol = LIN
        # self.device_bus = LINConnectionInitData(port, baud)
        # self.__device_bus = LIN(port, baud)
        self.__device_bus = connection
        # self.__device_bus = DeviceRegistry.instance().getCurrentConnection()

    @property
    def device_bus(self):
        """Возвращает соединение (например, LIN). Если его нет, то исключение."""
        if self.__device_bus is None:
            # Если нет соединения, пробуем извлечь из реестра
            self.__device_bus = DeviceRegistry.instance().getCurrentConnection()
            if self.__device_bus is None:
                # Если соединения нет даже в реестре, исключение
                raise LINConnectionLookupError
        return self.__device_bus

    # TODO что должно из себя представлять подключение шины ???
    # @device_bus.setter
    # def device_bus(self, connection_data):
    #     if connection_data.baud is None:
    #         baud = self.BASE_SPEED
    #     print(connection_data)
    #     self.__device_bus = self.__protocol(connection_data.port, baud)

    @device_bus.deleter
    def device_bus(self):
        """Закрывает и удаляет соединение."""
        if self.__device_bus is not None:
            self.__device_bus.close()
            self.__device_bus = None
        DeviceRegistry.instance().setCurrentConnection(None)

    def send_short_command(self, cmd: List[int]) -> None:
        """Отправка короткой команды отопителю."""
        if len(cmd) != 2:
            raise LINBusCommandLengthError
        self.device_bus.send_command(self.SHORT_COMMAND, cmd)

    def send_long_command(self, cmd: List[int]) -> None:
        """Отправка длинной команды отопителю."""
        if len(cmd) != 8:
            raise LINBusCommandLengthError
        self.device_bus.send_command(self.LONG_COMMAND, cmd)

    def get_short_answer(self) -> str:
        """Запрос ответа на короткую команду отопителю."""
        self.device_bus.get_answer(self.SHORT_ANSWER)
        return self.device_bus.get_response(self.SHORT_ANS_LENGTH)

    def get_long_answer(self) -> str:
        """Запрос ответа на длинную команду отопителю."""
        self.device_bus.get_answer(self.LONG_ANSWER)
        return self.device_bus.get_response(self.LONG_ANS_LENGTH)


    def scheduleDiagMsg2(self, msg):
        if len(msg) == self.SHORT_CMD_LENGTH:
            self.send_short_command(msg)
        else:
            self.send_long_command(msg)
        answer = self.device_bus.get_response(16)
        print('эхо после команды:', answer)

        # self.linbus.getAnswer(0x85)
        print('запрос короткого ответа:')
        print (self.get_short_answer())
        # self.linbus.getAnswer(0xC4)
        print('запрос длинного ответа:')
        print (self.get_long_answer())

    def scheduleDiagMsg(self, msg):
        self.device_bus.send_command(0x03, msg)
        print('эхо после команды:', self.device_bus.get_response(16))

        self.device_bus.get_answer(0x85)
        print('запрос короткого ответа:')
        print (self.device_bus.get_response(26))
        self.device_bus.get_answer(0xC4)
        print('запрос длинного ответа:')
        return self.device_bus.get_response(26)

    def testing(self):
        print(self.port)