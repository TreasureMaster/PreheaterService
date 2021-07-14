"""Виджет ScrolledText с текстом только для чтения."""
from tkinter import DISABLED, NORMAL, END
from tkinter.scrolledtext import ScrolledText


class ReadonlyScrolledText(ScrolledText):
    """Исправлены только методы delete и insert. Остальные могут работать неправильно."""
    def __init__(self, master=None, **kw):
        ScrolledText.__init__(self, master, **kw)
        self.config(state=DISABLED)

    def delete(self, index1='1.0', index2=END):
        self.config(state=NORMAL)
        super().delete(index1, index2)
        self.config(state=DISABLED)

    def insert(self, index, chars, *args):
        self.config(state=NORMAL)
        super().insert(index, chars, *args)
        self.see(END)
        self.config(state=DISABLED)

    def update_text(self, text):
        self.delete('1.0', END)
        self.insert('1.0', text)
        self.see('1.0')


class LoggerWindow(ReadonlyScrolledText):
    """Должна быть добавлена подсветка частей текста в зависимости от уровня логов."""

    def __init__(self, master=None, **kw):
        ReadonlyScrolledText.__init__(self, master, **kw)
        self.tag_config('error', foreground='red')
