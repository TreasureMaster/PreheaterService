from tkinter import *

# from widgets import GUIWidgetConfiguration
from config import LabelsConfig


class SendingFrame(Frame, LabelsConfig):

    def __init__(self, master, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.labels = {}
        self._make_widgets()

    def _make_widgets(self):
        # Вывод информации об отправке пакетов (нижняя часть)
        pkginfo_frame = Frame(self)
        pkginfo_frame.pack(side=TOP, fill=X, padx=10, pady=2)

        # for column, key in zip(
        #     range(0, len(list(self._get_labels())) * 2, 2),
        #     self._get_labels()
        # ):
        for column, key in enumerate(self._get_labels()):
            # self.labels[key]['var'].set(self.labels[key]['text'])
            Label(
                pkginfo_frame,
                text=self.labels[key]['text'],
                # width=len(self.labels[key]['text']),
                width=30 if column < 3 else 10,
                anchor=W
            ).grid(row=0, column=column)
            lbl = Label(
                pkginfo_frame,
                text=self.labels[key]['var'],
                # textvariable=self.labels[key]['var'],
                width=30 if column < 3 else 10,
                anchor=W
            )
            lbl.grid(row=1, column=column)
            self.labels[key]['label'] = lbl

    def _get_labels(self):
        for title, text in self._ALL_LABELS.items():
            self.labels[title] = {
                'text': text,
                'var': ''
            }

        for keys in self.labels:
            yield keys


if __name__ == '__main__':
    root = Tk()
    conn = SendingFrame(root)
    conn.pack()
    # print(conn.initComPortList(10))
    root.mainloop()