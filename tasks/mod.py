"""Тестовый модуль, который используется для проработки вида модуля без использования архивов."""

# REVIEW Что расположено в модуле сейчас:
# 1) Команды обработки кнопок модуля
# 2) GUI модуля
# 3) TODO: скрипт связи (команды) для отопителей

import collections
import os
import queue
import time
import threading as th
from tkinter import messagebox
import tkinter.font as tkFont

# from typing import List
from dataclasses import dataclass, field
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showwarning
import typing as t
# import extras
from widgets import infolabels
from widgets.infolabels import InfoTitleLabel
from lxml import objectify

from appmeta import AbstractSingletonMeta
from registry import DeviceRegistry, PackageRegistry, WidgetsRegistry, ModuleRegistry
from widgets import ScrolledListboxFrame, GUIWidgetConfiguration, MonitoringFrame
from views import InfoModuleFrame
from config import LabelsConfig
from connections import microsleep
from applogger import AppLogger
from extras import StopWatch, MulticastQueue

# ------------------------------ Команды модуля ------------------------------ #
from commands import Command, maincommands

LINE_DIVIDER = '  |  '
# WARNING Определяется в 2 местах! Нужно подобрать одно место!
REPEAT_REQUESTS_COUNT = 3

# _LOCK = th.Lock()

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
                command = self.set_commands,
                variable = self.maincommand,
                value = key
            ).pack(anchor=NW)
        self.maincommand.set(0)

        Scale(
            direct,
            label = 'Дополнительно',
            command = self.set_extracommand,
            from_ = 0, to = 255,
            orient = 'horizontal'
        ).pack()

        self.longanswer = BooleanVar()
        Checkbutton(
            direct,
            text = 'Получение расширенного ответа',
            variable = self.longanswer,
            command = self.set_package_type
        ).pack()

        self.tracing = BooleanVar()
        self.tracing.set(
            ModuleRegistry.instance().getTracingView()
        )
        Checkbutton(
            direct,
            text = 'Просмотр отправленных/полученных ответов',
            variable = self.tracing,
            command = self.setup_tracing_view
        ).pack()


        direct.pack()
        self.setup_tracing_view()
        # scroll.bind_widgets(info.getScrollWidgets())
        # WidgetsRegistry.instance().pushWorkInfoFrame(info)
        # Button(direct, text='Отправить', command=self.do_command).pack()

    def set_commands(self):
        """Установка в реестр байта 0xB0."""
        PackageRegistry.instance().set0xB0(self.maincommand.get())
        # print(self.maincommand.get())

    def set_extracommand(self, value):
        """Установка в реестр байта 0xB1."""
        PackageRegistry.instance().set0xB1(int(value))

    def set_package_type(self):
        """Установка в реестр типа пакета - короткий или расширенный."""
        PackageRegistry.instance().setAnswerType(self.longanswer.get())
        # print(self.longanswer.get())

    def setup_tracing_view(self):
        """Установка в реестр вида окна - с просмотром отправленных/полученных ответов или без."""
        is_visible = self.tracing.get()
        ModuleRegistry.instance().setTracingView(is_visible)
        sending_view = ModuleRegistry.instance().getSendingFrame()
        # FIXME изменение ширины окна
        # положение сохраняется, если использовать метод grid_remove()
        sending_view.grid() if is_visible else sending_view.grid_remove()
        # print(self.longanswer.get())

    # NOTE Это не сюда, а в "Подключить"
    # def do_command(self):
    #     """Начинает непрерывную передачу команд."""
    #     # print('full answer:', self.maincommand.get(), ', ', self.extracommand.get(), ', ', self.longanswer.get())
    #     protocol = DeviceRegistry.instance().getDeviceProtocol()
    #     if protocol:
    #         DeviceRegistry.instance().getDeviceProtocol().direct_request()


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
        cmdbutton_frame.pack(fill=X, padx=10)
        Button(
            cmdbutton_frame,
            text='Загрузить прошивку из XML файла',
            command=self.load_xml_data
        ).grid(row=0, column=0, sticky='ew', padx=2, pady=2)
        Button(
            cmdbutton_frame,
            text='Обновить прошивку',
            command=self.do_firmware_update
        ).grid(row=0, column=1, sticky='ew', padx=2, pady=2)
        Button(
            cmdbutton_frame,
            text='Загрузить прошивку из FNP файла',
            command=self.load_fnp_data
        ).grid(row=1, column=0, sticky='ew', padx=2, pady=2)
        Button(
            cmdbutton_frame,
            text='Прервать прошивку',
            # command=self.do_firmware_update
            command=lambda: None
        ).grid(row=1, column=1, sticky='ew', padx=2, pady=2)

    def load_xml_data(self):
        """Подготовка данных прошивки из XML файла."""
        data_filename = askopenfilename(initialdir=os.getcwd(), filetypes=(('xml files', '*.xml'),))
        if data_filename:
            with open(data_filename, encoding='utf-8') as f:
                device = objectify.XML(f.read())
            self.firmware = [LINE_DIVIDER.join([line.strip()[i:i+2] for i in range(0, len(line.strip()), 2)])
                        for line in str(device.firmware).strip().split('\n') if line]
        # else:
        #     # self.logger.error('Не выбрана папка или модуль для работы.')
        #     showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
        self.create_firmware_grid()

    def load_fnp_data(self):
        """Подготовка данных прошивки из FNP файла."""
        data_filename = askopenfilename(initialdir=os.getcwd(), filetypes=(('fnp files', '*.fnp'),))
        if data_filename:
            self.firmware = []
            for line in open(data_filename, encoding='utf-8'):
                self.firmware.append(LINE_DIVIDER.join([line.strip()[i:i+2] for i in range(0, len(line.strip()), 2)]))
        # else:
        #     # self.logger.error('Не выбрана папка или модуль для работы.')
        #     showerror('Выбор папки', 'Вы должны выбрать папку или модуль для работы.')
        self.create_firmware_grid()

    # Заполнить сетку прошивки данными
    def create_firmware_grid(self):
        """Строит сетку с данными прошивки."""
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
        print('\n---> Нажали кнопку "обновить прошивку"')
        if self.firmware is None:
            showwarning(title='Предупреждение безопасности', message='Прошивка еще не выбрана!')
            return
        protocol = DeviceRegistry.instance().getDeviceProtocol()
        if protocol is not None:
            for firmware_update_attempt in range(REPEAT_REQUESTS_COUNT):
                try:
                    print('Запуск firmware update')
                    protocol.firmware_update(self.firmware, self.progress_exec, firmware_update_attempt)
                except FirmwareUpdateStop:
                    showwarning(title='Предупреждение безопасности', message='Прошивка остановлена!')
                    return
                except FirmwareUpdateError:
                    pass
                else:
                    break
            else:
                protocol.firmware_update_stop()
                showwarning(title='Предупреждение безопасности', message='Ошибка прошивки!')
                return
        else:
            showwarning(title='Предупреждение безопасности', message='Соединение еще не установлено!')
            return


class Monitoring(ModuleCommand):

    def execute(self, parent, scroll):
        # Необходимо очистить фрейм от дочерних элементов
        for child in parent.winfo_children():
            if not isinstance(child, InfoTitleLabel):
                child.destroy()
        # Основное информационное окно
        monitoring_frame = MonitoringFrame(parent)
        monitoring_frame.pack()
        scroll.bind_widgets(monitoring_frame.getScrollWidgets())
        # WidgetsRegistry.instance().pushWorkInfoFrame(info)


# ------------------------------- Фрейм модуля ------------------------------- #
# class WorkModuleFrame(ttk.Notebook):
class WorkModuleFrame(Frame, GUIWidgetConfiguration):
    # Список для Listbox
    __baselist = (
        'Общее описание',
        'Прямое управление',
        'Обновление ПО',
        'Мониторинг',
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
        FirmwareUpdate(),
        Monitoring()
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

        if current in range(len(WorkModuleFrame.__commands_list)):
            print(current)
            print(WorkModuleFrame.__commands_list[current])
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
    DATA_UPDATE_BEGIN_CMD = 0x10
    # Начало записи управляющей программы блока управления отопителем
    FIRMWARE_UPDATE_BEGIN_CMD = 0x20
    # Окончание записи
    FIRMWARE_UPDATE_END_CMD = 0x30

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
    REPEAT_REQUESTS_COUNT = 14

    # Пауза (в sec), после которой следует "разбудить" шину LIN
    # LIN_WAKEUP_TIME = 0.145

    # ----------------------------- Заготовки команд ----------------------------- #
    # Выключить блок
    TURN_OFF_BLOCK = [0x00, 0x00]


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


# Остановка прошивки
class FirmwareUpdateStop(Exception):
    pass

# ---------------------------------------------------------------------------- #


# LINConfig - просто имплементация констант, которые потом можно заменить внешними
class DeviceProtocol(BusConfig, LabelsConfig):

    __device_bus = None
    @dataclass(order=True)
    class PriorityPackage:
        """Пакет передачи информации в очереди с приоритетом."""
        time_marker: float
        data: t.Optional[dict] = field(compare=False, default=None)
        pack: t.Optional[list] = field(compare=False, default=None)
        is_good_answer: t.Optional[bool] = field(compare=False, default=None)

    MAPPER = {
        # 'not_controlled_queues': [queue.Queue(), queue.Queue()],
        # удалить и перенести в config
        'is_controlled': True,
        # удалить и перенести в config
        'all_timeouts': 3,
        'controlled_queues': {
            # Очередь ответов из блока во время прошивки
            'firmware': queue.PriorityQueue(),
            # Очередь для мониторинга
            'monitoring': queue.PriorityQueue(),
            # Очередь для трассировки (вывода отправленных/полученных пакетов из блока на экран)
            'tracing': queue.PriorityQueue()
        },
    }

    def __init__(self, connection):
        # Получили соединение, значит подключились и можно работать
        self.__device_bus = connection
        # Событие отключения
        self.disconnect_event = th.Event()
        # Условие начала приема ответа при прошивке блока
        self.__fw_update_condition = th.Condition()
        # Очередь передачи пакетов для прошивки блока
        self.__fw_update_queue = queue.PriorityQueue()
        # Пробуем создать многоадресную рассылку
        self.multicast = MulticastQueue(
            is_controlled=self.MAPPER['is_controlled'] if 'is_controlled' in self.MAPPER else True,
            all_timeouts=self.MAPPER['all_timeouts'] if 'all_timeouts' in self.MAPPER else None,
            **self.MAPPER['controlled_queues'],
        )
        # FIXME если будет None
        self.__sending_frame = ModuleRegistry.instance().getSendingFrame()
        self.__counter = collections.Counter(
            dict.fromkeys(self._COUNTER_LABELS.keys(), 0)
        )

        self._lock = th.Lock()

        # import logging
        # self.logger = logging.getLogger('direct_request')
        # self.logger.setLevel(logging.DEBUG)
        # handler = logging.FileHandler(filename='tmplog/fw_multiupdate1.log', mode='w', encoding='UTF-8')
        # formatter = logging.Formatter(
        #     '%(asctime)s [%(funcName)s] %(levelname)s: %(message)s\n---> %(package)s  time: %(nano)d => %(created)f\n'
        # )
        # formatter = logging.Formatter(
        #     '%(asctime)s [%(funcName)s] %(levelname)s: %(message)s\n---> %(package)s'
        # )
        # handler.setFormatter(formatter)
        # self.logger.addHandler(handler)
        # self.start = time.perf_counter_ns()
        # self.logger.debug('Старт логера:', extra={'package': None, 'nano': 0})
        # self.logger.debug('Старт логера', extra={'package': None})

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
        self.__counter.clear()
        with th.Lock():
            if self.__device_bus is not None:
                self.__device_bus.protocol.close()
                self.__device_bus = None
            DeviceRegistry.instance().setCurrentConnection(None)

    @property
    def protocol(self):
        return self.device_bus.protocol

    # ------------------------------ Базовые команды ----------------------------- #
    def send_short_command(self, cmd: t.List[int]) -> None:
        """Отправка короткой команды отопителю."""
        if len(cmd) != 2:
            raise LINBusCommandLengthError
        return self.protocol.send_command(self.SHORT_COMMAND, cmd)

    def send_long_command(self, cmd: t.List[int]) -> None:
        """Отправка длинной команды отопителю."""
        if len(cmd) != 8:
            raise LINBusCommandLengthError
        return self.protocol.send_command(self.LONG_COMMAND, cmd)

    def get_short_answer(self, view_text: bool=False) -> str:
        """Запрос ответа на короткую команду отопителю."""
        self.protocol.get_answer(self.SHORT_ANSWER)
        return self.protocol.get_response(self.SHORT_ANS_LENGTH, view_text)

    def get_long_answer(self, view_text: bool=False) -> str:
        """Запрос ответа на длинную команду отопителю."""
        self.protocol.get_answer(self.LONG_ANSWER)
        return self.protocol.get_response(self.LONG_ANS_LENGTH, view_text)

    def is_correct_CRC(self, answer: str) -> bool:
        """Проверка контрольной суммы ответа."""
        bad_answer = False
        try:
            answer_package = tuple(map(lambda i: int(i, 16), answer.split(' ')[2:]))
            must_crc = self.protocol.check_CRC(answer_package)
        except Exception as e:
            pass
        else:
            if must_crc != 0xFF:
                bad_answer = True
        return bad_answer

    # ----------------------------- Составные команды ---------------------------- #
    def direct_request(self):
        """Отправка прямого запроса (выбор команды и ее сборка из прямого соединения)"""

        self.multicast.hard_start()
        exit_marker = False
        good_answer_marker = None

        while True:
            with self._lock:
                # в начале проверяем, нужно ли слать в окно информации о пакетах
                (
                    self.multicast.start('tracing')
                    if ModuleRegistry.instance().getTracingView()
                    else self.multicast.stop('tracing')
                )

                if self.multicast.is_started('firmware'):
                    try:
                        package = self.__fw_update_queue.get_nowait()
                    except queue.Empty:
                        package = None
                    else:
                        package = package.pack
                        is_long_answer = True
                        is_long_query = True
                else:
                    package = PackageRegistry.instance().getPackage()
                    is_long_answer = PackageRegistry.instance().getAnswerType()
                    is_long_query = False
                # disconnect_event = DeviceRegistry.instance().getDisconnectEvent()

                if self.disconnect_event.is_set():
                    exit_marker = True
                    print('Отключаемся...')
                    self.multicast.all_clear()
                    close_answer = DeviceProtocol.PriorityPackage(time.time()+.0001, data=None, is_good_answer=False)
                    self.multicast.put(close_answer, stop_signal=True)
                    self.multicast.put_stop()

                    with self.__fw_update_condition:
                        self.__fw_update_condition.notify()
                    self.multicast.stop('firmware')
                elif package is not None:
                    answer = ''
                    self.__counter['all'] += 1
                    good_answer_marker = True

                    if is_long_query:
                        command = self.send_long_command(package)
                    else:
                        command = self.send_short_command(package)

                    # --- Получение эха от преобразователя USB->Serial (CH340, FTDI)
                    echo = self.protocol.get_response(16, view_text=True)
                    if not echo:
                        self.__counter['bad_echo'] += 1
                        good_answer_marker = False

                    # Нет эха, нет смысла запрашивать ответ ?
                    else:
                        # --- Получение ответа от устройства LIN
                        if is_long_answer:
                            answer = self.get_long_answer(view_text=True)
                        else:
                            answer = self.get_short_answer(view_text=True)
                        # if self.fw_update_event.is_set():
                        #     get = (list(map(lambda n: (int(n, 16)), answer.split())))[2:-1]
                        # FIXME сделать контроль ответа для прошивки
                        if not answer:
                            self.__counter['bad_answer'] += 1
                            good_answer_marker = False
                        else:
                            if not self.is_correct_CRC(answer):
                                self.__counter['bad_crc'] += 1
                                good_answer_marker = False
                            elif self.multicast.is_started('firmware'):
                                if len(package) != 8:
                                    # print('Длина пакета внутри:', len(package))
                                    self.__counter['bad_answer'] += 1
                                    good_answer_marker = False
                                else:
                                    get = (list(map(lambda n: (int(n, 16)), answer.split())))[2:-1]
                                    if package != get:
                                        self.__counter['bad_answer'] += 1
                                        good_answer_marker = False

                    self.__counter['good'] = (
                        self.__counter['all'] -\
                        self.__counter['bad_echo'] -\
                        self.__counter['bad_answer'] -\
                        self.__counter['bad_crc']
                    )
                    self.__counter['bad'] = self.__counter['all'] - self.__counter['good']

                    
                    answer_pack = DeviceProtocol.PriorityPackage(
                            time_marker=time.time(),
                            data = {
                                'send': command,
                                'echo': echo,
                                'answer': answer,
                                **self.__counter
                            },
                            is_good_answer=good_answer_marker
                        )
                    # Отправить инфу меткам менеджера
                    self.multicast.put(answer_pack)
                    # Отправить инфу методу прошивки
                    if self.multicast.is_started('firmware'):
                        with self.__fw_update_condition:
                            self.__fw_update_condition.notify()

                    package = None

            if self.multicast.is_started('firmware'):
                # Необходима прерываемая потоком пауза для того, чтобы
                # основной поток успел отработать с очередями
                # Скорее всего можно сделать меньше, но Win не поддерживает меньше 10..15 мсек
                # microsleep использовать нельзя, т.к. нужно гарантированное переключение между потоками
                time.sleep(0.01)

            if exit_marker:
                break

    def firmware_update(self, firmware, progress, attempt):
        """Прошивка микроконтроллера."""
        # TODO проверить firmware ???
        # Инициализация счетчика отправленных строк данных
        count = FirmwareUpdateCount()
        header = self.get_header(count, is_first=True)
        first = header + [0]*6
        second = header + [int(digit.strip(), 16) for digit in firmware[0].strip().split(LINE_DIVIDER)]
        try:
            self.firmware_update_start()
            # Первая пустая команда прошивки для перезагрузки блока
            self.send_line(first)
            # Блокирующее ожидание не менее 2 сек перезагрузки
            time.sleep(2.5)
            # Теперь можно стартовать прошивку
            self.send_line(second)
        except (FirmwareUpdateError, FirmwareUpdateStop) as e:
            self.firmware_update_stop()
            raise

        length = len(firmware)
        sw = StopWatch()
        # for num, line in enumerate(firmware, start=1):
        for num, line in enumerate(firmware[1:], start=2):
            # message = [self.FIRMWARE_UPDATE, self.DATA_UPDATE_CMD + count.next]
            message = self.get_header(count)
            message.extend([int(digit.strip(), 16) for digit in line.strip().split(LINE_DIVIDER)])
            try:
                self.send_line(message)
            except (FirmwareUpdateError, FirmwareUpdateStop):
                self.firmware_update_stop()
                raise
            # TODO поменять на format с контролем пробелов, чтобы текст не дергался
            sw.set_elapsed()
            progress.config(text=f'Отправлено: {int(100 * round(num/length, 2))}% Время: {sw.mins} мин {sw.secs} сек')
            progress.update()

        # TODO что происходит, если при данной отправке ошибка? Действия те же, что и при всех остальных?
        firmware_end = [self.FIRMWARE_UPDATE, self.FIRMWARE_UPDATE_END_CMD + count.start] + [0]*6
        try:
            self.send_line(firmware_end)
        except (FirmwareUpdateError, FirmwareUpdateStop):
            self.firmware_update_stop()
            raise
        print('Прошивка окончена.')

        # Отключить, проверить отключение.
        # NOTE вроде команду "выключить" не надо отсылать. Режим "выключено" должен устанавливаться по команде "окончание прошивки"
        # self.send_short_command(self.TURN_OFF_BLOCK)
        # print(self.get_long_answer(view_text=True))
        # print(self.get_short_answer(view_text=True))

        time.sleep(0.2)
        # Сбросить флаг прошивки и очистить очередь, если там еще что-то осталось
        self.firmware_update_stop()
        print('Флаг прошивки очищен.')

    # ---------------------------------- События --------------------------------- #
    def firmware_update_start(self):
        """Все команды старта прошивки"""
        self.multicast.start('firmware')
        # Очистить все очереди от мусора перед стартом прошивки
        self.multicast.all_clear()
    
    def firmware_update_stop(self):
        """Все команды остановки прошивки"""
        self.multicast.stop('firmware')
        # Если остановились, то надо очистить очередь
        self.multicast.clear('firmware')

    # -------------------------- Вспомогательные функции ------------------------- #
    def is_response_correct(self, message, cmd_type='long'):
        """Проверяет совпадение отправленного менеджером и принятого отопителем пакета."""
        crc = self.protocol.calc_CRC(message)
        package = [0x55, self.LONG_COMMAND if cmd_type == 'long' else self.SHORT_COMMAND] + message + [crc]
        # NOTE вероятно нужно отсылать get_long_answer, а не get_response
        response = self.protocol.get_response(16)
        response = response[response.index(0x55):] if response else response
        if response != package or (package[3] & 240) == self.FIRMWARE_UPDATE_END_CMD:
            print(package)
            print(response)
        # print('Ответ:', self.get_long_answer(view_text=True))
            # print('16:', self.protocol.byte2hex_text(response))
        return response == package

    # FIXME при отключении надо изменить схему работы (выдавать исключение FirmwareUpdateStop, чтобы не брать больше в работу)
    def is_response_correct2(self):
        while True:
            try:
                # Пока аналогично, потом надо что-то поменять
                package = self.multicast.get_nowait('firmware')
            except queue.Empty:
                pass
            else:
                response = None if package.data is None else package.is_good_answer
                break
        return response

    def send_line(self, message: list):
        """
        Схема отправка пакета при прошивке блока.
        
        Строка кода прошивки из 6 чисел плюс 2 управляющих числа (длинная команда)
        отправляется в блок несколько раз (сейчас 3) до тех пор, пока не будет
        получен корректный ответ. Правильность ответа проверяется в direct_request().
        Здесь обрабатывается только флаг - "хороший/плохой ответ" вне зависимости от
        причины ошибки.
        """
        for _ in range(self.REPEAT_REQUESTS_COUNT):
            with self.__fw_update_condition:
                self.__fw_update_queue.put(
                            DeviceProtocol.PriorityPackage(
                                time_marker=time.time(),
                                pack=message,
                            )
                        )
                # Здесь будет проверка таймаута 3 сек
                # Включение прошивки после старта через 2 сек, поэтому нужно ждать больше времени
                conclusion = self.__fw_update_condition.wait(3)
                if not conclusion:
                    raise FirmwareUpdateError('Превышение времени ожидания ответа')
                response = self.is_response_correct2()
                if response is None:
                    raise FirmwareUpdateStop('Прошивка остановлена')
                elif response:
                    break
        else:
            raise FirmwareUpdateError('Пакет отправлен с ошибкой')

    def get_header(self, count, is_first=False):
        """Формирование заголовка пакета 0xB0 и 0xB1 при прошивке."""
        cmd = ((self.FIRMWARE_UPDATE_BEGIN_CMD + count.start)\
            if is_first else (self.DATA_UPDATE_CMD + count.next))
        return [self.FIRMWARE_UPDATE, cmd]

    def update_labels(self):
        """Обновление меток с данными отправленных и полученных пакетов."""
        # TODO изменить режим работы отправки данных во фрейм
        package = self.multicast.get_instantly('tracing')
        if package is not None:
            if package.data is not None:
                for title, text in package.data.items():
                    self.__sending_frame.labels[title]['label'].configure(
                        text=text
                    )
            else:
                # пока стоп такой же - package.data == None
                return
        # При 64 на 3..5 хороших приходится 1 пустой; после отключения могут прийти 1 или 2; на старте 15 или 16 пустых
        # При 48 на 2 хороших приходится 1 пустой; после отключения могут прийти 1 или 2; на старте 17 или 18 пустых
        # При 32 на 1 хороший приходиться 1 или 2 пустых; после отключения приходит 1; на старте 23..24 пустых
        WidgetsRegistry.instance().getCurrentModuleWindow().after(48, self.update_labels)

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