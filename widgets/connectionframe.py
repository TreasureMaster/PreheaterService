import collections
from tkinter import *
from tkinter import ttk

# from connectimages import IndicatorImage
from registry import AppRegistry
from widgets import GUIWidgetConfiguration, ModuleImage

COMPORTS = 7
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
        self.comports = self.initComPortList(comports)
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
        rmc_frame.pack(side=LEFT, padx=5, fill=Y)
        com_label = Label(rmc_frame, text='Пульт:', anchor=W)
        com_label.pack(side=TOP, padx=5, fill=X)

        self.combo_rmc = ttk.Combobox(rmc_frame, values=self.remote_controls)
        # Текущее значение - первая таблица
        self.combo_rmc.current(0)
        self.combo_rmc.pack(side=TOP, padx=5)
        # Сразу же вывод первой таблицы при первом запуске программы
        self.combo_rmc.bind("<<ComboboxSelected>>", self.setRemoteControl)

        # (2) Фрейм выбора COM-порта и его скорости
        port_frame = Frame(self)
        port_frame.pack(side=LEFT, padx=5, fill=Y)
        port_label = Label(port_frame, text='Порт:', anchor=W)
        port_label.pack(side=TOP, padx=5, fill=X)

        self.combo_port = ttk.Combobox(port_frame, values=self.comports)
        # Текущее значение - первая таблица
        self.combo_port.current(0)
        self.combo_port.pack(side=TOP, padx=5)
        # Сразу же вывод первой таблицы при первом запуске программы
        self.combo_port.bind("<<ComboboxSelected>>", self.setComPort)

        # baud_label = Label(port_frame, text='Скорость:', anchor=W)
        # baud_label.pack(side=TOP, padx=5, fill=X)

        # self.combo_baud = ttk.Combobox(port_frame, values=(['----'] + BAUDRATES))
        # # Текущее значение - первая таблица
        # self.combo_baud.current(0)
        # self.combo_baud.pack(side=TOP, padx=5)
        # # Сразу же вывод первой таблицы при первом запуске программы
        # self.combo_baud.bind("<<ComboboxSelected>>", self.setBaudRate)

        # метка соединения
        # indicator = IndicatorImage(self.serialframe, image='yes2')
        # indicator.pack(side=LEFT, padx=5)

        # (3) Фрейм кнопок управления
        btn_frame = Frame(self)
        btn_frame.pack(side=LEFT, padx=5, fill=Y)
        # Кнопка настройки соединения
        # combtn = Button(btn_frame, text='Настройки', command=lambda: ComportWindow(comports=self.comports))
        # combtn.pack(side=TOP, padx=5, fill=X, pady=2)

        # Кнопка открытия/закрытия соединения
        connectbtn = Button(btn_frame, text='Открыть/Закрыть', command=lambda: None)
        connectbtn.pack(side=TOP, padx=5, fill=X, pady=2)

        # Кнопка считывания блока?
        readbtn = Button(btn_frame, text='Считать', command=lambda: None)
        readbtn.pack(side=TOP, padx=5, fill=X, pady=2)

        # (4) Фрейм с информацией о модуле
        info_frame = Frame(self)
        info_frame.pack(side=LEFT, padx=5, fill=Y)
        # self.add_border(info_frame, width=2, color='red')
        # Информация о блоке
        versionlabel = Label(info_frame, text=f'Версия:     {self.current_module.getBaseRevision()}', anchor=W)
        versionlabel.pack(side=TOP, padx=5, fill=X)
        # self.add_border(versionlabel, width=2, color='blue', relief=SOLID)
        numberlabel = Label(info_frame, text=f'Редакция: {self.current_module.getEdition()}', anchor=W)
        numberlabel.pack(side=TOP, padx=5, fill=X)

        # (5) Маленькая картинка модуля
        # image_frame = Frame(self)
        # image_frame = OnceByHeightMappedImage(self, lastadded=self)
        # image_frame.pack(side=LEFT, padx=5, expand=NO)
        # img = HeightResizedImage(image_frame, maxheight=80)
        # img.pack(expand=NO)
        # self.bind('<Map>', lambda event, img=img: img.pack(side=LEFT, padx=5, expand=NO))
        # self.bind('<Map>', lambda event, info=btn_frame: print(info.winfo_reqheight()))
        image_frame = ModuleImage(self, image=self.current_module.getImageLink(), maxheight=80)
        image_frame.pack(side=RIGHT)

    def setRemoteControl(self, event):
        rmc = self.combo_rmc.get()
        print(rmc)

    def setComPort(self, event):
        comport = self.combo_port.get()
        print(comport)

    # def setBaudRate(self, event):
    #     baudrate = self.combo_baud.get()
    #     print(baudrate)

    def initComPortList(self, comport_number=None):
        if not comport_number:
            comport_number = COMPORTS
        ports = list(map(lambda n: 'COM'+str(n), range(comport_number)))
        ports[0] = '----'
        return ports

    def initRemoteControlList(self, rmc_list=None):
        # if rmc_list:
            # TODO список совместимых пультов
            # remotecontrols = list(map(lambda n: 'COM'+str(n), range(rmc_list)))
        remotecontrols = ['----'] + rmc_list
        return remotecontrols


if __name__ == '__main__':
    root = Tk()
    conn = ConnectionFrame(root, comports=10)
    # print(conn.initComPortList(10))
    root.mainloop()