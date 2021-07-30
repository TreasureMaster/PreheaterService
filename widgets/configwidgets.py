"""Класс-миксин с функциями изменения конфигурации виджета."""
from registry import WidgetsRegistry
from tkinter import Frame, FLAT

class GUIWidgetConfiguration:

    def add_border(self, widget=None, width: int=0, color: str='gray', relief: str=FLAT) -> None:
        """Установка границы виджета."""
        widget = widget or self
        # WARNING не работает цвет рамки для Label ???
        widget.config(
            borderwidth=width,
            highlightthickness=width,
            highlightbackground=color,
            relief=relief
        )

    def add_underline(self, widget, width: int=0, color: str='gray'):
        widget = Frame(widget)
        self.add_border(widget, width=width, color=color)
        return widget