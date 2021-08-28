import collections

from serial.tools import list_ports
from tkinter import *
from tkinter import ttk

# from connectimages import IndicatorImage
from registry import AppRegistry, DeviceRegistry
from widgets import GUIWidgetConfiguration, ModuleImage
from commands import DeviceConnect

BAUDRATES = [
    'Custom',
    '110',
    '300',
    '600',
    '1200',
    '2400',
    '4800',
    '9600',
    '14400',
    '19200',
    '38400',
    '56000',
    '57600',
    '115200',
    '128000',
    '256000'
]
comport_settings = collections.OrderedDict([
    ('Baud rate', BAUDRATES),
    ('Data bits', ['5', '6', '7', '8']),
    ('Stop bits', ['1', '1.5', '2']),
    ('Parity', ['None', 'Odd', 'Even', 'Mark', 'Space']),
    ('Flow control', ['None', 'Hardware', 'Software', 'Custom'])
])

class ComportWindow(Toplevel):

    def __init__(self, *args, comports=None):
        Toplevel.__init__(self, *args)
        self.comports = comports
        self.settings = {}
        self._make_widgets()
        self.focus_set()
        self.grab_set()
        self.wait_window()

    def _make_widgets(self):
        # self.master.title = 'Настройки'
        Label(self, text='Настройки').pack(fill=X, padx=5)
        
        # Сетка с настройками
        self.combo = Frame(self)
        self.combo.pack(fill=X)
        Label(self.combo, text='Port').grid(row=0, column=0, padx=5, pady=5, sticky=W)
        ports = ttk.Combobox(self.combo, values=self.comports)
        ports.current(0)
        ports.grid(row=0, column=1, padx=5, pady=5)
        self.settings['Port'] = ports
        for row, (key, values) in enumerate(comport_settings.items(), start=1):
            # print(key, values)
            Label(self.combo, text=key).grid(row=row, column=0, padx=5, pady=5, sticky=W)
            combo = ttk.Combobox(self.combo, values=values)
            # Текущее значение
            if key == 'Baud rate':
                combo.current(7)
            elif key == 'Data bits':
                combo.current(3)
            else:
                combo.current(0)
            combo.grid(row=row, column=1, padx=5, pady=5)
            self.settings[key] = combo
            # Сразу же вывод первой таблицы при первом запуске программы
            # self.setComPort(0)
            combo.bind("<<ComboboxSelected>>", lambda event: None)

        frm_buttons = Frame(self)
        frm_buttons.pack(fill=X)
        Button(frm_buttons, text='Cancel', command=self.destroy).pack(side=RIGHT, padx=5, pady=5)
        Button(frm_buttons, text='OK', command=self.destroy).pack(side=RIGHT, padx=5, pady=5)


class ConnectionFrame(Frame, GUIWidgetConfiguration):
    def __init__(self, master, comports=None, **kwargs):
        super().__init__(master, **kwargs)
        # self.mainframe = Frame(master)
        # self.mainframe.pack(expand=YES, fill=BOTH, pady=5)
        self.current_module = AppRegistry.instance().getCurrentModule()
        self.remote_controls = self.initRemoteControlList(self.current_module.getRemoteControlList())
        # self.comports = self.initComPortList(comports)
        # self.initComPortList(comports)
        self.comports = list_ports.comports()
        # self.serialframe = Frame(master)
        # self.serialframe.pack(expand=YES, fill=X, pady=5)
        self._make_widgets()
        # Информационная панель (нужна ли ?)
        # self.infopanel = Frame(master)
        # self.infopanel.pack(fill=X, padx=5, pady=5)
        # Label(self.infopanel, text='Здесь можно выводить информацию о состоянии подключения', justify=LEFT).pack(fill=X)

    def _make_widgets(self):
        # (1) Фрейм выбора пультов
        rmc_frame = Frame(self)
        rmc_frame.pack(side=LEFT, fill=Y)
        self.add_border(rmc_frame, width=1)
        com_label = Label(rmc_frame, text='Пульт:', anchor=W)
        com_label.pack(side=TOP, padx=5, fill=X)

        self.combo_rmc = ttk.Combobox(rmc_frame, values=self.remote_controls, exportselection=0)
        # Текущее значение - первая таблица
        self.combo_rmc.current(0)
        self.combo_rmc.pack(side=TOP, padx=5)
        # Сразу же вывод первой таблицы при первом запуске программы
        self.combo_rmc.bind("<<ComboboxSelected>>", self.setRemoteControl)

        # (2) Фрейм выбора COM-порта и его скорости
        port_frame = Frame(self)
        port_frame.pack(side=LEFT, fill=Y)
        self.add_border(port_frame, width=1)
        port_label = Label(port_frame, text='Порт:', anchor=W)
        port_label.pack(side=TOP, padx=5, fill=X)

        self.combo_port = ttk.Combobox(
            port_frame,
            values=(['----'] + [port.device for port in self.comports]),
            postcommand=self.updateComPortList,
            exportselection=0
        )
        # Текущее значение - первая таблица
        self.combo_port.current(0)
        self.combo_port.pack(side=TOP, padx=5, anchor=W)
        # Сразу же вывод первой таблицы при первом запуске программы
        self.combo_port.bind("<<ComboboxSelected>>", self.setComPort)

        # Описание выбранного порта
        self.port_description = Label(port_frame, text='', width=28, anchor=W)
        self.port_description.pack()

        # метка соединения
        # indicator = IndicatorImage(self.serialframe, image='yes2')
        # indicator.pack(side=LEFT, padx=5)

        # (3) Фрейм кнопок управления
        btn_frame = Frame(self)
        btn_frame.pack(side=LEFT, fill=Y)
        self.add_border(btn_frame, width=1)
        # Кнопка настройки соединения
        # combtn = Button(btn_frame, text='Настройки', command=lambda: ComportWindow(comports=self.comports))
        # combtn.pack(side=TOP, padx=5, fill=X, pady=2)
        Label(btn_frame, text='Соединение:').pack(padx=10, pady=2, fill=X)

        # Кнопка открытия/закрытия соединения
        connectbtn = Button(btn_frame, text='Подключить')
        connectbtn.config(
            command=DeviceConnect(connectbtn)
        )
        connectbtn.pack(side=TOP, padx=5, fill=X, pady=2)

        # Кнопка считывания блока?
        readbtn = Button(btn_frame, text='Сохранить', command=lambda: None)
        readbtn.pack(side=TOP, padx=5, fill=X, pady=2)

        # (4) Фрейм с информацией о модуле
        info_frame = Frame(self)
        info_frame.pack(side=LEFT, fill=Y)
        self.add_border(info_frame, width=1)
        # self.add_border(info_frame, width=2, color='red')
        # Информация о блоке
        versionlabel = Label(info_frame, text=f'Версия:     {self.current_module.getBaseRevision()}', anchor=W)
        versionlabel.pack(side=TOP, padx=5, fill=X)
        # self.add_border(versionlabel, width=2, color='blue', relief=SOLID)
        numberlabel = Label(info_frame, text=f'Редакция: {self.current_module.getEdition()}', anchor=W)
        numberlabel.pack(side=TOP, padx=5, fill=X)

        # (5) Маленькая картинка модуля
        image_frame = ModuleImage(self, image=self.current_module.getImageLink(), maxheight=80)
        image_frame.pack(side=RIGHT)

    def setRemoteControl(self, event):
        """Команда выбора пульта управления."""
        # rmc = self.combo_rmc.get()
        DeviceRegistry.instance().setCurrentRemoteControl(self.combo_rmc.get() or None)
        print(DeviceRegistry.instance().getCurrentRemoteControl())

    def setComPort(self, event):
        """Выбор com-порта из списка."""
        # Обновляет Label с описанием выбранного порта для соединения
        current = event.widget.current()
        self.port_description.config(
            text=(self.comports[current-1].description if current else ''),
            justify=LEFT
        )
        DeviceRegistry.instance().setCurrentComPort(self.comports[current-1].name if current else None)
        print(DeviceRegistry.instance().getCurrentComPort())

    def updateComPortList(self):
        """Обновление списка com-портов.
        
        Необходимо, так как устройство может быть физически подключено позже старта программы.
        Добавление прочерков в список com-портов после формирования последнего."""
        self.comports = list_ports.comports()
        self.combo_port.config(
            values=([''] + [port.device for port in self.comports])
        )

    def initRemoteControlList(self, rmc_list=None):
        """Формирование списка пультов управления."""
        # if rmc_list:
            # TODO список совместимых пультов
            # remotecontrols = list(map(lambda n: 'COM'+str(n), range(rmc_list)))
        remotecontrols = [''] + rmc_list
        return remotecontrols


if __name__ == '__main__':
    root = Tk()
    conn = ConnectionFrame(root, comports=10)
    # print(conn.initComPortList(10))
    root.mainloop()