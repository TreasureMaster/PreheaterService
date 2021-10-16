from dataclasses import dataclass

from registry import DeviceRegistry
# from connections import LIN
from connections import LIN_REVISIONS_BUSES


# Подключение создается в момент нажатия 'подключить',
# т.е. код модуля в данный момент уже должен быть загружен
@dataclass
class LINConnection:
    # NOTE оформление в виду dataclass дает возможность в будущем добавлять разные данные
    port: str
    baud: int = 9600
    lin_revision: int = 0

    def __post_init__(self):
        self.protocol = LIN_REVISIONS_BUSES[self.lin_revision](self.port, self.baud)
        print(self.lin_revision)
        # TODO возможно, нет необходимости сохранять
        DeviceRegistry.instance().setCurrentConnection(self.protocol)