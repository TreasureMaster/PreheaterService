from tkinter import *


class ScrolledWindow(Frame):

    def __init__(self, parent, **kwargs):
        Frame.__init__(self, parent, kwargs)
        self.canvas = Canvas(self, borderwidth=0)
        self.frame = Frame(self.canvas)
        self.vsb = Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        self.canvas_frame = self.canvas.create_window(
            (0, 0),
            window=self.frame,
            anchor='nw',
            tags='self.frame'
        )
        # Изменяет скорость прокрутки главного окна колесом мышки (не влияет на боковой скролл)
        self.canvas.config(yscrollincrement='20')
        # Добавилось событие прокрутки колеса мыши
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.frame.bind('<Configure>', self.onFrameConfigure)

    def bind_widgets(self, widgets):
        """Привязывает виджеты, которые должны иметь свою собственную независимую прокрутку."""
        # попытка привязать события входа и выхода для виджетов Text, чтобы прокручивать их отдельно
        for widget in widgets:
            widget.bind('<Leave>', self.on_binds)
            widget.bind('<Enter>', self.off_binds)

    def on_binds(self, event):
        """Включает прокрутку всего главного экрана."""
        self.frame.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def off_binds(self, event):
        """Отключить прокрутку всего главного экрана для прокрутки встроенных экранов."""
        self.frame.unbind_all("<MouseWheel>")

    def onFrameConfigure(self, event):
        """Сбросьте область прокрутки, чтобы охватить внутреннюю рамку"""
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    def _on_mousewheel(self, event): 
        # отработка события прокрутки (деление delta - скорость)
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


if __name__ == '__main__':
    root = Tk()
    example = ScrolledWindow(root)
    example.pack(side=TOP, fill=BOTH, expand=YES)
    root.mainloop()