from tkinter import *


class ScrolledListboxFrame(Frame):

    def __init__(self, master, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self._make_widgets()

    def _make_widgets(self):
        # Для прокрутки окна со значениями вводим Scrollbar (если значений больше, чем размер таблицы)
        sbar = Scrollbar(self)
        self.listbox = Listbox(self, width=64)
        sbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, expand=YES, fill=BOTH)

        # self.listmodules = StringVar(value=ModListRegistry.instance().getListModules())
        # self.listbox.config(listvariable=self.listmodules)
        # WidgetsRegistry.instance().setModulesListbox(self.listbox)
        # WidgetsRegistry.instance().setListVar(self.listmodules)
        # self.listbox.bind('<<ListboxSelect>>', ViewModule())

    def add_list(self, lb_list, register=None):
        """Добавить список в Listbox и зарегистрировать в реестре, если нужно."""
        itemlist = StringVar(value=lb_list)
        self.listbox.config(
            listvariable=itemlist
        )
        # WidgetsRegistry.instance().setListVar(itemlist)
        self.register(itemlist, register)

    def set_register(self, item, register=None):
        """Зарегистрировать переменную(список, виджет и т.п.) в реестре. Команда реестра должна быть получена извне."""
        if register is not None:
            register(item)

    def set_command(self, command):
        """Установить команду обработки выбора строки в списке."""
        self.listbox.bind('<<ListboxSelect>>', command)


if __name__ == '__main__':
    root = Tk()
    conn = ScrolledListboxFrame(root)
    conn.pack(expand=YES, fill=BOTH)
    # print(conn.initComPortList(10))
    conn.add_list(['Первый выбор', 'Второй выбор', 'Третий выбор'])
    conn.set_command(lambda event: print(f'checked: {event.widget.get(event.widget.curselection())}'))

    root.mainloop()