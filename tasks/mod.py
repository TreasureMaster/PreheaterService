"""Тестовый модуль, который используется для проработки вида модуля без использования архивов."""

# REVIEW Что расположено в модуле сейчас:
# 1) Команды обработки кнопок модуля
# 2) GUI модуля
# 3) TODO: скрипт связи (команды) для отопителей

import os
from tkinter import messagebox
import tkinter.font as tkFont

from typing import List
from dataclasses import dataclass, field
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showwarning
import typing
from widgets import infolabels
from widgets.infolabels import InfoTitleLabel
from lxml import objectify

from appmeta import AbstractSingletonMeta
from registry import DeviceRegistry, WidgetsRegistry
from widgets import ScrolledListboxFrame, GUIWidgetConfiguration
from views import InfoModuleFrame

# ------------------------------ Команды модуля ------------------------------ #
from commands import Command

LINE_DIVIDER = '  |  '
# WARNING Определяется в 2 местах! Нужно подобрать одно место!
REPEAT_REQUESTS_COUNT = 3

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
        # print(self.maincommand.get(), self.extracommand.get(), self.longanswer.get())
        Button(direct, text='Отправить', command=self.do_command).pack()

    def check_commands(self):
        print(self.maincommand.get())

    def extra_command(self, value):
        print(value)

    def extra_answer(self):
        print(self.longanswer.get())

    def do_command(self):
        print('full answer:', self.maincommand.get(), ', ', self.extracommand.get(), ', ', self.longanswer.get())
        DeviceRegistry.instance().getDeviceProtocol().direct_request(
            command = self.maincommand.get(),
            is_long_query = self.longanswer.get(),
            data = [self.extracommand.get()]
        )


class FirmwareUpdate(ModuleCommand):
    """Создает окно виджета для прошивки микроконтроллера."""

    def execute(self, parent, scroll):
        self.firmware = None
        self.scroll = scroll
        for child in parent.winfo_children():
            if not isinstance(child, InfoTitleLabel):
                child.destroy()

        # Основное окно
        self.firmware_frame = Frame(parent)
        self.firmware_frame.pack()
        # scroll.bind_widgets(info.getScrollWidgets())

        cmdbutton_frame = Frame(self.firmware_frame)
        cmdbutton_frame.pack(fill=X)
        Button(cmdbutton_frame, text='Загрузить прошивку', command=self.load_module_data).pack(side=LEFT)
        Button(cmdbutton_frame, text='Обновить прошивку', command=self.do_firmware_update).pack(side=LEFT)

    def load_module_data(self):
        data_filename = askopenfilename(initialdir=os.getcwd(), filetypes=(('xml files', '*.xml'),))
        if data_filename:
            with open(data_filename, encoding='utf-8') as f:
                device = objectify.XML(f.read())
            # print(type(device.firmware))
            # for line in str(device.firmware).split('\n'):
            #     print(line.strip())
            # firmware = [[int(line.strip()[i:i+2], 16) for i in range(0, len(line.strip()), 2)]
            self.firmware = [LINE_DIVIDER.join([line.strip()[i:i+2] for i in range(0, len(line.strip()), 2)])
                        for line in str(device.firmware).strip().split('\n') if line]
            # firmware = [line for line in str(device.firmware).strip().split('\n')]
            # print(len(firmware))
            # print(f"'{firmware[0]}'", f"'{firmware[-1]}'")
            # firmware = [line for line in firmware if line]
            # print(len(self.firmware))
            print(self.firmware[:5])
        # else:
        #     # self.logger.error('Не выбрана папка или модуль для работы.')
        #     showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
        grid_frame = ScrolledListboxFrame(self.firmware_frame)
        grid_frame.pack(padx=10, pady=10)
        self.scroll.bind_widgets((grid_frame,))
        # grid_frame.add_list(firmware)
        # print(grid_frame.listbox.cget('font'))
        # print(tkFont.Font(font='TkDefaultFont').configure())
        grid_frame.listbox.config(font=('courier 10'), justify='center', width=43)
        grid_frame.add_list(self.firmware)
        info_labels = Frame(self.firmware_frame)
        info_labels.pack(pady=10, padx=10)
        Label(info_labels, text=f'Количество пакетов: {len(self.firmware)}').pack(side=LEFT)
        # self.progress_exec = StringVar(value='Отправлено: 0%')
        # self.progress_exec.set('Отправлено: 0%')
        # Label(info_labels, textvariable=self.progress_exec).pack(side=LEFT, padx=10)
        self.progress_exec = Label(info_labels, text='Отправлено: 0%')
        self.progress_exec.pack(side=LEFT, padx=10)

    def do_firmware_update(self):
        if self.firmware is None:
            showwarning(title='Предупреждение безопасности', message='Прошивка еще не выбрана!')
            return
        device = DeviceRegistry.instance().getDeviceProtocol()
        if device is not None:
            for _ in range(REPEAT_REQUESTS_COUNT):
        #     self.send_long_command(message)
        #     if self.is_echo_correct(message):
        #         break
        # else:
        #     raise FirmwareUpdateError('Пакет отправлен с ошибкой')
            # if device is not None:
                try:
                    device.firmware_update(self.firmware, self.progress_exec)
                except FirmwareUpdateError:
                    pass
                    # TODO Надо определить первая прошивка или повторная, чтобы отправить 0xB0 = 0001 0000 (начало записи данных)
                    # обнулить счетчик при этом ??? что-то слать при этом или нули ???
                else:
                    break
            else:
                showwarning(title='Предупреждение безопасности', message='Ошибка прошивки!')
                return
        else:
            showwarning(title='Предупреждение безопасности', message='Соединение еще не установлено!')
            return



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
        DirectControl(),
        FirmwareUpdate()
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

        if current in range(3):
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

    # ----------------------------- Базовые ID команд ---------------------------- #
    # 0х85 - запрос короткого ответа, 0хС4 - запрос длинного ответа
    SHORT_ANSWER = 0x85
    LONG_ANSWER = 0xC4
    # 0x03 - короткая команда, 0x42 - длинная команда
    SHORT_COMMAND = 0x03
    LONG_COMMAND = 0x42

    # ------------------------- Непосредственные команды ------------------------- #
    # Команды управления загрузкой:
    # Прошивка блока (байт 0xB0)
    FIRMWARE_UPDATE = 0x07
    # Команды прошивки (байт 0xB1, но используются только старшие 4 бита, младшие - это счетчик)
    # Данные для записи блока управления отопителем
    DATA_UPDATE_CMD = 0x00
    # Начало записи данных
    DATA_BEGIN_UPDATE_CMD = 0x10
    # Начало записи управляющей программы блока управления отопителем
    FIRMWARE_BEGIN_UPDATE_CMD = 0x20
    # Окончание записи
    END_UPDATE_CMD = 0x30

    # Базовая скорость передачи данных
    # BASE_SPEED = 9600

    # Длина команд
    SHORT_CMD_LENGTH = 2
    LONG_CMD_LENGTH = 8
    # Длина ответа
    # TODO скорее всего нужно будет изменить, т.к. первые байты не будут нужны
    SHORT_ANS_LENGTH = 6
    LONG_ANS_LENGTH = 12

    # Количество раз, которое менеджер пытается отправить отопителю пакет,
    # прежде чем сообщить об ошибке.
    REPEAT_REQUESTS_COUNT = 3

    # Пауза (в sec), после которой следует "разбудить" шину LIN
    # LIN_WAKEUP_TIME = 0.145


@dataclass
class FirmwareUpdateCount:
    """Счетчик отправленных в прошивку записей."""
    count: int = 0x00
    COUNT_END: int = field(default=0x0F, init=False)

    @property
    def start(self):
        self.count = 0x00
        return self.count

    @property
    def next(self):
        self.inc()
        return self.count

    def inc(self):
        if self.count == self.COUNT_END:
            self.count = 0x00
        else:
            self.count += 1


# ---------------------------------- Ошибки ---------------------------------- #
# Ошибка длины команды
class LINBusCommandLengthError(Exception):
    pass


# Подключение по шине не существует
class LINConnectionLookupError(Exception):
    pass


# Ошибка отправки прошивки
class FirmwareUpdateError(Exception):
    pass

# ---------------------------------------------------------------------------- #


# LINConfig - просто имплементация констант, которые потом можно заменить внешними
class DeviceProtocol(BusConfig):

    __device_bus = None

    def __init__(self, connection):
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

    @property
    def protocol(self):
        return self.device_bus.protocol

    # ------------------------------ Базовые команды ----------------------------- #
    def send_short_command(self, cmd: List[int]) -> None:
        """Отправка короткой команды отопителю."""
        if len(cmd) != 2:
            raise LINBusCommandLengthError
        self.protocol.send_command(self.SHORT_COMMAND, cmd)

    def send_long_command(self, cmd: List[int]) -> None:
        """Отправка длинной команды отопителю."""
        if len(cmd) != 8:
            raise LINBusCommandLengthError
        self.protocol.send_command(self.LONG_COMMAND, cmd)

    def get_short_answer(self) -> str:
        """Запрос ответа на короткую команду отопителю."""
        self.protocol.get_answer(self.SHORT_ANSWER)
        return self.protocol.get_response(self.SHORT_ANS_LENGTH)

    def get_long_answer(self) -> str:
        """Запрос ответа на длинную команду отопителю."""
        self.protocol.get_answer(self.LONG_ANSWER)
        return self.protocol.get_response(self.LONG_ANS_LENGTH)

    # ----------------------------- Составные команды ---------------------------- #
    def direct_request(self, command, is_long_query, data):
        """Отправка прямого запроса (выбор команды и ее сборка из прямого соединения)"""
        msg = [command, *data] + [0] * (
            (self.LONG_CMD_LENGTH if is_long_query else self.SHORT_CMD_LENGTH) - len(data) - 1
        )
        if is_long_query:
            self.send_long_command(msg)
        else:
            self.send_short_command(msg)
        echo = self.protocol.get_response(16)
        print('эхо после команды:', echo)

        if is_long_query:
            print('запрос длинного ответа:')
            print (self.get_long_answer())
        else:
            print('запрос короткого ответа:')
            print (self.get_short_answer())

    def firmware_update(self, firmware, progress):
        """Прошивка микроконтроллера."""
        # TODO проверить firmware ???
        # Инициализация счетчика отправленных строк данных
        count = FirmwareUpdateCount()
        # Отправить заголовок
        header = [self.FIRMWARE_UPDATE, self.DATA_BEGIN_UPDATE_CMD + count.start] + [0]*6
        try:
            self.send_line(header)
        except FirmwareUpdateError:
            raise
        # if not self.send_line(header):
        #     showwarning(title='Предупреждение безопасности', message='Ошибка при отправке заголовка прошивки.')
        #     return
        print('Заголовок отправлен и принят правильно.')
        # print(progress._root)
        # print(progress._tk)
        # print(progress.get())
        # return

        length = len(firmware)
        for num, line in enumerate(firmware[:20], start=1):
            message = [self.FIRMWARE_UPDATE, self.DATA_UPDATE_CMD + count.next]
            message.extend([int(digit.strip(), 16) for digit in line.strip().split(LINE_DIVIDER)])
            print(f'Посылка {num}:', message)
            try:
                self.send_line(message)
            except FirmwareUpdateError:
                raise
            # if not self.send_line(message):
            #     showwarning(title='Предупреждение безопасности', message='Ошибка при отправке заголовка прошивки.')
            #     return
            # if not num % 50:
            #     print(num)
            # TODO поменять на format с контролем пробелов, чтобы текст не дергался
            progress.config(text=f'Отправлено: {round(num/length, 2)}%')
            progress.update()
            # progress._tk.update()
        print('Прошивка отправлена.')

    # -------------------------- Вспомогательные функции ------------------------- #
    def is_echo_correct(self, message, cmd_type='long'):
        """Проверяет совпадение отправленного менеджером и принятого отопителем пакета."""
        crc = self.protocol.calc_CRC(message)
        package = [0x55, self.LONG_COMMAND if cmd_type == 'long' else self.SHORT_COMMAND] + message + [crc]
        echo = e[e.index(0x55):] if (e := self.protocol.get_response(16)) else e
        if echo != package:
            print(package)
            print(echo)
        return echo == package

    def send_line(self, message):
        for _ in range(self.REPEAT_REQUESTS_COUNT):
            self.send_long_command(message)
            if self.is_echo_correct(message):
                break
        else:
            raise FirmwareUpdateError('Пакет отправлен с ошибкой')
            # showwarning(title='Предупреждение безопасности', message='Ошибка при отправке прошивки.')
            # return
        # return True

    # ------------------------ Пробные (тестовые) команды ------------------------ #
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