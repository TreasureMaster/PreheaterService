"""Тестовый модуль, который используется для проработки вида модуля без использования архивов."""

# REVIEW Что расположено в модуле сейчас:
# 1) Команды обработки кнопок модуля
# 2) GUI модуля
# 3) TODO: скрипт связи (команды) для отопителей

from tkinter import *
from widgets.infolabels import InfoTitleLabel
# from tkinter import ttk

from registry import WidgetsRegistry
from widgets import ScrolledListboxFrame, GUIWidgetConfiguration
from views import InfoModuleFrame


from commands import Command

class ViewInfo(Command):

    def __call__(self, parent, scroll):
        self.execute(parent, scroll)

    def execute(self, parent, scroll):
        # Необходимо очистить фрейм от дочерних элементов
        for child in parent.winfo_children():
            if isinstance(child, InfoModuleFrame):
                WidgetsRegistry.instance().popWorkInfoFrame()
            if not isinstance(child, InfoTitleLabel):
                child.destroy()
        # Основное информационное окно
        info = InfoModuleFrame(parent)
        # info.grid(pady=5, row=1, column=1)
        info.pack()
        scroll.bind_widgets(info.getScrollWidgets())
        WidgetsRegistry.instance().pushWorkInfoFrame(info)


class DirectControl:
    __commands = [
        'Выключить',
        'Отопление',
        'Вентиляция'
    ]

    def __call__(self, parent):
        self.execute(parent)

    def execute(self, parent):
        # Необходимо очистить фрейм от дочерних элементов
        for child in parent.winfo_children():
            # print(child)
            # if isinstance(child, InfoModuleFrame):
                # WidgetsRegistry.instance().popWorkInfoFrame()
            if not isinstance(child, InfoTitleLabel):
                child.destroy()
        # Основное информационное окно
        direct = Frame(parent)
        self.maincommand = IntVar()
        for key, text in enumerate(DirectControl.__commands):
            Radiobutton(
                direct,
                text = text,
                command = self.check_commands,
                variable = self.maincommand,
                value = key
            ).pack(anchor=NW)
        self.maincommand.set(0)

        self.extracommand = IntVar()
        Scale(
            direct,
            label = 'Дополнительно',
            command = self.extra_command,
            variable = self.extracommand,
            from_ = 0, to = 255,
            orient = 'horizontal'
        ).pack()

        self.longanswer = BooleanVar()
        Checkbutton(
            direct,
            text = 'Расширенный запрос',
            variable = self.longanswer,
            command = self.extra_answer
        ).pack()
        # Button(direct, text='Выключить', command=lambda: None).grid(sticky=W+E, pady=2)
        # Button(direct, text='Отопление', command=lambda: None).grid(sticky=W+E, pady=2)
        # Button(direct, text='Вентиляция', command=lambda: None).grid(sticky=W+E, pady=2)
        # Button(direct, text='Расширенный запрос', command=lambda: None).grid(sticky=W+E, pady=2)
        # info.grid(pady=5, row=1, column=1)
        direct.pack()
        # direct.config(
        #     borderwidth=2,
        #     highlightthickness=2,
        #     highlightbackground='gray',
        #     relief=FLAT
        # )
        # scroll.bind_widgets(info.getScrollWidgets())
        # WidgetsRegistry.instance().pushWorkInfoFrame(info)

    def check_commands(self):
        print(self.maincommand.get())

    def extra_command(self, value):
        print(value)

    def extra_answer(self):
        print(self.longanswer.get())


# ----------------------------------- Фрейм ---------------------------------- #
# class WorkModuleFrame(ttk.Notebook):
class WorkModuleFrame(Frame, GUIWidgetConfiguration):
    # Список для Listbox
    __baselist = (
        'Общее описание',
        'Прямое управление',
        'Обновление ПО',
        'Журнал неисправностей',
        'Состояние узлов блока',
        'Коррекция параметров',
        'График'
    )
    # Команды для listbox
    # TODO нужно унифицировать аргументы, чтобы сделать одинаковый ввод
    __commands_list = [
        ViewInfo(),
        DirectControl()
    ]

    def __init__(self, master=None, root=None, **kwargs):
        super().__init__(master, **kwargs)
        # root - главный виджет (не к которому крепится, а который создан изначально)
        self.root = root
        self._make_widgets()

    def _make_widgets(self):
        # Первая вкладка с кнопками управления
        # rc_frame = Frame(self)
        # rc_frame.pack(expand=YES, fill=BOTH)
        from widgets import InfoTitleLabel
        # InfoTitleLabel(rc_frame, text='Пульт (прямое управление)').grid(sticky=W+E+S+N, pady=2)
        # # WARNING размещено здесь из-за перекрестного импорта
        # # from commands.maincommands import ReplaceImage, SaveModule
        # Button(rc_frame, text='Выключить', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        # Button(rc_frame, text='Отопление', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        # Button(rc_frame, text='Вентиляция', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        # Button(rc_frame, text='Расширенный запрос', command=lambda: None).grid(sticky=W+E+S+N, pady=2)
        # # Button(rc_frame, text='Сохранить', command=SaveModule()).grid(sticky=W+E+S+N, pady=2)
        # Button(rc_frame, text='Отмена', command=self.root._quit).grid(sticky=W+E+S+N, pady=2)
        # ------------------------------------
        # Левая часть рабочего окна модуля (listbox выбора функций)
        funcselect_frame = Frame(self)
        # funcselect_frame.pack(side=LEFT, expand=YES, fill=BOTH)
        funcselect_frame.grid(row=0, column=0, sticky=W+N)
        # self.add_border(funcselect_frame, 2)
        InfoTitleLabel(funcselect_frame, text='Управление:').pack(fill=X, pady=2)
        listbar = ScrolledListboxFrame(funcselect_frame)
        listbar.pack(pady=10)
        # listbar.grid(padx=10, row=1, column=0, sticky=N)
        listbar.add_list(WorkModuleFrame.__baselist)
        listbar.set_command(self.__select_commands)
        listbar.listbox.config(width=30)
        listbar.listbox.select_set(0)
        # listbar.listbox.event_generate('<<ListboxSelect>>')

        # Button(funcselect_frame, text='Save to file', command=lambda: None).pack(fill=X, pady=2)
        # Button(funcselect_frame, text='Load from file', command=lambda: None).pack(fill=X, pady=2)
        # Button(funcselect_frame, text='AddRow', command=lambda: None).pack(fill=X, pady=2)
        # Button(funcselect_frame, text='DelRow', command=lambda: None).pack(fill=X, pady=2)
        # Button(funcselect_frame, text='Upload to Block', command=lambda: None).pack(fill=X, pady=2)
        # Button(funcselect_frame, text='Мониторинг', command=lambda: None).pack(fill=X, pady=2)
        # Button(funcselect_frame, text='Прошивка', command=lambda: None).pack(fill=X, pady=2)
        # Button(rc_frame, text='Сохранить', command=SaveModule()).grid(sticky=W+E+S+N, pady=2)
        Button(funcselect_frame, text='Выход', command=self.root._quit).pack(fill=X, pady=2)

        # self.add(rc_frame, text='Пульт')
        # self.add(funcselect_frame, text='Розжиг')

        # Основное информационное окно
        # info = InfoModuleFrame(self)
        # info.grid(pady=5, row=1, column=1)
        # self.scrollwindow.bind_widgets(info.getScrollWidgets())
        # WidgetsRegistry.instance().pushWorkInfoFrame(info)

        # Правая часть рабочего окна модуля (изменяется в зависимости от выбора listbox)
        self.work_frame = Frame(self)
        # work_frame.pack(expand=YES, fill=BOTH)
        self.work_frame.grid(row=0, column=1, sticky=E+W+N+S)
        # self.add_border(work_frame, 2)
        InfoTitleLabel(self.work_frame, text='Здесь будут различные окна работы с модулем').pack(fill=X, pady=2)

        listbar.listbox.event_generate('<<ListboxSelect>>')

    def __select_commands(self, event):
        # print(event.widget.curselection())
        current = event.widget.curselection()
        if current:
            current = current[0]
        else:
            return
        # print(current)
        print(event.widget.get(current))
        # print(self.work_frame.winfo_children())
        if current == 0:
            # ViewInfo().execute(self.work_frame, self.root.scrollwindow)
            WorkModuleFrame.__commands_list[0](self.work_frame, self.root.scrollwindow)
        elif current == 1:
            WorkModuleFrame.__commands_list[1](self.work_frame)

    def view_info(self):
        pass
