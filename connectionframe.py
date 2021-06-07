from tkinter import *
from tkinter.ttk import *

from connectimages import IndicatorImage

COMPORTS = 7

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

        self.combo = Combobox(self.serialframe, values=self.comports)
        # Текущее значение - первая таблица
        self.combo.current(0)
        self.combo.pack(side=LEFT, padx=5)
        # Сразу же вывод первой таблицы при первом запуске программы
        self.setComPort(0)
        self.combo.bind("<<ComboboxSelected>>", self.setComPort)

        # метка соединения
        indicator = IndicatorImage(self.serialframe, image='yes2')
        indicator.pack(side=LEFT, padx=5)

        # Кнопка настройки соединения
        combtn = Button(self.serialframe, text='Настройки', command=lambda: None)
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
        comport = self.combo.get()
        print(comport)

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