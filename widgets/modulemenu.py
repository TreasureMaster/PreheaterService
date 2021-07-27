from tkinter import *

from commands.maincommands import (
    ViewModule, ClearModuleWindow, DeleteModule, EditModule,
    LoadModuleFile, LoadModuleDirectory,
    CommandMixin, StartModule
)

class ModuleMenu(Frame):

    def __init__(self, parent=None, **kwargs) -> None:
        self.parent = parent
        super().__init__(parent, **kwargs)
        self._make_menu()

    def _make_menu(self):
        mbutton = Menubutton(self, text='Модуль', underline=0, relief=RAISED)
        mbutton.pack(side=LEFT, padx=10, pady=5)
        module = Menu(mbutton, tearoff=False)
        for name, command in self._menu_composition().items():
            if name.lower() == 'выход':
                module.add_separator()
            module.add_command(label=name, command=command, underline=0)
        mbutton.config(menu=module)


    def _menu_composition(self):
        return {
            'Открыть': StartModule(),
            'Копировать': EditModule(),
            'Удалить': DeleteModule(),
            'Очистить': ClearModuleWindow(),
            'Добавить': LoadModuleFile(),
            'Загрузить папку': LoadModuleDirectory(),
            'Закрыть': self.parent.destroy
        }