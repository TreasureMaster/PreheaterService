from tkinter import *
# from tkinter.ttk import *
# from tkinter.messagebox import *
# from tkinter.filedialog import *

from registry import AppRegistry
from widgets.connectimages import ModuleImage
from widgets.readonlytext import ReadonlyScrolledText
from widgets.infolabels import InfoTitleLabel


class InfoModuleFrame(Frame):
    """Создает информационный (правый) фрейм с описанием модуля.

    editable - флаг, какой модуль используется (редактируемый или обычный)
    """
    # Левая панель выбора модулей из списка
    def __init__(self, master, *args, editable=False):
        Frame.__init__(self, master, *args)
        self.editable = editable
        # Переменные окон Message
        self.__make_widgets()
        self.updateText()

    def __make_widgets(self):
        Label(self, text='Информация о модуле').pack(padx=5)

        self.__modulemage = ModuleImage(self, image=(self._getWorkModule().getImageLink() if self._getWorkModule() else None))
        self.__modulemage.pack()

        InfoTitleLabel(self, text='Описание модуля:').pack(padx=5, fill=X)
        self.__description = ReadonlyScrolledText(self, width=75, height=10, wrap=WORD)
        self.__description.pack(padx=5, pady=5, fill=X)

        # InfoTitleLabel(self, text='Параметры модуля:').pack(padx=5, fill=X)
        # self.__options = ReadonlyScrolledText(self, width=75, height=10, wrap=WORD)
        # self.__options.pack(padx=5, pady=5, fill=X)

        InfoTitleLabel(self, text='Конфигурация модуля:').pack(padx=5, fill=X)
        self.__config = ReadonlyScrolledText(self, width=75, height=5, wrap=WORD)
        self.__config.pack(padx=5, pady=5, fill=X)

    def _getWorkModule(self):
        # Получение рабочего модуля
        if self.editable:
            return AppRegistry.instance().getEditableModule()
        else:
            return AppRegistry.instance().getCurrentModule()

    def __getText(self, field):
        # cur_mod = AppRegistry.instance().getCurrentModule()
        # print('info panel get text:', cur_mod)
        return self._getWorkModule().getDescription(field) if self._getWorkModule() else 'Сообщение: модуль не выбран.'

    def updateText(self):
        self.__description.update_text(self.__getText('description'))
        self.__config.update_text(self.__getText('config'))

    def updateImage(self):
        # cur_mod = AppRegistry.instance().getCurrentModule()
        self.__modulemage.updateImage(image=(self._getWorkModule().getImageLink() if self._getWorkModule() else None))

    def clearImage(self):
        self.__modulemage.clearImage()

    def getScrollWidgets(self):
        """Возвращает текстовые виджеты для корректировки событий прокрутки главного окна."""
        # WARNING опасно, можно изменить
        return (self.__description, self.__config)


if __name__ == '__main__':
    root = Tk()
    conn = InfoModuleFrame(root)
    root.mainloop()