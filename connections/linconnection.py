from dataclasses import dataclass

from registry import DeviceRegistry
from connections import LIN


# Подключение создается в момент нажатия 'подключить',
# т.е. код модуля в данный момент уже должен быть загружен
# NOTE создается соединение с базовыми командами LIN
@dataclass
class LINConnection:
    # NOTE оформление в виду dataclass дает возможность в будущем добавлять разные данные
    port: str
    baud: int = 9600

    def __post_init__(self):
        # device_commands = DeviceRegistry.instance().getPythonModule().DeviceProtocol('COM3')
        # # Динамическое добавление атрибутов из архива модуля
        # for attr in dir(device_commands):
        #     if not attr.startswith(('__', '_')):
        #         # print(attr)
        #         if not hasattr(self, attr):
        #             setattr(self, attr, getattr(device_commands, attr))
        # for attr in dir(self):
        #     if not attr.startswith('__'):
        #         print(attr)
        # self.testing(self)
        self.protocol = LIN(self.port, self.baud)
        DeviceRegistry.instance().setCurrentConnection(self.protocol)