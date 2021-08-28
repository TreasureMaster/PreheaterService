from .maincommands import Command
from registry import DeviceRegistry


class DeviceConnect(Command):
    __commands = [
        'Подключить',
        'Отключить'
    ]

    def __init__(self, itself):
        # itself - сам виджет кнопки, внешний вид которой необходимо изменять.
        # т.е. эта команда привязана к этой кнопке, но также должна изменять ее.
        self.itself = itself
        # False - маркер, что соединение отсутствует (True - есть соединение)
        self.connection_exists = False

    def execute(self):
        # print('Device connected')
        # Смена команды
        self.connection_exists = not self.connection_exists
        # print(self.itself.text)
        # Смена надписи на кнопке (не информативно, но эффективно)
        self.itself.config(
            text = DeviceConnect.__commands[self.connection_exists]
        )
        # Если поступила команда "подключить", подключаем
        # TODO необходимо сделать DeviceProtocol синглтоном, но предусмотреть возможность переподключения
        # NOTE будет ли у устройства несколько видов подключения ???
        if self.connection_exists:
            self.connection = DeviceRegistry.instance().getPythonModule().DeviceProtocol(
                port = DeviceRegistry.instance().getCurrentComPort()
            )
            self.connection.scheduleDiagMsg2([0x01, 0x40])
        # иначе надо отключить, но проверить есть ли соединение
        else:
            del self.connection.device_bus