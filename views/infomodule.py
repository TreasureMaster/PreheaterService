from tkinter import *

from registry import AppRegistry
from widgets import ModuleImage, InfoTitleLabel, ReadonlyScrolledText, EditableScrolledText


class InfoModuleFrame(Frame):
    """Создает информационный (правый) фрейм с описанием модуля.

    editable - флаг, какой модуль используется (редактируемый или обычный)
    """
    # Левая панель выбора модулей из списка
    def __init__(self, master, *args):
        Frame.__init__(self, master, *args)
        # Переменные окон Message
        self._make_widgets()
        self.updateText()

    def _make_widgets(self):
        Label(self, text='Информация о модуле').pack(padx=5)

        self._modulemage = ModuleImage(self, image=(self._getWorkModule().getImageLink() if self._getWorkModule() else None))
        self._modulemage.pack()

        InfoTitleLabel(self, text='Описание модуля:').pack(padx=5, fill=X)
        self._description = ReadonlyScrolledText(self, width=75, height=10, wrap=WORD)
        self._description.pack(padx=5, pady=5, fill=X)

        # InfoTitleLabel(self, text='Параметры модуля:').pack(padx=5, fill=X)
        # self.__options = ReadonlyScrolledText(self, width=75, height=10, wrap=WORD)
        # self.__options.pack(padx=5, pady=5, fill=X)

        InfoTitleLabel(self, text='Конфигурация модуля:').pack(padx=5, fill=X)
        self._config = ReadonlyScrolledText(self, width=75, height=5, wrap=WORD)
        self._config.pack(padx=5, pady=5, fill=X)

    def _getWorkModule(self):
        # Получение рабочего модуля
        return AppRegistry.instance().getCurrentModule()

    def _getModuleText(self, field):
        # cur_mod = AppRegistry.instance().getCurrentModule()
        # print('info panel get text:', cur_mod)
        return self._getWorkModule().getDescription(field) if self._getWorkModule() else 'Сообщение: модуль не выбран.'

    def updateText(self):
        self._description.update_text(self._getModuleText('description'))
        self._config.update_text(self._getModuleText('config'))

    def updateImage(self):
        # cur_mod = AppRegistry.instance().getCurrentModule()
        self._modulemage.updateImage(image=(self._getWorkModule().getImageLink() if self._getWorkModule() else None))

    def clearImage(self):
        self._modulemage.clearImage()

    def getScrollWidgets(self):
        """Возвращает текстовые виджеты для корректировки событий прокрутки главного окна."""
        # WARNING опасно, можно изменить
        return (self._description, self._config)


class EditableModuleFrame(InfoModuleFrame):

    def _getWorkModule(self):
        return AppRegistry.instance().getEditableModule()

    def _make_widgets(self):
        Label(self, text='Информация о модуле').pack(padx=5)

        self._modulemage = ModuleImage(self, image=(self._getWorkModule().getImageLink() if self._getWorkModule() else None))
        self._modulemage.pack()

        InfoTitleLabel(self, text='Описание модуля:').pack(padx=5, fill=X)
        self._description = EditableScrolledText(self, width=75, height=10, wrap=WORD)
        # self.__description = Text(self, width=75, height=10, wrap=WORD)
        self._description.pack(padx=5, pady=5, fill=X)

        InfoTitleLabel(self, text='Конфигурация модуля:').pack(padx=5, fill=X)
        self._config = ReadonlyScrolledText(self, width=75, height=5, wrap=WORD)
        self._config.pack(padx=5, pady=5, fill=X)

    def getText(self):
        return self._description.get('1.0', END)


if __name__ == '__main__':
    root = Tk()
    conn = InfoModuleFrame(root)
    root.mainloop()