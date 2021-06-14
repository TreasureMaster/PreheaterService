import collections
import glob, os
from tkinter import *
from tkinter import font
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.font import Font

from registry import AppRegistry
from commands.mainpanel import ViewModule


class InfoModuleFrame(Frame):
    # Левая панель выбора модулей из списка
    def __init__(self, master, *args):
        Frame.__init__(self, master, *args)
        # Сохранить фрейм в реестре
        AppRegistry.instance().setInfoFrame(self)
        # Переменные окон Message
        self.__description = StringVar(value=self.__getText('description'))
        self.__options = StringVar(value=self.__getText('options'))
        self.__make_widgets()

    def __make_widgets(self):
        titlefont = Font(family="Arial", size=10, weight="bold", slant="italic", underline=True)
        Label(self, text='Информация о модуле').pack(padx=5)
        # TODO здесь необходимо вставить картинку модуля
        Label(self,
              text='Описание модуля:',
              justify=LEFT,
              font=titlefont
            #   font=('Arial', 10, 'italic'),
            #   underline=True
        ).pack(padx=5, fill=X)

        # TODO вероятно придется сменить Label на Text, чтобы включить полосу прокрутки
        desc = Label(self, text='', textvariable=self.__description)
        # wraplength - размер в пикселях
        desc.config(justify=LEFT, wraplength=750)
        desc.config(relief=RIDGE)
        desc.pack(padx=5, pady=5, fill=X)

        Label(self,
              text='Параметры модуля:',
              justify=LEFT,
              font=titlefont
        ).pack(padx=5, fill=X)

        opts = Label(self, text='', textvariable=self.__options)
        opts.config(justify=LEFT, wraplength=750)
        opts.config(relief=RIDGE)
        opts.pack(padx=5, pady=5, fill=X)
        # TODO Сейчас нужно, чтобы Combobox получил названия модулей из архивов
        # 1) т.е. нужен хелпер извлечения отдельного модуля (в том числе проверка на корректность модуля)
        # 2) ??? команда извлечения имени (может извлечь из модуля)
        # 3) сам класс модуля
        # self.modules_list = Combobox(self, values=[mod.getTitle() for mod in AppRegistry.instance().getAllModules().values()])
        # Текущее значение - первая таблица
        # self.modules_list.current(0)
        # self.modules_list.pack(side=LEFT, padx=5)
        # Сразу же вывод первой таблицы при первом запуске программы
        # self.modules_list.bind("<<ComboboxSelected>>", self.setComPort)

        # К правому окну прикрепляем виджет вывода значений таблиц БД
        # textbar = Frame(self.infoframe)
        # textbar.pack(pady=10)
        # # Для прокрутки окна со значениями вводим Scrollbar (если значений больше, чем размер таблицы)
        # sbar = Scrollbar(textbar)
        # self.listbox = Listbox(textbar, width=64)
        # sbar.config(command=self.listbox.yview)
        # self.listbox.config(yscrollcommand=sbar.set)
        # sbar.pack(side=RIGHT, fill=Y)
        # self.listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        # # TODO изменить на listvariables
        # self.update_listbox()
        # self.listbox.bind('<<ListboxSelect>>', ViewModule())

        # Button(self, text='Открыть', command=lambda: None).pack()
        # Button(self, text='Копировать', command=lambda: None).pack()
        # Button(self, text='Удалить', command=lambda: None).pack()
        # Button(self, text='Загрузить из...', command=lambda: None).pack()

    def __getText(self, field):
        cur_mod = AppRegistry.instance().getCurrentModule()
        # print('info panel get text:', cur_mod)
        return cur_mod.getDescription(field) if cur_mod else ' Сообщение: модуль не выбран.'

    def updateText(self):
        # TODO как обновлять? Опять нужно StringVar отправить в реестр? Или лучше весь фрейм?
        # print(self.__getText('description'))
        self.__description.set(self.__getText('description'))
        self.__options.set(self.__getText('options'))
        # cur_mod = AppRegistry.instance().getCurrentModule()
        # return cur_mod.getDescription(field) if cur_mod else ' Сообщение: модуль не выбран.'

    # def getOptionsText(self):
    #     cur_mod = AppRegistry.instance().getCurrentModule()
    #     return cur_mod.getOptions() if cur_mod else ' Сообщение: модуль не выбран.'

    def setComPort(self, event):
        comport = self.modules_list.get()
        print(comport)

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
    conn = InfoModuleFrame(root)
    # print(conn.initComPortList(10))
    root.mainloop()