import dataclass_factory as df
import operator
import tkinter as tk
import tkinter.ttk as ttk
import yaml

from models import Monitoring


class MonitoringFrame(tk.Frame):

    def __init__(self, master, cnf={}, **kwargs):
        self.monitoring = kwargs.pop('monitoring', cnf.pop('monitoring', {}))
        super().__init__(master, cnf, **kwargs)

        # TODO убрать отсюда загрузку
        factory = df.Factory()
        self.monitoring = factory.load(
            yaml.load(
                open('module/data/monitoring.yml', encoding='utf-8'),
                Loader=yaml.SafeLoader
            ),
            Monitoring
        )
        if self.monitoring:
            self._create_table()

    def _create_table(self):
        """Создание таблицы мониторинга"""
        self.tree = ttk.Treeview(
            self, show='headings',
            columns=self.monitoring.indexes,
            # padding=10
        )
        # self.tree.pack()
        for idx, title in zip(self.monitoring.indexes, self.monitoring.headers):
            self.tree.heading(idx, text=title)

        self.ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.ysb.set)

        for params in sorted(self.monitoring.parameters, key=operator.attrgetter('key')):
            self.tree.insert(
                '', tk.END,
                # виртуальный номер строки (удобно задать по ключу параметра)
                iid=params.key,
                values=list(params)
            )

        self.tree.bind('<<TreeviewSelect>>', self.print_selection)

        self.tree.grid(row=0, column=0)
        self.ysb.grid(row=0, column=1, sticky=(tk.N + tk.S))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def print_selection(self, event):
        # selection() - получить текущее выделение(я)
        for selection in self.tree.selection():
            # selection - это номер iid
            print(selection)
            # item() - получить словарь параметров выбранного элемента
            item = self.tree.item(selection)
            # index() - это реальный номер строки (0, 1, 2, ...)
            print(self.tree.index(selection))
            # print(self.tree.item(128))
            print(item)
            value, description, key, ratio = item['values'][0:4]
            text = 'Выбор: {}, ({}): <{}>:<{}>'
            print(text.format(value, description, key, ratio))

        # Для прокрутки окна со значениями вводим Scrollbar (если значений больше, чем размер таблицы)
        # sbar = Scrollbar(self)
        # # WARNING exportselection=0 не отображается информационное окно
        # # при программном вызове события event_generate('<<ListboxSelect>>')
        # self.listbox = Listbox(self, width=64)#, exportselection=0)
        # sbar.config(command=self.listbox.yview)
        # self.listbox.config(yscrollcommand=sbar.set)
        # sbar.pack(side=RIGHT, fill=Y)
        # self.listbox.pack(side=LEFT, expand=YES, fill=BOTH)

    def getScrollWidgets(self):
        """Возвращает текстовые виджеты для корректировки событий прокрутки главного окна."""
        # WARNING опасно, можно изменить
        return (self.tree, self.ysb)

    # def add_list(self, lb_list, register=None):
    #     """Добавить список в Listbox и зарегистрировать в реестре, если нужно."""
    #     itemlist = StringVar(value=lb_list)
    #     self.listbox.config(
    #         listvariable=itemlist
    #     )
    #     # WidgetsRegistry.instance().setListVar(itemlist)
    #     self.register(itemlist, register)

    # def set_register(self, item, register=None):
    #     """Зарегистрировать переменную(список, виджет и т.п.) в реестре. Команда реестра должна быть получена извне."""
    #     if register is not None:
    #         register(item)

    # def set_command(self, command):
    #     """Установить команду обработки выбора строки в списке."""
    #     self.listbox.bind('<<ListboxSelect>>', command)


if __name__ == '__main__':
    root = tk.Tk()
    mon = MonitoringFrame(root)
    # mon = MonitoringFrame(
    #     root,
    #     {'bg': 'red', 'monitoring': 'yaml_test'},
    #     monitoring='yaml kwargs monitoring'
    # )
    mon.pack(expand=tk.YES, fill=tk.BOTH)
    tk.Label(mon, text='Test').pack(padx=10, pady=10)
    # print(conn.initComPortList(10))
    # conn.add_list(['Первый выбор', 'Второй выбор', 'Третий выбор'])
    # conn.set_command(lambda event: print(f'checked: {event.widget.get(event.widget.curselection())}'))

    print(mon.monitoring)

    root.mainloop()