from tkinter import *

# from widgets import GUIWidgetConfiguration
from config import LabelsConfig
from extra import islice_dict


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
        for column, (title, rows) in enumerate(zip(
            self._TITLE_LABELS,
            self._get_labels_by3()
        )):
            max_title_len = max(map(len, self._TITLE_LABELS))
            max_subtitle_len = max(map(len, self._ALL_LABELS.values()))
            # self.labels[key]['var'].set(self.labels[key]['text'])
            Label(
                pkginfo_frame,
                # text=self.labels[key]['text'],
                text = title,
                # width=len(self.labels[key]['text']),
                # width=30 if column < 3 else 10,
                width=max_title_len,
                anchor=W
            ).grid(row=0, rowspan=3, column=column*3)
            for row, key in enumerate(rows):
                Label(
                    pkginfo_frame,
                    text=self.labels[key]['text'],
                    # textvariable=self.labels[key]['var'],
                    width=max_subtitle_len,
                    anchor=W
                ).grid(row=row, column=column*3+1)
                lbl = Label(
                    pkginfo_frame,
                    text=self.labels[key]['var'],
                    # textvariable=self.labels[key]['var'],
                    width=30 if column == 0 else 10,
                    anchor=W
                )
                lbl.grid(row=row, column=column*3+2)
                self.labels[key]['label'] = lbl

    def _get_labels_by3(self):
        for title, text in self._ALL_LABELS.items():
            self.labels[title] = {
                'text': text,
                'var': ''
            }

        for seq in islice_dict(self.labels, 3):
            yield seq


if __name__ == '__main__':
    root = Tk()
    conn = SendingFrame(root)
    conn.pack()
    # print(conn.initComPortList(10))
    root.mainloop()