"""Виджет ScrolledText с текстом только для чтения."""
from tkinter import DISABLED, NORMAL
from tkinter.scrolledtext import ScrolledText


class ReadonlyScrolledText(ScrolledText):
    """Исправлены только методы delete и insert. Остальные могут работать неправильно."""
    def __init__(self, master=None, **kw):
        ScrolledText.__init__(self, master, **kw)
        self.config(state=DISABLED)

    def delete(self, *args, **kwargs):
        self.config(state=NORMAL)
        super().delete(*args, **kwargs)
        self.config(state=DISABLED)

    def insert(self, *args):
        self.config(state=NORMAL)
        super().insert(*args)
        self.config(state=DISABLED)