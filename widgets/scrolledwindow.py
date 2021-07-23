from tkinter import *


class ScrolledWindow(Frame):

    def __init__(self, parent, **kwargs):
        Frame.__init__(self, parent, kwargs)
        self.canvas = Canvas(self, bd=0, highlightthickness=0)
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
        # self.config(cursor='arrow')
        self.frame.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def off_binds(self, event):
        """Отключить прокрутку всего главного экрана для прокрутки встроенных экранов."""
        # self.config(cursor='right_ptr')
        self.frame.unbind_all("<MouseWheel>")

    def onFrameConfigure(self, event):
        """Сбросьте область прокрутки, чтобы охватить внутреннюю рамку"""
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    def _on_mousewheel(self, event):
        # Ищем родительский Canvas и обрабатываем либо его прокрутку, либо self.canvas, если не находим родителя-canvas
        # Иначе возникают ошибки прокрутки при возврает из окна скопированого модуля.
        w = event.widget
        while not (isinstance(w, Canvas) or w is None):
            w = w.master
        # отработка события прокрутки (деление delta - скорость)
        if w is None:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        else:
            w.yview_scroll(int(-1*(event.delta/120)), "units")


if __name__ == '__main__':
    root = Tk()
    example = ScrolledWindow(root)
    example.pack(side=TOP, fill=BOTH, expand=YES)
    root.mainloop()