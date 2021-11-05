from tkinter import *
# from tkinter import ttk

# from connectimages import IndicatorImage
# from registry import AppRegistry, DeviceRegistry
from widgets import GUIWidgetConfiguration
# from commands import DeviceConnect, TestConnect


class SendingFrame(Frame, GUIWidgetConfiguration):

    def __init__(self, master, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self._make_widgets()

    def _make_widgets(self):
        # (6+) Вывод информации об отправке пакетов (нижняя часть)
        pkginfo_frame = Frame(self)
        pkginfo_frame.pack(side=TOP, fill=X, padx=10, pady=2)
        # self.add_border(pkginfo_frame, width=2)

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

        # Label(pkginfo_frame, text='Хорошие:', anchor=W, width=10).grid(row=0, column=3)
        # Label(pkginfo_frame, text='Нет эха:', anchor=W, width=10).grid(row=0, column=4)
        # Label(pkginfo_frame, text='Нет ответа:', anchor=W, width=12).grid(row=0, column=5)

        # # self.labels['good']['var'] = ''
        # lbl = Label(pkginfo_frame, text='', anchor=W)
        # lbl.grid(row=1, column=3)
        # self.labels['good']['label'] = lbl

    def _get_labels(self):
        self.labels = {
            'send': {
                'text': 'Отправлено:',
                # 'var': StringVar()
                'var': ''
            },
            'echo': {
                'text': 'Эхо:',
                # 'var': StringVar()
                'var': ''
            },
            'answer': {
                'text': 'Ответ:',
                # 'var': StringVar()
                'var': ''
            },
            'all': {
                'text': 'Все:',
                # 'var': StringVar()
                'var': '0'
            },
            'good': {
                'text': 'Хорошие:',
                # 'var': StringVar()
                'var': '0'
            },
            'bad_echo': {
                'text': 'Нет эха:',
                # 'var': StringVar()
                'var': '0'
            },
            'bad_answer': {
                'text': 'Нет ответа',
                # 'var': StringVar()
                'var': '0'
            },
        }

        for keys in self.labels:
            yield keys

    # def setRemoteControl(self, event):
    #     """Команда выбора пульта управления."""
    #     # rmc = self.combo_rmc.get()
    #     DeviceRegistry.instance().setCurrentRemoteControl(self.combo_rmc.get() or None)
    #     print(DeviceRegistry.instance().getCurrentRemoteControl())

    # def setComPort(self, event):
    #     """Выбор com-порта из списка."""
    #     # Обновляет Label с описанием выбранного порта для соединения
    #     current = event.widget.current()
    #     self.port_description.config(
    #         text=(self.comports[current-1].description if current else ''),
    #         justify=LEFT
    #     )
    #     DeviceRegistry.instance().setCurrentComPort(self.comports[current-1].name if current else None)
    #     # print(DeviceRegistry.instance().getCurrentComPort())

    # def updateComPortList(self):
    #     """Обновление списка com-портов.
        
    #     Необходимо, так как устройство может быть физически подключено позже старта программы.
    #     Добавление прочерков в список com-портов после формирования последнего."""
    #     self.comports = list_ports.comports()
    #     self.combo_port.config(
    #         values=([''] + [port.device for port in self.comports])
    #     )

    # def initRemoteControlList(self, rmc_list=None):
    #     """Формирование списка пультов управления."""
    #     # if rmc_list:
    #         # TODO список совместимых пультов
    #         # remotecontrols = list(map(lambda n: 'COM'+str(n), range(rmc_list)))
    #     remotecontrols = [''] + rmc_list
    #     return remotecontrols

    # def setLINRev(self):
    #     """Выбор типа расчета CRC в зависимости от версии LIN."""
    #     DeviceRegistry.instance().setLINRevision(self.LINrevision.get())

if __name__ == '__main__':
    root = Tk()
    conn = SendingFrame(root)
    conn.pack()
    # print(conn.initComPortList(10))
    root.mainloop()