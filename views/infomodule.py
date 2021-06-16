from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *

from registry import AppRegistry, WidgetsRegistry
from views.connectimages import ModuleImage
from widgets.readonlytext import ReadonlyScrolledText
from widgets.infolabels import InfoTitleLabel


class InfoModuleFrame(Frame):
    # Левая панель выбора модулей из списка
    def __init__(self, master, *args):
        Frame.__init__(self, master, *args)
        # Сохранить фрейм в реестре
        WidgetsRegistry.instance().setInfoFrame(self)
        # Переменные окон Message
        self.__make_widgets()
        self.updateText()

    def __make_widgets(self):
        Label(self, text='Информация о модуле').pack(padx=5)

        cur_mod = AppRegistry.instance().getCurrentModule()
        self.__modulemage = ModuleImage(self, image=(cur_mod.getImageLink() if cur_mod else None))
        self.__modulemage.pack()

        InfoTitleLabel(self, text='Описание модуля:').pack(padx=5, fill=X)
        self.__description = ReadonlyScrolledText(self, width=75, height=10, wrap=WORD)
        self.__description.pack(padx=5, pady=5, fill=X)

        InfoTitleLabel(self, text='Параметры модуля:').pack(padx=5, fill=X)
        self.__options = ReadonlyScrolledText(self, width=75, height=10, wrap=WORD)
        self.__options.pack(padx=5, pady=5, fill=X)

        InfoTitleLabel(self, text='Конфигурация модуля:').pack(padx=5, fill=X)
        self.__config = ReadonlyScrolledText(self, width=75, height=5, wrap=WORD)
        self.__config.pack(padx=5, pady=5, fill=X)

    def __getText(self, field):
        cur_mod = AppRegistry.instance().getCurrentModule()
        # print('info panel get text:', cur_mod)
        return cur_mod.getDescription(field) if cur_mod else 'Сообщение: модуль не выбран.'

    def updateText(self):
        self.__description.delete('1.0', END)
        self.__description.insert('1.0', self.__getText('description'))
        self.__options.delete('1.0', END)
        self.__options.insert('1.0', self.__getText('options'))
        self.__config.delete('1.0', END)
        self.__config.insert('1.0', self.__getText('config'))

    def updateImage(self):
        cur_mod = AppRegistry.instance().getCurrentModule()
        self.__modulemage.updateImage(image=(cur_mod.getImageLink() if cur_mod else None))

    def clearImage(self):
        self.__modulemage.clearImage()


if __name__ == '__main__':
    root = Tk()
    conn = InfoModuleFrame(root)
    root.mainloop()