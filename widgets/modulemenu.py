from tkinter import *

# WARNING импортирование внутри класса (отложенный импорт) для избежания проблем циклического импорта
# from commands.maincommands import (
#     ViewModule, ClearModuleWindow, DeleteModule, EditModule,
#     LoadModuleFile, LoadModuleDirectory,
#     CommandMixin, StartModule
# )

class ModuleMenu(Frame):
    """Меню окна модуля."""
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
        """Шаблон команд меню модуля."""
        from commands import (
            StartModule,
            EditModule,
            DeleteModule,
            ClearModuleWindow,
            LoadModuleFile,
            LoadModuleDirectory
        )

        return {
            'Открыть': StartModule(),
            'Копировать': EditModule(),
            'Удалить': DeleteModule(),
            'Очистить': ClearModuleWindow(),
            'Добавить': LoadModuleFile(),
            'Загрузить папку': LoadModuleDirectory(),
            'Закрыть': self.parent.destroy
        }