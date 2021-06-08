from tkinter import *


class ControlPanelFrame(Frame):
    def __init__(self, master, *args):
        Frame.__init__(self, master, *args)
        # self.comports = self.initComPortList(comports)
        self.modelframe = Frame(master)
        self.modelframe.pack(pady=5, side=LEFT, fill=Y)
        self._make_widgets()

    def _make_widgets(self):
        control_row = Frame(self.modelframe)
        control_row.pack(padx=5, pady=5)

        Button(control_row, text='Режимы', command=lambda: None).pack(padx=5, pady=5, side=LEFT)
        Button(control_row, text='Графики', command=lambda: None).pack(padx=5, pady=5, side=LEFT)
        Button(control_row, text='Очистить', command=lambda: None).pack(padx=5, pady=5, side=LEFT)
        Button(control_row, text='Черный ящик', command=lambda: None).pack(padx=5, pady=5, side=LEFT)

        model_frm = Frame(self.modelframe)
        model_frm.pack(fill=X)
        Label(model_frm, text='Прямое управление пульта', justify=LEFT).pack()
        Label(model_frm, text='(здесь будет окно модуля)', justify=LEFT).pack()


class LogPanelFrame(Frame):
    def __init__(self, master, *args):
        Frame.__init__(self, master, *args)
        # self.comports = self.initComPortList(comports)
        self.logframe = Frame(master)
        self.logframe.pack(pady=5, side=RIGHT, expand=YES, fill=BOTH)
        self._make_widgets()

    def _make_widgets(self):
        # К правому окну прикрепляем виджет вывода значений таблиц БД
        textbar = Frame(self.logframe)
        textbar.pack(expand=YES, fill=BOTH)
        # Для прокрутки окна со значениями вводим Scrollbar (если значений больше, чем размер таблицы)
        sbar = Scrollbar(textbar)
        listbox = Listbox(textbar, width=64)
        sbar.config(command=listbox.yview)
        listbox.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        listbox.pack(side=LEFT, expand=YES, fill=BOTH)

        # Вставка фейковых данных
        listbox.delete(0, END)
        listbox.insert(END, 'Ошибка: COM-порт не открыт.')
        listbox.insert(END, 'Ошибка: Настройки соединения не выбраны.')
        listbox.insert(END, 'Невозможно считать чёрный ящик - не открыт порт связи с изделием.')