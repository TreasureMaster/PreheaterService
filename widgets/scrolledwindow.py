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

        # self.bind("<Enter>", self.on_binds)
        # self.bind('<Leave>', self.off_binds)
        # Добавилось событие прокрутки колеса мыши
        # self.canvas.bind_all("<MouseWheel>", self._on_mousewheel, add='+')
        self.frame.bind('<Configure>', self.onFrameConfigure)
        # self.canvas.bind('<Configure>', self.frameWidth)

        self.on_binds(None)

        # self.make_widgets(None)

    def make_widgets(self, widget):
        # попытка привязать события входа и выхода для виджетов Text, чтобы прокручивать их отдельно
        widget.bind("<Leave>", self.on_binds)
        widget.bind('<Enter>', self.off_binds)

        # widget.pack(expand=YES, fill=BOTH)
        # for row in range(100):
        #     Label(self.frame, text='%s' % row, width=3, borderwidth='1', relief=SOLID).grid(row=row, column=0)
        #     t = "Вторая колонка для строки %s" % row
        #     Label(self.frame, text=t).grid(row=row, column=1)

    def on_binds(self, event):
        # привязать прокрутку мыши
        self.idbind = self.frame.bind_all("<MouseWheel>", self._on_mousewheel)
        print(self.idbind)
        
    def off_binds(self, event):
        # отвязать прокрутку или все ???
        self.frame.unbind_all(self.idbind)

    def frameWidth(self, event):
        # расширяет canvas на всю область, но scroll это не ловит
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width, height=event.height)

    def onFrameConfigure(self, event):
        """Сбросьте область прокрутки, чтобы охватить внутреннюю рамку"""
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    def _on_mousewheel(self, event): 
        # print('working...')
        # отработка события прокрутки (деление delta - скорость)
        self.canvas.yview_scroll(int(-1*(event.delta/60)), "units")


if __name__ == '__main__':
    root = Tk()
    example = ScrolledWindow(root)
    example.pack(side=TOP, fill=BOTH, expand=YES)
    root.mainloop()