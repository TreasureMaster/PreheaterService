"""Тестовый модуль, который используется для проработки вида модуля без использования архивов."""
from tkinter import *
# from tkinter import ttk

from registry import WidgetsRegistry
from widgets import ScrolledListboxFrame
from views import InfoModuleFrame


# class LeftTabs(ttk.Notebook):
class LeftTabs(Frame):

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
        # Вторая вкладка с кнопками
        ignition_frame = Frame(self)
        ignition_frame.pack(expand=YES, fill=BOTH)
        InfoTitleLabel(ignition_frame, text='Управление:').pack(fill=X, pady=2)
        listbar = ScrolledListboxFrame(ignition_frame)
        # listbar.pack(pady=10)
        listbar.grid(padx=10, row=1, column=0, sticky=N)
        listbar.add_list([
            'Общее описание',
            'Прямое управление',
            'Обновление ПО',
            'Журнал неисправностей',
            'Состояние узлов блока',
            'Коррекция параметров',
            'График'
        ])
        listbar.set_command(self.__select_commands)
        listbar.listbox.config(width=30)
        listbar.listbox.select_set(0)
        listbar.listbox.event_generate('<<ListboxSelect>>')

        # Button(ignition_frame, text='Save to file', command=lambda: None).pack(fill=X, pady=2)
        # Button(ignition_frame, text='Load from file', command=lambda: None).pack(fill=X, pady=2)
        # Button(ignition_frame, text='AddRow', command=lambda: None).pack(fill=X, pady=2)
        # Button(ignition_frame, text='DelRow', command=lambda: None).pack(fill=X, pady=2)
        # Button(ignition_frame, text='Upload to Block', command=lambda: None).pack(fill=X, pady=2)
        # Button(ignition_frame, text='Мониторинг', command=lambda: None).pack(fill=X, pady=2)
        # Button(ignition_frame, text='Прошивка', command=lambda: None).pack(fill=X, pady=2)
        # Button(rc_frame, text='Сохранить', command=SaveModule()).grid(sticky=W+E+S+N, pady=2)
        Button(ignition_frame, text='Отмена', command=self.root._quit).pack(fill=X, pady=2)

        # self.add(rc_frame, text='Пульт')
        # self.add(ignition_frame, text='Розжиг')

        # Основное информационное окно
        info = InfoModuleFrame(self)
        info.grid(pady=5, row=1, column=1)
        self.scrollwindow.bind_widgets(info.getScrollWidgets())
        WidgetsRegistry.instance().pushWorkInfoFrame(info)

    def __select_commands(self, event):
        print(event.widget.get(event.widget.curselection()))
