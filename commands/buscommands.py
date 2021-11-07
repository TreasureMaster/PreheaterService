import threading
# from memory_profiler import profile
from .maincommands import Command
from registry import DeviceRegistry

from connections import LINConnection


# TODO DeviceConnect должен создавать соединение и подкючаться в отдельном потоке,
# который будет работать бесконечно.
# Т.е. отправка пакета будет происходить бесконечно, по циклу.
# Соответственно, в DeviceProtocol какой-то метод должен крутиться постоянно.
# А данные будут изменяться вне этого потока.
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
            with threading.Lock():
                self.connection = DeviceRegistry.instance().getPythonModule().DeviceProtocol(
                    connection = LINConnection(
                        port=DeviceRegistry.instance().getCurrentComPort(),
                        lin_revision=DeviceRegistry.instance().getLINRevision()
                    )
                )
                # DeviceRegistry.instance().setDisconnectEvent(
                #     threading.Event()
                #     # event=False
                # )
                self.packages_thread = threading.Thread(
                    target=self.connection.direct_request,
                    daemon=False
                )
                # self.connection.direct_request()
                self.packages_thread.start()
                self.connection.update_labels()
        # иначе надо отключить, но проверить есть ли соединение
        else:
            with threading.Lock():
                # DeviceRegistry.instance().getDisconnectEvent().set()
                self.connection.disconnect_event.set()
            self.packages_thread.join()
            del self.connection.device_bus
            self.connection = None
        print(self.connection)
        DeviceRegistry.instance().setDeviceProtocol(self.connection)


# Класс тестирования некоторых функций
class TestConnect(Command):
    def execute(self):
        print('test connection attributes:')
        self.conn = LINConnection('COM3')