import collections
from tkinter import *
from tkinter.ttk import *

from connectimages import IndicatorImage

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

class ComportSettings(Toplevel):

    def __init__(self, *args, comports=None):
        Toplevel.__init__(self, *args)
        self.comports = comports
        self.settings = {}
        self._make_widgets()
        self.focus_set()
        self.grab_set()
        self.wait_window()
        print('toplevel exit')
        # print(self)

    def _make_widgets(self):
        # self.master.title = 'Настройки'
        Label(self, text='Настройки').pack(fill=X, padx=5)
        
        # Сетка с настройками
        self.combo = Frame(self)
        self.combo.pack(fill=X)
        Label(self.combo, text='Port').grid(row=0, column=0, padx=5, pady=5, sticky=W)
        ports = Combobox(self.combo, values=self.comports)
        ports.current(0)
        ports.grid(row=0, column=1, padx=5, pady=5)
        self.settings['Port'] = ports
        for row, (key, values) in enumerate(comport_settings.items(), start=1):
            # print(key, values)
            Label(self.combo, text=key).grid(row=row, column=0, padx=5, pady=5, sticky=W)
            combo = Combobox(self.combo, values=values)
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

class ConnectionFrame(Frame):
    def __init__(self, master, *args, comports=None):
        Frame.__init__(self, master, *args)
        # self.mainframe = Frame(master)
        # self.mainframe.pack(expand=YES, fill=BOTH, pady=5)
        self.comports = self.initComPortList(comports)
        self.serialframe = Frame(master)
        self.serialframe.pack(expand=YES, fill=X, pady=5)
        self._make_widgets()

    def _make_widgets(self):

        # serialframe = Frame(self.mainframe)
        # serialframe.pack(fill=X)

        com_label = Label(self.serialframe, text='COM-порт:')
        com_label.pack(side=LEFT, padx=5)

        self.combo_port = Combobox(self.serialframe, values=self.comports)
        # Текущее значение - первая таблица
        self.combo_port.current(0)
        self.combo_port.pack(side=LEFT, padx=5)
        # Сразу же вывод первой таблицы при первом запуске программы
        # self.setComPort(0)
        self.combo_port.bind("<<ComboboxSelected>>", self.setComPort)

        baud_label = Label(self.serialframe, text='скорость:')
        baud_label.pack(side=LEFT, padx=5)

        self.combo_baud = Combobox(self.serialframe, values=(['----'] + BAUDRATES))
        # Текущее значение - первая таблица
        self.combo_baud.current(0)
        self.combo_baud.pack(side=LEFT, padx=5)
        # Сразу же вывод первой таблицы при первом запуске программы
        # self.setComPort(0)
        self.combo_baud.bind("<<ComboboxSelected>>", self.setBaudRate)

        # метка соединения
        indicator = IndicatorImage(self.serialframe, image='yes2')
        indicator.pack(side=LEFT, padx=5)

        # Кнопка настройки соединения
        combtn = Button(self.serialframe, text='Настройки', command=lambda: ComportSettings(comports=self.comports))
        combtn.pack(side=LEFT, padx=5)

        # Кнопка открытия/закрытия соединения
        connectbtn = Button(self.serialframe, text='Открыть/Закрыть', command=lambda: None)
        connectbtn.pack(side=LEFT, padx=5)

        # Кнопка считывания блока?
        readbtn = Button(self.serialframe, text='Считать', command=lambda: None)
        readbtn.pack(side=LEFT, padx=5)

        # Информация о блоке
        versionlabel = Label(self.serialframe, text='Версия: -------')
        versionlabel.pack(side=RIGHT, padx=5)
        numberlabel = Label(self.serialframe, text='Номер: -------')
        numberlabel.pack(side=RIGHT, padx=5)

    def setComPort(self, event):
        comport = self.combo_port.get()
        print(comport)

    def setBaudRate(self, event):
        baudrate = self.combo_baud.get()
        print(baudrate)

    def initComPortList(self, comport_number=None):
        if not comport_number:
            comport_number = COMPORTS
        ports = list(map(lambda n: 'COM'+str(n), range(comport_number)))
        ports[0] = '----'
        return ports


if __name__ == '__main__':
    root = Tk()
    conn = ConnectionFrame(root, comports=10)
    # print(conn.initComPortList(10))
    root.mainloop()