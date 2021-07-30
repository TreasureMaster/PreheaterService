from tkinter import *


class ModuleOperation(Frame):
    """Виджет операций над модулем."""
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._make_widgets()

    def _make_widgets(self):
        self.combo = Frame(self)
        self.combo.pack(fill=Y)
        Label(self.combo, text='Port').grid(row=0, column=0, padx=5, pady=5, sticky=W)