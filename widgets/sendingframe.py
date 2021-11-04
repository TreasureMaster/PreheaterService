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
        pkginfo_frame.pack(side=TOP, fill=X)
        # self.add_border(pkginfo_frame, width=2)

        for column, key in zip(
            range(0, len(list(self._get_labels())) * 2, 2),
            self._get_labels()
        ):
            # self.labels[key]['var'].set(self.labels[key]['text'])
            Label(
                pkginfo_frame,
                text=self.labels[key]['text'],
                width=len(self.labels[key]['text']),
                anchor=W
            ).grid(row=0, column=column, pady=2, padx=10)
            lbl = Label(
                pkginfo_frame,
                text=self.labels[key]['var'],
                # textvariable=self.labels[key]['var'],
                width=20,
                anchor=W
            )
            lbl.grid(row=0, column=column+1, padx=5, pady=2)
            self.labels[key]['label'] = lbl

    def _get_labels(self):
        self.labels = {
            'send': {
                'text': 'Отправлено: ',
                # 'var': StringVar()
                'var': ''
            },
            'echo': {
                'text': 'Эхо: ',
                # 'var': StringVar()
                'var': ''
            },
            'answer': {
                'text': 'Ответ: ',
                # 'var': StringVar()
                'var': ''
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