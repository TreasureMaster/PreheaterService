"""Виджет Label с предустановленными параметрами для заголовков информационных окон главного окна."""
from tkinter import Label, LEFT, W
from tkinter.font import Font


class InfoTitleLabel(Label):
    """Стилизация заголовка описания модуля в инфоокне."""
    def __init__(self, master=None, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)
        titlefont = Font(family="Arial", size=10, weight="bold", slant="italic", underline=True)
        self.config(anchor=W, font=titlefont)
