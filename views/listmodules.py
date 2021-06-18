from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *

from registry import ModListRegistry, WidgetsRegistry
from commands.maincommands import ViewModule, ClearModuleWindow, DeleteModule, LoadModuleFile, LoadModuleDirectory, TestSaveStream


class ListModulesFrame(Frame):
    # Левая панель выбора модулей из списка
    def __init__(self, master, *args):
        Frame.__init__(self, master, *args)
        self._make_widgets()

    def _make_widgets(self):
        Label(self, text='Список модулей').pack(padx=5)

        # К правому окну прикрепляем виджет вывода значений таблиц БД
        textbar = Frame(self)
        textbar.pack(pady=10)
        # Для прокрутки окна со значениями вводим Scrollbar (если значений больше, чем размер таблицы)
        sbar = Scrollbar(textbar)
        self.listbox = Listbox(textbar, width=64)
        sbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        self.listmodules = StringVar(value=ModListRegistry.instance().getListModules())
        self.listbox.config(listvariable=self.listmodules)
        WidgetsRegistry.instance().setListVar(self.listmodules)
        self.listbox.bind('<<ListboxSelect>>', ViewModule())

        btn_frame = Frame(self)
        btn_frame.pack(fill=X, padx=20)
        Button(btn_frame, text='Открыть', command=TestSaveStream()).grid(sticky=W+E+S+N, pady=2)
        Button(btn_frame, text='Копировать', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        Button(btn_frame, text='Удалить', command=DeleteModule()).grid(sticky=W+E+S+N, pady=2)
        Button(btn_frame, text='Очистить', command=ClearModuleWindow()).grid(sticky=W+E+S+N, pady=2)
        Button(btn_frame, text='Загрузить модуль', command=LoadModuleFile()).grid(sticky=W+E+S+N, pady=2)
        Button(btn_frame, text='Открыть папку с модулями', command=LoadModuleDirectory()).grid(sticky=W+E+S+N, pady=2)


if __name__ == '__main__':
    root = Tk()
    conn = ListModulesFrame(root)
    # print(conn.initComPortList(10))
    root.mainloop()