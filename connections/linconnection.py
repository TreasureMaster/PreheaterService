from dataclasses import dataclass

from registry import DeviceRegistry
from connections import LIN


# Подключение создается в момент нажатия 'подключить',
# т.е. код модуля в данный момент уже должен быть загружен
@dataclass
class LINConnection:
    # NOTE оформление в виду dataclass дает возможность в будущем добавлять разные данные
    port: str
    baud: int = 9600

    def __post_init__(self):
        self.protocol = LIN(self.port, self.baud)
        # TODO возможно, нет необходимости сохранять
        DeviceRegistry.instance().setCurrentConnection(self.protocol)