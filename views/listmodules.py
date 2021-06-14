import collections
import glob, os
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *

from .connectimages import IndicatorImage
from registry import AppRegistry
from commands.mainpanel import ViewModule

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


class ListModulesFrame(Frame):
    # Левая панель выбора модулей из списка
    def __init__(self, master, *args):
        Frame.__init__(self, master, *args)
        self.listframe = Frame(master)
        self.listframe.pack(expand=YES, fill=X, pady=5)
        self._make_widgets()

    def _make_widgets(self):
        modules_label = Label(self.listframe, text='Список модулей')
        modules_label.pack(padx=5)

        # TODO Сейчас нужно, чтобы Combobox получил названия модулей из архивов
        # 1) т.е. нужен хелпер извлечения отдельного модуля (в том числе проверка на корректность модуля)
        # 2) ??? команда извлечения имени (может извлечь из модуля)
        # 3) сам класс модуля
        # self.modules_list = Combobox(self.listframe, values=[mod.getTitle() for mod in AppRegistry.instance().getAllModules().values()])
        # # Текущее значение - первая таблица
        # self.modules_list.current(0)
        # self.modules_list.pack(side=LEFT, padx=5)
        # # Сразу же вывод первой таблицы при первом запуске программы
        # self.modules_list.bind("<<ComboboxSelected>>", self.setComPort)

        # К правому окну прикрепляем виджет вывода значений таблиц БД
        textbar = Frame(self.listframe)
        textbar.pack(pady=10)
        # Для прокрутки окна со значениями вводим Scrollbar (если значений больше, чем размер таблицы)
        sbar = Scrollbar(textbar)
        self.listbox = Listbox(textbar, width=64)
        sbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        # TODO изменить на listvariables
        self.update_listbox()
        self.listbox.bind('<<ListboxSelect>>', ViewModule())

        Button(self.listframe, text='Открыть', command=lambda: None).pack()
        Button(self.listframe, text='Копировать', command=lambda: None).pack()
        Button(self.listframe, text='Удалить', command=lambda: None).pack()
        Button(self.listframe, text='Загрузить из...', command=lambda: None).pack()


    # def setComPort(self, event):
    #     comport = self.modules_list.get()
    #     print(comport)

    # def setBaudRate(self, event):
    #     baudrate = self.combo_baud.get()
    #     print(baudrate)

    # def initComPortList(self, comport_number=None):
    #     if not comport_number:
    #         comport_number = COMPORTS
    #     ports = list(map(lambda n: 'COM'+str(n), range(comport_number)))
    #     ports[0] = '----'
    #     return ports

    def update_listbox(self):
        self.listbox.delete(0, END)
        for mod in AppRegistry.instance().getAllModules().values():
            self.listbox.insert(END, mod.getTitle())


if __name__ == '__main__':
    root = Tk()
    conn = ListModulesFrame(root)
    # print(conn.initComPortList(10))
    root.mainloop()